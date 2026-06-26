#!/usr/bin/env python3
"""
Minecraft Java Mod 多平台搜索脚本 v2.0
- Modrinth (主平台，国内可直连)
- CurseForge (备选，需 API Key；无 Key 时提示用户)
- MC百科 mcmod.cn (补充搜索，当 Modrinth 结果 < 3 个时启用)
- 快查表优先匹配 (references/mod_quickref.md)

新特性：
  - asyncio + aiohttp 并发请求，显著提速
  - 多关键词并行搜索（3-5 个候选词同时发起）
  - 快查表优先命中，无需 API 调用
  - 默认不查依赖（用 --deps 参数开启）
  - CurseForge API Key 为空时提示用户填写位置
  - 所有网络请求统一设置超时时间，避免卡死
"""

# ─────────────────────────────────────────────────────────────────────────────
# 编码 & 标准库 import（顶部 io 修复 Windows GBK）
# ─────────────────────────────────────────────────────────────────────────────
import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import argparse
import asyncio
import json
import math
import os
import re
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# aiohttp（可选，有则用；无则 fallback 到 urllib 同步）
# ─────────────────────────────────────────────────────────────────────────────
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False
    import urllib.request
    import urllib.parse
    import urllib.error

# ─────────────────────────────────────────────────────────────────────────────
# 路径常量
# ─────────────────────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).parent
_REPO_ROOT = _SCRIPT_DIR.parent
_QUICKREF_PATH = _REPO_ROOT / "references" / "mod_quickref.md"
_CF_CONFIG_PATH = _REPO_ROOT / "references" / "curseforge_api.md"

# ─────────────────────────────────────────────────────────────────────────────
# API 常量
# ─────────────────────────────────────────────────────────────────────────────
MODRINTH_BASE = "https://api.modrinth.com/v2"
CURSEFORGE_BASE = "https://api.curseforge.com/v1"
MCMOD_SEARCH_URL = "https://www.mcmod.cn/s?key={query}&mold=1&version={version}"
MCMOD_SEARCH_URL_NOVER = "https://www.mcmod.cn/s?key={query}&mold=1"

DEFAULT_TIMEOUT = 8        # 秒，单个请求超时
MULTI_SEARCH_TIMEOUT = 12  # 秒，多关键词并发总超时
MAX_RESULTS_PER_PLATFORM = 20

SORT_SCORE_WEIGHTS = {
    "downloads": 0.30,
    "update_frequency": 0.25,
    "rating": 0.25,
    "version_match": 0.20,
}

# ─────────────────────────────────────────────────────────────────────────────
# TACZ 枪械生态常量
# ─────────────────────────────────────────────────────────────────────────────
TACZ_MOD_SLUG = "timeless-and-classics-zero"
TACZ_MOD_NAME = "Timeless and Classics Zero (TaCZ)"
TACZ_MODRINTH_URL = f"https://modrinth.com/mod/{TACZ_MOD_SLUG}"

TACZ_GUN_KEYWORDS = {
    "枪", "枪械", "枪包", "枪mod", "枪模组", "射击", "武器", "手枪", "步枪",
    "狙击", "霰弹", "冲锋枪", "机枪", "左轮", "燧发枪", "火枪", "枪战",
    "现代战争", "军事", "弹药", "子弹",
    "gun", "firearm", "weapon", "pistol", "rifle", "sniper", "shotgun",
    "smg", "submachine", "lmg", "machine gun", "revolver", "musket",
    "gunpack", "gun pack", "tacz", "tac", "bullet", "ammo", "ammunition",
    "fps", "combat", "warfare", "military",
}

TACZ_GUNPACK_CATEGORIES = {"equipment", "adventure", "game-mechanics"}

TACZ_SUPPORTED_VERSIONS = {
    "1.18.2", "1.19", "1.19.1", "1.19.2", "1.20", "1.20.1",
}

# ─────────────────────────────────────────────────────────────────────────────
# Create 机械动力生态常量
# ─────────────────────────────────────────────────────────────────────────────
CREATE_MOD_SLUG = "create"
CREATE_MOD_NAME = "Create (机械动力)"
CREATE_MODRINTH_URL = "https://modrinth.com/mod/create"

CREATE_KEYWORDS = {
    "机械", "机械动力", "自动化", "传送带", "齿轮", "活塞", "动力",
    "轴承", "铁路", "火车", "矿车", "旋转", "应力", "流水线",
    "工厂", "制造", "加工", "搅拌", "碾压", "装配", "压缩",
    "机械臂", "部署器", "红石机械", "蒸汽", "风车", "水车",
    "create mod", "create addon", "create ",
    "conveyor", "belt", "gear", "pulley", "bearing", "piston",
    "automation", "factory", "assembly", "mechanical",
    "train", "railway", "steam", "windmill", "waterwheel",
    "rotational", "kinetic", "stress", "cogwheel", "shaft",
    "deployer", "mixer", "press", "millstone", "crusher",
}

CREATE_ADDON_CATEGORIES = {"technology", "equipment", "transportation", "utility"}

CREATE_SUPPORTED_VERSIONS = {
    "1.14.4", "1.15.2", "1.16.5", "1.18.2", "1.19.2", "1.20.1",
}

# ─────────────────────────────────────────────────────────────────────────────
# 数据模型
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class ModDependency:
    name: str
    slug: str
    required: bool
    downloads: int = 0
    url: str = ""


@dataclass
class ModResult:
    name: str
    slug: str
    author: str
    description: str
    downloads: int
    categories: list
    game_versions: list
    loaders: list
    favorites: int = 0
    latest_version: str = ""
    published: str = ""
    updated: str = ""
    icon_url: str = ""
    modrinth_url: str = ""
    curseforge_url: str = ""
    curseforge_id: int = 0
    dependencies: list = field(default_factory=list)
    score: float = 0.0
    warnings: list = field(default_factory=list)
    platform: str = ""
    source: str = ""   # "quickref" | "modrinth" | "curseforge" | "mcmod"

    def __post_init__(self):
        if isinstance(self.game_versions, str):
            self.game_versions = [self.game_versions]
        if isinstance(self.loaders, str):
            self.loaders = [self.loaders]


# ─────────────────────────────────────────────────────────────────────────────
# 快查表解析器
# ─────────────────────────────────────────────────────────────────────────────

_quickref_cache: Optional[list] = None


