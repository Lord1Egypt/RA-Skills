"""
PingCode 共享配置 —— 从 .env 文件和环境变量加载凭证
优先级：环境变量 > .env 文件
"""
import os

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(SKILL_ROOT, ".env")


def _load_env_file():
    """从 .env 文件加载变量到 os.environ（不覆盖已有环境变量）"""
    if not os.path.isfile(ENV_FILE):
        return
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


_load_env_file()

BASE_URL = "https://open.pingcode.com"
CLIENT_ID = os.environ.get("PINGCODE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("PINGCODE_CLIENT_SECRET")
