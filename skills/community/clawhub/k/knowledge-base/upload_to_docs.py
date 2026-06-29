#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯文档一键上传脚本
自动完成: pre_import → COS PUT → async_import → poll → add_to_sheet
"""

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def file_md5(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def mcporter(tool: str, args: dict) -> dict:
    r = subprocess.run(
        ["mcporter", "call", "tencent-docs", tool, "--args", json.dumps(args, ensure_ascii=False)],
        capture_output=True, text=True, timeout=60,
    )
    r.check_returncode()
    return json.loads(r.stdout)


def curl_put(url: str, path: str) -> None:
    r = subprocess.run(
        ["curl.exe", "-X", "PUT", "--upload-file", path,
         url, "-H", f"Content-Type: application/octet-stream",
         "--max-time", "300", "-sS"],
        capture_output=True, text=True, timeout=310,
    )
    if r.returncode != 0:
        raise RuntimeError(f"CURL upload failed: {r.stderr[:200]}")


def main():
    if len(sys.argv) < 2:
        print("用法: python upload_to_docs.py <文件路径> [选项]")
        print("选项:")
        print("  --name <标题>")
        print("  --format <mp4|pdf|pptx|docx|jpg|png|文章>")
        print("  --source-type <视频号|抖音|小红书|微信公众号|本地上传>")
        print("  --source-url <原始链接>")
        print("  --is-external <True|False>    默认 False")
        print("  --level <机密|高|一般|普通>    默认 一般")
        print("  --author <作者名>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)

    # 解析参数
    args = {}
    i = 2
    while i < len(sys.argv):
        key = sys.argv[i].lstrip("-")
        val = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
        args[key] = val
        i += 2

    name = args.get("name", file_path.stem)
    fmt = args.get("format", file_path.suffix.lstrip("."))
    source_type = args.get("source-type", "本地上传")
    source_url = args.get("source-url", "")
    is_external = args.get("is-external", "False") == "True"
    level = args.get("level", "一般")
    author = args.get("author", "")

    size = file_path.stat().st_size
    md5 = file_md5(str(file_path))

    print(f"📤 上传: {name} ({size // 1024}KB, {fmt})")

    # 1. pre_import
    print("  [1/5] 获取上传凭证...")
    pre = mcporter("manage.pre_import", {
        "file_name": f"{name}.{fmt}" if fmt != "文章" else f"{name}",
        "file_size": size,
        "file_md5": md5,
    })
    upload_url = pre["upload_url"]
    file_key = pre["file_key"]
    task_id = pre["task_id"]

    # 2. PUT to COS
    print("  [2/5] 上传到 COS...")
    curl_put(upload_url, str(file_path))
    print("         ✅ 完成")

    # 3. async_import
    print("  [3/5] 触发导入...")
    mcporter("manage.async_import", {
        "file_key": file_key,
        "task_id": task_id,
        "file_name": f"{name}.{fmt}" if fmt != "文章" else f"{name}",
        "file_md5": md5,
        "file_size": size,
    })

    # 4. Poll progress
    print("  [4/5] 等待导入完成...")
    for _ in range(30):
        time.sleep(2)
        prog = mcporter("manage.import_progress", {"task_id": task_id})
        if prog.get("progress") == 100:
            doc_url = prog.get("file_url", "")
            print(f"         ✅ {doc_url}")
            break
    else:
        print("         ⚠️ 超时，但文件可能已导入")

    # 5. Add index record
    print("  [5/5] 添加索引...")
    from add_to_sheet import main as add_main
    sys.argv = [
        "add_to_sheet.py",
        "--name", name,
        "--size", str(size // 1024),
        "--format", fmt,
        "--source-type", source_type,
        "--source-url", source_url,
        "--is-external", str(is_external),
        "--doc-url", doc_url,
        "--level", level,
    ]
    add_main()

    print("✅ 全部完成!")


if __name__ == "__main__":
    main()
