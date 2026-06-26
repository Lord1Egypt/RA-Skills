#!/usr/bin/env python3
"""Ensure a workspace has a local persona library.

Usage:
  python3 ensure-personas.py <workspace_root> <skill_dir>
"""

from pathlib import Path
import shutil
import subprocess
import sys
import json


def main():
    if len(sys.argv) != 3:
        print("Usage: ensure-personas.py <workspace_root> <skill_dir>", file=sys.stderr)
        sys.exit(1)

    workspace = Path(sys.argv[1]).expanduser().resolve()
    skill_dir = Path(sys.argv[2]).expanduser().resolve()
    personas_dir = workspace / "personas"
    starter_dir = skill_dir / "assets" / "personas"
    rebuild = skill_dir / "scripts" / "rebuild-index.py"
    config_path = personas_dir / "config.json"

    personas_dir.mkdir(parents=True, exist_ok=True)

    if not (personas_dir / "index.json").exists():
        if not starter_dir.exists():
            print(f"Bundled personas not found: {starter_dir}", file=sys.stderr)
            sys.exit(1)
        for child in starter_dir.iterdir():
            dest = personas_dir / child.name
            if child.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(child, dest)
            else:
                shutil.copy2(child, dest)
        subprocess.run([sys.executable, str(rebuild), str(personas_dir)], check=True, stdout=subprocess.DEVNULL)
        print(f"Bootstrapped starter personas into {personas_dir}", file=sys.stderr)

    if not config_path.exists():
        config_path.write_text(json.dumps({"context_files": []}, indent=2) + "\n", encoding="utf-8")
        print(f"Created shared context config at {config_path}", file=sys.stderr)

    print(str(personas_dir))


if __name__ == "__main__":
    main()
