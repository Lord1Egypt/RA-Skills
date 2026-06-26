#!/usr/bin/env python3
"""
Apply a zip produced by pack_openclaw.py into a local OpenClaw home + workspace.

Never writes to credentials/. Rejects path-traversal archive names.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile, ZipInfo

from openclaw_paths import openclaw_home, resolve_workspace


def _arc_parts(name: str) -> list[str]:
    return [p for p in name.replace("\\", "/").split("/") if p != ""]


def _is_safe_arcname(name: str) -> bool:
    if not name or name.endswith("/"):
        return False
    parts = _arc_parts(name)
    return ".." not in parts


def _classify_arcname(arcname: str) -> tuple[str, Path] | None:
    """
    Returns (layer, relative Path inside that layer) for file members.
    layer is workspace | managed | sessions | config
    For sessions, relative path is agent_id / rest_under_sessions_dir
    """
    if not _is_safe_arcname(arcname):
        return None
    parts = _arc_parts(arcname)
    if not parts:
        return None
    if parts[0] == "EXPORT_MANIFEST.txt":
        return None
    if parts[0] == "workspace":
        if len(parts) < 2:
            return None
        return ("workspace", Path(*parts[1:]))
    if parts[0] == "managed-skills":
        if len(parts) < 2:
            return None
        return ("managed", Path(*parts[1:]))
    if parts[0] == "sessions":
        # sessions/<agentId>/sessions/<...>
        if len(parts) < 4 or parts[2] != "sessions":
            return None
        agent_id = parts[1]
        rest = Path(*parts[3:]) if len(parts) > 3 else Path()
        return ("sessions", Path(agent_id) / rest)
    if parts[0] == "config" and len(parts) == 2 and parts[1] == "openclaw.json":
        return ("config", Path("openclaw.json"))
    return None


def _resolve_dest(
    layer: str,
    rel: Path,
    *,
    workspace: Path,
    home: Path,
) -> Path | None:
    ws = workspace.resolve()
    hm = home.resolve()
    if layer == "workspace":
        dest = (ws / rel).resolve()
        try:
            dest.relative_to(ws)
        except ValueError:
            return None
        return dest
    if layer == "managed":
        base = (hm / "skills").resolve()
        dest = (base / rel).resolve()
        try:
            dest.relative_to(base)
        except ValueError:
            return None
        return dest
    if layer == "sessions":
        # rel = agent_id / file...
        parts = rel.parts
        if len(parts) < 1:
            return None
        agent_id = parts[0]
        tail = Path(*parts[1:]) if len(parts) > 1 else Path()
        base = (hm / "agents" / agent_id / "sessions").resolve()
        dest = (base / tail).resolve()
        try:
            dest.relative_to((hm / "agents").resolve())
        except ValueError:
            return None
        if agent_id == ".." or ".." in agent_id:
            return None
        return dest
    if layer == "config":
        return (hm / "openclaw.json").resolve()
    return None


def _gather_plan(
    zf: ZipFile,
    *,
    workspace: Path,
    home: Path,
    apply_workspace: bool,
    apply_managed: bool,
    apply_sessions: bool,
    apply_config: bool,
) -> tuple[list[tuple[str, str, Path]], list[str]]:
    """Returns (ops: arcname, layer, dest), skips)."""
    ops: list[tuple[str, str, Path]] = []
    skips: list[str] = []
    names = {zi.filename.replace("\\", "/"): zi for zi in zf.infolist()}
    for arcname, zi in sorted(names.items()):
        if zi.is_dir():
            continue
        cl = _classify_arcname(arcname)
        if cl is None:
            if arcname != "EXPORT_MANIFEST.txt" and not arcname.endswith("EXPORT_MANIFEST.txt"):
                skips.append(f"unrecognized (skipped): {arcname}")
            continue
        layer, rel = cl
        if layer == "workspace" and not apply_workspace:
            skips.append(f"skipped (--no-apply-workspace): {arcname}")
            continue
        if layer == "managed" and not apply_managed:
            skips.append(f"skipped (need --apply-managed-skills): {arcname}")
            continue
        if layer == "sessions" and not apply_sessions:
            skips.append(f"skipped (need --apply-sessions + ack): {arcname}")
            continue
        if layer == "config" and not apply_config:
            skips.append(f"skipped (need --apply-config + ack): {arcname}")
            continue
        dest = _resolve_dest(layer, rel, workspace=workspace, home=home)
        if dest is None:
            skips.append(f"unsafe path (skipped): {arcname}")
            continue
        ops.append((arcname, layer, dest))
    return ops, skips


def _write_member(zf: ZipFile, zi: ZipInfo, dest: Path, *, dry_run: bool) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        return
    with zf.open(zi, "r") as src:
        data = src.read()
    dest.write_bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply openclaw-user-export zip (from pack_openclaw.py) into local OpenClaw dirs."
    )
    parser.add_argument("--zip", "-z", type=Path, required=True, help="Path to export .zip")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Target workspace root (created if missing when passed; else resolve from config)",
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
        help="Path to openclaw.json for workspace resolution (default: <openclaw-home>/openclaw.json)",
    )
    parser.add_argument(
        "--no-apply-workspace",
        action="store_true",
        help="Do not extract workspace/ from zip",
    )
    parser.add_argument(
        "--apply-managed-skills",
        action="store_true",
        help="Extract managed-skills/ into ~/.openclaw/skills/",
    )
    parser.add_argument(
        "--apply-sessions",
        action="store_true",
        help="Extract sessions/ into ~/.openclaw/agents/<id>/sessions/",
    )
    parser.add_argument(
        "--i-know-restoring-sessions-overwrites",
        action="store_true",
        help="Required with --apply-sessions",
    )
    parser.add_argument(
        "--apply-config",
        action="store_true",
        help="Write config/openclaw.json from zip to ~/.openclaw/openclaw.json",
    )
    parser.add_argument(
        "--i-know-config-overwrites-secrets",
        action="store_true",
        help="Required with --apply-config",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned writes only",
    )
    args = parser.parse_args()

    if args.apply_sessions and not args.i_know_restoring_sessions_overwrites:
        raise SystemExit("Refusing --apply-sessions without --i-know-restoring-sessions-overwrites")

    if args.apply_config and not args.i_know_config_overwrites_secrets:
        raise SystemExit("Refusing --apply-config without --i-know-config-overwrites-secrets")

    home = (args.openclaw_home or openclaw_home()).expanduser().resolve()
    cfg_path = args.config.expanduser().resolve() if args.config else None

    if args.workspace is not None:
        ws = args.workspace.expanduser().resolve()
        ws.mkdir(parents=True, exist_ok=True)
    else:
        ws = resolve_workspace(workspace=None, openclaw_home_dir=home, config_path=cfg_path)

    zip_path = args.zip.expanduser().resolve()
    if not zip_path.is_file():
        raise SystemExit(f"zip not found: {zip_path}")

    apply_workspace = not args.no_apply_workspace

    with ZipFile(zip_path, "r") as zf:
        ops, skips = _gather_plan(
            zf,
            workspace=ws,
            home=home,
            apply_workspace=apply_workspace,
            apply_managed=args.apply_managed_skills,
            apply_sessions=args.apply_sessions,
            apply_config=args.apply_config,
        )

        for s in skips:
            print(f"warning: {s}", file=sys.stderr)

        if not ops:
            raise SystemExit("Nothing to apply (check flags and zip contents).")

        # Config: backup existing
        config_ops = [(a, l, d) for a, l, d in ops if l == "config"]
        other_ops = [(a, l, d) for a, l, d in ops if l != "config"]

        print(f"openclaw_home: {home}")
        print(f"workspace: {ws}")
        print(f"operations: {len(ops)}")

        if args.dry_run:
            for arc, layer, dest in sorted(ops, key=lambda x: x[2].as_posix()):
                print(f"  [{layer}] {arc}  ->  {dest}")
            return

        name_map = {zi.filename.replace("\\", "/"): zi for zi in zf.infolist()}
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Non-config first so files land before openclaw.json is replaced.
        for arc, layer, dest in sorted(other_ops, key=lambda x: x[2].as_posix()):
            zi = name_map.get(arc)
            if zi is None:
                continue
            _write_member(zf, zi, dest, dry_run=False)
            print(f"wrote: {dest}")

        for arc, layer, dest in config_ops:
            cfg_dest = dest
            if cfg_dest.is_file():
                bak = cfg_dest.with_name(f"openclaw.json.bak.{stamp}")
                shutil.copy2(cfg_dest, bak)
                print(f"backup: {bak}", file=sys.stderr)
            zi = name_map.get(arc)
            if zi is None:
                continue
            _write_member(zf, zi, cfg_dest, dry_run=False)
            print(f"wrote: {cfg_dest}")

    print("done.")


if __name__ == "__main__":
    main()
