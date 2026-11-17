#!/usr/bin/env python3
"""
scripts/public_apis_catalog.py — public-apis 目录解析器（v1.0.0 · P0a）

把 GitHub public-apis 仓库的 README（分类 API 目录）解析为本地 JSON 索引，
供 infoseek 三级路由的「L0 免费优先层」消费：按 分类/关键词/认证方式 检索
免费公开 API，作为 AgentKey（付费网关）与 QVeris（专用路由）的免费降级/长尾补充。

设计对齐 infoseek 架构（M0.2.5 声明式 + 降级链同构）：
  - 本地索引优先（fresh）→ 在线拉取更新（网络抖动自动重试）→ 内嵌最小集兜底（L3）
  - 输出统一 schema：{category, name, description, auth, https, cors, url, source}
  - 目录落盘到 INFOSEEK_DATA_DIR/public_apis_catalog.json（与 state_dir 一致）

CLI 用法:
    python scripts/public_apis_catalog.py --refresh          # 拉取最新 README 重建索引
    python scripts/public_apis_catalog.py --stats            # 索引统计
    python scripts/public_apis_catalog.py --search 汇率      # 关键词检索
    python scripts/public_apis_catalog.py --category Finance # 按分类列举

Python API:
    from public_apis_catalog import load_catalog, search_free_api, get_categories
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

# ── 常量 ──
README_URL = "https://raw.githubusercontent.com/public-apis/public-apis/master/README.md"
_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
_TIMEOUT = 45
_RETRY = 3
_RETRY_SLEEP = 3.0

# ── 分类别名表（英文分类 → 中文语义标签，供关键词检索跨语言命中）──
_CATEGORY_ALIASES: Dict[str, List[str]] = {
    "Finance": ["金融", "股票", "汇率", "财经", "行情"],
    "Cryptocurrency": ["加密", "币圈", "区块链资产", "数字货币", "BTC", "ETH"],
    "Currency Exchange": ["汇率", "外汇", "货币兑换"],
    "Weather": ["天气", "气象", "温度", "预报"],
    "News": ["新闻", "资讯", "头条"],
    "Social": ["社交", "社区", "论坛", "微博"],
    "Geocoding": ["地理", "经纬度", "定位", "地图"],
    "Health": ["健康", "医疗", "疾病"],
    "Food & Drink": ["食品", "餐饮", "食谱", "菜谱"],
    "Books": ["图书", "书籍", "文献"],
    "Dictionaries": ["词典", "字典", "释义", "单词"],
    "Games & Comics": ["游戏", "动漫", "漫画"],
    "Music": ["音乐", "歌曲", "歌词"],
    "Movies": ["电影", "影视", "视频"],
    "Sports": ["体育", "运动", "赛事"],
    "Science & Math": ["科学", "数学", "物理", "化学"],
    "Open Data": ["开放数据", "公共数据", "数据集"],
    "Security": ["安全", "漏洞", "威胁"],
    "Machine Learning": ["机器学习", "AI", "人工智能", "模型"],
    "Data Validation": ["校验", "验证", "身份证", "手机号"],
    "Business": ["商业", "企业", "公司", "工商"],
    "Jobs": ["招聘", "职位", "求职"],
    "Travel": ["旅行", "旅游", "机票", "酒店"],
    "Transportation": ["交通", "运输", "航班", "物流"],
    "Animals": ["动物", "宠物", "猫", "狗"],
    "Entertainment": ["娱乐", "影音"],
    "Environment": ["环境", "环保", "污染"],
    "Events": ["活动", "事件", "日历"],
    "Email": ["邮件", "邮箱", "email"],
    "Cloud Storage & File Sharing": ["云存储", "网盘", "文件"],
    "Photography": ["摄影", "图片", "照片"],
    "Video": ["视频", "影片"],
    "Text Analysis": ["文本", "分析", "NLP", "语义"],
    "Anti-Malware": ["恶意软件", "杀毒", "病毒"],
    "Art & Design": ["艺术", "设计", "素材"],
    "Authentication & Authorization": ["认证", "授权", "登录"],
    "Blockchain": ["区块链", "链上", "合约"],
    "Calendar": ["日历", "节假日"],
    "Continuous Integration": ["CI", "集成", "构建"],
    "Development": ["开发", "编程", "代码", "Dev"],
    "Documents & Productivity": ["文档", "办公", "效率"],
    "Personality": ["性格", "人格", "心理"],
    "Programming": ["编程", "程序"],
    "Search": ["搜索", "检索"],
    "Shopping": ["购物", "电商", "商品"],
    "Telephony": ["电话", "通讯", "短信"],
    "Government": ["政府", "政务", "公共"],
    "Patent": ["专利", "知识产权"],
}

# ── 内嵌最小集兜底（README 拉取失败 / 索引缺失时保证路由不塌）──
_BUILTIN_MINIMAL: List[Dict] = [
    {"category": "Finance", "name": "Fixer", "description": "外汇汇率（当前与历史）",
     "auth": "apiKey", "https": "Yes", "cors": "No", "url": "https://fixer.io/", "source": "builtin"},
    {"category": "Finance", "name": "Marketstack", "description": "全球股票市场数据",
     "auth": "apiKey", "https": "Yes", "cors": "Unknown", "url": "https://marketstack.com/", "source": "builtin"},
    {"category": "Currency Exchange", "name": "Currency-api", "description": "免费汇率 150+ 币种无限额",
     "auth": "No", "https": "Yes", "cors": "Yes", "url": "https://github.com/fawazahmed0/currency-api", "source": "builtin"},
    {"category": "Weather", "name": "Open-Meteo", "description": "免费天气预报与历史气象数据（无需 key）",
     "auth": "No", "https": "Yes", "cors": "Yes", "url": "https://open-meteo.com/", "source": "builtin"},
    {"category": "Geocoding", "name": "Open-Meteo Geocoding", "description": "免费地理编码（城市→经纬度）",
     "auth": "No", "https": "Yes", "cors": "Yes", "url": "https://open-meteo.com/", "source": "builtin"},
    {"category": "Cryptocurrency", "name": "CoinGecko", "description": "加密市场数据（价格/市值/涨跌）",
     "auth": "apiKey", "https": "Yes", "cors": "Yes", "url": "https://www.coingecko.com/", "source": "builtin"},
    {"category": "Social", "name": "Hacker News", "description": "Hacker News 文章与评论（免费无 key）",
     "auth": "No", "https": "Yes", "cors": "Yes", "url": "https://github.com/HackerNews/API", "source": "builtin"},
    {"category": "News", "name": "Spaceflight News", "description": "航天新闻 API（免费无 key）",
     "auth": "No", "https": "Yes", "cors": "Yes", "url": "https://spaceflightnewsapi.net/", "source": "builtin"},
    {"category": "Data Validation", "name": "abstractapi Validation", "description": "邮箱/手机号/身份证校验",
     "auth": "apiKey", "https": "Yes", "cors": "Yes", "url": "https://abstractapi.com/", "source": "builtin"},
    {"category": "Dictionaries", "name": "Free Dictionary", "description": "英文单词释义 API",
     "auth": "No", "https": "Yes", "cors": "Unknown", "url": "https://dictionaryapi.dev/", "source": "builtin"},
]


# ═══════════════════════════════════════════════════════════════
# 数据目录（对齐 state_dir）
# ═══════════════════════════════════════════════════════════════

def _data_dir() -> Path:
    env = os.environ.get("INFOSEEK_DATA_DIR")
    if env:
        p = Path(env)
    else:
        db = os.environ.get("INFOSEEK_DB")
        p = Path(db).parent if db else (Path.home() / ".infoseek")
    p.mkdir(parents=True, exist_ok=True)
    return p


def catalog_path() -> Path:
    return _data_dir() / "public_apis_catalog.json"


# ═══════════════════════════════════════════════════════════════
# README 解析
# ═══════════════════════════════════════════════════════════════

_TABLE_ROW = re.compile(r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*(.*?)\s*\|\s*`?([^`|]*)`?\s*\|\s*([^|]*)\s*\|\s*([^|]*)\s*\|")
# 兼容无链接格式（纯文本 API 名）
_TABLE_ROW_PLAIN = re.compile(r"^\|\s*([^|\[]+?)\s*\|\s*(.*?)\s*\|\s*`?([^`|]*)`?\s*\|\s*([^|]*)\s*\|\s*([^|]*)\s*\|")


def _parse_readme(text: str) -> List[Dict]:
    """解析 README：### 分类标题 + | API | Description | Auth | HTTPS | CORS | 表格行。"""
    entries: List[Dict] = []
    current_cat = "Uncategorized"
    for line in text.split("\n"):
        line = line.strip()
        m_cat = re.match(r"^###\s+(.+)$", line)
        if m_cat:
            current_cat = m_cat.group(1).strip()
            continue
        if not line.startswith("|"):
            continue
        m = _TABLE_ROW.match(line)
        if m:
            name, url, desc, auth, https, cors = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6)
        else:
            m2 = _TABLE_ROW_PLAIN.match(line)
            if not m2:
                continue
            name, desc, auth, https, cors = m2.group(1), m2.group(2), m2.group(3), m2.group(4), m2.group(5)
            url = ""
        # 清洗
        name = name.strip().strip("`").strip()
        desc = desc.strip().strip("`").strip()
        auth = auth.strip().strip("`").strip() or "No"
        https = https.strip().strip("`").strip() or "Unknown"
        cors = cors.strip().strip("`").strip() or "Unknown"
        if not name or name in ("API", "Description", "Auth", "HTTPS", "CORS") or name.startswith(":---"):
            continue
        entries.append({
            "category": current_cat,
            "name": name,
            "description": desc,
            "auth": auth,
            "https": https,
            "cors": cors,
            "url": url,
            "source": "public-apis",
        })
    return entries


