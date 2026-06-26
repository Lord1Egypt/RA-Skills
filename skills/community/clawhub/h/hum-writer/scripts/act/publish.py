#!/usr/bin/env python3
"""
Publish Hum drafts to X or LinkedIn via platform connectors.

Connectors handle the transport layer (API vs CDP relay browser).
This script handles draft parsing, preview, and metadata updates.

Examples:
  python3 publish.py --draft "../content/drafts/X - Example.md" --publish
  python3 publish.py --draft "../content/drafts/LinkedIn - Example.md" --image /tmp/post.png --publish
  python3 publish.py --draft "../content/drafts/X - Example.md" --platform x --account <account>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Add scripts dir to path so act.connectors and config are importable
_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from act.connectors import load as load_connector


class PublishError(RuntimeError):
    pass


def infer_platform(path: Path) -> str:
    name = path.name.lower()
    if name.startswith("linkedin"):
        return "linkedin"
    if name.startswith("x"):
        return "x"
    raise PublishError("Could not infer platform from draft filename. Use --platform.")


def parse_draft(path: Path) -> dict[str, Any]:
    text = path.read_text()
    lines = text.splitlines()

    title = ""
    fmt = ""
    status = ""
    topic = ""
    body_start = 0

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
        elif stripped.startswith("_Format:"):
            fmt = stripped.strip("_").split(":", 1)[1].strip()
        elif stripped.startswith("_Status:"):
            status = stripped.strip("_").split(":", 1)[1].strip()
        elif stripped.startswith("_Topic:"):
            topic = stripped.strip("_").split(":", 1)[1].strip()
        elif stripped == "---":
            body_start = idx + 1
            break

    while body_start < len(lines) and lines[body_start].strip() == "":
        body_start += 1
    if body_start < len(lines) and lines[body_start].strip() == "---":
        body_start += 1

    body = "\n".join(lines[body_start:]).strip()
    if not body:
        raise PublishError(f"Draft body is empty: {path}")

    return {
        "path": path,
        "title": title or path.stem,
        "format": fmt.lower(),
        "status": status,
        "topic": topic,
        "body": body,
        "raw": text,
    }


def collapse_whitespace(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def draft_to_linkedin_commentary(draft: dict[str, Any]) -> str:
    body = collapse_whitespace(draft["body"])
    body = re.sub(r"^##\s+", "", body, flags=re.MULTILINE)
    return body.strip()


def draft_to_x_segments(draft: dict[str, Any]) -> list[str]:
    body = draft["body"].strip()
    matches = list(re.finditer(r"(?m)^(?P<num>\d+)\.\s+", body))
    if not matches:
        return [collapse_whitespace(body)]

    segments: list[str] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        segment = collapse_whitespace(body[start:end])
        if segment:
            segments.append(segment)

    if not segments:
        raise PublishError("Could not parse numbered X thread from draft.")
    return segments


def preview_x(draft: dict[str, Any], account: str | None) -> dict[str, Any]:
    segments = draft_to_x_segments(draft)
    for idx, seg in enumerate(segments, 1):
        if len(seg) > 280:
            raise PublishError(f"X segment {idx} exceeds 280 chars ({len(seg)}).")
    return {"platform": "x", "account": account or "unknown", "segments": segments}


def preview_linkedin(draft: dict[str, Any], account: str | None) -> dict[str, Any]:
    if "article" in draft["format"] and "source_url:" not in draft["raw"].lower():
        raise PublishError(
            "LinkedIn API publishing supports feed posts, image posts, and article-link posts. "
            "This draft looks like a native long-form article with no source_url metadata."
        )
    commentary = draft_to_linkedin_commentary(draft)
    return {"platform": "linkedin", "account": account or "unknown", "commentary": commentary}


def upsert_publish_metadata(path: Path, platform: str, url: str, external_id: str) -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    block = (
        "\n\n## Publishing Metadata\n"
        f"- Platform: {platform}\n"
        f"- Published At: {now}\n"
        f"- External ID: {external_id}\n"
        f"- URL: {url}\n"
    )
    text = path.read_text()
    text = re.sub(r"\n## Publishing Metadata\n(?:- .*\n)+$", "", text, flags=re.MULTILINE)
    path.write_text(text.rstrip() + block + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", required=True, help="Path to draft markdown file")
    parser.add_argument("--platform", choices=["x", "linkedin"])
    parser.add_argument("--account", help="Account key from credentials file")
    parser.add_argument("--image", help="Optional image path")
    parser.add_argument("--publish", action="store_true", help="Actually publish instead of previewing")
    parser.add_argument("--update-draft", action="store_true", help="Write publish metadata back to the draft")
    args = parser.parse_args()

    draft_path = Path(args.draft).resolve()
    draft = parse_draft(draft_path)
    platform = args.platform or infer_platform(draft_path)

    # Preview mode
    if not args.publish:
        if platform == "x":
            result = preview_x(draft, args.account)
        else:
            result = preview_linkedin(draft, args.account)
        print(json.dumps(result, indent=2))
        return

    # Publish mode — delegate to connectors
    if not args.account:
        raise PublishError("--account is required for publishing.")

    connector = load_connector(platform)

    if platform == "x":
        segments = draft_to_x_segments(draft)
        for idx, seg in enumerate(segments, 1):
            if len(seg) > 280:
                raise PublishError(f"X segment {idx} exceeds 280 chars ({len(seg)}).")

        if len(segments) > 1:
            result = connector.post_thread(segments, args.account, args.image)
        else:
            result = connector.post(segments[0], args.account, args.image)

        external_id = ",".join(result.get("posted_ids", [])) or result.get("tweet_id", "")

    else:
        commentary = draft_to_linkedin_commentary(draft)
        if "article" in draft["format"] and "source_url:" not in draft["raw"].lower():
            raise PublishError("Native LinkedIn articles require browser publishing, not this script.")

        result = connector.post(commentary, args.account, args.image)
        external_id = result.get("post_urn", "")

    # Update draft metadata and move to published/
    if args.update_draft:
        url = result.get("url", "")
        if url and external_id:
            upsert_publish_metadata(draft_path, platform, url, external_id)
        published_dir = draft_path.parent.parent / "published"
        if published_dir.is_dir():
            dest = published_dir / draft_path.name
            draft_path.rename(dest)
            print(f"[publish] Moved to {dest}", file=sys.stderr)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (PublishError, RuntimeError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)
