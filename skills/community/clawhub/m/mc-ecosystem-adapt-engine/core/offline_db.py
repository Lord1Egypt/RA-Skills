# -*- coding: utf-8 -*-
"""V1.0.2 增强：离线数据库模块

提供增强的离线查询能力：
1. 扩展本地数据库覆盖度（热门模组索引）
2. 支持模糊匹配和多语言搜索
3. 支持版本兼容性快速查询
4. 本地缓存最近查询结果
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = _PROJECT_ROOT / "data"
RECOMMENDATIONS_FILE = DATA_DIR / "mod_version_recommendations.json"

# === V1.0.2 新增: 热门模组索引（离线快速查询）===
# 这些是高频使用的模组，离线时可以快速匹配
HOT_MOD_INDEX = {
    "create": {
        "aliases": ["create", "机械动力", "Create", "create mod"],
        "slug": "create",
        "name_cn": "机械动力",
        "name_en": "Create",
        "categories": ["tech", "redstone"],
        "popular": True,
    },
    "fabric-api": {
        "aliases": ["fabric-api", "fabric api", "FabricAPI"],
        "slug": "fabric-api",
        "name_cn": "Fabric API",
        "name_en": "Fabric API",
        "categories": ["utility"],
        "popular": True,
    },
    "forge-config-api": {
        "aliases": ["forge-config-api", "config api", "配置API"],
        "slug": "forge-config-api",
        "name_cn": "Forge Config API",
        "name_en": "Forge Config API",
        "categories": ["utility"],
        "popular": False,
    },
    "jei": {
        "aliases": ["jei", "物品管理", "物品查询"],
        "slug": "jei",
        "name_cn": "物品管理 (JEI)",
        "name_en": "Just Enough Items",
        "categories": ["utility"],
        "popular": True,
    },
    "sodium": {
        "aliases": ["sodium", "钠", "性能优化"],
        "slug": "sodium",
        "name_cn": "钠 (Sodium)",
        "name_en": "Sodium",
        "categories": ["performance"],
        "popular": True,
    },
    "iris": {
        "aliases": ["iris", "虹膜", "光影"],
        "slug": "iris",
        "name_cn": "虹膜 (Iris)",
        "name_en": "Iris",
        "categories": ["performance"],
        "popular": True,
    },
    "nei": {
        "aliases": ["nei", "NotEnoughItems"],
        "slug": "notenoughitems",
        "name_cn": "物品管理 (NEI)",
        "name_en": "NotEnoughItems",
        "categories": ["utility"],
        "popular": False,
    },
    "applied-energistics-2": {
        "aliases": ["ae2", "applied energistics", "应用能源", "应用能源2"],
        "slug": "applied-energistics-2",
        "name_cn": "应用能源2",
        "name_en": "Applied Energistics 2",
        "categories": ["tech", "storage"],
        "popular": True,
    },
    "thermal-expansion": {
        "aliases": ["thermal expansion", "热力膨胀", "TE"],
        "slug": "thermal-expansion",
        "name_cn": "热力膨胀",
        "name_en": "Thermal Expansion",
        "categories": ["tech"],
        "popular": True,
    },
    "mekanism": {
        "aliases": ["mekanism", "机械"],
        "slug": "mekanism",
        "name_cn": "机械 (Mekanism)",
        "name_en": "Mekanism",
        "categories": ["tech"],
        "popular": True,
    },
    "ic2": {
        "aliases": ["ic2", "工业时代", "IndustrialCraft"],
        "slug": "industrialcraft-2",
        "name_cn": "工业时代2",
        "name_en": "IndustrialCraft 2",
        "categories": ["tech"],
        "popular": True,
    },
    "forestry": {
        "aliases": ["forestry", "林业"],
        "slug": "forestry",
        "name_cn": "林业 (Forestry)",
        "name_en": "Forestry",
        "categories": ["tech", "food"],
        "popular": True,
    },
    "thaumcraft": {
        "aliases": ["thaumcraft", "神秘时代", "神秘"],
        "slug": "thaumcraft",
        "name_cn": "神秘时代",
        "name_en": "Thaumcraft",
        "categories": ["magic"],
        "popular": True,
    },
    "twilightforest": {
        "aliases": ["twilight forest", "暮色森林", "暮色"],
        "slug": "twilightforest",
        "name_cn": "暮色森林",
        "name_en": "Twilight Forest",
        "categories": ["adventure", "worldgen"],
        "popular": True,
    },
    "tconstruct": {
        "aliases": ["tconstruct", "匠魂", "Tinkers Construct"],
        "slug": "tconstruct",
        "name_cn": "匠魂",
        "name_en": "Tinkers Construct",
        "categories": ["equipment", "mobs"],
        "popular": True,
    },
    "farmersdelight": {
        "aliases": ["farmers delight", "农夫乐事", "乐事"],
        "slug": "farmersdelight",
        "name_cn": "农夫乐事",
        "name_en": "Farmer's Delight",
        "categories": ["food", "fun"],
        "popular": True,
    },
    "buildcraft": {
        "aliases": ["buildcraft", "建筑"],
        "slug": "buildcraft",
        "name_cn": "建筑 (BuildCraft)",
        "name_en": "BuildCraft",
        "categories": ["redstone"],
        "popular": False,
    },
    "railcraft": {
        "aliases": ["railcraft", "铁路"],
        "slug": "railcraft",
        "name_cn": "铁路 (Railcraft)",
        "name_en": "Railcraft",
        "categories": ["redstone"],
        "popular": False,
    },
    "immersiveengineering": {
        "aliases": ["immersive engineering", "沉浸工程"],
        "slug": "immersiveengineering",
        "name_cn": "沉浸工程",
        "name_en": "Immersive Engineering",
        "categories": ["tech"],
        "popular": True,
    },
    "draconicevolution": {
        "aliases": ["draconic evolution", "龙之研究", "龙研"],
        "slug": "draconicevolution",
        "name_cn": "龙之研究",
        "name_en": "Draconic Evolution",
        "categories": ["tech", "magic"],
        "popular": True,
    },
    "bloodmagic": {
        "aliases": ["blood magic", "血魔法"],
        "slug": "bloodmagic",
        "name_cn": "血魔法",
        "name_en": "Blood Magic",
        "categories": ["magic"],
        "popular": True,
    },
    "roots": {
        "aliases": ["roots", "根源"],
        "slug": "roots",
        "name_cn": "根源 (Roots)",
        "name_en": "Roots",
        "categories": ["magic"],
        "popular": False,
    },
    "psi": {
        "aliases": ["psi", "心灵感应"],
        "slug": "psi",
        "name_cn": "心灵感应 (Psi)",
        "name_en": "Psi",
        "categories": ["magic"],
        "popular": False,
    },
    "bluepower": {
        "aliases": ["blue power", "蓝色能量"],
        "slug": "bluepower",
        "name_cn": "蓝色能量",
        "name_en": "Blue Power",
        "categories": ["magic"],
        "popular": False,
    },
    "openblocks": {
        "aliases": ["openblocks", "开源方块"],
        "slug": "openblocks",
        "name_cn": "开源方块",
        "name_en": "OpenBlocks",
        "categories": ["utility", "decoration"],
        "popular": False,
    },
    "opencomputers": {
        "aliases": ["opencomputers", "开源电脑", "OC"],
        "slug": "opencomputers",
        "name_cn": "开源电脑",
        "name_en": "OpenComputers",
        "categories": ["redstone", "utility"],
        "popular": False,
    },
    "computercraft": {
        "aliases": ["computercraft", "电脑工艺", "CC"],
        "slug": "computer-craft",
        "name_cn": "电脑工艺",
        "name_en": "ComputerCraft",
        "categories": ["redstone", "utility"],
        "popular": False,
    },
    "refinedstorage": {
        "aliases": ["refined storage", "精致存储", "RS"],
        "slug": "refinedstorage",
        "name_cn": "精致存储",
        "name_en": "Refined Storage",
        "categories": ["storage"],
        "popular": True,
    },
    "logistics-pipes": {
        "aliases": ["logistics pipes", "物流管道", "LP"],
        "slug": "logisticspipes",
        "name_cn": "物流管道",
        "name_en": "Logistics Pipes",
        "categories": ["redstone", "storage"],
        "popular": False,
    },
    "storage-drawers": {
        "aliases": ["storage drawers", "存储抽屉", "抽屉"],
        "slug": "storagedrawers",
        "name_cn": "存储抽屉",
        "name_en": "Storage Drawers",
        "categories": ["storage"],
        "popular": True,
    },
    "iron-chest": {
        "aliases": ["iron chest", "铁箱子"],
        "slug": "ironchest",
        "name_cn": "铁箱子",
        "name_en": "Iron Chests",
        "categories": ["storage"],
        "popular": False,
    },
    "better-dungeons": {
        "aliases": ["better dungeons", "更好的地牢"],
        "slug": "better-dungeons",
        "name_cn": "更好的地牢",
        "name_en": "Better Dungeons",
        "categories": ["adventure"],
        "popular": False,
    },
    "aether": {
        "aliases": ["aether", "以太"],
        "slug": "aether",
        "name_cn": "以太 (Aether)",
        "name_en": "The Aether",
        "categories": ["adventure", "worldgen"],
        "popular": False,
    },
    "biomes-o-plenty": {
        "aliases": ["biomes o plenty", "超多生物群系", "BOP"],
        "slug": "biomes-o-plenty",
        "name_cn": "超多生物群系",
        "name_en": "Biomes O' Plenty",
        "categories": ["worldgen"],
        "popular": True,
    },
    "supplementaries": {
        "aliases": ["supplementaries", "补充"],
        "slug": "supplementaries",
        "name_cn": "补充 (Supplementaries)",
        "name_en": "Supplementaries",
        "categories": ["decoration", "gameplay"],
        "popular": True,
    },
    "chisels-and-bits": {
        "aliases": ["chisels and bits", "凿子与方块"],
        "slug": "chisels-and-bits",
        "name_cn": "凿子与方块",
        "name_en": "Chisels & Bits",
        "categories": ["decoration"],
        "popular": False,
    },
    "controlling": {
        "aliases": ["controlling", "控制"],
        "slug": "controlling",
        "name_cn": "控制 (Controlling)",
        "name_en": "Controlling",
        "categories": ["utility"],
        "popular": True,
    },
    "modmenu": {
        "aliases": ["modmenu", "模组菜单"],
        "slug": "modmenu",
        "name_cn": "模组菜单",
        "name_en": "Mod Menu",
        "categories": ["utility"],
        "popular": True,
    },
    "cloth-config": {
        "aliases": ["cloth config", "布料配置"],
        "slug": "cloth-config",
        "name_cn": "布料配置",
        "name_en": "Cloth Config",
        "categories": ["utility"],
        "popular": True,
    },
    "appleskin": {
        "aliases": ["appleskin", "苹果皮"],
        "slug": "appleskin",
        "name_cn": "苹果皮",
        "name_en": "AppleSkin",
        "categories": ["gameplay"],
        "popular": True,
    },
    "spice-of-life": {
        "aliases": ["spice of life", "生命香料"],
        "slug": "spiceoflife",
        "name_cn": "生命香料",
        "name_en": "Spice of Life",
        "categories": ["food", "gameplay"],
        "popular": False,
    },
    "cold-sweat": {
        "aliases": ["cold sweat", "冷汗"],
        "slug": "cold-sweat",
        "name_cn": "冷汗",
        "name_en": "Cold Sweat",
        "categories": ["survival"],
        "popular": True,
    },
    "morph": {
        "aliases": ["morph", "变形"],
        "slug": "morph",
        "name_cn": "变形 (Morph)",
        "name_en": "Morph",
        "categories": ["gameplay", "mobs"],
        "popular": False,
    },
    "xnet": {
        "aliases": ["xnet", "X网络"],
        "slug": "xnet",
        "name_cn": "X网络",
        "name_en": "XNet",
        "categories": ["redstone"],
        "popular": False,
    },
    "cyclic": {
        "aliases": ["cyclic", "循环"],
        "slug": "cyclic",
        "name_cn": "循环 (Cyclic)",
        "name_en": "Cyclic",
        "categories": ["utility", "gameplay"],
        "popular": False,
    },
    "extra-utils": {
        "aliases": ["extra utils", "额外实用工具", "EU"],
        "slug": "extrautils2",
        "name_cn": "额外实用工具2",
        "name_en": "Extra Utilities 2",
        "categories": ["utility"],
        "popular": False,
    },
    "actually-additions": {
        "aliases": ["actually additions", "实际添加"],
        "slug": "actuallyadditions",
        "name_cn": "实际添加",
        "name_en": "Actually Additions",
        "categories": ["tech"],
        "popular": False,
    },
    "big-reactors": {
        "aliases": ["big reactors", "大型反应堆"],
        "slug": "bigreactors",
        "name_cn": "大型反应堆",
        "name_en": "Big Reactors",
        "categories": ["tech"],
        "popular": False,
    },
}

# 本地查询缓存（进程内）
_query_cache: Dict[str, Tuple[float, Any]] = {}
QUERY_CACHE_TTL = 300  # 本地查询缓存 5 分钟


def load_recommendations() -> Dict[str, Any]:
    """加载本地兼容规则库

    Returns:
        兼容规则库数据
    """
    try:
        if RECOMMENDATIONS_FILE.exists():
            with open(RECOMMENDATIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"_meta": {}, "mods": {}}
    except Exception as e:
        logger.error(f"加载兼容规则库失败: {e}")
        return {"_meta": {}, "mods": {}}


def save_recommendations(data: Dict[str, Any]) -> bool:
    """保存兼容规则库到本地

    Args:
        data: 兼容规则库数据

    Returns:
        是否保存成功
    """
    try:
        RECOMMENDATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"兼容规则库已保存: {RECOMMENDATIONS_FILE}")
        return True
    except Exception as e:
        logger.error(f"保存兼容规则库失败: {e}")
        return False


def search_offline(
    query: str,
    mc_version: str = "",
    loader: str = "",
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """V1.0.2 新增: 离线模糊搜索模组

    Args:
        query: 搜索关键词（支持中英文、别名）
        mc_version: MC版本（可选）
        loader: 加载器（可选）
        limit: 返回数量上限

    Returns:
        匹配的模组列表
    """
    cache_key = f"offline_search:{query.lower()}:{mc_version}:{loader}:{limit}"
    now = time.time()

    # 检查本地缓存
    if cache_key in _query_cache:
        expire_at, value = _query_cache[cache_key]
        if expire_at > now:
            return value

    results = []
    query_lower = query.lower().strip()

    # 1. 从热门模组索引搜索
    for slug, mod_info in HOT_MOD_INDEX.items():
        score = 0

        # 精确匹配 slug
        if slug.lower() == query_lower:
            score = 100
        # 匹配别名
        elif query_lower in [a.lower() for a in mod_info["aliases"]]:
            score = 90
        # slug 包含
        elif query_lower in slug.lower():
            score = 70
        # 别名包含
        elif any(query_lower in a.lower() for a in mod_info["aliases"]):
            score = 60
        # 中文名包含
        elif query_lower in mod_info["name_cn"].lower():
            score = 55
        # 英文名包含
        elif query_lower in mod_info["name_en"].lower():
            score = 50

        if score > 0:
            result = {
                "slug": mod_info["slug"],
                "title": mod_info["name_en"],
                "name_cn": mod_info["name_cn"],
                "description": f"[离线数据库] {mod_info['name_cn']} - {', '.join(mod_info['categories'])}",
                "categories": mod_info["categories"],
                "source": "offline_index",
                "match_score": score,
                "aliases": mod_info["aliases"],
            }

            # 如果指定了 MC 版本和加载器，尝试获取版本信息
            if mc_version or loader:
                rec_data = load_recommendations()
                mod_data = rec_data.get("mods", {}).get(slug, {})
                version_info = _get_version_from_recommendations(mod_data, mc_version, loader)
                if version_info:
                    result["version_info"] = version_info

            results.append(result)

    # 2. 从兼容规则库搜索
    if len(results) < limit:
        rec_data = load_recommendations()
        mods_db = rec_data.get("mods", {})

        for slug, mod_data in mods_db.items():
            if any(r["slug"] == slug for r in results):
                continue

            score = 0
            name_cn = mod_data.get("name_cn", "")
            name_en = mod_data.get("name_en", "")
            description = mod_data.get("description", "")
            categories = mod_data.get("categories", [])

            if query_lower == slug.lower():
                score = 80
            elif query_lower in slug.lower():
                score = 65
            elif query_lower in name_cn.lower():
                score = 55
            elif query_lower in name_en.lower():
                score = 50
            elif query_lower in description.lower():
                score = 30
            elif any(query_lower in c.lower() for c in categories):
                score = 25

            if score > 0:
                result = {
                    "slug": slug,
                    "title": name_en or slug,
                    "name_cn": name_cn,
                    "description": description or "[离线数据库]",
                    "categories": categories,
                    "source": "offline_recommendations",
                    "match_score": score,
                }

                # 获取版本信息
                version_info = _get_version_from_recommendations(mod_data, mc_version, loader)
                if version_info:
                    result["version_info"] = version_info

                results.append(result)

    # 3. 按匹配分数排序
    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    results = results[:limit]

    # 写入本地缓存
    _query_cache[cache_key] = (now + QUERY_CACHE_TTL, results)

    return results


def _get_version_from_recommendations(
    mod_data: Dict,
    mc_version: str = "",
    loader: str = "",
) -> Optional[Dict[str, Any]]:
    """从兼容规则库获取版本信息

    Args:
        mod_data: 模组数据
        mc_version: MC版本
        loader: 加载器

    Returns:
        版本信息字典
    """
    if not mod_data:
        return None

    versions_db = mod_data.get("minecraft_versions", {})

    if not mc_version:
        # 返回所有版本
        return {
            "available_versions": list(versions_db.keys()),
            "all_versions": versions_db,
        }

    if mc_version not in versions_db:
        return None

    loader_data = versions_db[mc_version]

    if not loader:
        return {
            "mc_version": mc_version,
            "available_loaders": list(loader_data.keys()),
            "versions": loader_data,
        }

    if loader not in loader_data:
        return None

    return {
        "mc_version": mc_version,
        "loader": loader,
        "recommended": loader_data[loader].get("recommended", ""),
        "minimum": loader_data[loader].get("minimum", ""),
        "notes": loader_data[loader].get("notes", ""),
    }


def get_mod_version_offline(
    slug: str,
    mc_version: str,
    loader: str,
) -> Optional[Dict[str, Any]]:
    """V1.0.2 新增: 离线获取模组版本信息

    Args:
        slug: 模组 slug
        mc_version: MC 版本
        loader: 加载器

    Returns:
        版本信息字典
    """
    rec_data = load_recommendations()
    mod_data = rec_data.get("mods", {}).get(slug, {})

    if not mod_data:
        # 尝试从热门索引中查找
        if slug in HOT_MOD_INDEX:
            mod_data = {
                "name_cn": HOT_MOD_INDEX[slug]["name_cn"],
                "name_en": HOT_MOD_INDEX[slug]["name_en"],
                "minecraft_versions": {},
            }
        else:
            return None

    version_info = _get_version_from_recommendations(mod_data, mc_version, loader)

    if version_info:
        return {
            "slug": slug,
            "name_cn": mod_data.get("name_cn", ""),
            "name_en": mod_data.get("name_en", ""),
            "source": "offline_database",
            "version_info": version_info,
            "available": True,
        }

    return {
        "slug": slug,
        "name_cn": mod_data.get("name_cn", ""),
        "name_en": mod_data.get("name_en", ""),
        "source": "offline_database",
        "available": False,
        "message": f"本地数据库中无 {slug} 在 MC {mc_version} + {loader} 的版本信息",
    }


def search_by_category_offline(
    category: str,
    mc_version: str = "",
    loader: str = "",
) -> List[Dict[str, Any]]:
    """V1.0.2 新增: 离线按分类搜索模组

    Args:
        category: 分类 ID
        mc_version: MC版本
        loader: 加载器

    Returns:
        该分类下的模组列表
    """
    results = []

    # 从热门索引按分类筛选
    for slug, mod_info in HOT_MOD_INDEX.items():
        if category in mod_info.get("categories", []):
            result = {
                "slug": mod_info["slug"],
                "title": mod_info["name_en"],
                "name_cn": mod_info["name_cn"],
                "description": f"[离线分类] {mod_info['name_cn']}",
                "categories": mod_info["categories"],
                "source": "offline_category",
            }

            # 获取版本信息
            version_info = get_mod_version_offline(slug, mc_version, loader)
            if version_info and version_info.get("available"):
                result["version_info"] = version_info["version_info"]

            results.append(result)

    return results


def get_all_offline_mods() -> Dict[str, Any]:
    """V1.0.2 新增: 获取所有离线模组索引

    Returns:
        统计信息和模组列表
    """
    rec_data = load_recommendations()
    mods_count = len(rec_data.get("mods", {}))
    hot_count = len(HOT_MOD_INDEX)

    # 统计分类
    category_stats: Dict[str, int] = {}
    for mod_info in HOT_MOD_INDEX.values():
        for cat in mod_info.get("categories", []):
            category_stats[cat] = category_stats.get(cat, 0) + 1

    return {
        "total_hot_mods": hot_count,
        "total_recommendation_mods": mods_count,
        "total_indexed_mods": hot_count + mods_count,
        "categories": category_stats,
        "has_recommendations_db": bool(rec_data.get("mods")),
        "recommendations_last_updated": rec_data.get("_meta", {}).get("last_updated", ""),
    }


def clear_query_cache() -> None:
    """清空本地查询缓存"""
    global _query_cache
    _query_cache.clear()
    logger.info("离线查询缓存已清空")


def is_offline_available() -> bool:
    """检查离线数据库是否可用"""
    try:
        rec_data = load_recommendations()
        has_recs = bool(rec_data.get("mods"))
        has_hot = len(HOT_MOD_INDEX) > 0
        return has_recs or has_hot
    except Exception:
        return False


def get_offline_stats() -> Dict[str, Any]:
    """获取离线数据库统计"""
    return {
        "hot_mod_index_count": len(HOT_MOD_INDEX),
        "query_cache_entries": len(_query_cache),
        "recommendations_file_exists": RECOMMENDATIONS_FILE.exists(),
        "recommendations_file_size": (
            RECOMMENDATIONS_FILE.stat().st_size if RECOMMENDATIONS_FILE.exists() else 0
        ),
        "is_available": is_offline_available(),
    }
