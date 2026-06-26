"""Image and video upload helpers.

LinkedIn's media upload is a three-step handshake:

1. `initializeUpload` — register the upload. LinkedIn returns an upload URL
   (or several, for multipart video) and a pre-assigned URN.
2. `PUT` the binary — upload the actual bytes to the returned URL(s).
3. (videos only) `finalizeUpload` for multipart, then poll status until the
   video reaches `AVAILABLE`.

Only then is the URN safe to reference in a post. Skipping the poll is the
single most common cause of "the post published but the video is broken"
complaints — LinkedIn happily accepts the post but the video isn't ready.
"""

from __future__ import annotations

import mimetypes
import os
import time
from pathlib import Path

from .client import LinkedInClient


# LinkedIn's own thresholds from its docs.
IMAGE_MAX_PIXELS = 36_152_320
VIDEO_MULTIPART_THRESHOLD_BYTES = 200 * 1024 * 1024  # 200 MB
VIDEO_CHUNK_SIZE_BYTES = 4 * 1024 * 1024  # 4 MB chunks when multipart

# How long to wait for LinkedIn to process a video before giving up.
VIDEO_POLL_INTERVAL_SECONDS = 5
VIDEO_POLL_TIMEOUT_SECONDS = 600  # 10 minutes


# --- Images ------------------------------------------------------------------


def upload_image(client: LinkedInClient, image_path: str | os.PathLike) -> str:
    """Upload an image and return its URN (e.g. `urn:li:image:D4E10AQ...`).

    The returned URN goes in `content.media.id` for single-image posts or in
    `content.multiImage.images[].id` for carousels.
    """
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    # Step 1: initialize.
    resp = client.post(
        "images?action=initializeUpload",
        body={"initializeUploadRequest": {"owner": client.author_urn}},
    )
    value = resp.json()["value"]
    upload_url = value["uploadUrl"]
    image_urn = value["image"]

    # Step 2: upload the bytes.
    with path.open("rb") as fh:
        data = fh.read()
    content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    client.put_upload(upload_url, data, extra_headers={"Content-Type": content_type})

    # Images are processed fast enough that we don't poll — the post endpoint
    # accepts them almost immediately. If you see "image not visible" issues,
    # add a small sleep or poll `GET /rest/images/{urn}` for status.
    return image_urn


# --- Videos ------------------------------------------------------------------


def upload_video(
    client: LinkedInClient,
    video_path: str | os.PathLike,
    *,
    poll: bool = True,
) -> str:
    """Upload a video and return its URN (e.g. `urn:li:video:C5F10AQ...`).

    Automatically chooses single-part vs multipart based on file size.
    Polls until the video finishes processing (pass `poll=False` to skip —
    but don't create the post until processing is done or the video will
    appear broken).
    """
    path = Path(video_path)
    if not path.is_file():
        raise FileNotFoundError(f"Video not found: {path}")

    size = path.stat().st_size
    if size > VIDEO_MULTIPART_THRESHOLD_BYTES:
        video_urn = _upload_video_multipart(client, path, size)
    else:
        video_urn = _upload_video_single(client, path, size)

    if poll:
        _wait_for_video_available(client, video_urn)
    return video_urn


def _upload_video_single(client: LinkedInClient, path: Path, size: int) -> str:
    """Single-URL upload for videos under the multipart threshold."""
    resp = client.post(
        "videos?action=initializeUpload",
        body={
            "initializeUploadRequest": {
                "owner": client.author_urn,
                "fileSizeBytes": size,
                "uploadCaptions": False,
                "uploadThumbnail": False,
            }
        },
    )
    value = resp.json()["value"]
    video_urn = value["video"]

    # For single-part videos, `uploadInstructions` is a one-element list.
    instructions = value["uploadInstructions"]
    if len(instructions) != 1:
        # LinkedIn changed its mind about file size — fall through to multipart.
        return _upload_video_multipart(client, path, size, pre_initialized=value)

    upload_url = instructions[0]["uploadUrl"]
    with path.open("rb") as fh:
        upload_resp = client.put_upload(upload_url, fh.read())

    etag = upload_resp.headers.get("etag") or upload_resp.headers.get("ETag")
    if not etag:
        raise RuntimeError(
            "Single-part video upload returned no ETag header; cannot finalize. "
            "Retry with a freshly initialized upload."
        )
    _finalize_video(client, video_urn, [etag])
    return video_urn


def _upload_video_multipart(
    client: LinkedInClient,
    path: Path,
    size: int,
    *,
    pre_initialized: dict | None = None,
) -> str:
    """Chunked upload for videos over the multipart threshold."""
    if pre_initialized is None:
        resp = client.post(
            "videos?action=initializeUpload",
            body={
                "initializeUploadRequest": {
                    "owner": client.author_urn,
                    "fileSizeBytes": size,
                    "uploadCaptions": False,
                    "uploadThumbnail": False,
                }
            },
        )
        value = resp.json()["value"]
    else:
        value = pre_initialized

    video_urn = value["video"]
    instructions = value["uploadInstructions"]

    etags: list[str] = []
    with path.open("rb") as fh:
        for instruction in instructions:
            first = instruction["firstByte"]
            last = instruction["lastByte"]
            fh.seek(first)
            chunk = fh.read(last - first + 1)
            resp = client.put_upload(instruction["uploadUrl"], chunk)
            etag = resp.headers.get("etag") or resp.headers.get("ETag")
            if not etag:
                raise RuntimeError(
                    f"Upload chunk at bytes {first}-{last} returned no ETag; "
                    "cannot finalize multipart upload."
                )
            etags.append(etag)

    _finalize_video(client, video_urn, etags)
    return video_urn


def _finalize_video(client: LinkedInClient, video_urn: str, etags: list[str]) -> None:
    """Call finalizeUpload with the per-part ETags."""
    client.post(
        "videos?action=finalizeUpload",
        body={
            "finalizeUploadRequest": {
                "video": video_urn,
                "uploadToken": "",
                "uploadedPartIds": etags,
            }
        },
    )


def _wait_for_video_available(client: LinkedInClient, video_urn: str) -> None:
    """Poll `GET /rest/videos/{urn}` until status == AVAILABLE or timeout."""
    deadline = time.monotonic() + VIDEO_POLL_TIMEOUT_SECONDS
    encoded = video_urn.replace(":", "%3A")
    while time.monotonic() < deadline:
        result = client.get(f"videos/{encoded}")
        status = result.get("status")
        if status == "AVAILABLE":
            return
        if status == "PROCESSING_FAILED":
            raise RuntimeError(f"LinkedIn reported processing failure for {video_urn}")
        time.sleep(VIDEO_POLL_INTERVAL_SECONDS)
    raise TimeoutError(
        f"Video {video_urn} did not reach AVAILABLE within "
        f"{VIDEO_POLL_TIMEOUT_SECONDS}s. You can retry polling later — the "
        "upload itself succeeded."
    )
