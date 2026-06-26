#!/usr/bin/env python3
"""
OpenDream Validation Script
Check if OpenDream is properly configured.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).resolve().parent.parent


def find_workspace(explicit: str | None = None) -> Path:
    if explicit:
        ws = Path(explicit).expanduser().resolve()
        if not ws.is_dir():
            print(f"  Path does not exist: {ws}", file=sys.stderr)
            sys.exit(1)
        return ws
    candidate = SKILL_DIR.parent.parent
    if (candidate / "AGENTS.md").exists() or (candidate / "SOUL.md").exists():
        return candidate
    default = Path.home() / ".openclaw" / "workspace"
    if default.is_dir():
        return default
    print("  Could not detect workspace. Pass path as argument.", file=sys.stderr)
    sys.exit(1)

def check_file(filepath: Path, required_content: str = None) -> tuple:
    """Check if a file exists and optionally contains specific content."""
    if not filepath.exists():
        return False, "File does not exist"
    
    if required_content:
        content = filepath.read_text()
        if required_content not in content:
            return False, f"Missing content: {required_content[:30]}..."
    
    return True, "OK"

def check_gateway_config(gateway_file: Path):
    """Check gateway heartbeat configuration."""
    if not gateway_file.exists():
        return False, "Gateway config not found"
    
    try:
        with open(gateway_file) as f:
            config = json.load(f)
        
        heartbeat = config.get("agents", {}).get("defaults", {}).get("heartbeat", {})
        
        required_keys = ["activeHours", "isolatedSession", "lightContext", "every"]
        missing = [k for k in required_keys if k not in heartbeat]
        
        if missing:
            return False, f"Missing keys: {', '.join(missing)}"
        
        active_hours = heartbeat.get("activeHours", {})
        if "start" not in active_hours or "end" not in active_hours:
            return False, "activeHours missing start/end"
        
        return True, f"activeHours: {active_hours.get('start')}–{active_hours.get('end')}"
    
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, str(e)

def check_dreams_today(dreams_dir: Path):
    """Check if there are dream files for today."""
    today = datetime.now().strftime("%Y-%m-%d")
    today_dir = dreams_dir / today
    
    if not today_dir.exists():
        return None, "No dreams yet today"
    
    files = list(today_dir.glob("*.md"))
    if not files:
        return None, "Dream directory exists but empty"
    
    return True, f"{len(files)} file(s)"

def main():
    explicit = sys.argv[1] if len(sys.argv) > 1 else None
    workspace = find_workspace(explicit)
    root = workspace.parent

    heartbeat_file = workspace / "HEARTBEAT.md"
    soul_file = workspace / "SOUL.md"
    dreams_dir = workspace / "dreams"
    gateway_file = root / "openclaw.json"

    print("=" * 50)
    print("OpenDream Validation")
    print("=" * 50)
    print(f"\n  Workspace: {workspace}\n")
    
    memory_dir = workspace / "memory"

    checks = [
        ("HEARTBEAT.md", lambda: check_file(heartbeat_file, "## Dream mode")),
        ("SOUL.md", lambda: check_file(soul_file, "ElectricSheep mode")),
        ("Dreams directory", lambda: check_file(dreams_dir)),
        ("Memory directory", lambda: (None, "Not yet created (OpenClaw creates on first use)") if not memory_dir.is_dir() else (True, "OK")),
        ("Gateway config", lambda: check_gateway_config(gateway_file)),
        ("Today's dreams", lambda: check_dreams_today(dreams_dir)),
    ]
    
    results = []
    
    for name, check_func in checks:
        status, msg = check_func()
        symbol = "✓" if status else ("○" if status is None else "✗")
        results.append((name, status, symbol, msg))
        print(f"\n{symbol} {name}")
        print(f"  {msg}")
    
    print("\n" + "=" * 50)
    
    critical = [r for r in results if r[1] is False]
    optional = [r for r in results if r[1] is None]
    passed = [r for r in results if r[1] is True]
    
    if critical:
        print(f"⚠️  {len(critical)} critical issue(s) found")
        print("\nRun setup to fix:")
        print("  python3 scripts/setup.py")
        sys.exit(1)
    else:
        print(f"✅ All checks passed ({len(passed)} critical, {len(optional)} optional)")
        
        if optional:
            print(f"\nNote: {optional[0][0]} — this is normal if dream window hasn't started")
        
        print("\nDream mode active: 23:00–06:00")
        print("Restart gateway if you haven't:")
        print("  openclaw gateway restart")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
