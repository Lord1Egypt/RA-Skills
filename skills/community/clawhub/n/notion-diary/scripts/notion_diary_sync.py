#!/usr/bin/env python3
"""
Sync diary entries or short reports into Notion using the public REST API.

This script is designed for OpenClaw skills and uses only the Python standard
library so it can run in minimal environments.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import pathlib
import re
import sys
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

API_BASE = "https://api.notion.com/v1"
API_VERSION = "2026-03-11"
MAX_TEXT_CHUNK = 1900
MAX_IMAGE_BYTES = 20 * 1024 * 1024

STYLE_LABELS = {
    "plain": "纪实简洁",
    "gentle": "温柔叙事",
    "reflective": "克制反思",
    "lyrical": "轻文艺",
}

MODE_LABELS = {
    "diary": "Diary",
    "report": "Report",
}


class NotionSyncError(RuntimeError):
    pass


@dataclass
class TargetInfo:
    database_id: str
    data_source_id: str
    database_url: Optional[str]
    created_database: bool


@dataclass
class ResolvedImage:
    source: str
    name: str
    file_upload_id: Optional[str] = None
    external_url: Optional[str] = None
    error: Optional[str] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync diary content into Notion.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--api-key", default=os.getenv("NOTION_API_KEY"))
    common.add_argument("--database-id", default=os.getenv("NOTION_DIARY_DATABASE_ID"))
    common.add_argument("--data-source-id", default=os.getenv("NOTION_DIARY_DATA_SOURCE_ID"))
    common.add_argument("--parent-page-id", default=os.getenv("NOTION_DIARY_PARENT_PAGE_ID"))
    common.add_argument(
        "--database-name",
        default=os.getenv("NOTION_DIARY_DATABASE_NAME", "Daily Journal"),
    )
    common.add_argument("--dry-run", action="store_true")

    lookup = subparsers.add_parser("lookup", parents=[common], help="Find an entry by date.")
    lookup.add_argument("--date", required=True)
    lookup.add_argument("--mode", choices=["diary", "report", "any"], default="any")

    sync = subparsers.add_parser("sync", parents=[common], help="Create or update an entry.")
    sync.add_argument("--date", required=True)
    sync.add_argument("--mode", choices=["diary", "report"], required=True)
    sync.add_argument(
        "--style",
        choices=sorted(STYLE_LABELS.keys()),
        default=os.getenv("NOTION_DIARY_DEFAULT_STYLE", "reflective"),
    )
    sync.add_argument("--title")
    sync.add_argument("--summary")
    sync.add_argument("--content")
    sync.add_argument("--content-file")
    sync.add_argument("--image", action="append", default=[])
    sync.add_argument("--strict-images", action="store_true")

    return parser.parse_args()


def require_api_key(value: Optional[str], allow_dummy: bool = False) -> str:
    if not value and allow_dummy:
        return "dry-run-placeholder"
    if not value:
        raise NotionSyncError(
            "Missing NOTION_API_KEY. In OpenClaw set skills.entries['notion-diary'].apiKey."
        )
    return value


def normalize_uuidish(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    match = re.search(
        r"([0-9a-fA-F]{32}|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
        value,
    )
    if not match:
        return value
    raw = match.group(1).replace("-", "").lower()
    if len(raw) != 32:
        return value
    return str(uuid.UUID(raw))


def text_object(text: str) -> Dict[str, object]:
    return {
        "type": "text",
        "text": {
            "content": text,
        },
    }


def rich_text_chunks(text: str) -> List[Dict[str, object]]:
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text_object(text[start : start + MAX_TEXT_CHUNK]))
        start += MAX_TEXT_CHUNK
    return chunks


def property_title(text: str) -> Dict[str, object]:
    return {"title": rich_text_chunks(text)}


def property_rich_text(text: str) -> Dict[str, object]:
    return {"rich_text": rich_text_chunks(text)}


def property_date(date_str: str) -> Dict[str, object]:
    return {"date": {"start": date_str}}


def property_select(name: str) -> Dict[str, object]:
    return {"select": {"name": name}}


class NotionClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, object]] = None,
        raw_body: Optional[bytes] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, object]:
        url = f"{API_BASE}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": API_VERSION,
        }
        body = None
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif raw_body is not None:
            body = raw_body
        if extra_headers:
            headers.update(extra_headers)

        for attempt in range(4):
            request = urllib.request.Request(url, data=body, headers=headers, method=method)
            try:
                with urllib.request.urlopen(request) as response:
                    data = response.read()
                    return json.loads(data.decode("utf-8")) if data else {}
            except urllib.error.HTTPError as exc:
                if exc.code == 429 and attempt < 3:
                    retry_after = exc.headers.get("Retry-After")
                    sleep_seconds = float(retry_after) if retry_after else 1.5 * (attempt + 1)
                    time.sleep(sleep_seconds)
                    continue
                detail = exc.read().decode("utf-8", errors="replace")
                raise NotionSyncError(
                    f"Notion API {exc.code} {method} {path} failed: {detail}"
                ) from exc
            except urllib.error.URLError as exc:
                raise NotionSyncError(f"Network error calling Notion API: {exc}") from exc
        raise NotionSyncError(f"Notion API {method} {path} failed after retries.")

    def paginate_block_children(self, block_id: str) -> List[Dict[str, object]]:
        results: List[Dict[str, object]] = []
        cursor = None
        while True:
            query = {"page_size": 100}
            if cursor:
                query["start_cursor"] = cursor
            path = f"/blocks/{block_id}/children?{urllib.parse.urlencode(query)}"
            payload = self.request("GET", path)
            batch = payload.get("results", [])
            if isinstance(batch, list):
                results.extend(batch)
            if not payload.get("has_more"):
                break
            cursor = payload.get("next_cursor")
        return results

    def upload_small_file(self, path: pathlib.Path) -> str:
        if not path.exists():
            raise NotionSyncError(f"Image file not found: {path}")
        size = path.stat().st_size
        if size > MAX_IMAGE_BYTES:
            raise NotionSyncError(
                f"Image file is larger than 20 MB and cannot use single-part upload: {path}"
            )
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        create_payload = {
            "mode": "single_part",
            "filename": path.name,
            "content_type": mime,
        }
        created = self.request("POST", "/file_uploads", payload=create_payload)
        file_upload_id = created["id"]

        boundary = f"----notiondiary{uuid.uuid4().hex}"
        file_bytes = path.read_bytes()
        body_parts = [
            f"--{boundary}\r\n".encode("utf-8"),
            (
                'Content-Disposition: form-data; name="file"; '
                f'filename="{path.name}"\r\n'
            ).encode("utf-8"),
            f"Content-Type: {mime}\r\n\r\n".encode("utf-8"),
            file_bytes,
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
        body = b"".join(body_parts)
        uploaded = self.request(
            "POST",
            f"/file_uploads/{file_upload_id}/send",
            raw_body=body,
            extra_headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        if uploaded.get("status") != "uploaded":
            raise NotionSyncError(
                f"File upload did not finish successfully for {path}: {uploaded}"
            )
        return file_upload_id


def ensure_target(
    client: NotionClient,
    database_id: Optional[str],
    data_source_id: Optional[str],
    parent_page_id: Optional[str],
    database_name: str,
) -> TargetInfo:
    database_id = normalize_uuidish(database_id)
    data_source_id = normalize_uuidish(data_source_id)
    parent_page_id = normalize_uuidish(parent_page_id)

    if data_source_id:
        data_source = client.request("GET", f"/data_sources/{data_source_id}")
        parent = data_source.get("parent", {})
        resolved_database_id = normalize_uuidish(parent.get("database_id"))
        database_url = None
        if resolved_database_id:
            database = client.request("GET", f"/databases/{resolved_database_id}")
            database_url = database.get("url")
        return TargetInfo(
            database_id=resolved_database_id or "",
            data_source_id=data_source_id,
            database_url=database_url,
            created_database=False,
        )

    if database_id:
        database = client.request("GET", f"/databases/{database_id}")
        sources = database.get("data_sources", [])
        if not sources:
            raise NotionSyncError("The target database has no data sources.")
        return TargetInfo(
            database_id=database_id,
            data_source_id=normalize_uuidish(sources[0]["id"]) or sources[0]["id"],
            database_url=database.get("url"),
            created_database=False,
        )

    if not parent_page_id:
        raise NotionSyncError(
            "Missing target. Set NOTION_DIARY_DATA_SOURCE_ID, NOTION_DIARY_DATABASE_ID, "
            "or NOTION_DIARY_PARENT_PAGE_ID."
        )

    child_blocks = client.paginate_block_children(parent_page_id)
    for block in child_blocks:
        if block.get("type") != "child_database":
            continue
        title = block.get("child_database", {}).get("title")
        if title == database_name:
            db_id = normalize_uuidish(block.get("id")) or block.get("id")
            database = client.request("GET", f"/databases/{db_id}")
            sources = database.get("data_sources", [])
            if not sources:
                raise NotionSyncError("Found child database but it has no data sources.")
            return TargetInfo(
                database_id=db_id,
                data_source_id=normalize_uuidish(sources[0]["id"]) or sources[0]["id"],
                database_url=database.get("url"),
                created_database=False,
            )

    created = client.request(
        "POST",
        "/databases",
        payload={
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [text_object(database_name)],
            "description": [text_object("Diary entries and fallback 24-hour reports.")],
            "is_inline": False,
            "initial_data_source": {
                "properties": {
                    "Title": {"title": {}},
                    "Date": {"date": {}},
                    "Mode": {
                        "select": {
                            "options": [
                                {"name": "Diary", "color": "blue"},
                                {"name": "Report", "color": "gray"},
                            ]
                        }
                    },
                    "Style": {
                        "select": {
                            "options": [
                                {"name": "纪实简洁", "color": "gray"},
                                {"name": "温柔叙事", "color": "orange"},
                                {"name": "克制反思", "color": "blue"},
                                {"name": "轻文艺", "color": "purple"},
                            ]
                        }
                    },
                    "Summary": {"rich_text": {}},
                    "Photos": {"files": {}},
                }
            },
        },
    )
    db_id = normalize_uuidish(created.get("id")) or created.get("id")
    sources = created.get("data_sources", [])
    if not sources:
        database = client.request("GET", f"/databases/{db_id}")
        sources = database.get("data_sources", [])
        database_url = database.get("url")
    else:
        database_url = created.get("url")
    if not sources:
        raise NotionSyncError("Created the database but could not find its data source.")
    return TargetInfo(
        database_id=db_id,
        data_source_id=normalize_uuidish(sources[0]["id"]) or sources[0]["id"],
        database_url=database_url,
        created_database=True,
    )


def build_query_filter(date_str: str, mode: str) -> Dict[str, object]:
    date_filter = {"property": "Date", "date": {"equals": date_str}}
    if mode == "any":
        return date_filter
    return {
        "and": [
            date_filter,
            {"property": "Mode", "select": {"equals": MODE_LABELS[mode]}},
        ]
    }


def lookup_entry(client: NotionClient, data_source_id: str, date_str: str, mode: str) -> Optional[Dict[str, object]]:
    payload = client.request(
        "POST",
        f"/data_sources/{data_source_id}/query",
        payload={
            "filter": build_query_filter(date_str, mode),
            "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}],
            "page_size": 10,
        },
    )
    results = payload.get("results", [])
    return results[0] if results else None


def read_content(args: argparse.Namespace) -> str:
    if args.content:
        return args.content
    if args.content_file:
        return pathlib.Path(args.content_file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise NotionSyncError("No content provided. Use --content, --content-file, or stdin.")


def build_summary(text: str) -> str:
    flattened = " ".join(text.replace("\n", " ").split())
    return flattened[:120]


def paragraph_block(text: str) -> Dict[str, object]:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": rich_text_chunks(text),
        },
    }


def bullet_block(text: str) -> Dict[str, object]:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": rich_text_chunks(text),
        },
    }


def image_block_external(url: str) -> Dict[str, object]:
    return {
        "object": "block",
        "type": "image",
        "image": {
            "type": "external",
            "external": {"url": url},
            "caption": [],
        },
    }


def image_block_file_upload(file_upload_id: str) -> Dict[str, object]:
    return {
        "object": "block",
        "type": "image",
        "image": {
            "type": "file_upload",
            "file_upload": {"id": file_upload_id},
            "caption": [],
        },
    }


def resolve_image_reference(
    client: NotionClient,
    image_ref: str,
    strict_images: bool,
) -> ResolvedImage:
    try:
        if re.match(r"^https?://", image_ref):
            parsed = urllib.parse.urlparse(image_ref)
            name = pathlib.Path(parsed.path).name or "image"
            return ResolvedImage(source=image_ref, name=name, external_url=image_ref)
        path = pathlib.Path(image_ref).expanduser().resolve()
        upload_id = client.upload_small_file(path)
        return ResolvedImage(source=str(path), name=path.name, file_upload_id=upload_id)
    except Exception as exc:  # noqa: BLE001 - best effort by design
        if strict_images:
            raise
        return ResolvedImage(
            source=image_ref,
            name=pathlib.Path(image_ref).name or "image",
            error=str(exc),
        )


def prepare_images(
    client: NotionClient,
    image_refs: Sequence[str],
    strict_images: bool,
) -> List[ResolvedImage]:
    return [resolve_image_reference(client, image_ref, strict_images) for image_ref in image_refs]


def simulate_images(image_refs: Sequence[str]) -> List[ResolvedImage]:
    images: List[ResolvedImage] = []
    for index, image_ref in enumerate(image_refs, start=1):
        if re.match(r"^https?://", image_ref):
            parsed = urllib.parse.urlparse(image_ref)
            name = pathlib.Path(parsed.path).name or f"image-{index}"
            images.append(ResolvedImage(source=image_ref, name=name, external_url=image_ref))
        else:
            name = pathlib.Path(image_ref).name or f"image-{index}"
            images.append(
                ResolvedImage(
                    source=image_ref,
                    name=name,
                    file_upload_id=f"dry-run-upload-{index}",
                )
            )
    return images


def image_block_from_resolved(image: ResolvedImage) -> Dict[str, object]:
    if image.file_upload_id:
        return image_block_file_upload(image.file_upload_id)
    if image.external_url:
        return image_block_external(image.external_url)
    suffix = f" ({image.error})" if image.error else ""
    return paragraph_block(f"图片待补传：{image.source}{suffix}")


def image_property_item(image: ResolvedImage) -> Optional[Dict[str, object]]:
    if image.file_upload_id:
        return {
            "name": image.name,
            "type": "file_upload",
            "file_upload": {"id": image.file_upload_id},
        }
    if image.external_url:
        return {
            "name": image.name,
            "type": "external",
            "external": {"url": image.external_url},
        }
    return None


def cover_from_resolved(image: ResolvedImage) -> Optional[Dict[str, object]]:
    if image.file_upload_id:
        return {"type": "file_upload", "file_upload": {"id": image.file_upload_id}}
    if image.external_url:
        return {"type": "external", "external": {"url": image.external_url}}
    return None


def build_children(
    content: str,
    images: Sequence[ResolvedImage],
) -> List[Dict[str, object]]:
    blocks: List[Dict[str, object]] = []
    used_images = set()

    normalized = content.replace("\r\n", "\n").strip()
    if not normalized:
        return [paragraph_block("（空白内容）")]

    chunks = re.split(r"\n\s*\n", normalized)
    for chunk in chunks:
        candidate = chunk.strip()
        marker = re.fullmatch(r"\[\[image:(\d+)]]", candidate)
        if marker:
            index = int(marker.group(1)) - 1
            if 0 <= index < len(images):
                blocks.append(image_block_from_resolved(images[index]))
                used_images.add(index)
            else:
                blocks.append(paragraph_block(f"图片待补传：image:{index + 1}"))
            continue

        lines = [line.strip() for line in candidate.splitlines() if line.strip()]
        if lines and all(line.startswith("- ") for line in lines):
            for line in lines:
                blocks.append(bullet_block(line[2:].strip()))
            continue
        blocks.append(paragraph_block("\n".join(lines)))

    for index, image in enumerate(images):
        if index in used_images:
            continue
        blocks.append(image_block_from_resolved(image))

    return blocks


def delete_existing_children(client: NotionClient, page_id: str) -> None:
    for block in client.paginate_block_children(page_id):
        block_id = normalize_uuidish(block.get("id")) or block.get("id")
        client.request("DELETE", f"/blocks/{block_id}")


def append_children(client: NotionClient, page_id: str, children: Sequence[Dict[str, object]]) -> None:
    if not children:
        return
    for start in range(0, len(children), 50):
        chunk = children[start : start + 50]
        client.request(
            "PATCH",
            f"/blocks/{page_id}/children",
            payload={"children": list(chunk)},
        )


def page_properties(
    title: str,
    date_str: str,
    mode: str,
    style: str,
    summary: str,
    images: Sequence[ResolvedImage],
) -> Dict[str, object]:
    photo_items = [item for item in (image_property_item(image) for image in images) if item]
    return {
        "Title": property_title(title),
        "Date": property_date(date_str),
        "Mode": property_select(MODE_LABELS[mode]),
        "Style": property_select(STYLE_LABELS[style]),
        "Summary": property_rich_text(summary),
        "Photos": {"files": photo_items},
    }


def sync_entry(client: NotionClient, args: argparse.Namespace) -> Dict[str, object]:
    content = read_content(args)
    summary = args.summary or build_summary(content)
    title = args.title or f"{args.date} | {'简短日报' if args.mode == 'report' else '日记'}"
    images: List[ResolvedImage] = (
        simulate_images(args.image)
        if args.dry_run
        else prepare_images(client, args.image, args.strict_images)
    )
    props = page_properties(title, args.date, args.mode, args.style, summary, images)

    if args.dry_run:
        return {
            "target": {
                "database_id": normalize_uuidish(args.database_id),
                "data_source_id": normalize_uuidish(args.data_source_id),
                "parent_page_id": normalize_uuidish(args.parent_page_id),
                "database_name": args.database_name,
            },
            "title": title,
            "summary": summary,
            "properties": props,
            "content_preview": content[:500],
            "images": args.image,
            "photo_property_count": len(args.image),
        }

    target = ensure_target(
        client,
        args.database_id,
        args.data_source_id,
        args.parent_page_id,
        args.database_name,
    )

    existing = lookup_entry(client, target.data_source_id, args.date, args.mode)
    children = build_children(content, images)
    cover = cover_from_resolved(images[0]) if images else None

    if existing:
        page_id = normalize_uuidish(existing["id"]) or existing["id"]
        update_payload: Dict[str, object] = {"properties": props}
        if cover:
            update_payload["cover"] = cover
        client.request("PATCH", f"/pages/{page_id}", payload=update_payload)
        delete_existing_children(client, page_id)
        append_children(client, page_id, children)
        return {
            "action": "updated",
            "page_id": page_id,
            "page_url": existing.get("url"),
            "database_url": target.database_url,
            "database_created": target.created_database,
        }

    created = client.request(
        "POST",
        "/pages",
        payload={
            "parent": {"type": "data_source_id", "data_source_id": target.data_source_id},
            "properties": props,
            **({"cover": cover} if cover else {}),
        },
    )
    page_id = normalize_uuidish(created.get("id")) or created.get("id")
    append_children(client, page_id, children)
    return {
        "action": "created",
        "page_id": page_id,
        "page_url": created.get("url"),
        "database_url": target.database_url,
        "database_created": target.created_database,
    }


def main() -> int:
    args = parse_args()
    client = NotionClient(require_api_key(args.api_key, allow_dummy=args.dry_run))

    try:
        if args.command == "lookup":
            if args.dry_run:
                print(
                    json.dumps(
                        {
                            "target": {
                                "database_id": normalize_uuidish(args.database_id),
                                "data_source_id": normalize_uuidish(args.data_source_id),
                                "parent_page_id": normalize_uuidish(args.parent_page_id),
                                "database_name": args.database_name,
                            },
                            "date": args.date,
                            "mode": args.mode,
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                )
                return 0
            target = ensure_target(
                client,
                args.database_id,
                args.data_source_id,
                args.parent_page_id,
                args.database_name,
            )
            page = lookup_entry(client, target.data_source_id, args.date, args.mode)
            print(
                json.dumps(
                    {
                        "found": bool(page),
                        "page": page,
                        "database_url": target.database_url,
                        "data_source_id": target.data_source_id,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        if args.command == "sync":
            result = sync_entry(client, args)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0

        raise NotionSyncError(f"Unknown command: {args.command}")
    except NotionSyncError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
