#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全局剪贴板监听：不依赖浏览器，轮询系统剪贴板，发现网盘/直链自动投递到本机 pan serve。

兼容：macOS 用 pbpaste；Linux 尝试 xclip/xsel；Windows 尝试 powershell Get-Clipboard。
只投递 http(s) 链接，且会去重（同一链接 10 分钟内不重复投递一次）；
投递成功后把 pan serve 返回的 /live 链接打印出来，方便 Agent/用户打开实时进度。

用法：
  python3 clipboard_monitor.py                 # 常驻监听（默认 127.0.0.1:17890）
  python3 clipboard_monitor.py --once          # 只检查一次当前剪贴板并退出
  python3 clipboard_monitor.py --interval 2    # 轮询间隔（秒）
  python3 clipboard_monitor.py --port 17890    # 本机 serve 端口
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

_URL_RE = re.compile(r"https?://[^\s<>\"]+", re.IGNORECASE)
_BASE = "http://127.0.0.1:%s"
_DEDUP_SECONDS = 600


def read_clipboard():
    """读取系统剪贴板文本；成功返回 str，失败返回空串。"""
    for argv in _clipboard_readers():
        try:
            proc = subprocess.run(argv, capture_output=True, text=True, timeout=8)
            text = (proc.stdout or "").strip()
            if text:
                return text
        except (OSError, subprocess.TimeoutExpired):
            continue
    return ""


def _clipboard_readers():
    out = []
    from platform import system as _platform
    sysname = (_platform() or "").lower()
    if sysname == "darwin":
        out.append(["pbpaste"])
    elif sysname.startswith("windows"):
        out.append(["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"])
    else:
        out.append(["xclip", "-selection", "clipboard", "-o"])
        out.append(["xsel", "--clipboard", "--output"])
    return out


def extract_urls(text):
    """从任意文本中抽取 http(s) 链接（含被包在聊天/括号里的情况）。"""
    if not text:
        return []
    return list(dict.fromkeys(_URL_RE.findall(text)))


def _post_download(url, port, pwd=""):
    data = json.dumps({"url": url, "pwd": pwd or ""}).encode("utf-8")
    req = urllib.request.Request(_BASE % port + "/api/download", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8") or "{}")


def main():
    parser = argparse.ArgumentParser(description="全局剪贴板监听 → 自动投递本机 pan serve")
    parser.add_argument("--once", action="store_true", help="只检查一次当前剪贴板")
    parser.add_argument("--interval", type=float, default=2.0, help="轮询间隔秒数")
    parser.add_argument("--port", type=int, default=17890)
    parser.add_argument("--pwd", default="", help="提取码（剪贴板里没有时使用）")
    parser.add_argument("--dedup-seconds", type=float, default=_DEDUP_SECONDS, help="同一链接去重秒数")
    args = parser.parse_args()

    last_seen = {}  # url -> time
    checked_once = False
    while True:
        text = read_clipboard()
        urls = extract_urls(text)
        for url in urls:
            now = time.time()
            if url in last_seen and now - last_seen[url] < args.dedup_seconds:
                continue
            last_seen[url] = now
            try:
                res = _post_download(url, args.port, pwd=args.pwd)
            except Exception as exc:  # noqa: BLE001
                sys.stderr.write("投递失败 %s : %s\n" % (url, exc))
                continue
            if res.get("ok"):
                live = res.get("live_url") or ""
                sys.stdout.write("✅ 已投递下载：%s%s\n" % (url, "　实时进度：%s" % live if live else ""))
            else:
                sys.stdout.write("❌ 投递被拒：%s → %s\n" % (url, res.get("error") or "未知"))
        if args.once:
            return 0
        time.sleep(max(0.3, args.interval))


if __name__ == "__main__":
    sys.exit(main())
