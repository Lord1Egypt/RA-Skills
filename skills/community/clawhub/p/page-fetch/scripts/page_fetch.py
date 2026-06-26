#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

SKILL_DIR = Path(__file__).resolve().parent
FETCH_WECHAT = SKILL_DIR / "fetch_wechat_article.py"
FETCH_PAGE = SKILL_DIR / "fetch_page.py"
RENDER_PAGE = SKILL_DIR / "render_page.py"
DEFAULT_SAVE_DIR = Path("/home/admin/projects/openclaw/reports/page-fetch")


def is_wechat_url(url: str) -> bool:
    return urlparse(url).netloc.endswith("mp.weixin.qq.com")


def run_json(script: Path, url: str, timeout: int, max_chars: int, wait_ms: int | None = None, cookie: str | None = None) -> tuple[int, dict]:
    cmd = [sys.executable, str(script), url, "--format", "json", "--max-chars", str(max_chars)]
    if timeout:
        cmd.extend(["--timeout", str(timeout)])
    if wait_ms is not None:
        cmd.extend(["--wait-ms", str(wait_ms)])
    if cookie:
        cmd.extend(["--cookie", cookie])

    run = subprocess.run(cmd, capture_output=True, text=True)
    stdout = (run.stdout or "").strip()
    stderr = (run.stderr or "").strip()
    if not stdout:
        payload = {
            "url": url,
            "method": f"runner:{script.stem}:no-output",
            "error": stderr or f"{script.name} produced no output",
        }
        return run.returncode or 1, payload
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        payload = {
            "url": url,
            "method": f"runner:{script.stem}:invalid-json",
            "error": stderr or "script output was not valid JSON",
            "raw_output": stdout[:2000],
        }
        return run.returncode or 1, payload
    if stderr:
        notes = data.get("notes")
        if isinstance(notes, list):
            notes.append(f"stderr: {stderr}")
        else:
            data["notes"] = [f"stderr: {stderr}"]
    return run.returncode, data


def is_good_enough(payload: dict) -> bool:
    text = str(payload.get("text") or "").strip()
    method = str(payload.get("method") or "")
    if payload.get("access_limited"):
        return False
    if method in {"metadata-only", "requests-failed", "browser-render:failed", "browser-render:unavailable"}:
        return False
    return len(text) >= 400


def save_json(payload: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified webpage fetch runner with no-persist default.")
    parser.add_argument("url")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--wait-ms", type=int, default=2500)
    parser.add_argument("--max-chars", type=int, default=12000)
    parser.add_argument("--cookie", default=None, help="Optional cookie for WeChat article fetches")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--save-json", action="store_true", help="Persist final JSON explicitly; default is no disk writes")
    parser.add_argument("--output", default=None, help="Explicit JSON output path; requires --save-json to persist")
    args = parser.parse_args()

    steps: list[str] = []
    payload: dict
    code: int

    if is_wechat_url(args.url):
        steps.append("wechat-first")
        code, payload = run_json(FETCH_WECHAT, args.url, timeout=max(args.timeout, 30), max_chars=args.max_chars, cookie=args.cookie)
        if not is_good_enough(payload):
            steps.append("wechat-fallback-general")
            code, payload = run_json(FETCH_PAGE, args.url, timeout=args.timeout, max_chars=args.max_chars)
            if not is_good_enough(payload):
                steps.append("wechat-fallback-browser")
                code, payload = run_json(RENDER_PAGE, args.url, timeout=0, max_chars=args.max_chars, wait_ms=args.wait_ms)
    else:
        steps.append("general-first")
        code, payload = run_json(FETCH_PAGE, args.url, timeout=args.timeout, max_chars=args.max_chars)
        if not is_good_enough(payload):
            steps.append("general-fallback-browser")
            code, payload = run_json(RENDER_PAGE, args.url, timeout=0, max_chars=args.max_chars, wait_ms=args.wait_ms)

    notes = payload.get("notes")
    if isinstance(notes, list):
        notes.append(f"runner_steps: {' -> '.join(steps)}")
    else:
        payload["notes"] = [f"runner_steps: {' -> '.join(steps)}"]

    if args.save_json:
        output_path = Path(args.output).expanduser() if args.output else DEFAULT_SAVE_DIR / "latest.json"
        saved_to = save_json(payload, output_path)
        payload["saved_to"] = str(saved_to)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Title: {payload.get('title') or ''}")
        if payload.get("author"):
            print(f"Author: {payload['author']}")
        if payload.get("account_nickname"):
            print(f"Account: {payload['account_nickname']}")
        if payload.get("published_time"):
            print(f"Published: {payload['published_time']}")
        print(f"Method: {payload.get('method') or ''}")
        if payload.get("access_limited"):
            print(f"Access: {payload.get('access_limit_reason')}")
        print()
        print(payload.get("text") or payload.get("description") or "")
        if payload.get("notes"):
            print()
            print("Notes:")
            for note in payload["notes"]:
                print(f"- {note}")

    return 0 if code == 0 or payload.get("text") else (code or 1)


if __name__ == "__main__":
    sys.exit(main())