def load_quickref() -> list:
    """加载并解析 mod_quickref.md，返回快查记录列表"""
    global _quickref_cache
    if _quickref_cache is not None:
        return _quickref_cache

    if not _QUICKREF_PATH.exists():
        _quickref_cache = []
        return _quickref_cache

    records = []
    current_category = ""
    try:
        with open(_QUICKREF_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                # 分类标题
                if line.startswith("## "):
                    current_category = line[3:].strip()
                # mod 条目：- Name | slug: xxx | 描述 | fabric/forge 1.20.1
                elif line.startswith("- ") and "|" in line:
                    parts = [p.strip() for p in line[2:].split("|")]
                    if len(parts) < 2:
                        continue
                    name = parts[0]
                    slug = ""
                    desc = ""
                    loaders_ver = ""
                    for part in parts[1:]:
                        if part.startswith("slug:"):
                            slug = part[5:].strip()
                        elif any(kw in part for kw in ["fabric", "forge", "quilt", "1."]):
                            loaders_ver = part
                        else:
                            desc = part
                    records.append({
                        "name": name,
                        "slug": slug,
                        "desc": desc,
                        "loaders_ver": loaders_ver,
                        "category": current_category,
                        "keywords": f"{name} {slug} {desc} {current_category}".lower(),
                    })
    except Exception as e:
        print(f"[quickref] 读取失败: {e}", file=sys.stderr)

    _quickref_cache = records
    return records


def search_quickref(query: str, version: str = None, limit: int = 5) -> list[ModResult]:
    """在快查表中搜索，返回 ModResult 列表"""
    records = load_quickref()
    if not records:
        return []

    q_lower = query.lower()
    # 提取候选关键词
    keywords = _extract_keywords(query)
    kw_lower = [k.lower() for k in keywords]

    scored = []
    for rec in records:
        kw_text = rec["keywords"]
        score = 0

        # 名称完全匹配
        if rec["name"].lower() in q_lower or q_lower in rec["name"].lower():
            score += 100
        # slug 匹配
        if rec["slug"] and rec["slug"] in q_lower:
            score += 80
        # 关键词命中
        for kw in kw_lower:
            if kw and kw in kw_text:
                score += 30
        # 分类命中
        if rec["category"].lower() in q_lower:
            score += 20
        # 版本过滤（快查表有标注版本时检查）
        if version and rec["loaders_ver"] and version not in rec["loaders_ver"]:
            score = max(0, score - 20)

        if score > 0:
            scored.append((score, rec))

    scored.sort(key=lambda x: -x[0])
    results = []
    for score, rec in scored[:limit]:
        slug = rec["slug"] or rec["name"].lower().replace(" ", "-")
        mr = ModResult(
            name=rec["name"],
            slug=slug,
            author="",
            description=rec["desc"],
            downloads=0,
            categories=[rec["category"]],
            game_versions=[rec["loaders_ver"]] if rec["loaders_ver"] else [],
            loaders=[],
            modrinth_url=f"https://modrinth.com/mod/{slug}" if rec["slug"] else "",
            platform="quickref",
            source="quickref",
            score=float(score),
        )
        results.append(mr)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# 多关键词提取
# ─────────────────────────────────────────────────────────────────────────────

# 中文→英文通用映射（合并 gun + create + 通用 NPC/生存等）
_CN_EN_MAP = {
    # 枪械
    "步枪": "rifle", "狙击": "sniper", "霰弹": "shotgun",
    "手枪": "pistol", "冲锋枪": "smg", "机枪": "machine gun",
    "左轮": "revolver", "燧发枪": "musket", "火枪": "musket",
    "枪": "gun", "枪械": "gun", "枪包": "gun pack",
    "武器": "weapon", "弹药": "ammo", "子弹": "bullet",
    "射击": "shooting", "军事": "military", "战争": "warfare",
    "现代": "modern", "废土": "fallout post-apocalyptic", "末日": "apocalypse",
    "科幻": "scifi", "未来": "futuristic", "西部": "western",
    # Create 机械
    "机械": "mechanical", "机械动力": "create", "自动化": "automation",
    "传送带": "conveyor belt", "齿轮": "gear cogwheel", "活塞": "piston",
    "轴承": "bearing", "铁路": "railway train", "火车": "train",
    "矿车": "minecart", "旋转": "rotational", "应力": "stress",
    "流水线": "assembly line", "工厂": "factory", "制造": "manufacturing",
    "加工": "processing", "搅拌": "mixing", "碾压": "crushing",
    "装配": "assembly", "压缩": "pressing", "机械臂": "deployer",
    "部署器": "deployer", "蒸汽": "steam", "风车": "windmill",
    "水车": "waterwheel", "动力": "kinetic", "科技": "technology",
    # NPC / 生物 / 生存
    "npc": "npc", "村民": "villager", "幸存者": "survivor",
    "中立": "neutral", "生成": "spawn", "自然生成": "naturally spawning",
    "友好": "friendly", "可交互": "interactive", "对话": "dialogue",
    "生物": "mob creature", "怪物": "monster", "动物": "animal",
    "生存": "survival", "冒险": "adventure", "探索": "exploration",
    "地下城": "dungeon", "副本": "dungeon instance", "boss": "boss",
    "魔法": "magic", "巫术": "witchcraft", "附魔": "enchantment",
    "农业": "farming agriculture", "农场": "farm", "食物": "food",
    "建筑": "building construction", "装饰": "decoration",
    "存储": "storage", "物流": "logistics", "运输": "transport",
    "能源": "energy power", "电力": "electricity",
    "太空": "space", "星球": "planet", "飞船": "spaceship",
    "末地": "end dimension", "下界": "nether",
    "铠甲": "armor", "盔甲": "armor", "剑": "sword",
    "工具": "tool", "采矿": "mining",
}


def _extract_keywords(query: str) -> list[str]:
    """
    从查询字符串提取 3-5 个候选搜索词（中英文混合）。
    策略：
      1. 原始查询（如果包含英文）
      2. 中文词逐一翻译为英文
      3. 从映射中挑选最相关的前 3 个
    返回去重后的列表（max 5 个）
    """
    q = query.strip()
    candidates = set()

    # 中文词映射（优先长词）
    q_lower = q.lower()
    translated_parts = []
    for cn, en in sorted(_CN_EN_MAP.items(), key=lambda x: -len(x[0])):
        if cn in q_lower:
            translated_parts.append(en.split()[0])  # 取第一个英文词

    # 如果没有中文词，直接用原始查询
    if not translated_parts:
        candidates.add(q)
    else:
        # 最多选 3 个翻译词加原词
        for part in translated_parts[:3]:
            candidates.add(part)
        # 保留查询中的英文部分
        en_parts = re.sub(r'[\u4e00-\u9fff]+', ' ', q).strip()
        if en_parts:
            candidates.add(en_parts)

    # 去除空串
    result = [c for c in candidates if c and len(c) >= 2]

    # 去重（不区分大小写）
    seen = set()
    unique = []
    for c in result:
        if c.lower() not in seen:
            seen.add(c.lower())
            unique.append(c)

    return unique[:5] if unique else [q]


def translate_query_primary(query: str) -> str:
    """将查询词翻译为主要英文搜索词（第一个候选词）"""
    kws = _extract_keywords(query)
    return kws[0] if kws else query


# ─────────────────────────────────────────────────────────────────────────────
# 异步 HTTP 工具
# ─────────────────────────────────────────────────────────────────────────────

async def async_http_get(
    session: "aiohttp.ClientSession",
    url: str,
    headers: dict = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Optional[dict]:
    """异步 GET 请求，返回 JSON（aiohttp 版）"""
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "MinecraftModSearch/2.0")
    try:
        async with session.get(
            url,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as resp:
            if resp.status != 200:
                print(f"HTTP {resp.status}: {url}", file=sys.stderr)
                return None
            text = await resp.text(encoding="utf-8")
            return json.loads(text)
    except asyncio.TimeoutError:
        print(f"[超时] {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[错误] {e} — {url}", file=sys.stderr)
        return None


async def async_http_get_html(
    session: "aiohttp.ClientSession",
    url: str,
    headers: dict = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Optional[str]:
    """异步 GET 请求，返回 HTML 文本"""
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    try:
        async with session.get(
            url,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as resp:
            if resp.status != 200:
                print(f"HTTP {resp.status}: {url}", file=sys.stderr)
                return None
            return await resp.text(encoding="utf-8", errors="replace")
    except asyncio.TimeoutError:
        print(f"[超时] {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[错误] {e} — {url}", file=sys.stderr)
        return None


# fallback 同步版（仅在无 aiohttp 时使用）
def _sync_http_get(url: str, headers: dict = None, timeout: int = DEFAULT_TIMEOUT) -> Optional[dict]:
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "MinecraftModSearch/2.0")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[错误] {e} — {url}", file=sys.stderr)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Modrinth 搜索（异步，多关键词并行）
# ─────────────────────────────────────────────────────────────────────────────

def _build_modrinth_url(query: str, version: str = None, loader: str = None,
                         category: str = None, limit: int = 20) -> str:
    endpoint = f"{MODRINTH_BASE}/search"
    params = [("query", query), ("limit", str(min(limit, 100))), ("index", "downloads")]
    facets_list = []
    if version:
        facets_list.append([f"versions:{version}"])
    if loader:
        facets_list.append([f"loaders:{loader}"])
    if category:
        facets_list.append([f"categories:{category}"])
    if facets_list:
        params.append(("facets", json.dumps(facets_list)))
    from urllib.parse import quote
    return endpoint + "?" + "&".join(f"{k}={quote(str(v))}" for k, v in params)


async def _search_modrinth_single(
    session: "aiohttp.ClientSession",
    query: str,
    version: str = None,
    loader: str = None,
    category: str = None,
    limit: int = MAX_RESULTS_PER_PLATFORM,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[dict]:
    """单个关键词搜索 Modrinth，返回 hits 列表"""
    url = _build_modrinth_url(query, version, loader, category, limit)
    data = await async_http_get(session, url, timeout=timeout)
    if not data or "hits" not in data:
        return []
    return data.get("hits", [])


async def search_modrinth_multi(
    queries: list[str],
    version: str = None,
    loader: str = None,
    category: str = None,
    limit: int = MAX_RESULTS_PER_PLATFORM,
    timeout: int = MULTI_SEARCH_TIMEOUT,
) -> list[ModResult]:
    """
    并行用多个关键词搜索 Modrinth，合并去重后返回 ModResult 列表。
    默认不查依赖（提速）。
    """
    async with aiohttp.ClientSession() as session:
        tasks = [
            _search_modrinth_single(session, q, version, loader, category, limit, DEFAULT_TIMEOUT)
            for q in queries
        ]
        # 设置总超时
        try:
            all_hits_list = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            print(f"[Modrinth] 并发搜索超时（{timeout}s）", file=sys.stderr)
            all_hits_list = []

    seen_slugs: set = set()
    mods: list[ModResult] = []

    for result in all_hits_list:
        if isinstance(result, Exception) or not result:
            continue
        for hit in result:
            slug = hit.get("slug", "").lower()
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            mod = _hit_to_modresult(hit, version)
            mods.append(mod)

    print(f"  [Modrinth] 多关键词({len(queries)}) 合并 {len(mods)} 条结果", file=sys.stderr)
    return mods


def _hit_to_modresult(hit: dict, version: str = None) -> ModResult:
    """将 Modrinth API hit 转为 ModResult"""
    updated_date = hit.get("date_modified", "")
    warnings = _check_warnings_hit(hit, version)
    return ModResult(
        name=hit.get("title", ""),
        slug=hit.get("slug", "").lower(),
        author=hit.get("author", ""),
        description=hit.get("description", ""),
        downloads=hit.get("downloads", 0),
        favorites=0,
        categories=hit.get("categories", []),
        game_versions=[hit.get("latest_version", "")],
        loaders=hit.get("loaders", []) or [],
        latest_version=hit.get("latest_version", ""),
        published=hit.get("date_created", "")[:10] if hit.get("date_created") else "",
        updated=updated_date[:10] if updated_date else "",
        icon_url=hit.get("icon_url", ""),
        modrinth_url=f"https://modrinth.com/mod/{hit.get('slug', '')}",
        warnings=warnings,
        platform="modrinth",
        source="modrinth",
    )


def _check_warnings_hit(hit: dict, version: str = None) -> list[str]:
    warnings = []
    updated_date = hit.get("date_modified", "")
    if updated_date:
        try:
            update_time = datetime.fromisoformat(updated_date.replace("Z", "+00:00"))
            days_since = (datetime.now(update_time.tzinfo) - update_time).days
            if days_since > 365:
                warnings.append("久未更新")
            elif days_since > 180:
                warnings.append("更新较久")
        except Exception:
            pass
    return warnings


# ─────────────────────────────────────────────────────────────────────────────
# 依赖查询（按需，异步）
# ─────────────────────────────────────────────────────────────────────────────

async def fetch_modrinth_dependencies_async(
    session: "aiohttp.ClientSession",
    project_id: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[ModDependency]:
    """异步获取 Modrinth Mod 的依赖列表"""
    if not project_id:
        return []
    url = f"{MODRINTH_BASE}/project/{project_id}/dependencies"
    data = await async_http_get(session, url, timeout=timeout)
    if not data:
        return []

    if isinstance(data, dict):
        projects = data.get("projects", [])
        return [
            ModDependency(
                name=p.get("title", ""),
                slug=p.get("slug", ""),
                required=True,
                downloads=p.get("downloads", 0),
                url=f"https://modrinth.com/mod/{p.get('slug', '')}",
            )
            for p in projects if isinstance(p, dict)
        ]

    deps = []
    for item in data:
        if not isinstance(item, dict):
            continue
        proj = item.get("project")
        if not proj or not isinstance(proj, dict):
            continue
        dep_type = item.get("dependency_type", "optional")
        deps.append(ModDependency(
            name=proj.get("title", ""),
            slug=proj.get("slug", ""),
            required=(dep_type == "required"),
            downloads=proj.get("downloads", 0),
            url=f"https://modrinth.com/mod/{proj.get('slug', '')}",
        ))
    return deps


async def add_dependencies_async(mods: list[ModResult], timeout: int = DEFAULT_TIMEOUT) -> list[ModResult]:
    """并发补充所有 mod 的依赖信息"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for mod in mods:
            if mod.platform == "modrinth" and not mod.dependencies:
                tasks.append(fetch_modrinth_dependencies_async(session, mod.slug, timeout))
            else:
                tasks.append(asyncio.coroutine(lambda: [])())

        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=timeout * 2
            )
        except asyncio.TimeoutError:
            print("[依赖] 并发依赖查询超时", file=sys.stderr)
            return mods

        for mod, deps in zip(mods, results):
            if isinstance(deps, list):
                mod.dependencies = deps

    return mods


# ─────────────────────────────────────────────────────────────────────────────
# CurseForge 搜索（带 API Key 提示）
# ─────────────────────────────────────────────────────────────────────────────

_CF_API_MISSING_WARNED = False


def check_curseforge_api_key(api_key: str) -> tuple[bool, str]:
    """
    检查 CurseForge API Key 是否有效。
    返回 (has_key: bool, message: str)
    """
    if api_key and api_key.strip() and not api_key.startswith("<"):
        return True, ""

    msg = (
        "\n⚠️  【CurseForge API Key 未配置】\n"
        "   当前未设置 CurseForge API Key，已跳过 CurseForge 平台搜索。\n"
        "   如需启用 CurseForge 搜索，请：\n"
        "   1. 前往 https://console.curseforge.com/ 申请免费 API Key\n"
        f"  2. 编辑文件: {_CF_CONFIG_PATH}\n"
        "      在文件末尾添加: CF_API_KEY=你的key\n"
        "   3. 或通过 --api-key 参数传入: --api-key 你的key\n"
        "   4. 或设置环境变量: export CF_API_KEY=你的key\n"
    )
    return False, msg


async def search_curseforge_async(
    session: "aiohttp.ClientSession",
    query: str,
    version: str = None,
    loader: str = None,
    api_key: str = None,
    limit: int = MAX_RESULTS_PER_PLATFORM,
    timeout: int = 5,
) -> list[ModResult]:
    """异步搜索 CurseForge"""
    if not api_key or not api_key.strip():
        return []

    loader_map = {"forge": 2, "fabric": 4, "liteloader": 3, "rift": 5}
    mod_loader = loader_map.get(loader) if loader else None

    from urllib.parse import quote
    endpoint = f"{CURSEFORGE_BASE}/games/432/mods/search"
    params = [
        ("gameId", "432"),
        ("searchFilter", query),
        ("sortField", "1"),
        ("sortOrder", "desc"),
        ("pageSize", str(min(limit, 50))),
        ("classId", "6"),
    ]
    if version:
        params.append(("gameVersion", version))
    if mod_loader:
        params.append(("modLoaderType", str(mod_loader)))

    url = endpoint + "?" + "&".join(f"{k}={quote(str(v))}" for k, v in params)
    headers = {"X-API-Key": api_key}

    data = await async_http_get(session, url, headers=headers, timeout=timeout)
    if not data or "data" not in data:
        return []

    mods = []
    for item in data.get("data", []):
        warnings = []
        date_modified = item.get("dateModified", "")
        if date_modified:
            try:
                dt = datetime.fromisoformat(date_modified.replace("Z", "+00:00"))
                days_since = (datetime.now(dt.tzinfo) - dt).days
                if days_since > 365:
                    warnings.append("久未更新")
                elif days_since > 180:
                    warnings.append("更新较久")
            except Exception:
                pass

        latest_file = item.get("latestFiles", [{}])[0] if item.get("latestFiles") else {}
        game_versions = latest_file.get("gameVersions", []) if latest_file else []

        mod = ModResult(
            name=item.get("name", ""),
            slug=item.get("slug", ""),
            author=item.get("authors", [{}])[0].get("name", "") if item.get("authors") else "",
            description=item.get("summary", ""),
            downloads=item.get("downloadCount", 0),
            favorites=0,
            categories=[c.get("name", "") for c in item.get("categories", [])],
            game_versions=game_versions,
            loaders=[loader] if loader else [],
            latest_version=latest_file.get("version", "") if latest_file else "",
            published=item.get("dateCreated", "")[:10] if item.get("dateCreated") else "",
            updated=date_modified[:10] if date_modified else "",
            icon_url=item.get("logo", {}).get("url", "") if item.get("logo") else "",
            curseforge_url=item.get("externalUrl", "") or f"https://www.curseforge.com/minecraft/mc-mods/{item.get('slug', '')}",
            curseforge_id=item.get("id", 0),
            warnings=warnings,
            platform="curseforge",
            source="curseforge",
        )
        mods.append(mod)

    return mods


# ─────────────────────────────────────────────────────────────────────────────
# MC百科补充搜索（当 Modrinth 结果 < 3 时触发）
# ─────────────────────────────────────────────────────────────────────────────

def _parse_mcmod_results(html: str) -> list[ModResult]:
    """
    解析 MC百科搜索页 HTML，提取 mod 条目。
    MC百科搜索结果页的 mod 卡片格式：
      <div class="col-lg-...">
        <a href="/class/xxxx.html">
          <span class="name">ModName</span>
          <span class="desc">描述</span>
        </a>
      </div>
    """
    results = []
    if not html:
        return results

    try:
        # 提取搜索结果中的 mod 卡片
        # MC百科搜索结果中 mod 信息在 .result-item 或类似结构
        # 尝试多种模式
        pattern_name = re.compile(
            r'href="(/class/\d+\.html)"[^>]*>.*?<span[^>]*class="[^"]*name[^"]*"[^>]*>([^<]+)</span>',
            re.DOTALL
        )
        pattern_title = re.compile(
            r'href="(/class/\d+\.html)"[^>]*title="([^"]+)"'
        )
        pattern_item = re.compile(
            r'<a[^>]+href="(/class/(\d+)\.html)"[^>]*>.*?<p[^>]*class="[^"]*name[^"]*"[^>]*>(.*?)</p>.*?<p[^>]*class="[^"]*desc[^"]*"[^>]*>(.*?)</p>',
            re.DOTALL
        )

        # 尝试解析新版 MC百科
        items = pattern_item.findall(html)
        seen_ids = set()

        for match in items[:10]:
            path, mod_id, name_raw, desc_raw = match
            if mod_id in seen_ids:
                continue
            seen_ids.add(mod_id)
            name = re.sub(r'<[^>]+>', '', name_raw).strip()
            desc = re.sub(r'<[^>]+>', '', desc_raw).strip()
            if not name:
                continue
            mod = ModResult(
                name=name,
                slug=f"mcmod-{mod_id}",
                author="",
                description=desc,
                downloads=0,
                categories=["mc百科"],
                game_versions=[],
                loaders=[],
                modrinth_url="",
                curseforge_url=f"https://www.mcmod.cn{path}",
                platform="mcmod",
                source="mcmod",
                score=10.0,
            )
            results.append(mod)

        # 如果上面没找到，尝试简单提取标题
        if not results:
            title_matches = pattern_title.findall(html)
            for path, title in title_matches[:5]:
                mod_id = re.search(r'/class/(\d+)', path)
                mid = mod_id.group(1) if mod_id else path
                if mid in seen_ids:
                    continue
                seen_ids.add(mid)
                mod = ModResult(
                    name=title,
                    slug=f"mcmod-{mid}",
                    author="",
                    description="",
                    downloads=0,
                    categories=["mc百科"],
                    game_versions=[],
                    loaders=[],
                    modrinth_url="",
                    curseforge_url=f"https://www.mcmod.cn{path}",
                    platform="mcmod",
                    source="mcmod",
                    score=10.0,
                )
                results.append(mod)

    except Exception as e:
        print(f"[MC百科] 解析失败: {e}", file=sys.stderr)

    return results


async def search_mcmod_async(
    session: "aiohttp.ClientSession",
    query: str,
    version: str = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[ModResult]:
    """
    抓取 MC百科搜索页补充结果。
    仅在 Modrinth 结果 < 3 个时调用。
    """
    from urllib.parse import quote
    # 优先使用中文查询词（MC百科是中文数据库）
    q_encoded = quote(query)

    if version:
        url = MCMOD_SEARCH_URL.format(query=q_encoded, version=version)
    else:
        url = MCMOD_SEARCH_URL_NOVER.format(query=q_encoded)

    print(f"  [MC百科] Modrinth 结果不足，补充搜索: {url}", file=sys.stderr)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.mcmod.cn/",
    }

    html = await async_http_get_html(session, url, headers=headers, timeout=timeout)
    if not html:
        print("  [MC百科] 请求失败或超时", file=sys.stderr)
        return []

    results = _parse_mcmod_results(html)
    print(f"  [MC百科] 解析到 {len(results)} 条结果", file=sys.stderr)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# TACZ 枪械意图 & 搜索
# ─────────────────────────────────────────────────────────────────────────────

def detect_gun_intent(query: str) -> bool:
    q_lower = query.lower()
    return any(kw in q_lower for kw in TACZ_GUN_KEYWORDS)


async def search_tacz_gunpacks_async(
    query: str,
    version: str = None,
    limit: int = 10,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[bool, list]:
    keywords = _extract_keywords(query)
    # 为每个关键词构建 "tacz <kw>" 的搜索
    tacz_queries = [f"tacz {kw}" for kw in keywords[:3]]

    async with aiohttp.ClientSession() as session:
        # 策略1：equipment 分类
        tasks_s1 = []
        for q in tacz_queries:
            facets = [["categories:equipment"]]
            if version:
                facets.append([f"versions:{version}"])
            url = _build_modrinth_url(q, version=None, limit=20)
            # 重新构建带 facets 的 URL
            from urllib.parse import quote as uq
            params = [("query", q), ("limit", "20"), ("index", "downloads"),
                      ("facets", json.dumps(facets))]
            url = f"{MODRINTH_BASE}/search?" + "&".join(f"{k}={uq(str(v))}" for k, v in params)
            tasks_s1.append(async_http_get(session, url, timeout=DEFAULT_TIMEOUT))

        try:
            results_s1 = await asyncio.wait_for(
                asyncio.gather(*tasks_s1, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            results_s1 = []

    all_results = []
    seen_slugs: set = set()

    for data in results_s1:
        if isinstance(data, Exception) or not data:
            continue
        for hit in data.get("hits", []):
            slug = hit.get("slug", "").lower()
            title = hit.get("title", "").lower()
            if not _is_tacz_related(slug, title, hit.get("description", "")):
                continue
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            mod = _hit_to_modresult(hit, version)
            all_results.append(mod)

    if not all_results:
        return False, []

    for mod in all_results:
        mod.score = calculate_mod_score(mod, version)
    all_results.sort(key=lambda m: m.score, reverse=True)
    return True, all_results[:limit]


def _is_tacz_related(slug: str, title: str, description: str) -> bool:
    combined = f"{slug} {title} {description[:200]}".lower()
    return any(m in combined for m in [
        "tacz", "timeless and classics zero", "timeless-and-classics-zero",
        "timeless-and-classics", "gun pack", "gunpack"
    ])


def build_tacz_base_mod(version: str = None) -> ModResult:
    return ModResult(
        name="[TaCZ] Timeless and Classics Zero",
        slug=TACZ_MOD_SLUG,
        author="Timeless Squad",
        description=(
            "最沉浸、最可定制的 Minecraft 现代 FPS 体验。"
            "支持第三方枪包扩展，提供精致的射击动画和改装系统。"
            "枪包放入 .minecraft/tacz/ 目录即可加载。"
        ),
        downloads=17_000_000,
        favorites=2749,
        categories=["adventure", "equipment"],
        game_versions=list(TACZ_SUPPORTED_VERSIONS),
        loaders=["forge"],
        latest_version="1.1.4",
        modrinth_url=TACZ_MODRINTH_URL,
        warnings=(
            ["⚠️ 当前版本不在 TACZ 官方支持范围内，请关注社区移植版"]
            if version and version not in TACZ_SUPPORTED_VERSIONS
            else []
        ),
        platform="modrinth",
        source="builtin",
        score=99.0,
    )


def format_tacz_header(version: str = None, loader: str = None) -> str:
    return "\n".join([
        "\n" + "=" * 60,
        "  [TACZ] Minecraft 枪械 Mod 搜索 — TACZ 优先模式",
        f"  版本: {version or '不限'}  |  加载器: {loader or 'Forge（TACZ 默认）'}",
        "=" * 60,
        "",
        "  [第一步] 推荐基础框架",
        "  " + "-" * 40,
        f"  >> {TACZ_MOD_NAME}",
        f"     Modrinth: {TACZ_MODRINTH_URL}",
        f"     支持版本: 1.18.2 / 1.19.x / 1.20-1.20.1 (Forge)",
        "     安装枪包：将 .zip 放入 .minecraft/tacz/ 后执行 /tacz reload",
        "",
        "  [第二步] TACZ 枪包搜索结果",
        "  " + "-" * 40,
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Create 机械动力 意图 & 搜索
# ─────────────────────────────────────────────────────────────────────────────

def detect_create_intent(query: str) -> bool:
    q_lower = query.lower()
    return any(kw in q_lower for kw in CREATE_KEYWORDS)


async def search_create_addons_async(
    query: str,
    version: str = None,
    loader: str = None,
    limit: int = 10,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[bool, list]:
    keywords = _extract_keywords(query)
    create_queries = [f"create {kw}" for kw in keywords[:3]]

    async with aiohttp.ClientSession() as session:
        from urllib.parse import quote as uq

        tasks = []
        for q in create_queries:
            facets = [["categories:technology"]]
            if version:
                facets.append([f"versions:{version}"])
            if loader:
                facets.append([f"loaders:{loader}"])
            params = [("query", q), ("limit", "20"), ("index", "downloads"),
                      ("facets", json.dumps(facets))]
            url = f"{MODRINTH_BASE}/search?" + "&".join(f"{k}={uq(str(v))}" for k, v in params)
            tasks.append(async_http_get(session, url, timeout=DEFAULT_TIMEOUT))

        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            results = []

    all_results = []
    seen_slugs: set = set()

    for data in results:
        if isinstance(data, Exception) or not data:
            continue
        for hit in data.get("hits", []):
            slug = hit.get("slug", "").lower()
            if slug == CREATE_MOD_SLUG:
                continue
            title = hit.get("title", "").lower()
            if not _is_create_related(slug, title, hit.get("description", "")):
                continue
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            mod = _hit_to_modresult(hit, version)
            all_results.append(mod)

    if not all_results:
        return False, []

    for mod in all_results:
        mod.score = calculate_mod_score(mod, version)
    all_results.sort(key=lambda m: m.score, reverse=True)
    return True, all_results[:limit]


def _is_create_related(slug: str, title: str, description: str) -> bool:
    combined = f"{slug} {title} {description[:300]}".lower()
    return any(m in combined for m in ["create", "createaddon", "create addon", "simplycreate"])


def format_create_header(version: str = None, loader: str = None) -> str:
    return "\n".join([
        "\n" + "=" * 60,
        "  [Create] Minecraft 机械动力 Mod 搜索 — Create 优先模式",
        f"  版本: {version or '不限'}  |  加载器: {loader or 'Forge / Fabric'}",
        "=" * 60,
        "",
        "  [第一步] 推荐基础框架",
        "  " + "-" * 40,
        f"  >> {CREATE_MOD_NAME}",
        f"     Modrinth: {CREATE_MODRINTH_URL}",
        "     支持版本: 1.14.4 / 1.15.2 / 1.16.5 / 1.18.2 / 1.19.2 / 1.20.1",
        "     支持 Forge 和 Fabric 加载器",
        "",
        "  [第二步] Create 附属 Mod 搜索结果",
        "  " + "-" * 40,
    ])


# ─────────────────────────────────────────────────────────────────────────────
# 评分与排序
# ─────────────────────────────────────────────────────────────────────────────

def calculate_mod_score(mod: ModResult, target_version: str = None) -> float:
    scores = {}

    if mod.downloads > 0:
        scores["downloads"] = min(100, math.log10(mod.downloads + 1) / math.log10(100_000_000) * 100)
    else:
        scores["downloads"] = 0

    if mod.updated:
        try:
            dt = datetime.fromisoformat(mod.updated.replace("Z", "+00:00"))
            days_since = (datetime.now(dt.tzinfo) - dt).days
            if days_since <= 30:
                scores["update_frequency"] = 100
            elif days_since <= 90:
                scores["update_frequency"] = 90
            elif days_since <= 180:
                scores["update_frequency"] = 70
            elif days_since <= 365:
                scores["update_frequency"] = 50
            else:
                scores["update_frequency"] = max(0, 30 - (days_since - 365) // 365 * 20)
        except Exception:
            scores["update_frequency"] = 50
    else:
        scores["update_frequency"] = 50

    scores["rating"] = scores["downloads"] * 0.5 + (100 if mod.favorites > 10000 else mod.favorites / 100)

    if target_version:
        if target_version in mod.game_versions:
            scores["version_match"] = 100
        else:
            target_major = ".".join(target_version.split(".")[:2])
            has_near = any(target_major in v for v in mod.game_versions if v)
            scores["version_match"] = 60 if has_near else 0
    else:
        scores["version_match"] = 100

    total = sum(SORT_SCORE_WEIGHTS[k] * scores.get(k, 0) for k in SORT_SCORE_WEIGHTS)
    return round(total, 1)


def merge_and_rank(
    modrinth_mods: list[ModResult],
    curseforge_mods: list[ModResult],
    mcmod_mods: list[ModResult] = None,
    quickref_mods: list[ModResult] = None,
    target_version: str = None,
    top_n: int = 15,
) -> list[ModResult]:
    """合并多平台结果，去重并按评分排序。快查表命中优先展示。"""
    seen = {}
    all_mods: list[ModResult] = []

    # 快查表命中最优先
    for mod in (quickref_mods or []):
        key = mod.slug.lower()
        if key not in seen:
            seen[key] = mod
            all_mods.append(mod)

    # Modrinth（主平台）
    for mod in modrinth_mods:
        key = mod.slug.lower()
        if key not in seen:
            seen[key] = mod
            all_mods.append(mod)
        else:
            existing = seen[key]
            if mod.downloads > existing.downloads:
                seen[key] = mod
                all_mods = [m if m.slug.lower() != key else mod for m in all_mods]

    # CurseForge（补充）
    for mod in curseforge_mods:
        key = mod.slug.lower()
        if key not in seen:
            seen[key] = mod
            all_mods.append(mod)
        else:
            existing = seen[key]
            if not existing.curseforge_url and mod.curseforge_url:
                existing.curseforge_url = mod.curseforge_url
                existing.curseforge_id = mod.curseforge_id

    # MC百科（补充，仅在结果不足时）
    for mod in (mcmod_mods or []):
        key = mod.slug.lower()
        if key not in seen:
            seen[key] = mod
            all_mods.append(mod)

    # 计算评分
    for mod in all_mods:
        if mod.source == "quickref":
            mod.score = max(mod.score, 50.0)  # 快查表保底分
        elif mod.source in ("modrinth", "curseforge"):
            mod.score = calculate_mod_score(mod, target_version)
        # mcmod 保留 10.0 的分数

        if target_version and target_version not in mod.game_versions and mod.game_versions:
            if "版本不兼容" not in mod.warnings:
                mod.warnings.append(f"与 {target_version} 不兼容")

    all_mods.sort(key=lambda m: m.score, reverse=True)
    return all_mods[:top_n]


def normalize_slug(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-").replace("'", "")


# ─────────────────────────────────────────────────────────────────────────────
# 兼容性检查（保留原有逻辑，简化导入）
# ─────────────────────────────────────────────────────────────────────────────

HARD_CONFLICTS = {
    ("optifine", "sodium"): ("OptiFine", "Sodium", "两者均为渲染优化 Mod，功能重叠，同时安装会冲突"),
    ("optifine", "iris"): ("OptiFine", "Iris", "OptiFine 着色器与 Iris 着色器互斥"),
    ("optifine", "embeddium"): ("OptiFine", "Embeddium", "渲染引擎冲突"),
    ("optifine", "rubidium"): ("OptiFine", "Rubidium", "渲染引擎冲突"),
    ("sodium", "iris"): None,
    ("ae2", "refined-storage"): ("AE2", "Refined Storage", "两个存储系统不可同时启用"),
    ("ae2", "refinedstorage"): ("AE2", "Refined Storage", "两个存储系统不可同时启用"),
    ("ae2", "rs"): ("AE2", "Refined Storage", "两个存储系统不可同时启用"),
}

STORAGE_MODS_GROUP = {"ae2", "refined-storage", "refinedstorage", "rs",
                       "storage drawers", "storagedrawers", "industrial foregoing",
                       "simple storage network"}
INFO_DISPLAY_GROUP = {"jade", "wthit", "hwyla", "theoneprobe"}
ITEM_VIEW_GROUP = {"roughly enough items", "rei", "emi", "just enough items", "jei"}
OPTIMIZATION_GROUP = {"optifine", "sodium", "iris", "embeddium", "rubidium", "magnesium"}
LOADER_INCOMPATIBLE_PAIRS = [("forge", "fabric"), ("forge", "quilt"), ("fabric", "rift")]


@dataclass
class CompatibilityReport:
    loader_issues: list = field(default_factory=list)
    hard_conflicts: list = field(default_factory=list)
    version_incompat: list = field(default_factory=list)
    functional_overlap: list = field(default_factory=list)
    dependency_missing: list = field(default_factory=list)
    all_good: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)


def check_mod_compatibility(mods: list[ModResult], target_version: str = None) -> CompatibilityReport:
    report = CompatibilityReport()
    if not mods:
        return report

    all_loaders = set()
    for mod in mods:
        for loader in (mod.loaders or []):
            all_loaders.add(loader.lower())

    for loader_a, loader_b in LOADER_INCOMPATIBLE_PAIRS:
        if loader_a in all_loaders and loader_b in all_loaders:
            report.loader_issues.append({
                "type": "loader_conflict",
                "loaders": [loader_a, loader_b],
                "reason": f"{loader_a.title()} 和 {loader_b.title()} Mod 不可混用",
                "severity": "error",
            })

    mod_slugs = {normalize_slug(m.name): m for m in mods}
    mod_names_lower = {normalize_slug(m.name): m.name for m in mods}
    checked_pairs = set()

    for mod in mods:
        for (conf_a, conf_b), info in HARD_CONFLICTS.items():
            if info is None:
                continue
            norm_a, norm_b = normalize_slug(conf_a), normalize_slug(conf_b)
            pair = tuple(sorted([norm_a, norm_b]))
            if pair in checked_pairs:
                continue
            checked_pairs.add(pair)
            a_in = norm_a in mod_slugs or conf_a.lower() in mod_names_lower
            b_in = norm_b in mod_slugs or conf_b.lower() in mod_names_lower
            if a_in and b_in:
                report.hard_conflicts.append({
                    "type": "hard_conflict",
                    "mods": [mod_names_lower.get(norm_a, conf_a), mod_names_lower.get(norm_b, conf_b)],
                    "reason": info[2],
                    "severity": "error",
                    "solution": f"在 {conf_a} 和 {conf_b} 中选择一个",
                })

    groups = [("storage", STORAGE_MODS_GROUP), ("info_display", INFO_DISPLAY_GROUP),
              ("item_view", ITEM_VIEW_GROUP), ("optimization", OPTIMIZATION_GROUP)]

    for group_name, group_set in groups:
        found = []
        for mod in mods:
            slug = normalize_slug(mod.name)
            for keyword in group_set:
                if keyword in slug or slug in keyword:
                    found.append(mod.name)
                    break
        if len(found) > 1:
            if group_name == "optimization":
                sodium_found = any("sodium" in normalize_slug(n) for n in found)
                iris_found = any("iris" in normalize_slug(n) for n in found)
                if sodium_found and iris_found:
                    continue
            report.functional_overlap.append({
                "type": "functional_overlap",
                "group": group_name,
                "mods": found,
                "reason": "多个功能相同的 Mod 同时存在",
                "severity": "warning",
                "solution": f"建议只保留一个 {group_name} 类 Mod",
            })

    if target_version:
        for mod in mods:
            if mod.game_versions and target_version not in mod.game_versions:
                report.version_incompat.append({
                    "type": "version_incompatible",
                    "mod": mod.name,
                    "target_version": target_version,
                    "supported_versions": mod.game_versions[:5],
                    "severity": "error",
                    "suggestion": f"不支持 {target_version}，最高 {mod.game_versions[0] if mod.game_versions else '未知'}",
                })

    selected_slugs = {normalize_slug(m.name) for m in mods}
    for mod in mods:
        for dep in mod.dependencies:
            if dep.required:
                dep_slug = normalize_slug(dep.slug or dep.name)
                if dep_slug not in selected_slugs:
                    report.dependency_missing.append({
                        "type": "missing_dependency",
                        "parent_mod": mod.name,
                        "dependency": dep.name or dep.slug,
                        "required": dep.required,
                        "suggestion": f"安装 {mod.name} 前需先安装 {dep.name or dep.slug}",
                    })

    if report.loader_issues:
        loaders_used = [l for iss in report.loader_issues for l in iss.get("loaders", [])]
        report.recommendations.append({
            "type": "loader_decision",
            "suggestion": f"检测到加载器冲突：{loaders_used}。请选择单一加载器",
        })

    if not report.hard_conflicts and not report.loader_issues and not report.version_incompat:
        report.recommendations.append({
            "type": "all_clear",
            "suggestion": "整合包 Mod 之间未发现硬性冲突，可正常安装使用",
        })

    return report


# ─────────────────────────────────────────────────────────────────────────────
# 输出格式化
# ─────────────────────────────────────────────────────────────────────────────

def format_results_json(mods: list[ModResult], query: str, version: str = None,
                        cf_warning: str = "") -> str:
    output = {
        "query": query,
        "version": version,
        "total": len(mods),
        "results": [asdict(mod) for mod in mods],
        "warnings": [cf_warning] if cf_warning else [],
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def format_results_text(mods: list[ModResult], query: str, version: str = None) -> str:
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  Minecraft Mod 搜索结果")
    lines.append(f"  关键词: {query}  |  版本: {version or '不限'}")
    lines.append(f"{'='*60}\n")

    # 按来源分组展示
    quickref_mods = [m for m in mods if m.source == "quickref"]
    api_mods = [m for m in mods if m.source != "quickref"]

    if quickref_mods:
        lines.append("  【快查表命中 — 高可信度推荐】")
        lines.append("  " + "-" * 40)
        for i, mod in enumerate(quickref_mods, 1):
            lines.append(f"  ★ {i}. {mod.name}  [📚 快查表]")
            if mod.description:
                lines.append(f"    {mod.description}")
            if mod.modrinth_url:
                lines.append(f"    Modrinth: {mod.modrinth_url}")
            lines.append("")
        lines.append("")

    if api_mods:
        if quickref_mods:
            lines.append("  【API 搜索结果】")
            lines.append("  " + "-" * 40)

        for i, mod in enumerate(api_mods, 1):
            is_top3 = i <= 3 and not quickref_mods
            badge = " [🔥 TOP推荐]" if is_top3 else ""
            source_badge = ""
            if mod.source == "mcmod":
                source_badge = "  [MC百科]"
            elif mod.source == "curseforge":
                source_badge = "  [CurseForge]"

            lines.append(f"  {'▶' if is_top3 else '·'} {i}. {mod.name}{badge}{source_badge}")
            lines.append(f"    作者: {mod.author or '未知'}")
            lines.append(f"    下载: {mod.downloads:,}  |  版本: {mod.latest_version or (mod.game_versions[0] if mod.game_versions else '未知')}")

            cats = ", ".join(mod.categories[:3]) if mod.categories else "未分类"
            lines.append(f"    分类: {cats}")

            if mod.description:
                desc = mod.description[:120].replace("\n", " ")
                lines.append(f"    简介: {desc}{'...' if len(mod.description) > 120 else ''}")

            link_parts = []
            if mod.modrinth_url:
                link_parts.append(f"Modrinth: {mod.modrinth_url}")
            if mod.curseforge_url:
                link_parts.append(f"CurseForge: {mod.curseforge_url}")
            if link_parts:
                lines.append(f"    链接: {' | '.join(link_parts)}")

            for w in mod.warnings:
                lines.append(f"    ⚠️  {w}")

            lines.append("")

    lines.append(f"{'='*60}")
    lines.append(f"  共找到 {len(mods)} 个相关 Mod\n")
    return "\n".join(lines)


def format_compatibility_report(report: CompatibilityReport, mods: list[ModResult],
                                  target_version: str = None, loader: str = None) -> str:
    lines = [
        f"\n{'='*60}",
        f"  整合包兼容性检查报告",
        f"  版本: {target_version or '不限'}  |  加载器: {loader or '未指定'}",
        f"{'='*60}\n",
    ]

    if report.loader_issues or report.hard_conflicts:
        lines.append("  ❌ 严重冲突（必须解决）")
        lines.append("  " + "-"*40)
        for issue in report.loader_issues:
            lines.append(f"  ⚠️  加载器冲突: {' + '.join(issue['loaders'])}")
            lines.append(f"     {issue['reason']}")
            lines.append("")
        for conflict in report.hard_conflicts:
            lines.append(f"  ❌ {conflict['mods'][0]} + {conflict['mods'][1]}")
            lines.append(f"     {conflict['reason']}")
            lines.append(f"     → {conflict['solution']}")
            lines.append("")
        lines.append("")

    if report.version_incompat:
        lines.append("  🚫 版本不兼容（需换 Mod 或换版本）")
        lines.append("  " + "-"*40)
        for item in report.version_incompat:
            lines.append(f"  · {item['mod']} 不支持 {item['target_version']}")
            lines.append(f"    → {item['suggestion']}")
        lines.append("")

    if report.functional_overlap:
        lines.append("  ⚠️  功能重叠（建议精简）")
        lines.append("  " + "-"*40)
        for item in report.functional_overlap:
            lines.append(f"  · {item['group']}: {' + '.join(item['mods'])}")
            lines.append(f"    → {item['solution']}")
        lines.append("")

    if report.dependency_missing:
        lines.append("  ⬆️  缺失前置依赖（需补充安装）")
        lines.append("  " + "-"*40)
        for item in report.dependency_missing:
            lines.append(f"  · {item['parent_mod']} 需要 → {item['dependency']}")
        lines.append("")

    if report.recommendations:
        lines.append("  💡 推荐建议")
        lines.append("  " + "-"*40)
        for rec in report.recommendations:
            if rec["type"] == "all_clear":
                lines.append(f"  ✅ {rec['suggestion']}")
            else:
                lines.append(f"  · {rec['suggestion']}")
        lines.append("")

    lines.append(f"{'='*60}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# 主异步搜索逻辑
# ─────────────────────────────────────────────────────────────────────────────

async def run_search(args) -> tuple[list[ModResult], str]:
    """
    主搜索流程（异步）。
    返回 (results, cf_warning_message)
    """
    query = args.query
    version = args.version
    loader = getattr(args, "loader", None)
    limit = getattr(args, "limit", 15)
    timeout = getattr(args, "timeout", DEFAULT_TIMEOUT)
    fetch_deps = getattr(args, "deps", False)
    cf_api_key = getattr(args, "api_key", None) or os.environ.get("CF_API_KEY", "")

    # 检查 CurseForge API Key
    cf_has_key, cf_warning = check_curseforge_api_key(cf_api_key)

    # Step 1: 快查表
    print(f"  → 检索快查表...", file=sys.stderr)
    quickref_results = search_quickref(query, version, limit=5)
    if quickref_results:
        print(f"  [快查表] 命中 {len(quickref_results)} 条", file=sys.stderr)

    # Step 2: 提取多关键词
    keywords = _extract_keywords(query)
    print(f"  → 多关键词搜索: {keywords}", file=sys.stderr)

    # Step 3: TACZ 枪械优先路径
    if detect_gun_intent(query):
        print(f"  → 检测到枪械意图，启用 TACZ 优先搜索...", file=sys.stderr)
        tacz_found, tacz_mods = await search_tacz_gunpacks_async(
            query=query, version=version, limit=limit, timeout=timeout
        )
        if tacz_found and tacz_mods:
            if fetch_deps:
                tacz_mods = await add_dependencies_async(tacz_mods, timeout)
            return tacz_mods, cf_warning

        print(f"  → TACZ 枪包搜索无结果，回退到普通搜索...", file=sys.stderr)

    # Step 4: Create 机械动力优先路径
    if detect_create_intent(query):
        print(f"  → 检测到机械/自动化意图，启用 Create 优先搜索...", file=sys.stderr)
        create_found, create_mods = await search_create_addons_async(
            query=query, version=version, loader=loader, limit=limit, timeout=timeout
        )
        if create_found and create_mods:
            if fetch_deps:
                create_mods = await add_dependencies_async(create_mods, timeout)
            return create_mods, cf_warning

        print(f"  → Create 附属搜索无结果，回退到普通搜索...", file=sys.stderr)

    # Step 5: 普通多关键词并行搜索
    t0 = time.time()
    print(f"  → Modrinth 并发搜索 {len(keywords)} 个关键词...", file=sys.stderr)

    modrinth_results = await search_modrinth_multi(
        queries=keywords,
        version=version,
        loader=loader,
        category=getattr(args, "category", None),
        limit=limit,
        timeout=timeout,
    )
    print(f"  [Modrinth] 耗时 {time.time()-t0:.1f}s，得到 {len(modrinth_results)} 条", file=sys.stderr)

    # Step 6: CurseForge 并行搜索（如果有 Key）
    cf_results = []
    if cf_has_key and getattr(args, "platform", "all") in ("curseforge", "all"):
        print(f"  → CurseForge 搜索...", file=sys.stderr)
        t1 = time.time()
        async with aiohttp.ClientSession() as session:
            cf_tasks = [
                search_curseforge_async(session, kw, version, loader, cf_api_key, limit, 5)
                for kw in keywords[:2]  # CF 限制 2 个关键词
            ]
            try:
                cf_list = await asyncio.wait_for(asyncio.gather(*cf_tasks), timeout=10)
                for lst in cf_list:
                    if isinstance(lst, list):
                        cf_results.extend(lst)
            except asyncio.TimeoutError:
                print("  [CurseForge] 搜索超时", file=sys.stderr)
        print(f"  [CurseForge] 耗时 {time.time()-t1:.1f}s，得到 {len(cf_results)} 条", file=sys.stderr)

    # Step 7: MC百科补充（当 Modrinth 结果 < 3 时）
    mcmod_results = []
    if len(modrinth_results) < 3:
        print(f"  → Modrinth 结果不足 3 条，启用 MC百科补充搜索...", file=sys.stderr)
        async with aiohttp.ClientSession() as session:
            # 用原始中文查询词（MC百科是中文数据库）
            mcmod_results = await search_mcmod_async(session, query, version, timeout)

    # Step 8: 合并排序（快查表 > Modrinth > CurseForge > MC百科）
    merged = merge_and_rank(
        modrinth_results,
        cf_results,
        mcmod_mods=mcmod_results,
        quickref_mods=quickref_results,
        target_version=version,
        top_n=limit,
    )

    # Step 9: 按需补充依赖
    if fetch_deps and merged:
        print(f"  → 补充依赖信息...", file=sys.stderr)
        merged = await add_dependencies_async(merged, timeout)

    return merged, cf_warning


# ─────────────────────────────────────────────────────────────────────────────
# 整合包分析模式（异步）
# ─────────────────────────────────────────────────────────────────────────────

async def run_modpack_analysis(args) -> str:
    query = args.query
    version = args.version
    loader = getattr(args, "loader", None)
    directions = args.directions or [query]
    timeout = getattr(args, "timeout", DEFAULT_TIMEOUT)
    cf_api_key = getattr(args, "api_key", None) or os.environ.get("CF_API_KEY", "")
    cf_has_key, cf_warning = check_curseforge_api_key(cf_api_key)

    directions_results = {}
    all_mods = []

    for direction in directions:
        print(f"  → 分析方向: {direction}", file=sys.stderr)
        t0 = time.time()
        keywords = _extract_keywords(direction)

        mr = await search_modrinth_multi(keywords, version, loader, limit=5, timeout=timeout)
        cf = []
        if cf_has_key:
            async with aiohttp.ClientSession() as session:
                cf_tasks = [search_curseforge_async(session, kw, version, loader, cf_api_key, 3, 5)
                            for kw in keywords[:2]]
                try:
                    cf_list = await asyncio.wait_for(asyncio.gather(*cf_tasks), timeout=10)
                    for lst in cf_list:
                        if isinstance(lst, list):
                            cf.extend(lst)
                except asyncio.TimeoutError:
                    pass

        merged_dir = merge_and_rank(mr, cf, target_version=version, top_n=3)
        directions_results[direction] = merged_dir
        all_mods.extend(merged_dir)
        print(f"    返回 {len(merged_dir)} 个 Mod (耗时 {time.time()-t0:.1f}s)", file=sys.stderr)

    # 去重
    seen = {}
    for mod in all_mods:
        key = normalize_slug(mod.name)
        if key not in seen or mod.downloads > seen[key].downloads:
            seen[key] = mod
    all_mods = list(seen.values())

    compat_report = check_mod_compatibility(all_mods, target_version=version)

    output = format_modpack_report(directions_results, compat_report, version, loader)
    if cf_warning:
        output = cf_warning + output
    return output


def format_modpack_report(directions: dict, compat_report: CompatibilityReport,
                            version: str = None, loader: str = None) -> str:
    lines = [
        f"\n{'='*60}",
        f"  整合包规划与推荐报告",
        f"  版本: {version or '不限'}  |  加载器: {loader or '根据功能方向选择'}",
        f"{'='*60}\n",
        f"  {'─'*56}",
        f"  各功能方向推荐 Mod",
        f"  {'─'*56}\n",
    ]

    for i, (direction, mods) in enumerate(directions.items(), 1):
        lines.append(f"  【{i}. {direction}】")
        for j, mod in enumerate(mods[:3], 1):
            badge = "🔥 核心" if j == 1 else f"  备选{j}"
            lines.append(f"    {j}. {mod.name} [{badge}]")
            lines.append(f"       📥 {mod.downloads:,} | 🎮 {mod.latest_version or '未知'}")
            cats = ", ".join(mod.categories[:3]) if mod.categories else ""
            if cats:
                lines.append(f"       🏷️  {cats}")
            if mod.description:
                lines.append(f"       {mod.description[:100].replace(chr(10), ' ')}...")
            for w in mod.warnings:
                lines.append(f"       ⚠️  {w}")
            lines.append(f"       🔗 {mod.modrinth_url or mod.curseforge_url}")
            lines.append("")
        lines.append("")

    lines.append(f"  {'─'*56}")
    lines.append(f"  兼容性总览")
    lines.append(f"  {'─'*56}\n")

    if compat_report.hard_conflicts:
        lines.append(f"  ❌ 发现 {len(compat_report.hard_conflicts)} 项严重冲突：")
        for c in compat_report.hard_conflicts:
            lines.append(f"    · {c['mods'][0]} + {c['mods'][1]}: {c['reason']}")
    else:
        lines.append(f"  ✅ 核心 Mod 之间无硬性冲突\n")

    lines.append(f"{'='*60}\n")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# 同步 fallback（当无 aiohttp 时使用 urllib）
# ─────────────────────────────────────────────────────────────────────────────

def search_modrinth_sync(query: str, version: str = None, loader: str = None,
                          category: str = None, limit: int = 20, timeout: int = DEFAULT_TIMEOUT) -> list[ModResult]:
    from urllib.parse import quote
    url = _build_modrinth_url(query, version, loader, category, limit)
    data = _sync_http_get(url, timeout=timeout)
    if not data or "hits" not in data:
        return []
    return [_hit_to_modresult(hit, version) for hit in data.get("hits", [])]


def search_sync_main(args) -> tuple[list[ModResult], str]:
    """同步版主搜索（无 aiohttp 时）"""
    query = args.query
    version = args.version
    loader = getattr(args, "loader", None)
    limit = getattr(args, "limit", 15)
    timeout = getattr(args, "timeout", DEFAULT_TIMEOUT)
    cf_api_key = getattr(args, "api_key", None) or os.environ.get("CF_API_KEY", "")

    cf_has_key, cf_warning = check_curseforge_api_key(cf_api_key)

    quickref_results = search_quickref(query, version, limit=5)
    keywords = _extract_keywords(query)

    modrinth_results = []
    for kw in keywords:
        mods = search_modrinth_sync(kw, version, loader, limit=limit, timeout=timeout)
        modrinth_results.extend(mods)

    # 去重
    seen = {}
    deduped = []
    for m in modrinth_results:
        if m.slug not in seen:
            seen[m.slug] = True
            deduped.append(m)
    modrinth_results = deduped

    merged = merge_and_rank(modrinth_results, [], quickref_mods=quickref_results,
                             target_version=version, top_n=limit)
    return merged, cf_warning


# ─────────────────────────────────────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Minecraft Java Mod 多平台搜索 v2.0")
    parser.add_argument("--query", "-q", required=True, help="搜索关键词")
    parser.add_argument("--version", "-v", default=None, help="Minecraft 版本，如 1.20.1")
    parser.add_argument("--loader", "-l", default=None, help="加载器: forge/fabric/quilt")
    parser.add_argument("--category", "-c", default=None, help="Mod 分类")
    parser.add_argument("--platform", "-p", default="all", choices=["modrinth", "curseforge", "all"])
    parser.add_argument("--limit", type=int, default=15, help="返回结果数量")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="请求超时（秒）")
    parser.add_argument("--api-key", default=None, help="CurseForge API Key")
    parser.add_argument("--output", "-o", default="text", choices=["text", "json"])
    parser.add_argument("--deps", action="store_true",
                        help="查询依赖信息（默认关闭以提速，需要时手动开启）")
    # 整合包分析专用
    parser.add_argument("--modpack", action="store_true", help="启用整合包分析模式")
    parser.add_argument("--directions", "-d", nargs="+", default=None,
                        help="整合包各方向关键词（与 --modpack 配合）")

    args = parser.parse_args()

    if HAS_AIOHTTP:
        # 异步路径
        if args.modpack and args.directions:
            print(f"\n🎮 整合包分析模式（异步）", file=sys.stderr)
            output = asyncio.run(run_modpack_analysis(args))
            print(output)
        else:
            results, cf_warning = asyncio.run(run_search(args))

            if cf_warning:
                print(cf_warning)

            if detect_gun_intent(args.query):
                print(format_tacz_header(args.version, args.loader))
            elif detect_create_intent(args.query):
                print(format_create_header(args.version, args.loader))

            if args.output == "json":
                print(format_results_json(results, args.query, args.version, cf_warning))
            else:
                print(format_results_text(results, args.query, args.version))

    else:
        # 同步 fallback（无 aiohttp）
        print("⚠️  未安装 aiohttp，使用同步模式（速度较慢）。建议：pip install aiohttp", file=sys.stderr)
        results, cf_warning = search_sync_main(args)

        if cf_warning:
            print(cf_warning)

        if args.output == "json":
            print(format_results_json(results, args.query, args.version, cf_warning))
        else:
            print(format_results_text(results, args.query, args.version))


if __name__ == "__main__":
    main()
