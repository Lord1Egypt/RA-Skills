"""
引擎注册表 - 全局单一真相源
==============================
V1.2 新增（修复 P0-2 / P0-7）

问题背景：
    V1.1 新增 Yandex/Startpage/Qwant/Brave 四个引擎时，有三处引擎清单没有同步：
      1. privacy.py:97 的 all_engines 硬编码 6 个（少 4 个）
      2. config.yaml.example 的 allowed_engines 只列 2 个
      3. 文档中的引擎描述与实现不一致
    根因是"引擎清单"散落在多个文件中，没有唯一来源。

解决方案：
    本模块作为全局唯一真相源，所有需要"引擎清单"的地方一律从这里读取，
    以后新增引擎只需改这一个文件。
"""

import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True


# ============================================================
# 引擎元数据
# ============================================================

@dataclass(frozen=True)
class EngineMeta:
    """
    引擎元数据

    Attributes:
        name:          引擎标识（CLI 与配置文件中使用）
        display_name:  中文显示名
        region:        所属区域
        china_ok:      国内网络是否可直连
        privacy_level: 隐私保护等级 high | medium | low
        strict_ok:     是否允许在 strict 隐私模式下使用
        authority:     权威度权重（用于 F1-6 排序加权，1.0 为基准）
        note:          补充说明
    """
    name: str
    display_name: str
    region: str
    china_ok: bool
    privacy_level: str
    strict_ok: bool
    authority: float = 1.0
    note: str = ""


# ============================================================
# 十引擎注册表（唯一真相源）
# ============================================================
# 说明：
#   - 顺序即 strict 模式下的降级优先级（越靠前越优先）
#   - 新增引擎只需在此处追加一条，其它模块自动感知

ENGINE_REGISTRY: Dict[str, EngineMeta] = {
    # ---------- 本地优先 ----------
    "searxng": EngineMeta(
        name="searxng",
        display_name="本地 SearXNG",
        region="local",
        china_ok=True,
        privacy_level="high",
        strict_ok=True,
        authority=1.2,
        note="本地实例，隐私最佳；需先启动容器或 pip 实例",
    ),
    # ---------- 隐私优先（国内可用性递减） ----------
    "yandex": EngineMeta(
        name="yandex",
        display_name="Yandex",
        region="ru",
        china_ok=True,
        privacy_level="medium",
        strict_ok=True,
        authority=1.0,
        note="俄罗斯引擎，国内连接较稳定",
    ),
    "startpage": EngineMeta(
        name="startpage",
        display_name="Startpage",
        region="nl",
        china_ok=True,
        privacy_level="high",
        strict_ok=True,
        authority=1.1,
        note="Google 结果代理，不记录用户信息",
    ),
    "qwant": EngineMeta(
        name="qwant",
        display_name="Qwant",
        region="fr",
        china_ok=True,
        privacy_level="high",
        strict_ok=True,
        authority=1.0,
        note="法国引擎，遵循 GDPR",
    ),
    "brave": EngineMeta(
        name="brave",
        display_name="Brave Search",
        region="us",
        china_ok=True,
        privacy_level="high",
        strict_ok=True,
        authority=1.05,
        note="独立索引，隐私保护良好",
    ),
    "duckduckgo": EngineMeta(
        name="duckduckgo",
        display_name="DuckDuckGo",
        region="us",
        china_ok=False,
        privacy_level="high",
        strict_ok=True,
        authority=1.1,
        note="隐私优先，国内直连不稳定，建议配合代理",
    ),
    # ---------- 国内引擎（normal 模式） ----------
    "baidu": EngineMeta(
        name="baidu",
        display_name="百度",
        region="cn",
        china_ok=True,
        privacy_level="low",
        strict_ok=False,
        authority=1.0,
        note="中文内容覆盖最广，会记录搜索行为",
    ),
    "bing": EngineMeta(
        name="bing",
        display_name="必应",
        region="cn",
        china_ok=True,
        privacy_level="low",
        strict_ok=False,
        authority=1.15,
        note="中英文均衡，结果质量较高",
    ),
    "sogou": EngineMeta(
        name="sogou",
        display_name="搜狗",
        region="cn",
        china_ok=True,
        privacy_level="low",
        strict_ok=False,
        authority=0.9,
        note="微信公众号内容独家",
    ),
    "360": EngineMeta(
        name="360",
        display_name="360 搜索",
        region="cn",
        china_ok=True,
        privacy_level="low",
        strict_ok=False,
        authority=0.85,
        note="国内可用，隐私保护较弱",
    ),
}


