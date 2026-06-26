import os


def _env(name: str, default: str = "") -> str:
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).strip()


# 说明：
# - 请在本地填写真实凭据；不要把真实信息提交到公开仓库。
# - 推荐做法：把 `config.example.py` 复制为 `config.py` 再填写。
KINGDEE_CONFIG = {
    # 例如 https://xxxx.ik3cloud.com
    "base_url": _env("KINGDEE_BASE_URL", "https://your-k3cloud-host"),
    "acctid": _env("KINGDEE_ACCTID", ""),  # 账套 ID（AcctId）
    "username": _env("KINGDEE_USERNAME", ""),
    "password": _env("KINGDEE_PASSWORD", ""),
}

# 可选：企业微信群机器人 webhook。不填也能导出（配合 --no-wechat 或留空）。
WECHAT_CONFIG = {
    "webhook": _env("WECHAT_WEBHOOK", ""),
}
