import os


def _env(name: str, default: str = "") -> str:
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).strip()


# 将本文件复制为 config.py 后填写，或通过环境变量注入配置：
# - KINGDEE_BASE_URL
# - KINGDEE_ACCTID
# - KINGDEE_USERNAME
# - KINGDEE_PASSWORD
# - WECHAT_WEBHOOK（可选）
KINGDEE_CONFIG = {
    "base_url": _env("KINGDEE_BASE_URL", "https://your-k3cloud-host"),
    "acctid": _env("KINGDEE_ACCTID", ""),
    "username": _env("KINGDEE_USERNAME", ""),
    "password": _env("KINGDEE_PASSWORD", ""),
}

WECHAT_CONFIG = {
    "webhook": _env("WECHAT_WEBHOOK", ""),
}

