#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backup_state import FORMAT_VERSION  # type: ignore
import backup_state  # type: ignore


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(tmpdir: Path) -> dict[str, Any]:
    manifest_path = tmpdir / "meta" / "manifest.json"
    if not manifest_path.exists():
        raise RuntimeError("manifest.json missing from archive")
    return json.loads(manifest_path.read_text())


def check_compat(manifest: dict[str, Any], allow_version_mismatch: bool) -> list[str]:
    warnings: list[str] = []
    if manifest.get("formatVersion") != FORMAT_VERSION:
        raise RuntimeError(f"Unsupported formatVersion: {manifest.get('formatVersion')}")
    archived_version = ((manifest.get("openclaw") or {}).get("version"))
    current_version = backup_state.detect_openclaw_version(Path.home() / ".openclaw")
    if archived_version and current_version and archived_version != current_version:
        msg = f"OpenClaw version mismatch: archive={archived_version} current={current_version}"
        if allow_version_mismatch:
            warnings.append(msg)
        else:
            raise RuntimeError(msg)
    return warnings


def verify_manifest(tmpdir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    restored: list[dict[str, Any]] = []
    for item in manifest.get("files", []):
        path = tmpdir / item["path"]
        if not path.exists():
            raise RuntimeError(f"Archive file missing: {item['path']}")
        digest = sha256_file(path)
        if digest != item["sha256"]:
            raise RuntimeError(f"Checksum mismatch: {item['path']}")
        restored.append(item)
    return restored


def archive_to_dest(rel: str, workspace: Path, state_dir: Path) -> Path:
    rel_path = Path(rel)
    parts = rel_path.parts
    if len(parts) < 3:
        raise RuntimeError(f"Unexpected archive path: {rel}")
    scope = parts[1]
    remainder = Path(*parts[2:])
    if scope == "workspace":
        return workspace / remainder
    if scope == "state":
        return state_dir / remainder
    raise RuntimeError(f"Unknown archive scope: {scope}")


def write_report(report_dir: Path, report: dict[str, Any], prefix: str = "restore-report") -> str:
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = report_dir / f"{prefix}-{stamp}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    return str(path)


def make_rollback(
    workspace: Path,
    state_dir: Path,
    output_dir: Path,
    include_prefixes: list[str] | None = None,
    exclude_prefixes: list[str] | None = None,
) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rollback_dir = output_dir / "rollbacks"
    rollback_dir.mkdir(parents=True, exist_ok=True)
    label = f"pre-restore-{stamp}"
    files = backup_state.collect_files(
        workspace,
        state_dir,
        "full",
        include_prefixes=include_prefixes,
        exclude_prefixes=exclude_prefixes,
    )
    manifest = backup_state.build_manifest(
        files,
        "full",
        label,
        workspace,
        state_dir,
        include_prefixes=include_prefixes,
        exclude_prefixes=exclude_prefixes,
    )
    archive_name = f"openclaw-backup-{backup_state.safe_label(label)}-full-{stamp}.tar.gz"
    archive_path = rollback_dir / archive_name
    with tempfile.TemporaryDirectory(prefix="openclaw-rollback-") as td:
        tmpdir = Path(td)
        meta_dir = tmpdir / "meta"
        meta_dir.mkdir(parents=True, exist_ok=True)
        (meta_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(meta_dir / "manifest.json", arcname="meta/manifest.json")
            for f in files:
                tar.add(f.source, arcname=f.archive_path, recursive=False)
    return str(archive_path)


def build_plan(
    verified_files: list[dict[str, Any]],
    tmpdir: Path,
    workspace: Path,
    state_dir: Path,
    include_prefixes: list[str] | None = None,
    exclude_prefixes: list[str] | None = None,
) -> dict[str, Any]:
    plan_items: list[dict[str, Any]] = []
    counts = {"create": 0, "update": 0, "unchanged": 0}
    for item in verified_files:
        dst = archive_to_dest(item["path"], workspace, state_dir)
        src_sha = item["sha256"]
        exists = dst.exists()
        dst_sha = sha256_file(dst) if exists and dst.is_file() else None
        if not exists:
            action = "create"
        elif dst_sha == src_sha:
            action = "unchanged"
        else:
            action = "update"
        counts[action] += 1
        plan_items.append({
            "archivePath": item["path"],
            "targetPath": str(dst),
            "action": action,
            "sourceSha256": src_sha,
            "targetSha256": dst_sha,
            "size": item.get("size"),
            "kind": item.get("kind"),
        })

    target_paths = {entry["targetPath"] for entry in plan_items}
    missing_from_archive: list[str] = []
    current_files = backup_state.collect_files(
        workspace,
        state_dir,
        manifest_mode_guess(verified_files),
        include_prefixes=include_prefixes,
        exclude_prefixes=exclude_prefixes,
    )
    for f in current_files:
        if str(f.source.resolve()) not in target_paths:
            missing_from_archive.append(str(f.source.resolve()))

    return {
        "summary": {
            "create": counts["create"],
            "update": counts["update"],
            "unchanged": counts["unchanged"],
            "missingFromArchive": len(missing_from_archive),
            "total": len(plan_items),
        },
        "changes": plan_items,
        "missingFromArchive": missing_from_archive,
    }


def manifest_mode_guess(verified_files: list[dict[str, Any]]) -> str:
    if any(str(item.get("path", "")).startswith("static/") for item in verified_files):
        return "full"
    return "mutable"


def main() -> int:
    ap = argparse.ArgumentParser(description="Restore versioned OpenClaw state backup archive")
    ap.add_argument("--archive", required=True)
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--state-dir", required=True)
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-version-mismatch", action="store_true")
    ap.add_argument("--rollback-dir")
    ap.add_argument("--report-dir")
    ap.add_argument("--include-prefix", action="append", default=[])
    ap.add_argument("--exclude-prefix", action="append", default=[])
    args = ap.parse_args()

    archive = Path(args.archive).expanduser().resolve()
    workspace = Path(args.workspace).expanduser().resolve()
    state_dir = Path(args.state_dir).expanduser().resolve()
    rollback_dir = Path(args.rollback_dir).expanduser().resolve() if args.rollback_dir else archive.parent
    report_dir = Path(args.report_dir).expanduser().resolve() if args.report_dir else archive.parent
    include_prefixes = [backup_state.normalize_prefix(p) for p in args.include_prefix if backup_state.normalize_prefix(p)]
    exclude_prefixes = [backup_state.normalize_prefix(p) for p in args.exclude_prefix if backup_state.normalize_prefix(p)]

    if not archive.exists():
        raise SystemExit(f"Archive not found: {archive}")

    with tempfile.TemporaryDirectory(prefix="openclaw-restore-") as td:
        tmpdir = Path(td)
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(tmpdir)

        manifest = load_manifest(tmpdir)
        warnings = check_compat(manifest, args.allow_version_mismatch)
        verified_files = verify_manifest(tmpdir, manifest)
        if include_prefixes or exclude_prefixes:
            filtered = []
            for item in verified_files:
                rel = "/".join(Path(item["path"]).parts[2:])
                if backup_state.should_include_relative(rel, include_prefixes, exclude_prefixes):
                    filtered.append(item)
            verified_files = filtered
        plan = build_plan(verified_files, tmpdir, workspace, state_dir, include_prefixes, exclude_prefixes)

        pre_report = {
            "ok": True,
            "verified": True,
            "dryRun": bool(args.dry_run),
            "archive": str(archive),
            "files": len(verified_files),
            "warnings": warnings,
            "filters": {
                "includePrefixes": include_prefixes,
                "excludePrefixes": exclude_prefixes,
            },
            "plan": plan,
        }

        if args.verify_only or args.dry_run:
            report_path = write_report(report_dir, pre_report)
            pre_report["reportPath"] = report_path
            print(json.dumps(pre_report, ensure_ascii=False, indent=2))
            return 0

        rollback_archive = make_rollback(workspace, state_dir, rollback_dir, include_prefixes, exclude_prefixes)
        restored_paths = []
        for item in verified_files:
            src = tmpdir / item["path"]
            dst = archive_to_dest(item["path"], workspace, state_dir)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            restored_paths.append(str(dst))

        final_report = {
            "ok": True,
            "archive": str(archive),
            "rollbackArchive": rollback_archive,
            "restored": len(restored_paths),
            "warnings": warnings,
            "filters": {
                "includePrefixes": include_prefixes,
                "excludePrefixes": exclude_prefixes,
            },
            "plan": plan,
        }
        report_path = write_report(report_dir, final_report)
        final_report["reportPath"] = report_path
        print(json.dumps(final_report, ensure_ascii=False, indent=2))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
