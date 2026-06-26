from __future__ import annotations

import ipaddress
import mimetypes
import os
import socket
import subprocess
import tempfile
from contextlib import suppress
from pathlib import Path
from urllib.parse import urlparse

import requests


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".webm", ".mkv", ".flv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}


def is_remote_url(path: str) -> bool:
    return path.startswith(("http://", "https://"))


def _format_bytes(num_bytes: int) -> str:
    if num_bytes == 1:
        return "1 byte"
    return f"{num_bytes} bytes"


def _resolve_host_addresses(hostname: str) -> tuple[ipaddress._BaseAddress, ...]:
    try:
        addrinfo = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise RuntimeError(f"Unable to resolve remote media host: {hostname}") from exc

    addresses: list[ipaddress._BaseAddress] = []
    for entry in addrinfo:
        sockaddr = entry[4]
        if not sockaddr:
            continue
        try:
            address = ipaddress.ip_address(sockaddr[0])
        except ValueError:
            continue
        if address not in addresses:
            addresses.append(address)

    if not addresses:
        raise RuntimeError(f"Unable to resolve remote media host: {hostname}")
    return tuple(addresses)


def assert_public_https_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        raise RuntimeError(f"Only HTTPS remote media URLs are supported: {url}")
    if parsed.username or parsed.password:
        raise RuntimeError(f"Remote media URLs must not include credentials: {url}")
    if not parsed.hostname:
        raise RuntimeError(f"Remote media URL must include a hostname: {url}")

    for address in _resolve_host_addresses(parsed.hostname):
        if not address.is_global:
            raise RuntimeError(f"Remote media host is not public: {parsed.hostname}")


def detect_media_type(path_or_url: str) -> str:
    ext = Path(path_or_url).suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    content_type = mimetypes.guess_type(path_or_url)[0] or ""
    if content_type.startswith("image/"):
        return "image"
    if content_type.startswith("video/"):
        return "video"
    if content_type.startswith("audio/"):
        return "audio"
    return "unknown"


def get_image_dimensions(file_path: str) -> tuple[int, int]:
    try:
        from PIL import Image

        with Image.open(file_path) as img:
            return img.size
    except Exception:
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-select_streams",
                    "v:0",
                    "-show_entries",
                    "stream=width,height",
                    "-of",
                    "csv=s=x:p=0",
                    file_path,
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            if result.returncode == 0 and "x" in result.stdout:
                width, height = map(int, result.stdout.strip().split("x"))
                return width, height
        except Exception:
            pass
    return 0, 0


def get_video_metadata(file_path: str) -> dict[str, float | int]:
    try:
        duration_result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        duration = float(duration_result.stdout.strip()) if duration_result.returncode == 0 else 0.0

        dimension_result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height,r_frame_rate",
                "-of",
                "default=noprint_wrappers=1",
                file_path,
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        width = height = 0
        fps = 0.0
        if dimension_result.returncode == 0:
            for line in dimension_result.stdout.strip().splitlines():
                if line.startswith("width="):
                    width = int(line.split("=", 1)[1])
                elif line.startswith("height="):
                    height = int(line.split("=", 1)[1])
                elif line.startswith("r_frame_rate="):
                    frame_rate = line.split("=", 1)[1]
                    if "/" in frame_rate:
                        numerator, denominator = frame_rate.split("/", 1)
                        denominator_value = float(denominator or 0)
                        fps = float(numerator) / denominator_value if denominator_value else 0.0
                    else:
                        fps = float(frame_rate)
        return {"duration": duration, "width": width, "height": height, "fps": fps}
    except Exception:
        return {"duration": 0.0, "width": 0, "height": 0, "fps": 0.0}


def get_audio_duration(file_path: str) -> float:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except Exception:
        pass
    return 0.0


def download_remote_media_to_temp(url: str, suffix: str = "", max_bytes: int | None = None) -> str:
    assert_public_https_url(url)

    temp_path: str | None = None
    try:
        with requests.get(url, stream=True, timeout=60, allow_redirects=False) as response:
            status_code = getattr(response, "status_code", 200)
            if 300 <= status_code < 400:
                raise RuntimeError(f"Remote media redirects are not supported: {url}")

            response.raise_for_status()

            if max_bytes is not None:
                content_length_header = response.headers.get("Content-Length")
                if content_length_header:
                    with suppress(ValueError):
                        content_length = int(content_length_header)
                        if content_length > max_bytes:
                            raise RuntimeError(
                                f"Remote media exceeds the {max_bytes}-byte download cap: {url}"
                            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_path = temp_file.name
                total_bytes = 0
                for chunk in response.iter_content(chunk_size=1024 * 64):
                    if not chunk:
                        continue
                    total_bytes += len(chunk)
                    if max_bytes is not None and total_bytes > max_bytes:
                        raise RuntimeError(
                            f"Remote media exceeds the {max_bytes}-byte download cap: {url}"
                        )
                    temp_file.write(chunk)
            return temp_path
    except Exception:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        raise


def extract_video_cover_frame(file_path: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        output_path = temp_file.name

    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                file_path,
                "-frames:v",
                "1",
                "-q:v",
                "2",
                output_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "ffmpeg cover extraction failed")
        return output_path
    except Exception:
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise
