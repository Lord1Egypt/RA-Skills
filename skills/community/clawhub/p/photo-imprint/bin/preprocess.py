#!/usr/bin/env python3
"""Build an EXIF-ordered manifest for a photo-to-illustration carousel."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
EXIF_DATETIME_TAGS = ((36867, "DateTimeOriginal"), (36868, "DateTimeDigitized"), (306, "DateTime"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_capture_time(image: Image.Image) -> tuple[str | None, str | None, str | None]:
    exif = image.getexif()
    for tag, label in EXIF_DATETIME_TAGS:
        raw = exif.get(tag)
        if not raw:
            continue
        text = str(raw).strip()
        try:
            parsed = datetime.strptime(text, "%Y:%m:%d %H:%M:%S")
            return parsed.isoformat(timespec="seconds"), label, None
        except ValueError:
            return None, label, f"invalid EXIF {label}: {text}"
    return None, None, "missing EXIF capture time"


def inspect(path: Path) -> dict:
    with Image.open(path) as image:
        capture_time, exif_source, issue = read_capture_time(image)
        width, height = image.size
        return {
            "source_path": str(path.resolve()),
            "filename": path.name,
            "sha256": sha256(path),
            "width": width,
            "height": height,
            "capture_time": capture_time,
            "capture_time_source": exif_source,
            "metadata_issue": issue,
            "location": None,
            "subject": None,
            "date_label": capture_time[:10] if capture_time else None,
            "caption_status": {},
            "production_brief": {
                "subject_priority": None,
                "thumbnail_read": None,
                "preserve_anchors": [],
                "abstract_or_omit": [],
                "material_depth_cues": [],
                "structural_lines": [],
                "forbidden_inventions": [],
            },
            "notes": None,
        }


def load_resolved_config(path: Path | None) -> dict | None:
    if path is None:
        return None
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read resolved config {path}: {exc}") from exc
    if not isinstance(config, dict) or config.get("resolved") is not True:
        raise ValueError(f"config is not a resolved carousel config: {path}")
    return config


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="Directory containing source photos")
    parser.add_argument("--output", required=True, type=Path, help="Manifest JSON path")
    parser.add_argument("--config", type=Path, help="Resolved config from resolve_config.py")
    parser.add_argument("--allow-missing", action="store_true", help="Write a draft even when EXIF dates are missing")
    args = parser.parse_args()

    if not args.input.is_dir():
        parser.error(f"Input directory does not exist: {args.input}")
    try:
        config = load_resolved_config(args.config)
    except ValueError as exc:
        parser.error(str(exc))

    paths = sorted(p for p in args.input.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED)
    if not paths:
        parser.error("No supported image files found")

    records, failures = [], []
    for path in paths:
        try:
            record = inspect(path)
            records.append(record)
            if not record["capture_time"]:
                failures.append(f"{path.name}: {record['metadata_issue']}")
        except Exception as exc:
            failures.append(f"{path.name}: {exc}")

    if failures and not args.allow_missing:
        print("Missing or invalid EXIF capture time; ask the user instead of guessing:", file=sys.stderr)
        for item in failures:
            print(f"- {item}", file=sys.stderr)
        return 2

    dated = sorted((r for r in records if r["capture_time"]), key=lambda r: r["capture_time"])
    undated = [r for r in records if not r["capture_time"]]
    ordered = dated + undated
    for index, record in enumerate(ordered, start=1):
        record["page"] = index

    unconfirmed_fields = []
    if config and config.get("modules", {}).get("caption", {}).get("enabled"):
        caption_fields = config["modules"]["caption"].get("lines", [])
        manifest_field = {"date": "date_label"}
        for record in ordered:
            record["caption_status"] = {
                field: ("proposed" if record.get(manifest_field.get(field, field)) else "missing")
                for field in caption_fields
            }
            missing = [field for field, status in record["caption_status"].items() if status == "missing"]
            if missing:
                unconfirmed_fields.append({"page": record["page"], "fields": missing})

    unconfirmed_briefs = [
        {
            "page": record["page"],
            "fields": [
                "subject_priority", "thumbnail_read", "preserve_anchors", "abstract_or_omit",
                "material_depth_cues", "structural_lines", "forbidden_inventions",
            ],
        }
        for record in ordered
    ]
    style_contract = None
    if config:
        style_contract = config.get("profiles", {}).get("style", {}).get("sample_style_contract_defaults")

    payload = {
        "schema_version": "1.0.0",
        "ordering": "EXIF capture time ascending; undated files require user confirmation",
        "requires_user_confirmation": bool(failures or unconfirmed_fields or unconfirmed_briefs),
        "unconfirmed_caption_fields": unconfirmed_fields,
        "unconfirmed_production_briefs": unconfirmed_briefs,
        "sample_style_contract": style_contract,
        "review_gate": {
            "status": "intake_complete",
            "next_step": "propose every production_brief field, then build the production plan",
            "batch_render_authorized": False,
        },
        "preset": config.get("preset") if config else None,
        "profile_ids": ({key: value.get("id") for key, value in config.get("profiles", {}).items()} if config else None),
        "canvas": (config.get("profiles", {}).get("composition", {}).get("canvas") if config else None),
        "items": ordered,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(ordered)} items to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
