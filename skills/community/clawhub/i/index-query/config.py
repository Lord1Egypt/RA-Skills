"""Index Hub v3.0.0 统一配置（对外版本）.

鉴权方式（优先级从高到低）：
  1. 环境变量 INDEX_HUB_API_KEY（可选临时覆盖）
  2. 用户凭据文件 ~/.config/index-hub/api_key（安装默认）
  3. 环境变量 ETF_API_KEY（兼容旧版本）
"""

import os
from pathlib import Path

BASE_URL = "https://www.etf.com.cn/api/etf-api-service"
CREDENTIALS_FILE = Path.home() / ".config" / "index-hub" / "api_key"


def _read_credentials_file() -> str:
    try:
        return CREDENTIALS_FILE.read_text(encoding="utf-8").strip()
    except (FileNotFoundError, OSError):
        return ""


API_KEY = os.environ.get("INDEX_HUB_API_KEY") or _read_credentials_file() or os.environ.get("ETF_API_KEY") or ""

CALLER_TYPE = "external"

# 请求头固定配置
# 认证格式：Authorization: Bearer <API_KEY>
# 请求来源标识：X-Caller-Type: external

if not API_KEY:
    raise RuntimeError(
        "未找到 API Key。\n"
        "如需获取API Key，请在微信搜索“指数直通车”小程序，在「AI Skills」页面申请。更多说明可访问帮助文档：https://cdn.efunds.com.cn/eda/h5/itcenter/pd/ai-skills-doc/help.pdf"
    )
