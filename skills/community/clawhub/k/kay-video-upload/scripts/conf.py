"""
自动生成的 conf.py - 路径相对于本文件所在目录
"""
import os
from pathlib import Path

# BASE_DIR 指向 scripts/ 目录本身（所有资源相对于此）
BASE_DIR = Path(__file__).parent

# 视频目录 - 可通过环境变量 VIDEO_DIR 覆盖
VIDEO_DIR = Path(os.environ.get("VIDEO_DIR", str(BASE_DIR / "videos")))

# Chrome 路径 - 安装时由 setup.py 自动检测并写入，也可手动修改
LOCAL_CHROME_PATH = os.environ.get("CHROME_PATH", "")

# 是否无头模式（False = 显示浏览器窗口，登录时必须为 False）
LOCAL_CHROME_HEADLESS = False

# 小红书签名服务地址
XHS_SERVER = os.environ.get("XHS_SERVER", "http://127.0.0.1:11901")
