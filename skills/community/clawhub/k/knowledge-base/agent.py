#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库 Agent - 统一处理入口
调用方式:
  python agent.py identify <url>              # 识别链接类型
  python agent.py download-douyin <url>      # 下载抖音视频
  python agent.py parse-xhs <html-file>      # 解析小红书 HTML
  python agent.py parse-wechat <html-file> [url]  # 解析公众号文章
  python agent.py upload <file-path> <parent-id>  # 上传到腾讯文档
  python agent.py add-index <json-record>   # 追加索引记录
"""

import sys
import json
import argparse
import subprocess
import re
import os
import urllib.request
from pathlib import Path
from datetime import datetime

# ── 配置（通过环境变量设置，也可直接修改本文件）─────────────
# 每个用户需要配置自己的腾讯文档 ID 和视频号下载路径
# 设置方法：
#   Windows:  set KB_INDEX_FILE_ID=你的ID
#   macOS/Linux: export KB_INDEX_FILE_ID=你的ID
# 或直接修改下方等号右边的值

def _env_or(key: str, fallback: str = "") -> str:
    """读取环境变量，未设置时返回 fallback"""
    val = os.environ.get(key, "")
    if not val and not fallback:
        print(f"[知识库] ⚠️ 未配置 {key}，索引/上传功能可能不可用", file=sys.stderr)
    return val or fallback

TENCENT_SPACE_ID = _env_or("KB_TENCENT_SPACE_ID")        # 腾讯文档空间 ID
INDEX_FILE_ID    = _env_or("KB_INDEX_FILE_ID")           # 0号索引 智能表格 file_id
INDEX_SHEET_ID   = _env_or("KB_INDEX_SHEET_ID")          # 0号索引 sheet_id

# 视频号下载脚本路径 - 自动探测，也支持环境变量 KB_SPH_SKILL_PATH 覆盖
_SPH_ENV = os.environ.get("KB_SPH_SKILL_PATH", "")
if _SPH_ENV:
    SPH_SKILL_PATH = _SPH_ENV
else:
    _skill_base = Path(__file__).resolve().parent.parent.parent  # .workbuddy/skills/
    _candidates = [
        _skill_base / "sph-download" / "scripts" / "download.py",
        _skill_base / "sph-downloader" / "scripts" / "download.py",
    ]
    SPH_SKILL_PATH = ""
    for _c in _candidates:
        if _c.exists():
            SPH_SKILL_PATH = str(_c)
            break

TEMP_DIR = Path.home() / "Downloads" / "kb-temp"
# ─────────────────────────────────────────────────────────


def run(cmd: str, timeout: int = 300) -> str:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"命令失败: {cmd[:80]}\n{r.stderr[:300]}")
    return r.stdout.strip()


def identify_source(url: str) -> str:
    u = url.lower()
    if "weixin.qq.com/sph/" in u:
        return "视频号"
    if "douyin.com" in u or "iesdouyin.com" in u:
        return "抖音"
    if "xiaohongshu.com" in u or "xhslink.com" in u:
        return "小红书"
    if "mp.weixin.qq.com" in u:
        return "微信公众号"
    return "未知"


def download_douyin(url: str, output_dir: Path = None) -> dict:
    """调用 yt-dlp 下载抖音视频 + 提取文案描述"""
    output_dir = output_dir or TEMP_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    out_tmpl = str(output_dir / "%(id)s.%(ext)s")

    print(f"[抖音] 下载: {url[:60]}")

    # 提取文案描述
    description = ""
    try:
        dump = json.loads(run(f'yt-dlp --dump-json --no-playlist "{url}"', timeout=30))
        description = dump.get("description", "")
        if description:
            print(f"  [文案] 获取到描述 ({len(description)} 字)")
    except Exception:
        pass

    cmd = f'yt-dlp -f bestvideo+bestaudio/best --merge-output-format mp4 -o "{out_tmpl}" --no-playlist "{url}"'
    out = run(cmd, timeout=300)

    # 找下载的文件
    video_path = None
    for line in out.split("\n"):
        if "Destination:" in line or "已下载" in line or "Downloading" in line:
            f = line.split(": ", 1)[-1].strip()
            if Path(f).exists():
                video_path = Path(f)
    if not video_path:
        for f in output_dir.iterdir():
            if f.suffix in (".mp4", ".webm", ".mkv", ".flv"):
                video_path = f
                break
    if not video_path or not video_path.exists():
        raise FileNotFoundError("找不到下载后的视频文件")

    # 获取标题（yt-dlp --get-title）
    try:
        title = run(f'yt-dlp --get-title "{url}"', timeout=30).strip()
    except Exception:
        title = video_path.stem
    try:
        author = run(f'yt-dlp --get-uploader "{url}"', timeout=30).strip()
    except Exception:
        author = "unknown"

    # 保存文案为旁白文件
    if description:
        caption_path = video_path.with_suffix(".caption.txt")
        caption_path.write_text(description, encoding="utf-8")

    size = video_path.stat().st_size
    print(f"  [完成] {title[:40]} ({size // 1024}KB)")
    return {"title": title, "author": author, "path": str(video_path), "size": size, "description": description}


def parse_xhs_html(html: str) -> dict:
    """解析小红书笔记 HTML"""
    result = {"title": "", "author": "", "content": "", "images": []}
    m = re.search(r"window\.__INITIAL_STATE__\s*=\s*({.+?});", html)
    if m:
        try:
            data = json.loads(m.group(1))
            for note_map in data.get("noteDetailMap", {}).values():
                n = note_map.get("note", {})
                result["title"] = n.get("title", "")
                result["content"] = n.get("desc", "")
                result["author"] = n.get("user", {}).get("nickname", "")
                imgs = n.get("imageList", [])
                result["images"] = [i.get("urlDefault", "") for i in imgs if i.get("urlDefault")]
                break
        except Exception:
            pass
    if not result["title"]:
        t = re.search(r"<title>(.+?)</title>", html)
        if t:
            result["title"] = t.group(1).replace(" - 小红书", "").strip()
    return result


def parse_wechat_html(html: str, url: str = "") -> dict:
    """解析微信公众号文章 HTML"""
    result = {"title": "", "author": "", "content": "", "pub_time": "", "url": url}
    m = re.search(r"<h1[^>]*class=\"rich_media_title\"[^>]*>(.*?)</h1>", html, re.DOTALL)
    if not m:
        m = re.search(r"<title>(.+?)</title>", html)
    if m:
        result["title"] = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    m = re.search(r"var\s+nickname\s*=\s*\"([^\"]+)\"", html)
    if m:
        result["author"] = m.group(1)
    m = re.search(r"var\s+publish_time\s*=\s*\"([^\"]+)\"", html)
    if m:
        result["pub_time"] = m.group(1)
    m = re.search(r"<div\s+id=\"js_content\"[^>]*>(.*?)</div>\s*<script", html, re.DOTALL)
    if m:
        content = m.group(1)
        content = re.sub(r"<img[^>]+data-src=\"([^\"]+)\"[^>]*>", r"![](\1)\n\n", content)
        content = re.sub(r"<[^>]+>", "", content)
        content = content.replace("&nbsp;", " ").replace("&amp;", "&")
        result["content"] = re.sub(r"\n{3,}", "\n\n", content).strip()
    return result


def upload_to_tencent(file_path: Path, parent_id: str = "") -> dict:
    """上传文件到腾讯文档（调用 mcporter）"""
    size = file_path.stat().st_size
    md5 = run(f'certutil -hashfile "{file_path}" MD5 ^| find /v "MD5" ^| find /v "^$"').replace(" ", "")
    print(f"  [上传] {file_path.name} ({size // 1024}KB)...")
    # pre_import
    pre = json.loads(run(f'mcporter call tencent-docs manage.pre_import --args {{"file_name":"{file_path.name}","file_size":{size},"file_md5":"{md5}"}}'))
    upload_url = pre["upload_url"]
    file_key   = pre["file_key"]
    task_id    = pre["task_id"]
    # PUT 上传
    with open(file_path, "rb") as f:
        import urllib.request
        req = urllib.request.Request(upload_url, data=f.read(), method="PUT")
        urllib.request.urlopen(req)
    # async_import
    imp = json.loads(run(f'mcporter call tencent-docs manage.async_import --args {{"file_key":"{file_key}","file_md5":"{md5}","file_name":"{file_path.name}","file_size":{size},"task_id":"{task_id}"}}'))
    import time; time.sleep(5)
    return {"file_id": imp.get("file_id", ""), "file_url": imp.get("file_url", "")}


def add_index_record(record: dict):
    """向 0号索引追加一行"""
    if not INDEX_FILE_ID or not INDEX_SHEET_ID:
        print("  [跳过索引] 未配置 INDEX_FILE_ID / INDEX_SHEET_ID")
        return
    args = json.dumps({"file_id": INDEX_FILE_ID, "sheet_id": INDEX_SHEET_ID, "records": [{"fields": record}]})
    run(f'mcporter call tencent-docs smartsheet.add_records --args {args}')
    print(f"  [索引] 已追加: {record.get('文件名字', '')[:30]}")


def cmd_identify(args):
    src = identify_source(args.url)
    print(json.dumps({"url": args.url, "source_type": src}, ensure_ascii=False))


def cmd_download_douyin(args):
    r = download_douyin(args.url)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_parse_xhs(args):
    html = open(args.html_file, encoding="utf-8").read()
    r = parse_xhs_html(html)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_parse_wechat(args):
    html = open(args.html_file, encoding="utf-8").read()
    r = parse_wechat_html(html, args.url or "")
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_upload(args):
    f = Path(args.file_path)
    r = upload_to_tencent(f, args.parent_id or "")
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_add_index(args):
    record = json.loads(args.record_json)
    add_index_record(record)


def main():
    parser = argparse.ArgumentParser(description="知识库 Agent")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("identify", help="识别链接类型")
    p.add_argument("url")

    p = sub.add_parser("download-douyin", help="下载抖音视频")
    p.add_argument("url")

    p = sub.add_parser("parse-xhs", help="解析小红书 HTML")
    p.add_argument("html_file")

    p = sub.add_parser("parse-wechat", help="解析公众号文章 HTML")
    p.add_argument("html_file")
    p.add_argument("url", nargs="?", default="")

    p = sub.add_parser("upload", help="上传到腾讯文档")
    p.add_argument("file_path")
    p.add_argument("parent_id", nargs="?", default="")

    p = sub.add_parser("add-index", help="追加索引记录")
    p.add_argument("record_json")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
    else:
        {"identify": cmd_identify, "download-douyin": cmd_download_douyin,
         "parse-xhs": cmd_parse_xhs, "parse-wechat": cmd_parse_wechat,
         "upload": cmd_upload, "add-index": cmd_add_index}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
