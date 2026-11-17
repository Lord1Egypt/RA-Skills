#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 examples/*.puml 渲染成 assets/preview/*.svg，并校验结果是否为真图。

为什么需要这个脚本：
  PlantUML 官网的 /png/<encoded> / /svg/<encoded> 形式用的是**自定义 64 字符编码表**
  （0-9A-Za-z-_），不是标准 base64。用 base64 替换 +/= 是无效的，服务器会返回一张
  "bad URL ... looks like HUFFMAN encoding" 的错误提示图——它也是一张合法 SVG/PNG，
  肉眼很容易误判成渲染成功。本脚本在写盘前会检查内容里是否含错误标记。

用法：
  python scripts/render_preview.py                 # 渲染 examples/ 下全部
  python scripts/render_preview.py timing class    # 只渲染指定几个（不带扩展名）
  python scripts/render_preview.py --check         # 只校验已有的 svg，不重新请求

依赖：Python 3 标准库，无需 pip install。
"""

import glob
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "examples")
OUT_DIR = os.path.join(ROOT, "assets", "preview")
SERVER = "https://www.plantuml.com/plantuml"

# PlantUML 自定义 base64 字符表（与标准 base64 不同！）
TABLE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

# 错误提示图里会出现的标记。命中任何一个都说明这不是一张真图。
ERROR_MARKS = [
    b"bad URL", b"HUFFMAN", b"Syntax Error", b"Assumed diagram",
    b"has crashed", b"error code", b"Syntax Error?",
]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def _append_3bytes(out, b1, b2, b3):
    out.append(TABLE[(b1 >> 2) & 0x3F])
    out.append(TABLE[((b1 & 0x03) << 4 | ((b2 & 0xF0) >> 4)) & 0x3F])
    out.append(TABLE[((b2 & 0x0F) << 2 | ((b3 & 0xC0) >> 6)) & 0x3F])
    out.append(TABLE[b3 & 0x3F])


def encode(text: str) -> str:
    """PlantUML 官方 deflate + 自定义 64 字符编码。"""
    raw = zlib.compress(text.encode("utf-8"), 9)[2:-4]  # 去掉 zlib 头尾，只留 deflate
    out, i, n = [], 0, len(raw)
    while i < n:
        _append_3bytes(
            out,
            raw[i],
            raw[i + 1] if i + 1 < n else 0,
            raw[i + 2] if i + 2 < n else 0,
        )
        i += 3
    return "".join(out)


def is_real_diagram(data: bytes) -> bool:
    """排除「合法但内容是报错信息」的图。"""
    head = data[:4096]
    if b"<svg" not in head and b"<?xml" not in head and data[:8] != b"\x89PNG\r\n\x1a\n":
        return False
    return not any(m in data for m in ERROR_MARKS)


def fetch(src: str, fmt: str = "svg", tries: int = 4):
    """带退避重试的渲染请求。403/429/509 通常是限流或服务器瞬时故障。"""
    url = "%s/%s/%s" % (SERVER, fmt, encode(src))
    last = None
    for attempt in range(tries):
        req = urllib.request.Request(
            url, headers={"User-Agent": UA, "Accept": "image/svg+xml,image/png,*/*"}
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            last = (e.code, e.read())
            if e.code in (403, 429, 500, 502, 503, 509):
                time.sleep(6 * (attempt + 1))  # 限流：退避后重试
            else:
                break  # 400 是源码语法问题，重试没用
    return last


def brief_error(data: bytes) -> str:
    txt = data.decode("utf-8", "replace")
    hits = re.findall(r">([^<>]{0,90})<", txt)
    hits = [h for h in hits if any(k in h for k in ("Syntax", "Error", "Assumed"))]
    return hits[0] if hits else txt[:90].replace("\n", " ")


def render(name: str, fmt: str = "svg") -> bool:
    src_path = os.path.join(SRC_DIR, name + ".puml")
    with open(src_path, encoding="utf-8") as fp:
        source = fp.read()
    status, data = fetch(source, fmt)
    if status == 200 and is_real_diagram(data):
        os.makedirs(OUT_DIR, exist_ok=True)
        dst = os.path.join(OUT_DIR, name + ".svg")
        with open(dst, "wb") as fp:
            fp.write(data)
        print("  [OK]   %-20s %6d bytes" % (name, len(data)))
        return True
    reason = brief_error(data) if status != 200 else "返回的是错误提示图"
    print("  [FAIL] %-20s HTTP %s  %s" % (name, status, reason))
    return False


def check_only(names):
    ok = 0
    for name in names:
        p = os.path.join(OUT_DIR, name + ".svg")
        if not os.path.exists(p):
            print("  [MISS] %-20s 预览图不存在" % name)
            continue
        data = open(p, "rb").read()
        good = is_real_diagram(data)
        print("  [%s] %-20s %6d bytes" % ("OK  " if good else "BAD ", name, len(data)))
        ok += good
    print("\n真图 %d / %d" % (ok, len(names)))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    only_check = "--check" in sys.argv

    all_names = sorted(
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(SRC_DIR, "*.puml"))
    )
    names = args if args else all_names

    if only_check:
        check_only(names)
        return

    ok = sum(render(n) for n in names)
    print("\n成功 %d / %d" % (ok, len(names)))
    if ok != len(names):
        sys.exit(1)


if __name__ == "__main__":
    main()
