# -*- coding: utf-8 -*-
"""
用系统默认浏览器打开本地题库网站。供每日提醒的自动化任务调用。

用法：
    python open_quiz.py <site-dir-or-index.html>

为什么必须用这个脚本，而不是用预览面板打开：
    浏览器的 localStorage 按「来源（origin）」隔离，而题库的全部学习数据
    ——练习进度、错题本、收藏、打卡、每道题的记忆强度——都存在 localStorage。

        用户双击打开        → file:///.../index.html      → 数据仓库 A
        内置预览面板打开     → http://127.0.0.1:<随机端口>/ → 数据仓库 B（端口还会变）

    如果提醒用预览面板打开，用户会得到一个「进度全空」的题库，并且此后
    在两个仓库之间来回切换，数据永久分裂且无法合并。

    本脚本始终以 file:// 打开，与用户平时双击的行为完全一致，只有一份数据。
"""
import os
import sys
import webbrowser
from pathlib import Path


def resolve_index(target: str) -> Path:
    p = Path(target).expanduser().resolve()
    if p.is_dir():
        p = p / "index.html"
    if p.suffix.lower() not in (".html", ".htm"):
        raise SystemExit(f"目标不是 HTML 文件：{p}")
    if not p.is_file():
        raise SystemExit(f"找不到题库入口文件：{p}")
    return p


def main(argv):
    if not argv:
        print(__doc__)
        return 2

    index = resolve_index(argv[0])
    url = index.as_uri()  # 自动处理盘符、空格与中文路径

    ok = webbrowser.open(url)

    # webbrowser 在部分极简环境下会静默失败，回退到系统原生命令
    if not ok:
        if sys.platform.startswith("win"):
            os.startfile(str(index))  # noqa: S606
        elif sys.platform == "darwin":
            os.system(f'open "{index}"')
        else:
            os.system(f'xdg-open "{index}"')

    print(f"已在默认浏览器打开：{url}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