def _fetch_readme() -> str:
    """拉取 README（重试 + 退避）。失败抛异常由调用方降级。"""
    last_err: Optional[Exception] = None
    for attempt in range(_RETRY):
        try:
            req = urllib.request.Request(README_URL, headers={"User-Agent": _UA})
            with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
                return resp.read().decode("utf-8", errors="ignore")
        except Exception as e:
            last_err = e
            if attempt < _RETRY - 1:
                time.sleep(_RETRY_SLEEP)
    raise RuntimeError(f"README 拉取失败: {last_err}")


# ═══════════════════════════════════════════════════════════════
# 索引读写
# ═══════════════════════════════════════════════════════════════

def _index_payload(entries: List[Dict]) -> Dict:
    return {
        "version": "1.0.0",
        "source": "public-apis/public-apis",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "entry_count": len(entries),
        "entries": entries,
    }


def build_index(refresh: bool = False) -> Dict:
    """构建/刷新索引。refresh=False 时优先读本地（fresh 优先）；无本地则拉取；全失败回退内嵌最小集。"""
    path = catalog_path()
    if not refresh and path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("entries"):
                return data
        except Exception:
            pass
    try:
        text = _fetch_readme()
        entries = _parse_readme(text)
        if not entries:
            raise RuntimeError("README 解析 0 条")
        data = _index_payload(entries)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data
    except Exception as e:
        # L3 降级：内嵌最小集（不落盘，仅内存）
        return _index_payload(_BUILTIN_MINIMAL) | {"degraded": True, "degrade_reason": str(e)}