# ============================================================
# 派生清单（供各模块直接引用，避免重复硬编码）
# ============================================================

def all_engine_names() -> List[str]:
    """全部引擎名（十个）"""
    return list(ENGINE_REGISTRY.keys())


def strict_allowed_engines() -> List[str]:
    """strict 模式允许的引擎（按降级优先级排序）"""
    return [name for name, meta in ENGINE_REGISTRY.items() if meta.strict_ok]


def strict_fallback_engines() -> List[str]:
    """
    strict 模式降级链（不含 searxng）

    searxng 需本地实例，不适合作为自动降级目标，
    故降级链只包含可直接访问的公网隐私引擎。
    """
    return [
        name for name, meta in ENGINE_REGISTRY.items()
        if meta.strict_ok and name != "searxng"
    ]


def china_friendly_engines() -> List[str]:
    """国内可直连的引擎"""
    return [name for name, meta in ENGINE_REGISTRY.items() if meta.china_ok]


def default_engines() -> List[str]:
    """默认引擎组合（速度与覆盖面平衡）"""
    return ["baidu", "bing", "duckduckgo", "searxng"]


def get_meta(engine: str) -> Optional[EngineMeta]:
    """获取指定引擎的元数据，不存在返回 None"""
    return ENGINE_REGISTRY.get(engine)


def get_authority(engine: str) -> float:
    """获取引擎权威度权重（用于排序加权），未知引擎返回 1.0"""
    meta = ENGINE_REGISTRY.get(engine)
    return meta.authority if meta else 1.0


def is_valid_engine(engine: str) -> bool:
    """校验引擎名是否合法"""
    return engine in ENGINE_REGISTRY


def validate_engines(engines: List[str]) -> tuple:
    """
    校验引擎列表

    Returns:
        (合法引擎列表, 非法引擎列表)
    """
    valid = [e for e in engines if e in ENGINE_REGISTRY]
    invalid = [e for e in engines if e not in ENGINE_REGISTRY]
    return valid, invalid


def _display_width(text: str) -> int:
    """
    计算字符串显示宽度

    中日韩字符在等宽终端中占两列，需单独计算，
    否则中英文混排的表格无法对齐。
    """
    width = 0
    for ch in text:
        width += 2 if "\u1100" <= ch <= "\uffdc" and not ch.isascii() else 1
    return width


def _pad(text: str, width: int) -> str:
    """按显示宽度右侧补空格"""
    return text + " " * max(0, width - _display_width(text))


def format_engine_table() -> str:
    """生成引擎清单表格（供 CLI 与文档展示）"""
    headers = ["引擎名", "显示名", "区域", "国内直连", "隐私", "strict"]
    widths = [14, 16, 8, 10, 8, 6]

    lines = ["".join(_pad(h, w) for h, w in zip(headers, widths))]
    lines.append("-" * sum(widths))

    for meta in ENGINE_REGISTRY.values():
        row = [
            meta.name,
            meta.display_name,
            meta.region,
            "是" if meta.china_ok else "否",
            meta.privacy_level,
            "是" if meta.strict_ok else "否",
        ]
        lines.append("".join(_pad(c, w) for c, w in zip(row, widths)))

    return "\n".join(lines)


if __name__ == "__main__":
    print(format_engine_table())
    print(f"\n全部引擎（{len(all_engine_names())}）: {', '.join(all_engine_names())}")
    print(f"strict 允许（{len(strict_allowed_engines())}）: {', '.join(strict_allowed_engines())}")
    print(f"降级链: {' → '.join(strict_fallback_engines())}")
