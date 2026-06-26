import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lake.lake_setup import start_convert


def ensure_deps():
    try:
        import bs4, yaml, requests
    except ImportError:
        import subprocess

        req = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "requirements.txt"
        )
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req, "-q"])


def main():
    ensure_deps()
    parser = argparse.ArgumentParser(description="语雀 .lakebook 转 Markdown 工具")
    parser.add_argument("-i", "--meta", help="已解压的 meta.json 路径", type=str)
    parser.add_argument("-l", "--lake", help=".lakebook 文件路径", type=str)
    parser.add_argument(
        "-o", "--output", help="Markdown 输出文件夹", type=str, required=True
    )
    parser.add_argument(
        "-d",
        "--downloadImage",
        help="是否下载图片（默认 True）",
        type=bool,
        default=True,
    )
    parser.add_argument(
        "-s", "--skip-existing-resources", help="跳过已下载的资源", action="store_true"
    )
    args = parser.parse_args()
    start_convert(
        args.meta,
        args.lake,
        args.output,
        args.downloadImage,
        args.skip_existing_resources,
    )


if __name__ == "__main__":
    main()
