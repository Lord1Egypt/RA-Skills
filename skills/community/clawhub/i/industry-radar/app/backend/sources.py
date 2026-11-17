"""
默认信息源目录（免费公开 RSS）。

说明
----
1. 所有源均为公开 RSS，零成本、无需 API Key，符合"免费公开源起步"的定位。
2. 采集器对每个源做异常隔离：单个源失败不影响整体流程（多源冗余）。
3. `enabled=False` 的源为探测时不可达 / 长期无条目（如知乎、虎嗅、机器之心），
   保留在目录中以便网络恢复后一键启用，但默认不参与采集。
4. 网络受限环境可只保留可达源；也可在 Web 控制台为订阅自定义来源。

探测结论（2026-10，本机实测）：
    可达且有条目：36氪(30) IT之家(60) 少数派(10) 开源中国(50) 雷锋网(20)
                  InfoQ中文(20) 钛媒体(17) Solidot(18) TechCrunch(20)
                  The Verge(10) Ars Technica(20)
    不可达/无条目：知乎RSS(0) 虎嗅(超时) 机器之心(0) cnBeta(0)

每条源包含：id / name / url / lang / category / enabled
"""
from __future__ import annotations

from typing import Dict, List

# category: tech(科技) / business(商业) / finance(财经) / research(学术)
DEFAULT_SOURCES: List[Dict] = [
    # ---------------- 中文源 ----------------
    {
        "id": "36kr",
        "name": "36氪",
        "url": "https://www.36kr.com/feed",
        "home": "https://36kr.com",
        "lang": "zh",
        "category": "business",
        "enabled": True,
    },
    {
        "id": "ithome",
        "name": "IT之家",
        "url": "https://www.ithome.com/rss/",
        "home": "https://www.ithome.com",
        "lang": "zh",
        "category": "tech",
        "enabled": True,
    },
    {
        "id": "tmtpost",
        "name": "钛媒体",
        "url": "https://www.tmtpost.com/rss.xml",
        "home": "https://www.tmtpost.com",
        "lang": "zh",
        "category": "business",
        "enabled": True,
    },
    {
        "id": "leiphone",
        "name": "雷锋网",
        "url": "https://www.leiphone.com/feed",
        "home": "https://www.leiphone.com",
        "lang": "zh",
        "category": "tech",
        "enabled": True,
    },
    {
        "id": "infoq_cn",
        "name": "InfoQ 中文",
        "url": "https://www.infoq.cn/feed",
        "home": "https://www.infoq.cn",
        "lang": "zh",
        "category": "tech",
        "enabled": True,
    },
    {
        "id": "sspai",
        "name": "少数派",
        "url": "https://sspai.com/feed",
        "home": "https://sspai.com",
        "lang": "zh",
        "category": "tech",
        "enabled": True,
    },
    {
        "id": "oschina",
        "name": "开源中国",
        "url": "https://www.oschina.net/news/rss",
        "home": "https://www.oschina.net",
        "lang": "zh",
        "category": "tech",
        "enabled": True,
    },
    {
        "id": "solidot",
        "name": "Solidot 奇客",
        "url": "https://www.solidot.org/index.rss",
        "home": "https://www.solidot.org",
        "lang": "zh",
        "category": "tech",
        "enabled": True,
    },
    # ---------------- 英文源（科技前沿补充）----------------
    {
        "id": "techcrunch",
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "home": "https://techcrunch.com",
        "lang": "en",
        "category": "tech",
        "enabled": True,
    },
    {
        "id": "verge",
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "home": "https://www.theverge.com",
        "lang": "en",
        "category": "tech",
        "enabled": True,
    },
    {
        "id": "ars",
        "name": "Ars Technica",
        "url": "https://feeds.arstechnica.com/arstechnica/index",
        "home": "https://arstechnica.com",
        "lang": "en",
        "category": "tech",
        "enabled": True,
    },
    # ------------- 探测不可达 / 无条目（保留，默认关闭）-------------
    {
        "id": "zhihu_daily",
        "name": "知乎每日精选",
        "url": "https://www.zhihu.com/rss",
        "home": "https://www.zhihu.com",
        "lang": "zh",
        "category": "tech",
        "enabled": False,
    },
    {
        "id": "huxiu",
        "name": "虎嗅",
        "url": "https://www.huxiu.com/rss/0.xml",
        "home": "https://www.huxiu.com",
        "lang": "zh",
        "category": "business",
        "enabled": False,
    },
    {
        "id": "jiqizhixin",
        "name": "机器之心",
        "url": "https://www.jiqizhixin.com/rss",
        "home": "https://www.jiqizhixin.com",
        "lang": "zh",
        "category": "research",
        "enabled": False,
    },
]

_BY_ID: Dict[str, Dict] = {s["id"]: s for s in DEFAULT_SOURCES}


def default_sources() -> List[Dict]:
    """返回默认源（深拷贝，避免调用方修改全局）。"""
    return [dict(s) for s in DEFAULT_SOURCES]


def enabled_source_ids() -> List[str]:
    """默认启用的源 id 列表（用于新建订阅时的预勾选）。"""
    return [s["id"] for s in DEFAULT_SOURCES if s.get("enabled")]


def get_source(source_id: str) -> Dict | None:
    """按 id 查询源元信息。"""
    s = _BY_ID.get(source_id)
    return dict(s) if s else None


def all_source_meta() -> List[Dict]:
    """给前端展示用的来源目录。"""
    return [dict(s) for s in DEFAULT_SOURCES]