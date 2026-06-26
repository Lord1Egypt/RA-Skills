#!/usr/bin/env python3
"""analyze_pdf.py — PDF 分析整合工具

整合三種分析模式：
1. extract  — 萃取 PDF 文字內容
2. search    — 搜尋 PDF 內文關鍵字
3. vision    — 將 PDF 頁面轉圖片，用 MiniMax VLM 分析

使用方式：
  python analyze_pdf.py extract input.pdf [--output out.txt]
  python analyze_pdf.py search input.pdf "關鍵字" [--ignore-case]
  python analyze_pdf.py vision input.pdf "分析要求" [--api-key KEY]
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

MINIMAX_TOOL_JS = Path(__file__).parent / "minimax_coding_plan_tool.js"


# ─────────────────────────────────────────
# 1. extract — 萃取文字
# ─────────────────────────────────────────
def cmd_extract(pdf_path: str, output: str | None, pages: str | None):
    script = Path(__file__).parent / "extract_pdf_text.py"
    cmd = [sys.executable, str(script), pdf_path]
    if output:
        cmd.extend(["--output", output])
    if pages:
        cmd.extend(["--pages", pages])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


# ─────────────────────────────────────────
# 2. search — 搜尋內文
# ─────────────────────────────────────────
def cmd_search(pdf_path: str, query: str, ignore_case: bool = False,
               regex: bool = False, context: int = 80):
    script = Path(__file__).parent / "search_pdf.py"
    cmd = [sys.executable, str(script), pdf_path, query]
    if ignore_case:
        cmd.append("--ignore-case")
    if regex:
        cmd.append("--regex")
    if context != 80:
        cmd.extend(["--context", str(context)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


# ─────────────────────────────────────────
# 3. vision — VLM 圖片分析
# ─────────────────────────────────────────
def cmd_vision(pdf_path: str, prompt: str, api_key: str,
               pages: str | None = None, dpi: int = 200):
    """
    將 PDF 轉成圖片，再用 MiniMax VLM 分析。
    """
    # 1. PDF → PNG
    tmp_dir = Path(tempfile.mkdtemp(prefix="pdf_vision_"))
    try:
        conv_script = Path(__file__).parent / "pdf_to_images.py"
        page_arg = ["--pages", pages] if pages else []
        conv_result = subprocess.run(
            [sys.executable, str(conv_script), str(pdf_path), str(tmp_dir),
             "--dpi", str(dpi)] + page_arg,
            capture_output=True, text=True
        )
        if conv_result.returncode != 0:
            return "", conv_result.stderr, 1

        # 找出所有圖片
        images = sorted(tmp_dir.glob("*.png"))
        if not images:
            return "", "No images generated from PDF", 1

        # 2. 逐頁 VLM 分析
        tool_js = Path(__file__).parent / "minimax_coding_plan_tool.js"
        if not tool_js.exists():
            return "", "minimax_coding_plan_tool.js not found", 1

        all_results = []
        for img in images:
            with open(img, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            # 呼叫 MiniMax VLM（直接 POST，不走 CLI 以便取得完整回應）
            import urllib.request
            data = json.dumps({
                "prompt": prompt,
                "image_url": f"data:image/png;base64,{img_b64}"
            }).encode()
            req = urllib.request.Request(
                "https://api.minimax.io/v1/coding_plan/vlm",
                data=data,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    result = json.loads(resp.read())
                    content = result.get("content", "")
                    if content:
                        all_results.append(f"=== {img.name} ===\n{content}")
                    else:
                        all_results.append(f"=== {img.name} ===\n[No content returned]")
            except Exception as e:
                all_results.append(f"=== {img.name} ===\n[Error: {e}]")

        return "\n\n".join(all_results), "", 0

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ─────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="PDF 分析工具")
    sub = parser.add_subparsers(dest="command", required=True)

    # extract
    e = sub.add_parser("extract", help="萃取 PDF 文字")
    e.add_argument("pdf", help="PDF 檔案路徑")
    e.add_argument("--output", "-o", help="輸出文字檔")
    e.add_argument("--pages", help="頁面範圍，如 1-3,5")

    # search
    s = sub.add_parser("search", help="搜尋 PDF 內文")
    s.add_argument("pdf", help="PDF 檔案路徑")
    s.add_argument("query", help="搜尋關鍵字")
    s.add_argument("--ignore-case", action="store_true")
    s.add_argument("--regex", action="store_true")
    s.add_argument("--context", type=int, default=80)

    # vision
    v = sub.add_parser("vision", help="用 MiniMax VLM 分析 PDF 圖片")
    v.add_argument("pdf", help="PDF 檔案路徑")
    v.add_argument("prompt", help="分析要求")
    v.add_argument("--api-key", default=os.environ.get("MINIMAX_API_KEY", ""))
    v.add_argument("--pages", help="頁面範圍，如 1-3")
    v.add_argument("--dpi", type=int, default=200)

    args = parser.parse_args()

    if args.command == "extract":
        out, err, rc = cmd_extract(args.pdf, args.output, args.pages)
        if err:
            print("STDERR:", err, file=sys.stderr)
        print(out)
        sys.exit(rc)

    elif args.command == "search":
        out, err, rc = cmd_search(args.pdf, args.query,
                                    args.ignore_case, args.regex, args.context)
        if err:
            print("STDERR:", err, file=sys.stderr)
        print(out)
        sys.exit(rc)

    elif args.command == "vision":
        if not args.api_key:
            print("Error: MINIMAX_API_KEY not set. Use --api-key or set MINIMAX_API_KEY env var.", file=sys.stderr)
            sys.exit(1)
        out, err, rc = cmd_vision(args.pdf, args.prompt, args.api_key,
                                    args.pages, args.dpi)
        if err:
            print("STDERR:", err, file=sys.stderr)
        print(out)
        sys.exit(rc)


if __name__ == "__main__":
    main()
