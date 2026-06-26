#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from idea_inbox_config import load_config


def _run(cmd: list[str], text: str) -> dict:
    import subprocess

    p = subprocess.run(cmd, input=text.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.decode("utf-8", errors="replace").strip()
    if p.returncode != 0:
        raise RuntimeError((out or p.stderr.decode("utf-8", errors="replace")).strip() or "classify failed")
    obj = json.loads(out)
    if isinstance(obj, dict) and obj.get("error"):
        raise RuntimeError(str(obj.get("error")))
    if not isinstance(obj, dict):
        raise RuntimeError("classify output not dict")
    return obj


def classify(text: str) -> dict:
    cfg = load_config()
    ai_enabled = bool((cfg.get("ai") or {}).get("enabled", True))
    fallback_mode = str((cfg.get("ai") or {}).get("fallback_mode", "rules"))

    here = Path(__file__).resolve().parent
    ai_script = str(here / "idea_inbox_ai.py")
    rules_script = str(here / "idea_inbox_rules.py")

    if ai_enabled:
        try:
            return _run(["python3", ai_script], text)
        except Exception:
            if fallback_mode != "rules":
                raise

    return _run(["python3", rules_script], text)


def main() -> None:
    text = sys.stdin.read().strip()
    if not text:
        print(json.dumps({"error": "empty input"}, ensure_ascii=False))
        sys.exit(2)
    try:
        out = classify(text)
        print(json.dumps(out, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
