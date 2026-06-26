#!/usr/bin/env python3
"""
Markdown -> 微信兼容 HTML 转换器（统一入口）

这是对外接口，负责模式识别和配置参数解析，实际转换委托给：
  - md2news_html.py    —— 新闻模式（板块化日报）
  - md2article_html.py  —— 文章模式（长文叙事，配色通过 config.yaml 控制）

用法:
  python3 md2wechat_html.py --article <input.md> [output.html]    # 文章模式（默认）
  python3 md2wechat_html.py --news <input.md> [output.html]       # 新闻模式
  python3 md2wechat_html.py --config /path/to/config.yaml --article <input.md> [output.html]

不指定模式时默认为 --article。
"""

import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    args = sys.argv[1:]
    mode = "article"  # 默认文章模式
    config_path = None
    pass_through = []  # 透传给子脚本的参数（--no-title / --with-title）

    i = 0
    while i < len(args):
        if args[i] == '--news':
            mode = "news"
        elif args[i] == '--article':
            mode = "article"
        elif args[i] == '--config':
            i += 1
            if i < len(args):
                config_path = args[i]
        elif args[i] in ('--no-title', '--with-title'):
            pass_through.append(args[i])
        else:
            break
        i += 1
    positional = args[i:]

    if not positional:
        print("用法:")
        print("  python3 md2wechat_html.py --article <input.md> [output.html]    # 文章模式（默认）")
        print("  python3 md2wechat_html.py --news <input.md> [output.html]       # 新闻模式")
        print("  python3 md2wechat_html.py --config <path> --article <input.md> [output.html]")
        print()
        print("不指定模式时默认为 --article。")
        print("--no-title（默认，去除标题块）/ --with-title（保留标题块）")
        sys.exit(1)

    # 构建子脚本命令
    if mode == "article":
        script = os.path.join(SCRIPT_DIR, "md2article_html.py")
    else:
        script = os.path.join(SCRIPT_DIR, "md2news_html.py")

    cmd = [sys.executable, script]
    if config_path:
        cmd.extend(["--config", config_path])
    cmd.extend(pass_through + positional)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
