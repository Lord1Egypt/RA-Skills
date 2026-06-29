#!/usr/bin/env python3
"""Batch-publish local digital products with the official Gumroad CLI.

This helper intentionally stores no credentials. It expects `gumroad` to be on PATH
and authenticated via `GUMROAD_ACCESS_TOKEN` or `gumroad auth login`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".gif"]
ARCHIVE_EXTS = [".zip", ".pdf", ".7z", ".rar", ".psd"]


def run_gumroad(args: list[str], *, dry_run: bool = False) -> dict[str, Any]:
    cmd = ["gumroad", *args, "--json", "--no-input", "--non-interactive"]
    if dry_run:
        cmd.append("--dry-run")
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(json.dumps({"cmd": redact_cmd(cmd), "stderr": proc.stderr.strip(), "stdout": proc.stdout.strip()}, indent=2))
    if not proc.stdout.strip():
        return {"success": True}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"success": True, "raw": proc.stdout}


def redact_cmd(cmd: list[str]) -> list[str]:
    redacted: list[str] = []
    skip_next = False
    for part in cmd:
        if skip_next:
            redacted.append("<redacted>")
            skip_next = False
            continue
        redacted.append(part)
        if part.lower() in {"--token", "--access-token", "--client-secret"}:
            skip_next = True
    return redacted


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def titleize(stem: str) -> str:
    clean = re.sub(r"[_-]+", " ", stem).strip()
    return " ".join(word.upper() if word.lower() in {"psd", "pdf"} else word.capitalize() for word in clean.split())


def find_cover(source: Path, archive: Path) -> Path | None:
    for ext in IMAGE_EXTS:
        candidate = archive.with_suffix(ext)
        if candidate.exists():
            return candidate
    for ext in IMAGE_EXTS:
        candidate = source / f"{archive.stem}{ext}"
        if candidate.exists():
            return candidate
    return None


def make_record(source: Path, archive: Path, price: str) -> dict[str, Any]:
    cover = find_cover(source, archive)
    title = titleize(archive.stem)
    return {
        "sku": slugify(archive.stem),
        "title": title,
        "price": price,
        "description": f"<p>{title}</p><p>Digital download. No physical item is shipped.</p>",
        "custom_summary": "Digital download product.",
        "tags": [],
        "file": str(archive),
        "file_name": archive.name,
        "cover_image": str(cover) if cover else None,
        "thumbnail": str(cover) if cover else None,
        "product_id": None,
        "published": False,
        "verified": False,
        "content_set": False,
    }


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_manifest(args: argparse.Namespace) -> None:
    source = Path(args.source)
    if not source.exists():
        raise SystemExit(f"Source not found: {source}")
    records: list[dict[str, Any]] = []
    for path in sorted(source.rglob("*")):
        if path.is_file() and path.suffix.lower() in ARCHIVE_EXTS:
            records.append(make_record(source, path, args.price))
    manifest = {"source": str(source), "records": records}
    save_manifest(Path(args.out), manifest)
    print(json.dumps({"success": True, "out": args.out, "records": len(records)}, indent=2))


def selected_records(manifest: dict[str, Any], limit: int | None, only_sku: str | None) -> list[dict[str, Any]]:
    records = manifest.get("records", [])
    if only_sku:
        records = [r for r in records if r.get("sku") == only_sku]
    records = [r for r in records if not r.get("product_id")]
    return records[:limit] if limit else records


def cmd_plan(args: argparse.Namespace) -> None:
    manifest = load_manifest(Path(args.manifest))
    records = selected_records(manifest, args.limit, args.only_sku)
    print(json.dumps({"selected": len(records), "sample": records[:5]}, indent=2, ensure_ascii=False))


def product_from_response(response: dict[str, Any]) -> dict[str, Any]:
    return response.get("product") or response.get("data") or response


def create_product(record: dict[str, Any], *, publish: bool, dry_run: bool) -> dict[str, Any]:
    cmd = [
        "products", "create",
        "--name", record["title"],
        "--price", str(record["price"]),
        "--description", record.get("description") or "",
        "--custom-summary", record.get("custom_summary") or "",
        "--file", record["file"],
        "--file-name", record.get("file_name") or Path(record["file"]).name,
        "--yes",
    ]
    if record.get("cover_image"):
        cmd += ["--cover-image", record["cover_image"]]
    if record.get("thumbnail"):
        cmd += ["--thumbnail", record["thumbnail"]]
    for tag in record.get("tags") or []:
        if tag:
            cmd += ["--tag", tag]
    created = run_gumroad(cmd, dry_run=dry_run)
    product = product_from_response(created)
    product_id = product.get("id") or product.get("product_id")
    if dry_run:
        return {"dry_run": True, "response": created}
    if not product_id:
        raise RuntimeError(f"Could not find product id in Gumroad response: {created}")
    record["product_id"] = product_id
    ensure_rich_content(record)
    if publish:
        run_gumroad(["products", "publish", product_id, "--yes"])
        record["published"] = True
    verify_record(record)
    return created


def get_product(product_id: str) -> dict[str, Any]:
    return product_from_response(run_gumroad(["products", "view", product_id]))


def ensure_rich_content(record: dict[str, Any]) -> None:
    product_id = record.get("product_id")
    if not product_id:
        return
    product = get_product(product_id)
    files = product.get("files") or []
    rich_content = product.get("rich_content") or []
    if rich_content or not files:
        record["content_set"] = bool(rich_content)
        return
    file_id = files[0].get("id")
    if not file_id:
        return
    content = [{
        "title": None,
        "description": {
            "type": "doc",
            "content": [
                {"type": "fileEmbed", "attrs": {"id": file_id, "uid": str(uuid.uuid4()), "collapsed": False}},
                {"type": "paragraph"},
            ],
        },
    }]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
        json.dump(content, handle, ensure_ascii=False)
        temp_path = handle.name
    try:
        run_gumroad(["products", "content", "set", product_id, temp_path, "--yes"])
        record["content_set"] = True
    finally:
        Path(temp_path).unlink(missing_ok=True)


def verify_record(record: dict[str, Any]) -> dict[str, Any]:
    product_id = record.get("product_id")
    if not product_id:
        record["verified"] = False
        return record
    product = get_product(product_id)
    files = product.get("files") or []
    covers = product.get("covers") or []
    rich = product.get("rich_content") or []
    ok = bool(files) and bool(covers) and bool(product.get("thumbnail_url")) and bool(product.get("preview_url")) and bool(rich)
    record["verified"] = ok
    record["published"] = bool(product.get("published"))
    record["verification"] = {
        "files_count": len(files),
        "covers_count": len(covers),
        "thumbnail": bool(product.get("thumbnail_url")),
        "preview": bool(product.get("preview_url")),
        "rich_content_pages": len(rich),
    }
    return record


def cmd_publish(args: argparse.Namespace) -> None:
    if not args.yes and not args.dry_run:
        raise SystemExit("Refusing live batch publish without --yes after explicit user confirmation.")
    path = Path(args.manifest)
    manifest = load_manifest(path)
    records = selected_records(manifest, args.limit, args.only_sku)
    results = []
    for record in records:
        result = create_product(record, publish=args.publish, dry_run=args.dry_run)
        results.append({"sku": record.get("sku"), "product_id": record.get("product_id"), "verified": record.get("verified"), "response": result if args.dry_run else None})
        save_manifest(path, manifest)
    print(json.dumps({"success": True, "processed": len(results), "results": results}, indent=2, ensure_ascii=False))


def cmd_verify(args: argparse.Namespace) -> None:
    path = Path(args.manifest)
    manifest = load_manifest(path)
    records = manifest.get("records", [])
    if args.only_sku:
        records = [r for r in records if r.get("sku") == args.only_sku]
    if args.limit:
        records = records[:args.limit]
    for record in records:
        verify_record(record)
    save_manifest(path, manifest)
    print(json.dumps({"verified": sum(1 for r in records if r.get("verified")), "checked": len(records), "records": records}, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Batch-publish local digital products to Gumroad with the official CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("manifest")
    p.add_argument("--source", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--price", required=True, help="Price as Gumroad CLI string, e.g. 8.00")
    p.set_defaults(func=cmd_manifest)

    p = sub.add_parser("plan")
    p.add_argument("--manifest", required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--only-sku")
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("publish")
    p.add_argument("--manifest", required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--only-sku")
    p.add_argument("--publish", action="store_true", help="Publish products after verified creation")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_publish)

    p = sub.add_parser("verify")
    p.add_argument("--manifest", required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--only-sku")
    p.set_defaults(func=cmd_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
