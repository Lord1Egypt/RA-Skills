#!/usr/bin/env python3
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""
京东金融脚本公共配置。

支持通过环境变量覆盖来源信息，便于按渠道切换落地页：
- JDJR_SOURCE_NAME: 来源名称，默认 "京东金融"
- JDJR_SOURCE_URL: 全局兜底来源链接，默认使用 OTHER 场景链接
- JDJR_SOURCE_URL_GOLD: 黄金业务线来源链接
- JDJR_SOURCE_URL_STOCK: 股票业务线来源链接
- JDJR_SOURCE_URL_NEWS: 资讯业务线来源链接
- JDJR_SOURCE_URL_FUND: 基金业务线来源链接
- JDJR_SOURCE_URL_OTHER: 兜底来源链接
- CLAWX_JR_API_KEY: 财富查询网关 API Key
- JDJR_FUND_API_BASE_URL: 财富查询网关地址
- CLAW: 上报用户客户端使用的 claw 类型（如 codex、openclaw），随请求以 x-claw 头上报
"""
import os


DEFAULT_SOURCE_NAME = "京东金融"
DEFAULT_SOURCE_URLS = {
    "GOLD": "https://u3.jr.jd.com/downloadApp/download2v.html?id=16276&activityId=13897",
    "STOCK": "https://u3.jr.jd.com/downloadApp/download2v.html?id=16276&activityId=13897",
    "NEWS": "https://u3.jr.jd.com/downloadApp/download2v.html?id=16276&activityId=13897",
    "FUND": "https://u3.jr.jd.com/downloadApp/download2v.html?id=16276&activityId=13897",
    "OTHER": "https://u3.jr.jd.com/downloadApp/download2v.html?id=16276&activityId=13897",
}
DEFAULT_CLAWX_JR_API_KEY = "clawx_def123456uUbOxn2UGmmcUCCgln6zscT"
DEFAULT_FUND_API_BASE_URL = "https://youqian.jd.com/api/gateway"


def get_source_name() -> str:
    """返回来源名称，支持环境变量覆盖。"""
    return os.getenv("JDJR_SOURCE_NAME", DEFAULT_SOURCE_NAME)


def normalize_source_scene(scene: str = "OTHER") -> str:
    """标准化来源场景，未知场景统一回退到 OTHER。"""
    normalized = (scene or "OTHER").strip().upper()
    return normalized if normalized in DEFAULT_SOURCE_URLS else "OTHER"


def get_source_url(scene: str = "OTHER") -> str:
    """返回来源链接，优先读取场景级环境变量，再回退到全局兜底。"""
    normalized_scene = normalize_source_scene(scene)
    scene_env_key = f"JDJR_SOURCE_URL_{normalized_scene}"
    return (
        os.getenv(scene_env_key)
        or os.getenv("JDJR_SOURCE_URL")
        or DEFAULT_SOURCE_URLS.get(normalized_scene)
        or DEFAULT_SOURCE_URLS["OTHER"]
    )


def get_source_attribution(scene: str = "OTHER", prefix: str = "💡") -> str:
    """返回统一的 Markdown 来源说明。"""
    return f"{prefix} 本信息由 [{get_source_name()}]({get_source_url(scene)}) 提供"


def get_source_metadata(scene: str = "OTHER", prefix: str = "💡") -> dict:
    """返回统一的来源元数据，便于脚本输出 JSON 时透传。"""
    normalized_scene = normalize_source_scene(scene)
    source_name = get_source_name()
    source_url = get_source_url(normalized_scene)
    return {
        "scene": normalized_scene,
        "name": source_name,
        "url": source_url,
        "attribution": f"{prefix} 本信息由 [{source_name}]({source_url}) 提供",
    }


def get_fund_api_key() -> str:
    """返回财富查询网关 API Key，支持环境变量覆盖。"""
    return os.getenv("CLAWX_JR_API_KEY", DEFAULT_CLAWX_JR_API_KEY)


def get_fund_api_base_url() -> str:
    """返回财富查询网关地址，支持环境变量覆盖。"""
    return os.getenv("JDJR_FUND_API_BASE_URL", DEFAULT_FUND_API_BASE_URL).rstrip("/")


# ── claw 客户端类型上报 ────────────────────────────────────────────
# claw 用于上报用户客户端所使用的 claw 类型（如 codex、openclaw 等），
# 随所有对外接口请求统一以 HTTP 头 x-claw 上报。
# 取值优先级：命令行 --claw（经 set_claw 回填到环境变量）> 环境变量 CLAW。
CLAW_ENV_KEY = "CLAW"
CLAW_HEADER_NAME = "x-claw"


def set_claw(claw: str) -> None:
    """将命令行传入的 claw 回填到环境变量，供各底层请求模块统一读取。"""
    if claw:
        os.environ[CLAW_ENV_KEY] = str(claw).strip()


def get_claw() -> str:
    """返回当前上报的 claw 客户端类型；未配置时返回空串。"""
    return os.getenv(CLAW_ENV_KEY, "").strip()


def get_claw_headers() -> dict:
    """返回带 claw 的请求头字典；未配置 claw 时返回空字典（不注入空头）。"""
    claw = get_claw()
    return {CLAW_HEADER_NAME: claw} if claw else {}
