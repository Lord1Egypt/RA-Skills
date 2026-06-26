#!/usr/bin/env python3
"""Vidu 视频查询别名入口。

主实现位于 sora_query_video.py；本文件仅设置 provider hint 后转发到主入口。
"""

import os
import sys

os.environ.setdefault("VIDEO_PROVIDER_HINT", "vidu")
sys.path.insert(0, os.path.dirname(__file__))
from sora_query_video import main


if __name__ == "__main__":
    main()
