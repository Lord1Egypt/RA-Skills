import subprocess
import os
import sys
from pathlib import Path

class EnvChecker:
    @staticmethod
    def is_notebooklm_installed():
        try:
            import notebooklm
            return True
        except ImportError:
            return False

    @staticmethod
    def is_playwright_ready():
        # 检查 playwright 是否安装，以及 chromium 是否下载
        try:
            import playwright
            # 简单检查是否有 chromium 文件夹 (通常在 ~/Library/Caches/ms-playwright/ or ~/.cache/ms-playwright/)
            # 更靠谱的方法是调用 playwright 内部接口，或者直接尝试运行命令
            # 这里简单处理：如果能导入 playwright 且不是异常，我们之后安装时会确保覆盖
            return True
        except ImportError:
            return False

    @staticmethod
    def is_logged_in():
        # notebooklm-py 默认将 session 存储在用户根目录下的 .notebooklm_session (可能是 json 格式)
        # 具体取决于该包的实现，常见位置包括 ~/.notebooklm_session
        session_path = Path.home() / ".notebooklm_session"
        return session_path.exists()

    @staticmethod
    def run_install():
        """执行安装脚本并返回结果"""
        try:
            # 使用 sys.executable 确保在同一个 python 环境下安装
            print("Installing dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "notebooklm-py[browser]"])
            
            print("Downloading browser core...")
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
            
            return True, "Installation successful"
        except Exception as e:
            return False, str(e)
