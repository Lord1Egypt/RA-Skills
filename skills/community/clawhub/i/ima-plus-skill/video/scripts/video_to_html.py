#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
video_to_html.py — 把本地视频封装为「单文件 HTML」（用于上传知识库）

背景：知识库不接受 mp4/avi/mov 等视频文件本身（服务端限制）。
唯一可行的入库方式是把视频 base64 内嵌进单文件 HTML（≤10MB），
页面用 Blob URL 播放（比 data: URI 兼容性好，移动端 WebView 也能播）。

用法：
  python3 video_to_html.py --mp4 a.mp4 --title "标题" --out a.html
  python3 video_to_html.py --mp4 a.mp4 --title "标题" --out-dir ./html

输出：最后一行 JSON：{"ok":true,"out":"...","size_mb":1.18,...}
      HTML 超过 10MB 时 ok=false 并给出 warn（调用方应跳过上传）。

注意：知识库条目名 = 文件名，不得含 `# ? & /` 等 URL 危险字符
（`#` 会被当作锚点，导致打开条目时显示「无法打开网页」）。
safe_filename() 已做清洗，勿绕过。
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.normpath(os.path.join(HERE, '..', 'assets', 'video-template.html'))
HTML_LIMIT = 10 * 1024 * 1024  # 知识库单文件 HTML 上限


def probe_duration(path):
    """返回 'x分yy秒'；ffprobe 不可用时返回「未知」。"""
    try:
        p = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=nw=1:nk=1', path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        d = float(p.stdout.decode('utf-8', 'ignore').strip())
        return '%d分%02d秒' % (d // 60, d % 60)
    except Exception:
        return '未知'


def safe_filename(title, limit=44):
    """只保留 中文/英文/数字/空格/下划线/连字符 —— 去掉一切 URL 危险字符。"""
    s = re.sub(r'[^\u4e00-\u9fff\u3040-\u30ffA-Za-z0-9 _-]', '', title or '')
    s = re.sub(r'\s+', ' ', s).strip()
    if len(s) > limit:
        s = s[:limit].rstrip()
    return s or 'video'


def build_html(mp4, title, template):
    with open(mp4, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    size = os.path.getsize(mp4)
    tpl = open(template, encoding='utf-8').read()
    return (tpl.replace('__TITLE__', title)
               .replace('__FILENAME__', safe_filename(title))
               .replace('__B64__', b64)
               .replace('__DUR__', probe_duration(mp4))
               .replace('__SIZE__', '%.2f MB' % (size / 1048576.0)))


def main():
    ap = argparse.ArgumentParser(description='视频 → 内嵌单文件 HTML')
    ap.add_argument('--mp4', required=True, help='本地视频路径')
    ap.add_argument('--title', help='页面标题；默认取文件名')
    ap.add_argument('--out', help='输出 HTML 路径（与 --out-dir 二选一）')
    ap.add_argument('--out-dir', help='输出目录，文件名由标题自动清洗生成')
    ap.add_argument('--template', default=DEFAULT_TEMPLATE, help='HTML 模板路径')
    a = ap.parse_args()

    if not os.path.isfile(a.mp4):
        print(json.dumps({'ok': False, 'error': 'mp4 not found: %s' % a.mp4}, ensure_ascii=False))
        return 1
    if not os.path.isfile(a.template):
        print(json.dumps({'ok': False, 'error': 'template not found: %s' % a.template}, ensure_ascii=False))
        return 1

    title = a.title or os.path.splitext(os.path.basename(a.mp4))[0]
    html = build_html(a.mp4, title, a.template)

    if a.out:
        out = a.out
    else:
        d = a.out_dir or os.getcwd()
        os.makedirs(d, exist_ok=True)
        out = os.path.join(d, safe_filename(title) + '.html')

    parent = os.path.dirname(os.path.abspath(out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)

    n = os.path.getsize(out)
    ok = n <= HTML_LIMIT
    if not ok:
        try:
            os.remove(out)  # 超限文件不保留，避免误上传
        except OSError:
            pass
    print(json.dumps({
        'ok': ok, 'out': out if ok else '', 'size': n, 'size_mb': round(n / 1048576.0, 2),
        'title': title, 'limit_mb': 10,
        'warn': '' if ok else 'HTML 超过 10MB 上限，已丢弃、不上传：请压缩视频或缩短时长',
    }, ensure_ascii=False))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
