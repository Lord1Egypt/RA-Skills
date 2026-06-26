#!/usr/bin/env python3
"""
Pack OpenClaw user-owned data into a zip with EXPORT_MANIFEST.txt inside the archive.

Never includes ~/.openclaw/credentials/ (not implemented — do not add).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from openclaw_paths import openclaw_home, resolve_workspace


def iter_files(root: Path, *, exclude_git: bool) -> Iterable[Path]:
    root = root.resolve()
    always_skip = {"__pycache__", ".venv", "node_modules"}
    for dirpath, dirnames, filenames in os.walk(root):
        remove = [d for d in dirnames if d in always_skip or (d == ".git" and exclude_git)]
        for d in remove:
            dirnames.remove(d)
        for name in filenames:
            yield Path(dirpath) / name


@dataclass
class ManifestEntry:
    arcname: str
    size: int
    sha256: str | None = None


@dataclass
class PackPlan:
    entries: list[tuple[Path, str]] = field(default_factory=list)  # (abs_path, arcname)
    warnings: list[str] = field(default_factory=list)

    def total_bytes(self) -> int:
        return sum(p.stat().st_size for p, _ in self.entries if p.is_file())


def plan_workspace(root: Path, *, exclude_git: bool) -> PackPlan:
    plan = PackPlan()
    root = root.resolve()
    if not root.is_dir():
        plan.warnings.append(f"missing workspace: {root}")
        return plan
    prefix = "workspace/"
    for f in iter_files(root, exclude_git=exclude_git):
        if not f.is_file():
            continue
        try:
            rel = f.relative_to(root)
        except ValueError:
            continue
        arc = prefix + rel.as_posix()
        plan.entries.append((f, arc))
    return plan


def plan_managed_skills(home: Path) -> PackPlan:
    plan = PackPlan()
    skills = (home / "skills").resolve()
    if not skills.is_dir():
        plan.warnings.append(f"managed skills directory missing: {skills}")
        return plan
    prefix = "managed-skills/"
    for f in iter_files(skills, exclude_git=True):
        if not f.is_file():
            continue
        rel = f.relative_to(skills)
        plan.entries.append((f, prefix + rel.as_posix()))
    return plan


def plan_sessions(home: Path) -> PackPlan:
    plan = PackPlan()
    agents = home / "agents"
    if not agents.is_dir():
        plan.warnings.append(f"agents directory missing: {agents}")
        return plan
    for agent_dir in sorted(agents.iterdir()):
        if not agent_dir.is_dir():
            continue
        sess = agent_dir / "sessions"
        if not sess.is_dir():
            continue
        agent_id = agent_dir.name
        base = f"sessions/{agent_id}/sessions/"
        for f in iter_files(sess, exclude_git=True):
            if not f.is_file():
                continue
            rel = f.relative_to(sess)
            plan.entries.append((f, base + rel.as_posix()))
    if not any(e[1].startswith("sessions/") for e in plan.entries):
        plan.warnings.append("no session directories found under ~/.openclaw/agents/*/sessions/")
    return plan


def plan_config(home: Path) -> PackPlan:
    plan = PackPlan()
    cfg = home / "openclaw.json"
    if not cfg.is_file():
        plan.warnings.append(f"config missing: {cfg}")
        return plan
    plan.entries.append((cfg.resolve(), "config/openclaw.json"))
    return plan


def file_sha256(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        while True:
            b = fp.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def build_manifest(
    entries: list[tuple[Path, str]],
    *,
    with_sha256: bool,
    sha256_max_mb: float,
) -> list[ManifestEntry]:
    out: list[ManifestEntry] = []
    max_b = int(sha256_max_mb * 1024 * 1024)
    for abs_path, arcname in sorted(entries, key=lambda x: x[1]):
        if not abs_path.is_file():
            continue
        size = abs_path.stat().st_size
        digest = None
        if with_sha256 and size <= max_b:
            digest = file_sha256(abs_path)
        out.append(ManifestEntry(arcname=arcname, size=size, sha256=digest))
    return out


def write_zip(
    output: Path,
    entries: list[tuple[Path, str]],
    *,
    with_sha256: bool,
    sha256_max_mb: float,
) -> str:
    manifest_lines = [
        "# OpenClaw user data export",
        f"# created_utc: {datetime.now(timezone.utc).isoformat()}",
        "# format: path<TAB>size_bytes<TAB>sha256_or_empty",
        "",
    ]
    m_entries = build_manifest(entries, with_sha256=with_sha256, sha256_max_mb=sha256_max_mb)
    for m in m_entries:
        sh = m.sha256 or ""
        manifest_lines.append(f"{m.arcname}\t{m.size}\t{sh}")

    manifest_body = "\n".join(manifest_lines) + "\n"

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("EXPORT_MANIFEST.txt", manifest_body.encode("utf-8"))
        seen: set[str] = {"EXPORT_MANIFEST.txt"}
        for abs_path, arcname in entries:
            if not abs_path.is_file():
                continue
            if arcname in seen:
                continue
            seen.add(arcname)
            zf.write(abs_path, arcname)

    return manifest_body


def main() -> None:
    parser = argparse.ArgumentParser(description="Pack OpenClaw user data into a zip (workspace + optional layers).")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Agent workspace root (default: resolve from openclaw.json or ~/.openclaw/workspace[-profile])",
    )
    parser.add_argument(
        "--openclaw-home",
        type=Path,
        default=None,
        help="OpenClaw data directory (default: $OPENCLAW_HOME or ~/.openclaw)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to openclaw.json for workspace resolution only (default: <openclaw-home>/openclaw.json)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output zip path (default: ./openclaw-user-export-YYYYMMDD-HHMMSS.zip in cwd)",
    )
    parser.add_argument(
        "--exclude-git",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Skip .git directories under workspace (default: true)",
    )
    parser.add_argument(
        "--managed-skills",
        action="store_true",
        help="Include ~/.openclaw/skills as managed-skills/",
    )
    parser.add_argument(
        "--sessions",
        action="store_true",
        help="Include ~/.openclaw/agents/*/sessions/ (large, full chat transcripts)",
    )
    parser.add_argument(
        "--i-know-sessions-are-large-and-sensitive",
        action="store_true",
        help="Required with --sessions",
    )
    parser.add_argument(
        "--config-snapshot",
        action="store_true",
        help="Include openclaw.json as config/openclaw.json (may contain secrets)",
    )
    parser.add_argument(
        "--i-know-config-may-contain-secrets",
        action="store_true",
        help="Required with --config-snapshot",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned files and totals; do not write zip",
    )
    parser.add_argument(
        "--manifest-sha256",
        action="store_true",
        help="Add SHA256 per file in EXPORT_MANIFEST.txt (skipped for files larger than --sha256-max-mb)",
    )
    parser.add_argument(
        "--sha256-max-mb",
        type=float,
        default=32.0,
        help="Max file size (MB) to checksum when --manifest-sha256 (default: 32)",
    )

    args = parser.parse_args()
    home = (args.openclaw_home or openclaw_home()).expanduser().resolve()

    if args.sessions and not args.i_know_sessions_are_large_and_sensitive:
        raise SystemExit("Refusing --sessions without --i-know-sessions-are-large-and-sensitive")

    if args.config_snapshot and not args.i_know_config_may_contain_secrets:
        raise SystemExit("Refusing --config-snapshot without --i-know-config-may-contain-secrets")

    cfg_path = args.config.expanduser().resolve() if args.config else None
    ws = resolve_workspace(workspace=args.workspace, openclaw_home_dir=home, config_path=cfg_path)

    plans: list[PackPlan] = [plan_workspace(ws, exclude_git=args.exclude_git)]
    if args.managed_skills:
        plans.append(plan_managed_skills(home))
    if args.sessions:
        plans.append(plan_sessions(home))
    if args.config_snapshot:
        plans.append(plan_config(home))

    merged: list[tuple[Path, str]] = []
    for p in plans:
        merged.extend(p.entries)

    if not merged:
        raise SystemExit("Nothing to pack.")

    for p in plans:
        for w in p.warnings:
            print(f"warning: {w}", file=sys.stderr)

    total_files = len(merged)
    total_bytes = sum(Path(a).stat().st_size for a, _ in merged if Path(a).is_file())

    print(f"workspace: {ws}")
    print(f"openclaw_home: {home}")
    print(f"files: {total_files}  bytes: {total_bytes}")

    if args.dry_run:
        for abs_path, arc in sorted(merged, key=lambda x: x[1])[:500]:
            print(f"  {arc}  <=  {abs_path}")
        if total_files > 500:
            print(f"  ... ({total_files - 500} more)")
        return

    out = args.output
    if out is None:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out = Path.cwd() / f"openclaw-user-export-{stamp}.zip"
    else:
        out = out.expanduser().resolve()

    write_zip(
        out,
        merged,
        with_sha256=args.manifest_sha256,
        sha256_max_mb=args.sha256_max_mb,
    )
    print(f"wrote: {out}")


if __name__ == "__main__":
    main()
