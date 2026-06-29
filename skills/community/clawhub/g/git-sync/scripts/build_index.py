#!/usr/bin/env python3
"""
build_index.py - 为 dist/ 目录生成 HTML 索引页（含 file:// 超链接）

用法: python build_index.py <dist_dir>
示例: python build_index.py ~/.workbuddy/skills/.dist/
"""

import html
import os
import sys
from datetime import datetime

def build_index(dist_dir):
    if not os.path.isdir(dist_dir):
        print(f"❌ 目录不存在: {dist_dir}")
        sys.exit(1)

    # 收集 ZIP 文件
    zip_files = []
    for f in sorted(os.listdir(dist_dir)):
        if f.endswith(".zip") and os.path.isfile(os.path.join(dist_dir, f)):
            fpath = os.path.join(dist_dir, f)
            size = os.path.getsize(fpath)
            mtime = os.path.getmtime(fpath)
            zip_files.append((f, fpath, size, mtime))

    # 生成 file:// 链接
    def file_url(path):
        real = os.path.abspath(path)
        if os.sep == "\\":
            real = real.replace("\\", "/")
            if ":" in real:
                # C:/... -> /C:/...
                real = "/" + real
        return "file://" + html.escape(real, quote=True)

    def fmt_size(bytes_):
        if bytes_ < 1024:
            return f"{bytes_} B"
        elif bytes_ < 1024 * 1024:
            return f"{bytes_ / 1024:.1f} KB"
        else:
            return f"{bytes_ / (1024 * 1024):.1f} MB"

    rows = ""
    for f, fpath, size, mtime in zip_files:
        url = file_url(fpath)
        size_str = fmt_size(size)
        time_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        rows += (
            f"  <tr>\n"
            f"    <td><a href=\"{url}\">{html.escape(f)}</a></td>\n"
            f"    <td>{size_str}</td>\n"
            f"    <td>{time_str}</td>\n"
            f"  </tr>\n"
        )

    if not rows:
        rows = "  <tr><td colspan=\"3\" style=\"text-align:center;color:#999\">暂无 ZIP 包，请先运行 git-sync</td></tr>\n"

    dist_real = os.path.abspath(dist_dir)
    page = (
        "<!DOCTYPE html>\n"
        "<html lang=\"zh-CN\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "  <title>WorkBuddy Skills — ZIP 索引</title>\n"
        "  <style>\n"
        "    * { margin:0; padding:0; box-sizing:border-box; }\n"
        "    body {\n"
        "      font-family: -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", sans-serif;\n"
        "      background: #f5f7fa;\n"
        "      color: #333;\n"
        "      padding: 2rem;\n"
        "    }\n"
        "    h1 { font-size:1.4rem; margin-bottom:0.3rem; color:#1a1a1a; }\n"
        "    .subtitle { font-size:0.85rem; color:#888; margin-bottom:1.5rem; }\n"
        "    .subtitle code { background:#e8ecf1; padding:0.1rem 0.4rem; border-radius:3px; font-size:0.82rem; }\n"
        "    table { width:100%; border-collapse:collapse; background:#fff; border-radius:8px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,0.08); }\n"
        "    thead { background:#4a6cf7; color:#fff; }\n"
        "    th, td { padding:0.75rem 1rem; text-align:left; }\n"
        "    tbody tr:hover { background:#f0f4ff; }\n"
        "    a { color:#4a6cf7; text-decoration:none; }\n"
        "    a:hover { text-decoration:underline; }\n"
        "    .footer { margin-top:1.5rem; font-size:0.78rem; color:#aaa; }\n"
        "  </style>\n"
        "</head>\n"
        "<body>\n"
        "  <h1>📦 WorkBuddy Skills — ZIP 索引</h1>\n"
        f"  <p class=\"subtitle\">统一输出目录：<code>{html.escape(dist_real)}</code><br>点击文件名即可跳转 / 下载（需浏览器允许 file:// 协议）</p>\n"
        "  <table>\n"
        "    <thead><tr><th>文件名</th><th>大小</th><th>修改时间</th></tr></thead>\n"
        "    <tbody>\n"
        f"{rows}"
        "    </tbody>\n"
        "  </table>\n"
        f"  <p class=\"footer\">由 git-sync v1.5.0 自动生成 · 最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n"
        "</body>\n"
        "</html>\n"
    )

    index_path = os.path.join(dist_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(page)

    print(f"  ✅ HTML 索引已生成: {index_path}")
    return index_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python build_index.py <dist_dir>")
        sys.exit(1)
    build_index(sys.argv[1])
