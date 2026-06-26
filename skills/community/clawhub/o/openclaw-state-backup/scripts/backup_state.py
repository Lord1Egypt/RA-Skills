#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import socket
import tarfile
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

FORMAT_VERSION = 1

MUTABLE_WORKSPACE_FILES = [
    "MEMORY.md",
    "SESSION-STATE.md",
    "HEARTBEAT.md",
    "TOOLS.md",
]
MUTABLE_WORKSPACE_DIRS = [
    "memory",
    "skills",
]
MUTABLE_STATE_FILES = [
    "openclaw.json",
    "sessions.json",
    "restart-sentinel.json",
]
MUTABLE_STATE_DIRS = [
    "memory",
    "agents",
]
STATIC_WORKSPACE_FILES = [
    "SOUL.md",
    "USER.md",
    "IDENTITY.md",
    "AGENTS.md",
    "BOOTSTRAP.md",
]


@dataclass
class CollectedFile:
    source: Path
    archive_path: str
    sha256: str
    size: int
    kind: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_prefix(prefix: str) -> str:
    return prefix.strip().strip("/")


def should_include_relative(rel_path: str, include_prefixes: list[str], exclude_prefixes: list[str]) -> bool:
    rel_norm = rel_path.strip("/")
    if include_prefixes:
        if not any(rel_norm == p or rel_norm.startswith(p + "/") for p in include_prefixes):
            return False
    if exclude_prefixes:
        if any(rel_norm == p or rel_norm.startswith(p + "/") for p in exclude_prefixes):
            return False
    return True


def iter_files(
    base: Path,
    rel_paths: Iterable[str],
    archive_prefix: str,
    kind: str,
    include_prefixes: list[str] | None = None,
    exclude_prefixes: list[str] | None = None,
) -> list[CollectedFile]:
    include_prefixes = include_prefixes or []
    exclude_prefixes = exclude_prefixes or []
    collected: list[CollectedFile] = []
    for rel in rel_paths:
        path = base / rel
        if not path.exists():
            continue
        if path.is_file():
            rel_norm = rel.replace("\\", "/")
            if not should_include_relative(rel_norm, include_prefixes, exclude_prefixes):
                continue
            collected.append(
                CollectedFile(
                    source=path,
                    archive_path=f"{archive_prefix}/{rel_norm}",
                    sha256=sha256_file(path),
                    size=path.stat().st_size,
                    kind=kind,
                )
            )
        elif path.is_dir():
            for file in sorted(p for p in path.rglob("*") if p.is_file()):
                rel_file = file.relative_to(base).as_posix()
                if not should_include_relative(rel_file, include_prefixes, exclude_prefixes):
                    continue
                collected.append(
                    CollectedFile(
                        source=file,
                        archive_path=f"{archive_prefix}/{rel_file}",
                        sha256=sha256_file(file),
                        size=file.stat().st_size,
                        kind=kind,
                    )
                )
    return collected


def detect_openclaw_version(state_dir: Path) -> str | None:
    candidates = [
        Path(__file__).resolve().parents[4] / "package.json",
        Path.home() / ".nvm/versions/node/current/lib/node_modules/openclaw/package.json",
        Path.home() / ".openclaw/openclaw/package.json",
    ]
    for pkg in candidates:
        if not pkg.exists():
            continue
        try:
            return json.loads(pkg.read_text())["version"]
        except Exception:
            continue
    return None


def build_manifest(
    files: list[CollectedFile],
    mode: str,
    label: str | None,
    workspace: Path,
    state_dir: Path,
    include_prefixes: list[str] | None = None,
    exclude_prefixes: list[str] | None = None,
) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "formatVersion": FORMAT_VERSION,
        "createdAt": now,
        "mode": mode,
        "label": label,
        "filters": {
            "includePrefixes": include_prefixes or [],
            "excludePrefixes": exclude_prefixes or [],
        },
        "host": {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "python": platform.python_version(),
        },
        "openclaw": {
            "version": detect_openclaw_version(state_dir),
            "workspace": str(workspace),
            "stateDir": str(state_dir),
        },
        "files": [
            {
                "path": f.archive_path,
                "sha256": f.sha256,
                "size": f.size,
                "kind": f.kind,
            }
            for f in files
        ],
    }


def safe_label(label: str | None) -> str:
    if not label:
        return "snapshot"
    return "".join(c if c.isalnum() or c in ("-", "_") else "-" for c in label).strip("-") or "snapshot"


def collect_files(
    workspace: Path,
    state_dir: Path,
    mode: str,
    include_prefixes: list[str] | None = None,
    exclude_prefixes: list[str] | None = None,
) -> list[CollectedFile]:
    include_prefixes = include_prefixes or []
    exclude_prefixes = exclude_prefixes or []
    files: list[CollectedFile] = []
    files += iter_files(workspace, MUTABLE_WORKSPACE_FILES, "mutable/workspace", "workspace-mutable", include_prefixes, exclude_prefixes)
    files += iter_files(workspace, MUTABLE_WORKSPACE_DIRS, "mutable/workspace", "workspace-mutable", include_prefixes, exclude_prefixes)
    files += iter_files(state_dir, MUTABLE_STATE_FILES, "mutable/state", "state-mutable", include_prefixes, exclude_prefixes)
    files += iter_files(state_dir, MUTABLE_STATE_DIRS, "mutable/state", "state-mutable", include_prefixes, exclude_prefixes)
    if mode == "full":
        files += iter_files(workspace, STATIC_WORKSPACE_FILES, "static/workspace", "workspace-static", include_prefixes, exclude_prefixes)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="Create versioned OpenClaw state backup archive")
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--state-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--label")
    ap.add_argument("--mode", choices=["mutable", "full"], default="mutable")
    ap.add_argument("--include-prefix", action="append", default=[])
    ap.add_argument("--exclude-prefix", action="append", default=[])
    args = ap.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    state_dir = Path(args.state_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    include_prefixes = [normalize_prefix(p) for p in args.include_prefix if normalize_prefix(p)]
    exclude_prefixes = [normalize_prefix(p) for p in args.exclude_prefix if normalize_prefix(p)]

    files = collect_files(workspace, state_dir, args.mode, include_prefixes, exclude_prefixes)
    manifest = build_manifest(files, args.mode, args.label, workspace, state_dir, include_prefixes, exclude_prefixes)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    label = safe_label(args.label)
    archive_name = f"openclaw-backup-{label}-{args.mode}-{stamp}.tar.gz"
    archive_path = output_dir / archive_name

    with tempfile.TemporaryDirectory(prefix="openclaw-backup-") as tmp:
        tmpdir = Path(tmp)
        meta_dir = tmpdir / "meta"
        meta_dir.mkdir(parents=True, exist_ok=True)
        (meta_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(meta_dir / "manifest.json", arcname="meta/manifest.json")
            for f in files:
                tar.add(f.source, arcname=f.archive_path, recursive=False)

    print(json.dumps({
        "ok": True,
        "archive": str(archive_path),
        "files": len(files),
        "mode": args.mode,
        "label": args.label,
        "filters": {
            "includePrefixes": include_prefixes,
            "excludePrefixes": exclude_prefixes,
        },
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
