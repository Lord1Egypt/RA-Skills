#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = SCRIPT_DIR / "validate_cron_spec.py"
RENDERER = SCRIPT_DIR / "render_cron_command.py"


def load_spec(path_arg: str | None):
    if path_arg and path_arg != "-":
        return json.loads(Path(path_arg).read_text())
    return json.load(sys.stdin)


def run_json(cmd: list[str], input_text: str | None = None):
    proc = subprocess.run(cmd, input=input_text, text=True, capture_output=True)
    return proc.returncode, proc.stdout, proc.stderr


def main():
    parser = argparse.ArgumentParser(description="Validate, render, and optionally create an OpenClaw cron job from JSON spec")
    parser.add_argument("spec", nargs="?", help="Path to JSON spec (or omit / use - for stdin)")
    parser.add_argument("--apply", action="store_true", help="Actually run the generated openclaw cron add command")
    parser.add_argument("--print-command-only", action="store_true", help="Print only the rendered command")
    args = parser.parse_args()

    try:
        spec = load_spec(args.spec)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"failed to load spec: {e}"}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    spec_text = json.dumps(spec, ensure_ascii=False)
    rc, out, err = run_json([sys.executable, str(VALIDATOR), "-"], input_text=spec_text)
    validation = {}
    if out.strip():
        try:
            validation = json.loads(out)
        except Exception:
            validation = {"ok": False, "issues": [out.strip()], "warnings": []}
    if rc != 0:
        print(json.dumps({"ok": False, "stage": "validate", "validation": validation, "stderr": err}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    rc, out, err = run_json([sys.executable, str(RENDERER), "-"], input_text=spec_text)
    rendered = {}
    if out.strip():
        try:
            rendered = json.loads(out)
        except Exception:
            rendered = {"ok": False, "error": out.strip()}
    if rc != 0 or not rendered.get("ok"):
        print(json.dumps({"ok": False, "stage": "render", "render": rendered, "stderr": err}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    command = rendered.get("command")
    if not isinstance(command, str) or not command.strip():
        print(json.dumps({"ok": False, "stage": "render", "error": "renderer returned no command", "render": rendered}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    if args.print_command_only:
        print(command)
        raise SystemExit(0)

    if not args.apply:
        print(json.dumps({"ok": True, "mode": "dry-run", "validation": validation, "render": rendered}, ensure_ascii=False, indent=2))
        raise SystemExit(0)

    proc = subprocess.run(command, shell=True, text=True, capture_output=True)
    result = {
        "ok": proc.returncode == 0,
        "mode": "apply",
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "validation": validation,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
