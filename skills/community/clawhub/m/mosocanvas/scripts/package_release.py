#!/usr/bin/env python3
"""Build a deterministic MoSoCanvas release archive and integrity manifest."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {"__pycache__", ".DS_Store"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def included_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*")
        if path.is_file()
        and not any(part in EXCLUDED_PARTS for part in path.parts)
        and path.suffix != ".pyc"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Package the current MoSoCanvas release.")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--source-label", default=".agents/skills/mosocanvas")
    args = parser.parse_args()

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version or any(not part.isdigit() for part in version.split(".")):
        raise ValueError("VERSION must be a semantic version")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    archive = args.output_dir / f"mosocanvas-{version}.zip"
    manifest_path = args.output_dir / f"mosocanvas-{version}.manifest.json"
    files = included_files()

    with zipfile.ZipFile(
        archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as bundle:
        for path in files:
            info = zipfile.ZipInfo(
                f"mosocanvas/{path.relative_to(ROOT).as_posix()}",
                date_time=(2020, 1, 1, 0, 0, 0),
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            bundle.writestr(info, path.read_bytes())

    manifest = {
        "schema": "mosocanvas-release-manifest/0.2",
        "name": "mosocanvas",
        "version": version,
        "release_date": date.today().isoformat(),
        "source": args.source_label,
        "archive": archive.name,
        "archive_bytes": archive.stat().st_size,
        "archive_sha256": sha256(archive),
        "included_file_count": len(files),
        "included_files": [
            {
                "path": f"mosocanvas/{path.relative_to(ROOT).as_posix()}",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "version": version,
        "archive": str(archive.resolve()),
        "manifest": str(manifest_path.resolve()),
        "files": len(files),
        "sha256": manifest["archive_sha256"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
