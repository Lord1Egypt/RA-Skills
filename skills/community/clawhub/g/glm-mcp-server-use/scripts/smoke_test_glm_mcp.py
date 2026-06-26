#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from setup_glm_mcp_servers import main as setup_main  # type: ignore

WECHAT_TEST_URL = (
    "https://mp.weixin.qq.com/s?__biz=MjM5ODI5Njc2MA==&mid=2655938038&idx=1&"
    "sn=9405063ad00c8842c3a9f866e3ca177a&poc_token=HJ--2GmjXT7Nt1KHi0rSP4MyZk2cjj8GjJwpl79b"
)


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, text=True, capture_output=True)
    out = (r.stdout or "") + ("\n" + r.stderr if r.stderr else "")
    return r.returncode, out.strip()


def ok_text(output: str) -> bool:
    return "isError: true" not in output and "MCP error" not in output and "Unexpected error" not in output


def ensure_config(config_path: str) -> None:
    p = Path(config_path)
    if p.exists():
        return
    # call setup script entrypoint through subprocess to avoid argparse conflicts
    rc, out = run([
        "python3",
        str(Path(__file__).with_name("setup_glm_mcp_servers.py")),
        "--config",
        config_path,
    ])
    if rc != 0:
        raise RuntimeError(out or "Failed to setup config")


def test_vision(config_path: str) -> dict:
    result = {"list_ok": False, "analyze_ok": False, "note": ""}

    rc, out = run(["mcporter", "--config", config_path, "list", "zai-vision", "--schema", "--json"])
    result["list_ok"] = rc == 0 and '"name": "zai-vision"' in out
    if not result["list_ok"]:
        result["note"] = out[:300]
        return result

    try:
        from PIL import Image, ImageDraw  # type: ignore

        image_path = Path("/tmp/glm_mcp_vision_test.png")
        img = Image.new("RGB", (220, 120), "white")
        d = ImageDraw.Draw(img)
        d.rectangle((20, 20, 200, 100), outline="blue", width=3)
        d.text((35, 50), "Hello GLM", fill="black")
        img.save(image_path)

        rc, out = run([
            "mcporter",
            "--config",
            config_path,
            "call",
            "zai-vision.analyze_image",
            f"image_source={image_path}",
            "prompt=What text do you see and what shape appears?",
            "--output",
            "raw",
            "--timeout",
            "120000",
        ])
        result["analyze_ok"] = rc == 0 and ok_text(out)
        result["note"] = out[:300]
    except Exception as e:
        result["note"] = f"vision analyze skipped or failed: {e}"

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test 4 official GLM MCP servers")
    parser.add_argument("--config", default="./tmp/mcporter-glm.json")
    parser.add_argument("--reader-url", default=WECHAT_TEST_URL)
    parser.add_argument("--out", default="./tmp/glm-mcp-smoke-report.json")
    args = parser.parse_args()

    config_path = str(Path(args.config).expanduser().resolve())
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    ensure_config(config_path)

    report: dict = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config_path": config_path,
        "reader_url": args.reader_url,
        "tests": {},
    }

    # Search
    rc, out = run(["mcporter", "--config", config_path, "list", "web-search-prime", "--schema", "--json"])
    list_ok = rc == 0 and 'web_search_prime' in out
    rc2, out2 = run([
        "mcporter",
        "--config",
        config_path,
        "call",
        "web-search-prime.web_search_prime",
        "search_query=GLM-5.1 release notes",
        "--output",
        "raw",
        "--timeout",
        "120000",
    ])
    report["tests"]["search"] = {
        "list_ok": list_ok,
        "call_ok": rc2 == 0 and ok_text(out2),
        "sample": out2[:300],
    }

    # Reader (special target URL)
    rc, out = run(["mcporter", "--config", config_path, "list", "web-reader", "--schema", "--json"])
    list_ok = rc == 0 and 'webReader' in out
    rc2, out2 = run([
        "mcporter",
        "--config",
        config_path,
        "call",
        "web-reader.webReader",
        f"url={args.reader_url}",
        "no_cache=true",
        "return_format=text",
        "retain_images=false",
        "--output",
        "raw",
        "--timeout",
        "120000",
    ])
    reader_ok = rc2 == 0 and ok_text(out2)
    anti_bot = bool(re.search(r"verify|res\\.wx\\.qq\\.com|轻点两下取消赞|poc_token", out2, re.I))
    report["tests"]["reader"] = {
        "list_ok": list_ok,
        "call_ok": reader_ok,
        "anti_bot_likely": anti_bot,
        "sample": out2[:500],
    }

    # Zread
    rc, out = run(["mcporter", "--config", config_path, "list", "zread", "--schema", "--json"])
    list_ok = rc == 0 and 'get_repo_structure' in out
    rc2, out2 = run([
        "mcporter",
        "--config",
        config_path,
        "call",
        "zread.get_repo_structure",
        "repo_name=microsoft/vscode",
        "--output",
        "raw",
        "--timeout",
        "120000",
    ])
    report["tests"]["zread"] = {
        "list_ok": list_ok,
        "call_ok": rc2 == 0 and ok_text(out2),
        "sample": out2[:300],
    }

    # Vision
    report["tests"]["vision"] = test_vision(config_path)

    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(out_path)
    print(json.dumps(report["tests"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
