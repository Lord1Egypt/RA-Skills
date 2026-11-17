#!/usr/bin/env python3
"""
run_mannequin.py — 人台换模特全链路编排器

在进程内顺序完成：构参 → textgen 改写 → imagegen 出图。
替代脆弱的 bash 链式调用，规避 command 截断、heredoc 失败、长 prompt shell 变量等问题。

用法（推荐 --params-file，避免长命令行）：
  python <本skill根目录>/scripts/run_mannequin.py --params-file mannequin_job.json

params-file 示例：
  {
    "imageUrls": ["https://example.com/mannequin.jpg"],
    "customerKeywords": "",
    "provider": "BANANA_PRO",
    "ratio": "1:1",
    "resolution": "2K",
    "textgen_script": "/abs/.../linkfox-aigc-textgen/scripts/aigc_textgen.py",
    "imagegen_script": "/abs/.../linkfox-aigc-imagegen/scripts/aigc_imagegen.py"
  }

也可逐项传参：
  python <本skill根目录>/scripts/run_mannequin.py \\
    --image-urls '["https://..."]' \\
    --provider BANANA_PRO --ratio 1:1 --resolution 2K \\
    --textgen-script /abs/.../aigc_textgen.py \\
    --imagegen-script /abs/.../aigc_imagegen.py

前置条件：imageUrls 须全部为公开 https 地址（本地路径须先经 linkfox-file-upload 上传）。
输出：透传 imagegen 脚本的 stdout（含 Saved full response:），供 agent 原封不动展示。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import build_textgen_params as bt  # noqa: E402

SAVED_RE = re.compile(r"Saved full response:\s*(.+)\s*$", re.M)
TEXTGEN_TIMEOUT = 360
IMAGEGEN_TIMEOUT = 720
RETRY_BACKOFF_SEC = 2.0
TRANSIENT_RE = re.compile(
    r"(Connection failed|Connection reset|timed?\s?out|timeout|Temporary failure|"
    r"HTTP 5\d\d|URLError|Polling timeout|Max retries|Read timed out)",
    re.I,
)


def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def _is_transient(msg: str) -> bool:
    return bool(TRANSIENT_RE.search(msg or ""))


def _with_retry(label: str, fn):
    try:
        return fn()
    except RuntimeError as e:
        if _is_transient(str(e)):
            _log(f"[{label}] 瞬时错误，{RETRY_BACKOFF_SEC:.0f}s 后自动重试 1 次：{e}")
            time.sleep(RETRY_BACKOFF_SEC)
            return fn()
        raise


def _validate_image_urls(image_urls: list) -> None:
    if not isinstance(image_urls, list) or not image_urls:
        raise RuntimeError("imageUrls 为空——需先完成图片上传与 URL 校验（步骤1）")
    for u in image_urls:
        if not isinstance(u, str) or not u.startswith(("http://", "https://")):
            raise RuntimeError(
                f"imageUrls 含非 http(s) 地址: {u!r}——需先经 linkfox-file-upload 上传"
            )


def _run_textgen(textgen_script: str, params: dict) -> str:
    proc = subprocess.run(
        [sys.executable, textgen_script, "--stdin", "--content-only"],
        input=json.dumps(params, ensure_ascii=False),
        text=True,
        capture_output=True,
        timeout=TEXTGEN_TIMEOUT,
    )
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip().splitlines()[-3:]
        raise RuntimeError(f"textgen 失败(exit={proc.returncode}): {' | '.join(tail)}")
    content = proc.stdout.rstrip("\n")
    if not content:
        raise RuntimeError("textgen 返回空 content——提词模型未能生成有效 prompt")
    return content


def _run_imagegen(imagegen_script: str, params: dict) -> list[str]:
    proc = subprocess.run(
        [sys.executable, imagegen_script, json.dumps(params, ensure_ascii=False)],
        text=True,
        capture_output=True,
        timeout=IMAGEGEN_TIMEOUT,
    )
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    if stdout.strip():
        print(stdout, end="" if stdout.endswith("\n") else "\n")
    if stderr.strip():
        print(stderr, file=sys.stderr, end="" if stderr.endswith("\n") else "\n")

    m = SAVED_RE.search(stdout)
    if not m:
        tail = (stderr or stdout).strip().splitlines()[-3:]
        raise RuntimeError(f"imagegen 无 'Saved full response' 输出: {' | '.join(tail)}")

    payload = m.group(1).strip()
    if payload.startswith("["):
        try:
            images = json.loads(payload)
        except json.JSONDecodeError:
            raise RuntimeError(f"imagegen 图片路径数组解析失败: {payload[:120]}")
        if not images:
            raise RuntimeError("imagegen 返回空图片数组")
        return images
    raise RuntimeError(f"imagegen 业务失败，错误详情见: {payload}")


def _load_job(args: argparse.Namespace) -> dict:
    if args.params_file:
        path = os.path.abspath(args.params_file)
        if not os.path.isfile(path):
            raise SystemExit(f"ERROR: params-file 不存在: {path}")
        with open(path, encoding="utf-8") as f:
            job = json.load(f)
    else:
        if not args.image_urls:
            raise SystemExit("ERROR: 须指定 --params-file 或 --image-urls")
        try:
            image_urls = json.loads(args.image_urls)
        except json.JSONDecodeError as e:
            raise SystemExit(f"ERROR: --image-urls 解析失败: {e}") from e
        job = {
            "imageUrls": image_urls,
            "customerKeywords": args.customer_keywords or "",
            "provider": args.provider,
            "ratio": args.ratio,
            "resolution": args.resolution,
            "textgen_script": args.textgen_script,
            "imagegen_script": args.imagegen_script,
        }

    for key in ("imageUrls", "provider", "ratio", "resolution", "textgen_script", "imagegen_script"):
        if not job.get(key):
            raise SystemExit(f"ERROR: 任务参数缺少必填字段: {key}")

    for script_key in ("textgen_script", "imagegen_script"):
        script_path = os.path.abspath(job[script_key])
        if not os.path.isfile(script_path):
            raise SystemExit(f"ERROR: {script_key} 路径不存在: {script_path}")
        job[script_key] = script_path

    job.setdefault("customerKeywords", "")
    return job


def main() -> int:
    parser = argparse.ArgumentParser(
        description="人台换模特全链路编排器（构参 → textgen → imagegen）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--params-file", help="任务参数 JSON 文件（推荐）")
    parser.add_argument("--image-urls", help="JSON 数组格式的图片 URL 列表")
    parser.add_argument("--customer-keywords", default="", help="用户补充提示词")
    parser.add_argument("--provider", default="BANANA_PRO", help="生图模型")
    parser.add_argument("--ratio", default="1:1", help="图片比例 aspectRatio")
    parser.add_argument("--resolution", default="2K", help="分辨率 2K / 4K")
    parser.add_argument("--textgen-script", help="aigc_textgen.py 绝对路径")
    parser.add_argument("--imagegen-script", help="aigc_imagegen.py 绝对路径")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只构建 textgen 参数，不调用 textgen/imagegen API",
    )
    args = parser.parse_args()

    job = _load_job(args)
    image_urls = job["imageUrls"]
    _validate_image_urls(image_urls)

    tg_params = bt.build_params(
        image_urls,
        customer_keywords=job.get("customerKeywords") or "",
    )

    if args.dry_run:
        print(json.dumps(tg_params, ensure_ascii=False, indent=2))
        _log("dry-run：已构建 textgen 参数，未调用 API")
        return 0

    _log("textgen 改写中…")
    final_prompt = _with_retry(
        "textgen",
        lambda: _run_textgen(job["textgen_script"], tg_params),
    )

    ig_params = {
        "prompt": final_prompt,
        "imageUrls": image_urls,
        "provider": job["provider"],
        "outputNum": 1,
        "aspectRatio": job["ratio"],
        "resolution": job["resolution"],
        "quality": "high",
    }

    _log("imagegen 出图中…")
    _with_retry(
        "imagegen",
        lambda: _run_imagegen(job["imagegen_script"], ig_params),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
