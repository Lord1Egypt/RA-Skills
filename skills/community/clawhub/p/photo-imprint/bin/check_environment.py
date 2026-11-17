#!/usr/bin/env python3
"""Check runtime, dependencies, configured local assets, and explicit font readiness."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def version_tuple(raw: str) -> tuple[int, ...]:
    parts: list[int] = []
    for token in raw.split("."):
        digits = "".join(ch for ch in token if ch.isdigit())
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read resolved config {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("resolved") is not True:
        raise ValueError("config must be a resolved JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only execution environment and asset check")
    parser.add_argument("--config", type=Path, help="Resolved config; enables configured asset/font checks")
    parser.add_argument("--font", type=Path, help="Explicit font file for deterministic typography")
    parser.add_argument("--skill-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    checks: list[dict[str, Any]] = []
    errors: list[str] = []

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})
        if not ok:
            errors.append(f"{name}: {detail}")

    record("python", sys.version_info >= (3, 10), f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    try:
        import PIL
        from PIL import Image, ImageFont
        record("Pillow", version_tuple(PIL.__version__) >= (10, 0), PIL.__version__)
    except Exception as exc:
        Image = ImageFont = None  # type: ignore[assignment]
        record("Pillow", False, str(exc))
    try:
        import numpy
        record("NumPy", version_tuple(numpy.__version__) >= (1, 24), numpy.__version__)
    except Exception as exc:
        record("NumPy", False, str(exc))

    config: dict[str, Any] | None = None
    if args.config is not None:
        try:
            config = load(args.config)
            record("resolved-config", True, str(args.config.resolve()))
        except ValueError as exc:
            record("resolved-config", False, str(exc))
    if config is not None:
        modules = config.get("modules", {})
        needs_font = any(
            isinstance(modules.get(name), dict) and modules[name].get("enabled") is True
            for name in ("caption", "watermark")
        )
        if needs_font:
            if args.font is None or not args.font.is_file() or args.font.is_symlink():
                record("font", False, f"configured typography requires an explicit regular font file: {args.font}")
            elif ImageFont is None:
                record("font", False, "Pillow font loader unavailable")
            else:
                try:
                    loaded = ImageFont.truetype(str(args.font), 12)
                    family, style = loaded.getname()
                    record("font", True, f"{args.font.resolve()} ({family} {style})")
                except OSError as exc:
                    record("font", False, f"unreadable font {args.font}: {exc}")
        elif args.font is not None:
            if args.font.is_file() and not args.font.is_symlink():
                record("font", True, str(args.font.resolve()))
            else:
                record("font", False, f"font file missing or symlinked: {args.font}")

        style = config.get("profiles", {}).get("style", {})
        references = style.get("references", []) if isinstance(style, dict) else []
        if not isinstance(references, list):
            record("style-references", False, "style.references must be an array")
        else:
            for index, reference in enumerate(references, start=1):
                if not isinstance(reference, dict):
                    record(f"style-reference-{index}", False, "entry is not an object")
                    continue
                identity = reference.get("id", index)
                image_value, metadata_value = reference.get("image"), reference.get("source_metadata")
                if not isinstance(image_value, str) or not isinstance(metadata_value, str):
                    record(f"style-reference-{identity}", False, "image/source_metadata path missing")
                    continue
                image_path, metadata_path = Path(image_value), Path(metadata_value)
                if not image_path.is_absolute():
                    image_path = args.skill_root / image_path
                if not metadata_path.is_absolute():
                    metadata_path = args.skill_root / metadata_path
                ok = image_path.is_file() and metadata_path.is_file() and not image_path.is_symlink() and not metadata_path.is_symlink()
                detail = f"image={image_path}; metadata={metadata_path}"
                if ok and Image is not None:
                    try:
                        with Image.open(image_path) as opened:
                            opened.verify()
                    except Exception as exc:
                        ok, detail = False, f"unreadable image {image_path}: {exc}"
                record(f"style-reference-{identity}", ok, detail)

    report = {"ok": not errors, "checks": checks, "errors": errors}
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for item in checks:
            print(f"{'PASS' if item['ok'] else 'FAIL'} {item['name']}: {item['detail']}")
        print("Environment check passed" if not errors else "Environment check failed")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
