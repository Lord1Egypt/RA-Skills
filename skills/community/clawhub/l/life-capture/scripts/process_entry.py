#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--text")
    parser.add_argument("--input")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--today")
    parser.add_argument("--config")
    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read().strip()
    elif args.input:
        text = Path(args.input).read_text(encoding="utf-8").strip()
    elif args.text:
        text = args.text.strip()
    else:
        raise SystemExit("provide --text, --input, or --stdin")

    script_dir = Path(__file__).resolve().parent
    parse_cmd = [sys.executable, str(script_dir / "parse_entries.py"), "--text", text, "--db", args.db]
    if args.today:
        parse_cmd.extend(["--today", args.today])
    if args.config:
        parse_cmd.extend(["--config", args.config])
    parsed = subprocess.run(parse_cmd, check=True, capture_output=True, text=True)
    payload = parsed.stdout

    db_path = Path(args.db)
    if not db_path.exists():
        init_cmd = [sys.executable, str(script_dir / "init_db.py"), "--db", args.db]
        subprocess.run(init_cmd, check=True)

    save_cmd = [sys.executable, str(script_dir / "save_entry.py"), "--root", args.root, "--db", args.db, "--stdin-json"]
    saved = subprocess.run(save_cmd, input=payload, check=True, capture_output=True, text=True)
    parsed_obj = json.loads(payload)
    saved_obj = json.loads(saved.stdout)
    print(json.dumps({"parsed": parsed_obj["records"], "saved": saved_obj["saved"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