def load_catalog() -> Dict:
    """加载索引（fresh 优先，本地缺失才触发网络）。"""
    return build_index(refresh=False)


# ═══════════════════════════════════════════════════════════════
# 检索 API
# ═══════════════════════════════════════════════════════════════

def _alias_hits(category: str, keyword: str) -> bool:
    """分类别名命中（英文分类 ↔ 中文关键词）。"""
    aliases = _CATEGORY_ALIASES.get(category, [])
    kw = keyword.lower()
    return any(a.lower() in kw or kw in a.lower() for a in aliases)


def search_free_api(keyword: str = "", category: str = "", limit: int = 10,
                    auth_filter: Optional[str] = None) -> List[Dict]:
    """按关键词/分类检索免费 API。

    参数:
        keyword:     关键词（匹配 名称+描述+分类别名）
        category:    精确分类名（如 "Finance"）
        auth_filter: "No" 仅无 key；"apiKey" 仅需 key；None 不限
        limit:       返回上限
    """
    data = load_catalog()
    entries: List[Dict] = data.get("entries", [])
    kw = keyword.strip().lower()
    out = []
    for e in entries:
        if category and e["category"] != category:
            continue
        if auth_filter and e["auth"] != auth_filter:
            continue
        if kw:
            hay = f"{e['name']} {e['description']} {e['category']}".lower()
            hit = kw in hay or _alias_hits(e["category"], keyword.strip())
            if not hit:
                continue
        out.append(e)
        if len(out) >= limit:
            break
    return out


def get_categories() -> List[str]:
    data = load_catalog()
    seen: List[str] = []
    for e in data.get("entries", []):
        if e["category"] not in seen:
            seen.append(e["category"])
    return seen


def get_stats() -> Dict:
    data = load_catalog()
    entries = data.get("entries", [])
    by_cat: Dict[str, int] = {}
    no_auth = 0
    for e in entries:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + 1
        if e["auth"] == "No":
            no_auth += 1
    return {
        "total": len(entries),
        "categories": len(by_cat),
        "no_auth": no_auth,
        "top_categories": sorted(by_cat.items(), key=lambda x: -x[1])[:10],
        "degraded": data.get("degraded", False),
        "generated_at": data.get("generated_at", ""),
    }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="public-apis 目录解析器")
    ap.add_argument("--refresh", action="store_true", help="强制拉取最新 README 重建索引")
    ap.add_argument("--stats", action="store_true", help="索引统计")
    ap.add_argument("--search", metavar="KW", help="关键词检索")
    ap.add_argument("--category", metavar="CAT", help="按分类列举")
    ap.add_argument("--no-auth", action="store_true", help="仅显示无 key API")
    ap.add_argument("--limit", type=int, default=10, help="返回条数上限")
    args = ap.parse_args()

    if args.stats:
        s = get_stats()
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return 0
    if args.search or args.category:
        results = search_free_api(
            keyword=args.search or "",
            category=args.category or "",
            limit=args.limit,
            auth_filter="No" if args.no_auth else None,
        )
        print(f"命中 {len(results)} 条:")
        for e in results:
            print(f"  [{e['category']}] {e['name']} | auth={e['auth']} | https={e['https']} | {e['description'][:60]}")
        return 0
    # 默认：刷新并输出统计
    data = build_index(refresh=args.refresh)
    s = get_stats()
    print(f"索引 {'已刷新' if args.refresh else '已加载'}: 共 {s['total']} 条 / {s['categories']} 分类 / 无key {s['no_auth']} 条"
          + ("（降级内置集）" if s["degraded"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
