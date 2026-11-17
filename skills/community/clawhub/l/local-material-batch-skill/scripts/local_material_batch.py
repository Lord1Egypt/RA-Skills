#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

TEXT_EXTS = {".md", ".txt"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
MEDIA_EXTS = {".mp4", ".mov", ".m4a", ".mp3", ".wav", ".aac", ".mkv"}


def stable_id(path: Path) -> str:
    stem = path.stem.lower().replace(" ", "-")
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:8]
    return f"{stem}-{digest}"


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTS:
        return "text"
    if suffix in IMAGE_EXTS:
        return "image"
    if suffix in MEDIA_EXTS:
        return "media"
    return "unsupported"


def discover(root: Path) -> list[Path]:
    inbox = root / "Inbox"
    if not inbox.exists():
        return []
    return sorted(p for p in inbox.rglob("*") if p.is_file())


def process_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def process_item(path: Path, root: Path, force: bool) -> dict:
    item_type = classify(path)
    item_id = stable_id(path.relative_to(root))
    out_dir = root / "outputs" / "items" / item_id
    text_md = out_dir / "text.md"
    text_json = out_dir / "text.json"

    if text_md.exists() and not force:
        return {
            "item_id": item_id,
            "source_path": str(path.relative_to(root)),
            "source_type": item_type,
            "status": "skipped-existing",
            "backend": "none",
            "text": "",
            "error": "输出已存在；如需覆盖请传入 --force",
        }

    out_dir.mkdir(parents=True, exist_ok=True)

    if item_type == "text":
        text = process_text(path)
        status = "ok"
        backend = "local-text"
        error = ""
    elif item_type in {"image", "media"}:
        text = ""
        status = "pending-backend"
        backend = "not-configured"
        error = "请为这一类素材配置 OCR 或 ASR 后端"
    else:
        text = ""
        status = "failed"
        backend = "none"
        error = "不支持的文件扩展名"

    record = {
        "item_id": item_id,
        "source_path": str(path.relative_to(root)),
        "source_type": item_type,
        "status": status,
        "backend": backend,
        "text": text,
        "error": error,
    }

    if text:
        text_md.write_text(text, encoding="utf-8")
    else:
        text_md.write_text(f"# {item_id}\n\n状态：{status}\n\n{error}\n", encoding="utf-8")
    text_json.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def write_batch_outputs(root: Path, records: list[dict]) -> None:
    outputs = root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "items": records,
    }
    (outputs / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (outputs / "summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["item_id", "source_path", "source_type", "status", "backend", "error"],
        )
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in writer.fieldnames})


def init(root: Path) -> None:
    for name in ["Inbox", "outputs", "work", "scripts"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    print(f"已初始化 {root}")


def run(root: Path, dry_run: bool, limit: int | None, force: bool) -> None:
    items = discover(root)
    if limit is not None:
        items = items[:limit]
    if dry_run:
        for path in items:
            print(f"{classify(path):12} {path.relative_to(root)}")
        print(f"总数：{len(items)}")
        return
    records = [process_item(path, root, force) for path in items]
    write_batch_outputs(root, records)
    print(f"已处理：{len(records)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="工作流根目录")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--dry-run", action="store_true")
    run_parser.add_argument("--limit", type=int)
    run_parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.command == "init":
        init(root)
    elif args.command == "run":
        run(root, args.dry_run, args.limit, args.force)


if __name__ == "__main__":
    main()
