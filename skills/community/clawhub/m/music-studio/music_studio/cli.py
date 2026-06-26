"""统一 CLI 入口"""

import argparse
import sys

from music_studio import scripts, __version__


def main():
    parser = argparse.ArgumentParser(
        prog="music-studio",
        description="Music Studio — 面向大模型的音乐创作工作台",
    )
    parser.add_argument("--version", action="version", version=f"music-studio {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="初始化配置（默认不保存 API Key）")
    sub.add_parser("set-key", help="显式保存 API Key 到 config.json")
    sub.add_parser("clear-key", help="移除 config.json 中保存的 API Key")

    p = sub.add_parser("lyrics", help="作词")
    p.add_argument("prompt", nargs="?", help="主题/风格描述")
    p.add_argument("--title", help="指定歌曲标题")
    p.add_argument("--edit", help="续写已有歌词")

    p = sub.add_parser("music", help="文本生成音乐")
    p.add_argument("prompt", nargs="?", help="音乐风格/情绪/场景描述（必填）")
    p.add_argument("lyrics", nargs="?", help="歌词内容（\\n分隔）")
    p.add_argument("--instrumental", action="store_true", help="生成纯音乐（无人声）")
    p.add_argument("--optimizer", action="store_true", help="自动根据描述生成歌词")
    p.add_argument("--format", default="url", choices=["url", "hex"], help="输出格式（默认 url）")
    p.add_argument("--sr", type=int, default=44100, help="采样率（默认 44100）")
    p.add_argument("--bitrate", type=int, default=256000, help="比特率（默认 256000）")

    p = sub.add_parser("cover", help="翻唱（基于参考音频）")
    p.add_argument("prompt", nargs="?", help="目标翻唱风格描述（必填）")
    p.add_argument("--audio", required=True, help="参考音频 URL")
    p.add_argument("--lyrics", help="可选歌词")

    lp = sub.add_parser("library", help="音乐库管理")
    lp.add_argument("action", nargs="?", default="list")
    lp.add_argument("arg", nargs="?")
    lp.add_argument("sub", nargs="?")

    sub.add_parser("clean", help="清理过期文件")
    sub.add_parser("reset", help="重置配置和输出")
    sub.add_parser("help", help="显示完整帮助")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "init": (scripts.init_main, None),
        "set-key": (scripts.set_key_main, None),
        "clear-key": (scripts.clear_key_main, None),
        "lyrics": (scripts.lyrics_main, args),
        "music": (scripts.music_main, args),
        "cover": (scripts.cover_main, args),
        "library": (scripts.library_main, args),
        "clean": (scripts.clean_main, None),
        "reset": (scripts.reset_main, None),
        "help": (scripts.help_main, None),
    }

    fn, fn_args = dispatch.get(args.command, (None, None))
    if fn is None:
        parser.print_help()
        sys.exit(0)

    fn(fn_args)


if __name__ == "__main__":
    main()
