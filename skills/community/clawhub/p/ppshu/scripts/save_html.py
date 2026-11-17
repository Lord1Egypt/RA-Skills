#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ppshu — 把一张 HTML 图存入集中管理的「画册」，并按 001-* 序号命名。

用法
----
    # 从标准输入读取 HTML
    cat diagram.html | python save_html.py "<一句话描述>"

    # 从文件读取 HTML
    python save_html.py "<一句话描述>" --file diagram.html

    # 指定集中目录（默认当前工作目录下的 .ppshu/，可整目录删除）
    python save_html.py "<描述>" --dir "D:/my/ppshu"

行为
----
1. 扫描目标目录，找出当前最大序号，下一个序号为 最大值+1（从 001 起）。
2. 描述会被转成 kebab-case（中文保留），作为文件名后缀。
3. 写入 <NNN>-<描述>.html。
4. 重新生成 index.html —— 一个列出全部作品的画廊。
5. 把最终保存的绝对路径打印到 stdout，供上层调用 present_files。

文件名示例
----------
    001-股票价格走势图.html
    002-tcp-ip-协议栈.html
    003-登录表单原型.html
"""
import os
import re
import sys
import html as _html
import datetime

# 默认存到「当前工作目录」下的 .ppshu/ —— 作品落在用户正在做的项目里，好找、可整目录删除。
DEFAULT_DIR = os.path.join(os.getcwd(), ".ppshu")

# 技能根目录（scripts 的上一级），用于定位随包发布的 assets/mermaid.min.js
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MERMAID_SRC = os.path.join(SKILL_DIR, "assets", "mermaid.min.js")


def kebab(text: str) -> str:
    """转 kebab-case：英文小写、空格/符号转连字符，中文原样保留。"""
    text = text.lower().strip()
    # 保留中文、字母、数字，其余折叠成连字符
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:60] or "diagram"


def next_serial(directory: str) -> str:
    """返回下一个 3 位序号字符串（001, 002, ...）。"""
    highest = 0
    if os.path.isdir(directory):
        for fn in os.listdir(directory):
            m = re.match(r"^(\d{3})-", fn)
            if m:
                highest = max(highest, int(m.group(1)))
    return f"{highest + 1:03d}"


def maybe_copy_mermaid(directory: str, content: str) -> None:
    """若 HTML 引用了本地 mermaid（用 ./mermaid.min.js），则把随包发布的库复制到
    同目录，保证生成的流程图离线也能渲染，不依赖任何 CDN。"""
    if "mermaid.min.js" not in content or not os.path.isfile(MERMAID_SRC):
        return
    import shutil
    dest = os.path.join(directory, "mermaid.min.js")
    # 已存在且大小一致则跳过，避免每次保存都重写 3.3MB
    if os.path.exists(dest) and os.path.getsize(dest) == os.path.getsize(MERMAID_SRC):
        return
    shutil.copyfile(MERMAID_SRC, dest)


def build_index(directory: str) -> str:
    """生成画廊 index.html。"""
    items = []
    for fn in sorted(os.listdir(directory)):
        m = re.match(r"^(\d{3})-(.+)\.html$", fn)
        if not m:
            continue
        serial, desc = m.group(1), m.group(2)
        try:
            ts = datetime.datetime.fromtimestamp(
                os.path.getmtime(os.path.join(directory, fn))
            )
            date = ts.strftime("%Y-%m-%d %H:%M")
        except Exception:
            date = ""
        items.append((serial, desc, fn, date))

    rows = "\n".join(
        f'      <li><a href="{fn}">{serial} · {_html.escape(desc)}</a>'
        f'<span class="date">{date}</span></li>'
        for serial, desc, fn, date in sorted(items, key=lambda x: x[0])
    )
    count = len(items)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ppshu 图库</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ font-family: -apple-system, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
         background:#0f1115; color:#e6e6e6; margin:0; padding:32px; }}
  h1 {{ font-weight:600; margin:0 0 4px; }}
  .meta {{ color:#8a93a6; margin-bottom:20px; }}
  ul {{ list-style:none; padding:0; margin:0; }}
  li {{ padding:12px 16px; margin:8px 0; background:#1a1d24; border-radius:10px;
        display:flex; justify-content:space-between; align-items:center; }}
  a {{ color:#7cc4ff; text-decoration:none; font-size:15px; }}
  a:hover {{ text-decoration:underline; }}
  .date {{ color:#8a93a6; font-size:13px; }}
</style>
</head>
<body>
  <h1>🛠️ ppshu 图库</h1>
  <div class="meta">共 {count} 个 HTML 图 · 点击打开</div>
  <ul>
{rows}
  </ul>
</body>
</html>
"""


def main() -> None:
    args = sys.argv[1:]
    description = None
    file_path = None
    dir_override = None

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--file":
            file_path = args[i + 1]
            i += 2
            continue
        if a == "--dir":
            dir_override = args[i + 1]
            i += 2
            continue
        if description is None:
            description = a
        i += 1

    directory = dir_override or os.environ.get("PPSHU_DIR") or DEFAULT_DIR
    os.makedirs(directory, exist_ok=True)

    if not description:
        description = "diagram"

    serial = next_serial(directory)
    filename = f"{serial}-{kebab(description)}.html"

    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    out_path = os.path.join(directory, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 流程图类会引用 ./mermaid.min.js，这里自动把打包的库补到同目录，离线可用
    maybe_copy_mermaid(directory, content)

    with open(os.path.join(directory, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index(directory))

    print(os.path.abspath(out_path))


if __name__ == "__main__":
    main()
