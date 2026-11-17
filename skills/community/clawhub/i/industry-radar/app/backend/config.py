"""
全局配置。

所有配置均可通过环境变量覆盖，便于在本地 / 华为云 FunctionGraph / ECS 上无缝切换。

LLM 采用「OpenAI 兼容协议」，因此可直接对接：
  - 华为云 ModelArts Studio（盘古 / 开源模型推理服务）
  - 任意 OpenAI 兼容网关
未配置 LLM 时，系统自动降级为「抽取式摘要 + 规则洞察」，保证任何环境都能跑通。
"""
from __future__ import annotations

import os
from pathlib import Path

# ---------------------------------------------------------------- 路径
BASE_DIR = Path(__file__).resolve().parent.parent          # project/
DATA_DIR = Path(os.getenv("IR_DATA_DIR", str(BASE_DIR / "data")))
BRIEF_DIR = DATA_DIR / "briefings"
DB_PATH = Path(os.getenv("IR_DB_PATH", str(DATA_DIR / "industry_radar.db")))

DATA_DIR.mkdir(parents=True, exist_ok=True)
BRIEF_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- LLM
LLM_BASE_URL = os.getenv("IR_LLM_BASE_URL", "").rstrip("/")
LLM_API_KEY = os.getenv("IR_LLM_API_KEY", "")
LLM_MODEL = os.getenv("IR_LLM_MODEL", "deepseek-chat")
LLM_TIMEOUT = int(os.getenv("IR_LLM_TIMEOUT", "60"))
USE_LLM = bool(LLM_BASE_URL and LLM_API_KEY)

# ---------------------------------------------------------------- 采集
REQUEST_TIMEOUT = int(os.getenv("IR_HTTP_TIMEOUT", "15"))
USER_AGENT = os.getenv(
    "IR_USER_AGENT",
    "Mozilla/5.0 (compatible; IndustryRadar/1.0; +weekly-briefing)",
)
MAX_ARTICLES_PER_SOURCE = int(os.getenv("IR_MAX_PER_SOURCE", "15"))
FETCH_FULLTEXT = os.getenv("IR_FETCH_FULLTEXT", "1") == "1"
# 单次出站响应体上限（字节）：防止被超大页面拖垮，也限制 SSRF 探测的带宽面
MAX_FETCH_BYTES = int(os.getenv("IR_MAX_FETCH_BYTES", str(3 * 1024 * 1024)))

# ---------------------------------------------------- 自定义源（用户自填 RSS）
# 是否允许用户添加自定义 RSS/Atom 源；托管多租户场景可置 0 一并关闭。
ALLOW_CUSTOM_SOURCES = os.getenv("IR_ALLOW_CUSTOM_SOURCES", "1") == "1"
# 每个用户可保存的自定义源上限
CUSTOM_MAX_PER_USER = int(os.getenv("IR_CUSTOM_MAX_PER_USER", "10"))
# 单个订阅最多引用的自定义源数量
CUSTOM_MAX_PER_SUB = int(os.getenv("IR_CUSTOM_MAX_PER_SUB", "5"))
# 连续失败多少轮后自动禁用（避免死链拖慢整轮采集）
CUSTOM_DISABLE_AFTER_FAILS = int(os.getenv("IR_CUSTOM_DISABLE_AFTER_FAILS", "3"))
# 自定义源录入时的探测超时（秒）
CUSTOM_PROBE_TIMEOUT = int(os.getenv("IR_CUSTOM_PROBE_TIMEOUT", "10"))
# 允许出站的端口白名单（自定义源只走标准 Web 端口）
ALLOWED_PORTS = tuple(
    int(p) for p in os.getenv("IR_ALLOWED_PORTS", "80,443").split(",") if p.strip().isdigit()
) or (80, 443)

# ---------------------------------------------------------------- 生成策略
TOP_K_ARTICLES = int(os.getenv("IR_TOP_K", "12"))      # 每份简报纳入的文章上限
CLUSTER_THRESHOLD = float(os.getenv("IR_CLUSTER_THRESHOLD", "0.18"))  # token Jaccard 兜底阈值
MAX_SECTIONS = int(os.getenv("IR_MAX_SECTIONS", "5"))  # 简报板块数量上限（超出合并为「其他动态」）
DEDUP_HAMMING = int(os.getenv("IR_DEDUP_HAMMING", "3"))  # simhash 汉明距离阈值

# 编辑精选模式（curated）：每期从候选池精选的文章条数
CURATED_PICKS = int(os.getenv("IR_CURATED_PICKS", "5"))

# ---------------------------------------------------------------- 演示账号
DEMO_USER = os.getenv("IR_DEMO_USER", "demo")
DEMO_PASS = os.getenv("IR_DEMO_PASS", "demo")