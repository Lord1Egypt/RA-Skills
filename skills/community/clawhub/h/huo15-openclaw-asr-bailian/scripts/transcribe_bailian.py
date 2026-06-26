#!/usr/bin/env python3
"""
百炼 Paraformer 录音文件识别（异步转写）
用法:
  python transcribe_bailian.py --file-url "https://example.com/meeting.mp4" [-o out.txt]
  python transcribe_bailian.py --file-url "https://..." --model paraformer-v2 --diarization

百炼只接受 HTTP/HTTPS 公网 URL。OpenClaw 中由已有 enhance_share_file 生成
https://keepermac.huo15.com/plugins/enhance-share/... 再传入 --file-url。

依赖: pip install dashscope
环境变量: DASHSCOPE_API_KEY（必填）

文档: https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-python-sdk
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from http import HTTPStatus
from typing import Any


def _require_dashscope():
    try:
        import dashscope  # noqa: F401
        from dashscope.audio.asr import Transcription  # noqa: F401
    except ImportError:
        print("错误：未安装 dashscope。请执行: pip install dashscope", file=sys.stderr)
        sys.exit(1)
    return dashscope, Transcription


def _fetch_json(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_verbatim(result_json: dict[str, Any]) -> str:
    """从百炼 transcription_url 返回的 JSON 拼连续可读原文。"""
    lines: list[str] = []
    for tr in result_json.get("transcripts", []):
        sentences = tr.get("sentences")
        if sentences:
            for s in sentences:
                text = (s.get("text") or "").strip()
                if not text:
                    continue
                sid = s.get("speaker_id")
                if sid is not None:
                    lines.append(f"说话人 {sid}: {text}")
                else:
                    lines.append(text)
            continue
        text = (tr.get("text") or "").strip()
        if text:
            lines.append(text)
    return "\n".join(lines)


def collect_transcription_urls(wait_response: Any) -> list[str]:
    urls: list[str] = []
    output = getattr(wait_response, "output", None)
    if output is None:
        return urls
    results = getattr(output, "results", None)
    if results is None and isinstance(output, dict):
        results = output.get("results")
    if not results:
        return urls
    for item in results:
        if isinstance(item, dict):
            url = item.get("transcription_url")
        else:
            url = getattr(item, "transcription_url", None)
        if url:
            urls.append(url)
    return urls


def main() -> None:
    parser = argparse.ArgumentParser(description="百炼 Paraformer 录音文件识别")
    parser.add_argument(
        "--file-url",
        required=True,
        help="公网可访问的音频 URL（HTTP/HTTPS），百炼不支持本地直传",
    )
    parser.add_argument(
        "--model",
        default="paraformer-v2",
        help="模型名，默认 paraformer-v2；可选 fun-asr 等（见百炼文档）",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="将原文写入该文件；省略则打印到 stdout",
    )
    parser.add_argument(
        "--language-hints",
        nargs="*",
        default=["zh", "en"],
        help="语言提示，仅 paraformer-v2 等模型支持，默认 zh en",
    )
    parser.add_argument(
        "--diarization",
        action="store_true",
        help="开启说话人分离（diarization_enabled，仅单声道）",
    )
    parser.add_argument(
        "--speaker-count",
        type=int,
        default=None,
        help="说话人数量参考（可选）",
    )
    args = parser.parse_args()

    api_key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        print(
            "错误：未设置 DASHSCOPE_API_KEY。请在环境变量中配置百炼 API Key。",
            file=sys.stderr,
        )
        sys.exit(1)

    dashscope, Transcription = _require_dashscope()
    dashscope.api_key = api_key

    kwargs: dict[str, Any] = {}
    if args.model == "paraformer-v2" and args.language_hints:
        kwargs["language_hints"] = args.language_hints
    if args.diarization:
        kwargs["diarization_enabled"] = True
    if args.speaker_count is not None:
        kwargs["speaker_count"] = args.speaker_count

    print(f"[INFO] 提交百炼转写: model={args.model}", file=sys.stderr)
    task_response = Transcription.async_call(
        model=args.model,
        file_urls=[args.file_url],
        **kwargs,
    )
    if task_response.status_code != HTTPStatus.OK:
        print(f"错误：提交任务失败: {task_response}", file=sys.stderr)
        sys.exit(1)

    task_id = task_response.output.task_id
    print(f"[INFO] task_id={task_id}，等待完成…", file=sys.stderr)
    transcribe_response = Transcription.wait(task=task_id)
    if transcribe_response.status_code != HTTPStatus.OK:
        print(f"错误：转写失败: {transcribe_response}", file=sys.stderr)
        sys.exit(1)

    status = getattr(transcribe_response.output, "task_status", None)
    if status == "FAILED":
        print(f"错误：任务 FAILED: {transcribe_response.output}", file=sys.stderr)
        sys.exit(1)

    transcription_urls = collect_transcription_urls(transcribe_response)
    if not transcription_urls:
        print(
            "错误：响应中无 transcription_url，请检查 API 返回或升级 dashscope SDK。",
            file=sys.stderr,
        )
        sys.exit(1)

    parts: list[str] = []
    for i, url in enumerate(transcription_urls):
        print(f"[INFO] 下载识别结果 {i + 1}/{len(transcription_urls)}", file=sys.stderr)
        result_json = _fetch_json(url)
        parts.append(extract_verbatim(result_json))

    verbatim = "\n\n".join(p for p in parts if p.strip())
    if not verbatim.strip():
        print("错误：识别结果为空", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(verbatim)
        print(f"[INFO] 已写入 {args.output}", file=sys.stderr)
    else:
        print(verbatim)


if __name__ == "__main__":
    main()
