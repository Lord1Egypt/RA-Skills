"""Post body builders and publish helpers.

One function per post type. Each calls `POST /rest/posts` and returns the
post URN from the `x-restli-id` response header (e.g.
`urn:li:share:7045020441609936898`).

Every post shares the same envelope: `author`, `commentary`, `visibility`,
`distribution`, `lifecycleState`, `isReshareDisabledByAuthor`. The content
type is carried in the optional `content` field.
"""

from __future__ import annotations

from typing import Any

from .client import LinkedInClient, MAX_COMMENTARY_LENGTH
from .media import upload_image, upload_video


def _envelope(client: LinkedInClient, commentary: str, content: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build the shared post body. Every post type starts from this."""
    if len(commentary) > MAX_COMMENTARY_LENGTH:
        raise ValueError(
            f"Commentary is {len(commentary)} characters; LinkedIn rejects anything "
            f"over {MAX_COMMENTARY_LENGTH}. Trim before calling."
        )

    body: dict[str, Any] = {
        "author": client.author_urn,
        "commentary": commentary,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    if content is not None:
        body["content"] = content
    return body


def _publish(client: LinkedInClient, body: dict[str, Any]) -> str:
    """POST to /rest/posts and return the post URN from response headers."""
    resp = client.post("posts", body=body)
    post_urn = resp.headers.get("x-restli-id")
    if not post_urn:
        # Shouldn't happen for 201 responses, but fall back to the body just in case.
        payload = resp.json() if resp.content else {}
        post_urn = payload.get("id", "<unknown>")
    return post_urn


# --- Public API -------------------------------------------------------------


def post_text(client: LinkedInClient, text: str) -> str:
    """Publish a text-only post. Returns the post URN."""
    return _publish(client, _envelope(client, text))


def post_image(client: LinkedInClient, image_path: str, *, text: str, alt: str) -> str:
    """Upload an image and publish it as a single-image post."""
    if not alt:
        raise ValueError("alt text is required for accessibility and ranking.")
    image_urn = upload_image(client, image_path)
    content = {"media": {"id": image_urn, "altText": alt}}
    return _publish(client, _envelope(client, text, content))


def post_multi_image(
    client: LinkedInClient,
    image_paths: list[str],
    *,
    text: str,
    alts: list[str],
) -> str:
    """Upload multiple images and publish them as a carousel (2–20 images)."""
    if not 2 <= len(image_paths) <= 20:
        raise ValueError(
            f"Multi-image posts need between 2 and 20 images; got {len(image_paths)}."
        )
    if len(alts) != len(image_paths):
        raise ValueError(
            f"Alt text count ({len(alts)}) must match image count ({len(image_paths)})."
        )

    images = []
    for path, alt in zip(image_paths, alts, strict=True):
        if not alt:
            raise ValueError(f"Missing alt text for image {path}.")
        urn = upload_image(client, path)
        images.append({"id": urn, "altText": alt})

    content = {"multiImage": {"images": images}}
    return _publish(client, _envelope(client, text, content))


def post_video(
    client: LinkedInClient,
    video_path: str,
    *,
    text: str,
    title: str,
) -> str:
    """Upload a video and publish it. Waits for LinkedIn to finish processing
    before creating the post — a post created against a still-processing video
    will show a broken player to viewers."""
    video_urn = upload_video(client, video_path, poll=True)
    content = {"media": {"id": video_urn, "title": title}}
    return _publish(client, _envelope(client, text, content))


def post_article(
    client: LinkedInClient,
    url: str,
    *,
    text: str,
    title: str | None = None,
    description: str | None = None,
) -> str:
    """Publish a post with an article link preview.

    LinkedIn scrapes the URL's OpenGraph metadata for the preview card. You
    can override `title` and `description` explicitly, but LinkedIn may still
    prefer the OG tags. If the preview looks wrong, the fix is usually on the
    target page's `<meta property="og:...">` tags, not here.
    """
    article: dict[str, Any] = {"source": url}
    if title is not None:
        article["title"] = title
    if description is not None:
        article["description"] = description
    content = {"article": article}
    return _publish(client, _envelope(client, text, content))
