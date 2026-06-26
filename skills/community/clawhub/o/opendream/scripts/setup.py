#!/usr/bin/env python3
"""
OpenDream setup script — installs the dream skill into an OpenClaw workspace.

Usage:
    python3 scripts/setup.py                     # auto-detect workspace
    python3 scripts/setup.py /path/to/workspace   # explicit workspace path
    python3 scripts/setup.py --dry-run            # preview without changes

What it does:
    1. Detects your OpenClaw workspace directory
    2. Backs up HEARTBEAT.md, SOUL.md, and openclaw.json before modifying
    3. Merges the dream section into HEARTBEAT.md
    4. Merges the dream persona fragment into SOUL.md
    5. Creates the dreams/ directory
    6. Merges heartbeat config into openclaw.json
    7. Validates the installation

Note: The optional live dream viewer (tools/viewer/) is installed separately.
      See tools/viewer/README.md for instructions.
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths — relative to the skill directory
# ---------------------------------------------------------------------------

SKILL_DIR = Path(__file__).resolve().parent.parent          # skills/opendream/
ASSETS_DIR = SKILL_DIR / "assets"

HEARTBEAT_SECTION = ASSETS_DIR / "HEARTBEAT-dream-section.md"
SOUL_FRAGMENT = ASSETS_DIR / "SOUL-fragment.md"
GATEWAY_CONFIG = ASSETS_DIR / "openclaw.json"

DREAM_MARKER = "## Dream mode"


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


# ---------------------------------------------------------------------------
# Workspace detection
# ---------------------------------------------------------------------------

def find_workspace(explicit: str | None = None) -> Path:
    """Return the OpenClaw workspace directory."""
    if explicit:
        ws = Path(explicit).expanduser().resolve()
        if not ws.is_dir():
            fail(f"Workspace path does not exist: {ws}")
        return ws

    # Walk up from the skill dir — workspace is the grandparent of skills/
    candidate = SKILL_DIR.parent.parent  # skills/ -> workspace/
    if (candidate / "AGENTS.md").exists() or (candidate / "SOUL.md").exists():
        return candidate

    # Fallback: default OpenClaw location
    default = Path.home() / ".openclaw" / "workspace"
    if default.is_dir():
        return default

    fail(
        "Could not detect your OpenClaw workspace.\n"
        "  Run with an explicit path: python3 scripts/setup.py /path/to/workspace"
    )


def find_openclaw_root(workspace: Path) -> Path:
    """Return the OpenClaw root directory (parent of workspace/)."""
    return workspace.parent


# ---------------------------------------------------------------------------
# Backup
# ---------------------------------------------------------------------------

def backup(filepath: Path) -> Path | None:
    """Create a timestamped backup. Returns backup path or None."""
    if not filepath.exists():
        return None
    backup_dir = filepath.parent / ".opendream-backups"
    backup_dir.mkdir(exist_ok=True)
    dest = backup_dir / f"{filepath.name}.{timestamp()}"
    shutil.copy2(filepath, dest)
    info(f"Backed up {filepath.name} -> {dest.relative_to(filepath.parent)}")
    return dest


# ---------------------------------------------------------------------------
# HEARTBEAT.md merge
# ---------------------------------------------------------------------------

def merge_heartbeat(workspace: Path) -> bool:
    """Merge the dream section into HEARTBEAT.md. Returns True if modified."""
    target = workspace / "HEARTBEAT.md"
    section = HEARTBEAT_SECTION.read_text()

    if target.exists():
        existing = target.read_text()
        if DREAM_MARKER in existing:
            info("HEARTBEAT.md already contains dream section — skipping")
            return True
        backup(target)
        merged = existing.rstrip() + "\n\n" + section.strip() + "\n"
        target.write_text(merged)
        info("Merged dream section into existing HEARTBEAT.md")
    else:
        header = "# Heartbeat checklist\n\n"
        daytime = (
            "## Daytime (06:00-23:00)\n"
            "- Quick scan: anything urgent in reminders, calendar, or inboxes?\n"
            "- If nothing urgent, reply HEARTBEAT_OK.\n\n"
        )
        target.write_text(header + daytime + section.strip() + "\n")
        info("Created HEARTBEAT.md with dream section")

    return True


# ---------------------------------------------------------------------------
# SOUL.md merge
# ---------------------------------------------------------------------------

def merge_soul(workspace: Path) -> bool:
    """Merge the dream persona fragment into SOUL.md. Returns True if modified."""
    target = workspace / "SOUL.md"
    fragment = SOUL_FRAGMENT.read_text()

    if target.exists():
        existing = target.read_text()
        if DREAM_MARKER in existing:
            info("SOUL.md already contains dream persona — skipping")
            return True
        backup(target)
        merged = existing.rstrip() + "\n\n" + fragment.strip() + "\n"
        target.write_text(merged)
        info("Merged dream persona fragment into existing SOUL.md")
    else:
        target.write_text(fragment.strip() + "\n")
        info("Created SOUL.md with dream persona fragment")

    return True


# ---------------------------------------------------------------------------
# Dreams directory
# ---------------------------------------------------------------------------

def create_dreams_dir(workspace: Path) -> bool:
    """Create the dreams/ directory. Returns True on success."""
    dreams = workspace / "dreams"
    if dreams.is_dir():
        info("dreams/ directory already exists")
        return True
    dreams.mkdir(parents=True, exist_ok=True)
    (dreams / ".gitkeep").touch()
    info("Created dreams/ directory")
    return True


# ---------------------------------------------------------------------------
# Gateway config merge (openclaw.json)
# ---------------------------------------------------------------------------

def merge_gateway_config(workspace: Path) -> bool:
    """Merge heartbeat config into openclaw.json. Returns True on success."""
    root = find_openclaw_root(workspace)
    target = root / "openclaw.json"
    snippet = json.loads(GATEWAY_CONFIG.read_text())

    if not target.exists():
        # Create a new config from the snippet
        target.write_text(json.dumps(snippet, indent=2) + "\n")
        info(f"Created {target.name} with heartbeat config")
        return True

    try:
        existing = json.loads(target.read_text())
    except json.JSONDecodeError:
        warn(f"{target.name} is not valid JSON — skipping gateway merge")
        return False

    # Check if dream config already present
    hb = existing.get("agents", {}).get("defaults", {}).get("heartbeat", {})
    if hb.get("activeHours", {}).get("start") == "23:00":
        info("openclaw.json already has dream heartbeat config — skipping")
        return True

    backup(target)

    # Navigate/create the path: agents.defaults.heartbeat
    agents = existing.setdefault("agents", {})
    defaults = agents.setdefault("defaults", {})

    if "heartbeat" in defaults and defaults["heartbeat"]:
        warn(
            f"openclaw.json has existing heartbeat config "
            f"(activeHours: {json.dumps(hb.get('activeHours', 'none'))}). "
            f"Overwriting with dream config."
        )

    defaults["heartbeat"] = snippet["agents"]["defaults"]["heartbeat"]
    target.write_text(json.dumps(existing, indent=2) + "\n")
    info("Merged heartbeat config into openclaw.json")
    return True


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(workspace: Path) -> list[str]:
    """Run quick validation checks. Returns list of issues (empty = all good)."""
    issues = []

    hb = workspace / "HEARTBEAT.md"
    if not hb.exists():
        issues.append("HEARTBEAT.md does not exist")
    elif DREAM_MARKER not in hb.read_text():
        issues.append("HEARTBEAT.md missing dream section")

    soul = workspace / "SOUL.md"
    if not soul.exists():
        issues.append("SOUL.md does not exist")
    elif DREAM_MARKER not in soul.read_text():
        issues.append("SOUL.md missing dream persona fragment")

    if not (workspace / "dreams").is_dir():
        issues.append("dreams/ directory does not exist")

    root = find_openclaw_root(workspace)
    config = root / "openclaw.json"
    if config.exists():
        try:
            cfg = json.loads(config.read_text())
            hb = cfg.get("agents", {}).get("defaults", {}).get("heartbeat", {})
            active = hb.get("activeHours", {})
            if active.get("start") != "23:00" or active.get("end") != "06:00":
                issues.append("openclaw.json heartbeat activeHours not set to 23:00-06:00")
            prompt = hb.get("prompt", "")
            if "SOUL.md" not in prompt:
                issues.append("openclaw.json heartbeat prompt does not reference SOUL.md")
        except json.JSONDecodeError:
            issues.append("openclaw.json is not valid JSON")
    else:
        issues.append("openclaw.json not found")

    return issues


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

def info(msg: str):
    print(f"  [ok] {msg}")


def warn(msg: str):
    print(f"  [!!] {msg}")


def fail(msg: str):
    print(f"\n  [FAIL] {msg}\n", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> tuple:
    """Parse CLI args. Returns (workspace_path_or_None, dry_run)."""
    dry_run = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    workspace_path = args[0] if args else None
    return workspace_path, dry_run


def main():
    print("\n--- OpenDream Setup ---\n")

    workspace_path, dry_run = parse_args()
    workspace = find_workspace(workspace_path)
    print(f"  Workspace: {workspace}")
    if dry_run:
        print("  Mode: dry run (no changes)\n")
        # In dry-run, just validate current state
        issues = validate(workspace)
        if issues:
            for issue in issues:
                print(f"  [ ] {issue}")
            print(f"\n  {len(issues)} item(s) would be configured by setup.\n")
        else:
            print("  Everything is already configured.\n")
        return

    print()

    # Verify skill assets exist
    for name, asset in [("HEARTBEAT section", HEARTBEAT_SECTION),
                         ("SOUL fragment", SOUL_FRAGMENT),
                         ("Gateway config", GATEWAY_CONFIG)]:
        if not asset.exists():
            fail(f"Missing required asset ({name}): {asset}")

    # Step 1: HEARTBEAT.md
    print("  [1/4] HEARTBEAT.md")
    merge_heartbeat(workspace)

    # Step 2: SOUL.md
    print("  [2/4] SOUL.md")
    merge_soul(workspace)

    # Step 3: dreams/ directory
    print("  [3/4] dreams/ directory")
    create_dreams_dir(workspace)

    # Step 4: Gateway config
    print("  [4/4] Gateway config (openclaw.json)")
    merge_gateway_config(workspace)

    # Validate
    print("\n  --- Validation ---\n")
    issues = validate(workspace)
    if issues:
        for issue in issues:
            warn(issue)
        print(
            f"\n  Setup completed with {len(issues)} warning(s).\n"
            "  Run: python3 scripts/validate.py\n"
        )
    else:
        print("  [ok] All checks passed. OpenDream is installed.\n")
        print("  Your agent will begin dreaming at 23:00 tonight.")
        print("  Dream files will appear in: dreams/YYYY-MM-DD/")
        print("  Restart gateway if needed: openclaw gateway restart\n")


if __name__ == "__main__":
    main()
