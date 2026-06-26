#!/usr/bin/env python3
"""MinerU Agent 轻量解析 API - 文档转 Markdown

用法:
  URL 模式:  python3 mineru_parse.py --url "https://example.com/file.pdf"
  文件模式:  python3 mineru_parse.py --file /path/to/document.pdf

可选参数:
  --language ch|en        解析语言，默认 ch
  --page_range 1-10       页码范围，仅 PDF 有效
  --output /path/to/out.md  指定输出文件路径
  --timeout 300           轮询超时秒数，默认 300
"""

import argparse
import json
import os
import sys
import time

import requests

BASE_URL = "https://mineru.net/api/v1/agent"

STATE_LABELS = {
    "uploading": "文件下载中",
    "pending": "排队中",
    "running": "解析中",
    "waiting-file": "等待文件上传",
}


def poll_result(task_id, timeout=300, interval=3):
    """轮询查询解析结果，返回 Markdown 文本或 None。"""
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(f"{BASE_URL}/parse/{task_id}")
        result = resp.json()
        data = result.get("data", {})
        state = data.get("state", "unknown")
        elapsed = int(time.time() - start)

        if state == "done":
            md_url = data["markdown_url"]
            print(f"[{elapsed}s] 解析完成", file=sys.stderr)
            md_resp = requests.get(md_url)
            md_resp.encoding = "utf-8"
            return md_resp.text

        if state == "failed":
            err_msg = data.get("err_msg", "未知错误")
            err_code = data.get("err_code", "")
            print(f"[{elapsed}s] 解析失败 [{err_code}]: {err_msg}", file=sys.stderr)
            return None

        label = STATE_LABELS.get(state, state)
        print(f"[{elapsed}s] {label}...", file=sys.stderr)
        time.sleep(interval)

    print(f"轮询超时 ({timeout}s)，task_id: {task_id}", file=sys.stderr)
    return None


def parse_by_url(url, language="ch", page_range=None, timeout=300):
    """通过 URL 提交文档解析任务并等待结果。"""
    data = {"url": url, "language": language}
    if page_range:
        data["page_range"] = page_range

    resp = requests.post(f"{BASE_URL}/parse/url", json=data)
    result = resp.json()
    if result.get("code") != 0:
        print(f"提交失败: {result.get('msg')}", file=sys.stderr)
        return None

    task_id = result["data"]["task_id"]
    print(f"任务已提交, task_id: {task_id}", file=sys.stderr)
    return poll_result(task_id, timeout=timeout)


def parse_by_file(file_path, language="ch", page_range=None, timeout=300):
    """通过文件上传提交文档解析任务并等待结果。"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}", file=sys.stderr)
        return None

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    if file_size > 10 * 1024 * 1024:
        print(f"文件大小 {file_size/1024/1024:.1f}MB 超出 10MB 限制", file=sys.stderr)
        return None

    # 1. 获取签名上传 URL
    data = {"file_name": file_name, "language": language}
    if page_range:
        data["page_range"] = page_range

    resp = requests.post(f"{BASE_URL}/parse/file", json=data)
    result = resp.json()
    if result.get("code") != 0:
        print(f"获取上传链接失败: {result.get('msg')}", file=sys.stderr)
        return None

    task_id = result["data"]["task_id"]
    file_url = result["data"]["file_url"]
    print(f"任务已创建, task_id: {task_id}", file=sys.stderr)

    # 2. PUT 上传文件到 OSS
    with open(file_path, "rb") as f:
        put_resp = requests.put(file_url, data=f)
        if put_resp.status_code not in (200, 201):
            print(f"文件上传失败, HTTP {put_resp.status_code}", file=sys.stderr)
            return None
    print("文件上传成功，等待解析...", file=sys.stderr)

    # 3. 轮询等待结果
    return poll_result(task_id, timeout=timeout)


def main():
    parser = argparse.ArgumentParser(description="MinerU 文档解析")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="远程文件 URL")
    group.add_argument("--file", help="本地文件路径")
    parser.add_argument("--language", default="ch", help="解析语言 (默认 ch)")
    parser.add_argument("--page_range", help="页码范围，如 1-10（仅 PDF）")
    parser.add_argument("--output", "-o", help="输出文件路径（默认 stdout）")
    parser.add_argument("--timeout", type=int, default=300, help="轮询超时秒数（默认 300）")
    args = parser.parse_args()

    if args.url:
        content = parse_by_url(args.url, language=args.language, page_range=args.page_range, timeout=args.timeout)
    else:
        content = parse_by_file(args.file, language=args.language, page_range=args.page_range, timeout=args.timeout)

    if content is None:
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"结果已保存到: {args.output}", file=sys.stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
