# -*- coding: utf-8 -*-
"""F2: AI联网模组智能检索与精准下载

对接Modrinth和CurseForge官方API，按模组名称/关键词检索，
按MC版本和加载器过滤，自动匹配前置依赖，下载正版JAR文件，
生成适配清单。

V1.0.1 增强:
    - 支持批量关键词搜索（一次性搜索多个模组）
    - 支持分类搜索（预定义分类 + 动态分类）
    - 支持同类模组推荐
    - 动态获取Modrinth所有可用分类（支持世界上所有模组类型）
    - 每次搜索后自动更新兼容规则库（保持数据实时性）

使用方式:
    from core.mod_searcher import run
    import argparse
    args = argparse.Namespace(
        query="Create",
        mc_version="1.21.1",
        loader="neoforge",
        download=True,
        with_deps=True,
        platform="modrinth",
        output=None,
        category=None,  # 可选: 预定义分类(create/fun/tech/...) 或 动态分类(modrinth分类名)
        batch_mode=False,  # 批量搜索模式
        queries=None  # 批量搜索关键词列表
    )
    result = run(args)
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.api_client import (
    get_modrinth_client,
    get_curseforge_client,
    LOADER_TO_CURSEFORGE,
)
from utils.report_gen import ReportGenerator, generate_unified_output

logger = get_logger("mod_searcher")

# === 模组分类索引 (V1.0.1 新增) ===
# 预定义热门模组分类，便于分类搜索和推荐
MOD_CATEGORIES = {
    "create": {
        "name_cn": "机械动力系列",
        "keywords": ["create", "机械动力", "蒸汽与铁轨", "运算", "航空学", "回收", "切切乐", "飞轮"],
        "mod_ids": [
            "create", "create_railways", "steam_n_rails", "createaddition",
            "create_calculation", "create_aeronautics", "createrecycle",
            "create_crafts_and_additions", "create_deco", "createdeco_official",
            "sliceanddice", "create_addition", "copycats", "flywheel",
            "create_factory", "create_enchantment_industry", "create_minecraft_industrial",
        ],
        "description": "基于 Create 的机械自动化模组家族，包括蒸汽、运算、航空等多个扩展"
    },
    "fun": {
        "name_cn": "乐事系列",
        "keywords": ["乐事", "农夫乐事", "厨房", "欢乐", "fun"],
        "mod_ids": [
            "fun-mod", "fun-addon", "farmersdelight", "kitchensdelight",
            "cookingforblockheads", "spiceoflife", "pamharvestcraft",
            "extrabowman",
        ],
        "description": "休闲娱乐、烹饪美食相关的模组系列"
    },
    "tech": {
        "name_cn": "科技能源类",
        "keywords": ["工业", "能源", "电力", "机械", "应用能源", "热力", "林业"],
        "mod_ids": [
            "ic2", "ic2-classic", "ae2", "forestry", "thermal-core",
            "thermal-expansion", "thermal-dynamics", "mekanism",
            "immersiveengineering", "immersiveposts", "techreborn",
            "actuallyadditions", "extrautils2", "bigreactors",
            "draconicevolution",
        ],
        "description": "科技向模组，包括工业、能源、电力系统等"
    },
    "redstone": {
        "name_cn": "红石魔改类",
        "keywords": ["红石", "redstone", "buildcraft", "物流", "管道", "网络"],
        "mod_ids": [
            "redstoneflux", "buildcraft", "railcraft", "logisticspipes",
            "logisticsbuddies", "xnet", "refinedstorage", "draconicevolution",
            "cyclic", "openblocks", "tmechworks", "rftools",
            "endertheory", "computer-craft", "opencomputers",
        ],
        "description": "红石自动化、物流管道、计算机等魔改类模组"
    },
    "magic": {
        "name_cn": "魔法类",
        "keywords": ["神秘", "魔法", "巫术", "炼金术", "thaumcraft"],
        "mod_ids": [
            "thaumcraft", "arsmagica", "bloodmagic", "roots", "witchery",
            "psi", "bluepower", "amnether", "forbidden",
            "astral",
        ],
        "description": "魔法、神秘学、巫术、炼金术等魔法类模组"
    },
    "storage": {
        "name_cn": "仓储类",
        "keywords": ["存储", "抽屉", "箱子", "物流", "物品", "仓储"],
        "mod_ids": [
            "storagedrawers", "ironchest", "ae2", "refinedstorage",
            "applied-energistics-2", "deepstorage", "easy-villagers",
            "industrialforegoing", "endertheory", "xnet",
        ],
        "description": "物品存储、物流管理、仓储类模组"
    },
    "adventure": {
        "name_cn": "冒险类",
        "keywords": ["冒险", "暮色", "探索", "地牢", "boss"],
        "mod_ids": [
            "twilightforest", "twilightforest-dungeons", "aether",
            "better-dungeons", "cataclysm", "minecraft-butcher",
            "savage-and-ravage", "quark", "blueprint",
            "epic-knights", "ancient-ancestry",
        ],
        "description": "冒险探索、地牢、BOSS战等冒险类模组"
    },
    "survival": {
        "name_cn": "生存类",
        "keywords": ["生存", "难度", "挑战", "hardcore", "survival"],
        "mod_ids": [
            "extrautils2", "cyclic", "openblocks", "tough-as-nails",
            "hardcore-darkness", "scaling-health", "progressive-difficulty",
            "cold-sweat", "better-spawn", "improved-vanilla",
        ],
        "description": "生存挑战、难度调整、硬核生存等模组"
    },
    "decoration": {
        "name_cn": "装饰类",
        "keywords": ["装饰", "家具", "灯光", "窗帘", "装饰"],
        "mod_ids": [
            "create_deco", "createdeco_official", "openblocks",
            "chisel", "chisels-and-bits", "bits",
            "supplementaries", "decorative-blocks", "lightspeed",
            "fairy-lights", "ceiling-cinema",
        ],
        "description": "家具、装饰方块、灯光、建筑装饰等模组"
    },
    "mobs": {
        "name_cn": "生物类",
        "keywords": ["生物", "怪物", "动物", "宠物", "mob"],
        "mod_ids": [
            "tconstruct", "extrabowman", "morph", "farmersdelight",
            "forestry", "animania", "familiar-foxes",
            "mob-blocks", "more-mob-eggs", "savage-and-ravage",
            "epic-knights",
        ],
        "description": "新增生物、怪物、动物、宠物等模组"
    },
    "equipment": {
        "name_cn": "装备工具类",
        "keywords": ["装备", "工具", "武器", "盔甲", "weapon"],
        "mod_ids": [
            "tconstruct", "create", "extrabowman", "farmersdelight",
            "mekanism", "draconicevolution", "twilightforest",
            "arsmagica", "bloodmagic", "psi", "roots",
            "immersiveengineering",
        ],
        "description": "武器、盔甲、工具装备类模组"
    },
    "food": {
        "name_cn": "食物与农作物类",
        "keywords": ["食物", "烹饪", "农作物", "农场", "food"],
        "mod_ids": [
            "farmersdelight", "kitchensdelight", "cookingforblockheads",
            "spiceoflife", "pamharvestcraft", "fun-mod",
            "forestry", "extrabowman",
        ],
        "description": "食物、烹饪、农业、农作物相关模组"
    },
    "worldgen": {
        "name_cn": "世界元素类",
        "keywords": ["世界", "地形", "洞穴", "生物群系", "world"],
        "mod_ids": [
            "twilightforest", "aether", "better-biomes",
            "biomes-o-plenty", "biomes-you-want", "cave-enhancement",
            "cavernous", "yung's-api", "terralith",
            "amplified-nether", "deep-dark-exploration",
        ],
        "description": "世界生成、地形生成、洞穴、生物群系等模组"
    },
    "gameplay": {
        "name_cn": "游戏机制类",
        "keywords": ["机制", "玩法", "系统", "skill", "gameplay"],
        "mod_ids": [
            "morph", "appleskin", "spiceoflife", "pamharvestcraft",
            "cyclic", "openblocks", "extrautils2",
            "supplementaries", "better-spawn", "progressive-difficulty",
        ],
        "description": "游戏机制、玩法系统、技能系统等模组"
    },
    "performance": {
        "name_cn": "性能优化类",
        "keywords": ["优化", "渲染", "性能", "内存", "优化"],
        "mod_ids": [
            "sodium", "iris", "oculus", "ferritecore", "embeddium",
            "lithium", "phosphor", "starlight", "modernui",
        ],
        "description": "游戏性能优化、渲染优化类模组"
    },
    "utility": {
        "name_cn": "实用工具类",
        "keywords": ["工具", "实用", "图鉴", "按键", "提示"],
        "mod_ids": [
            "jei", "jade", "appleskin", "controlling", "modmenu",
            "cloth-config", "forge-config-api",
        ],
        "description": "游戏实用工具、辅助功能类模组"
    },
}


# === V1.0.1 新增: 动态分类获取与自动更新 ===

# 兼容规则库文件路径
RECOMMENDATIONS_FILE = _PROJECT_ROOT / "data" / "mod_version_recommendations.json"

# 动态分类缓存
_dynamic_categories_cache = None
_dynamic_categories_cache_time = 0

def fetch_dynamic_categories(force_refresh: bool = False) -> List[Dict[str, Any]]:
    """从Modrinth API动态获取所有可用的模组分类

    Args:
        force_refresh: 是否强制刷新缓存

    Returns:
        分类列表 [{"id": "mod", "name": "Mod", "description": "...", "mod_count": 0}]
    """
    global _dynamic_categories_cache, _dynamic_categories_cache_time
    
    # 缓存1小时
    if not force_refresh and _dynamic_categories_cache:
        if time.time() - _dynamic_categories_cache_time < 3600:
            return _dynamic_categories_cache
    
    try:
        client = get_modrinth_client()
        raw_categories = client.get_categories()
        
        dynamic_categories = []
        for cat in raw_categories:
            category_id = cat.get("category", "")
            if category_id and category_id != "mod":  # 排除mod本身
                dynamic_categories.append({
                    "id": category_id,
                    "name": cat.get("name", category_id),
                    "description": cat.get("description", ""),
                    "project_type": cat.get("project_type", "mod"),
                    "icon": cat.get("icon", ""),
                })
        
        # 按名称排序
        dynamic_categories.sort(key=lambda x: x["name"])
        
        _dynamic_categories_cache = dynamic_categories
        _dynamic_categories_cache_time = time.time()
        
        logger.info(f"动态获取到 {len(dynamic_categories)} 个模组分类")
        return dynamic_categories
        
    except Exception as e:
        logger.error(f"获取动态分类失败: {e}")
        return []


def get_all_categories(force_refresh: bool = False) -> Dict[str, Any]:
    """获取所有分类（包括预定义分类和动态分类）

    Args:
        force_refresh: 是否强制刷新

    Returns:
        {
            "preset_categories": [...],
            "dynamic_categories": [...],
            "total_count": int
        }
    """
    # 预定义分类
    preset = [
        {
            "id": cat_id,
            "name_cn": cat["name_cn"],
            "description": cat["description"],
            "mod_count": len(cat["mod_ids"]),
            "source": "preset",
        }
        for cat_id, cat in MOD_CATEGORIES.items()
    ]
    
    # 动态分类
    dynamic = fetch_dynamic_categories(force_refresh)
    
    return {
        "preset_categories": preset,
        "dynamic_categories": dynamic,
        "total_count": len(preset) + len(dynamic),
    }


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


def update_mod_recommendations(
    mod_id: str,
    mod_name_cn: str,
    mod_info: Dict[str, Any]
) -> bool:
    """更新单个模组的兼容规则库条目

    如果模组已存在则更新，不存在则新增。

    Args:
        mod_id: 模组ID/slug
        mod_name_cn: 模组中文名
        mod_info: 模组信息，包含 mc_versions 等

    Returns:
        是否更新成功
    """
    try:
        # 加载现有数据
        data = load_recommendations()
        mods = data.get("mods", {})
        
        # 构建新的模组条目
        new_entry = {
            "name_cn": mod_name_cn,
            "name_en": mod_info.get("name_en", ""),
            "source": "auto_updated",
            "last_updated": time.strftime("%Y-%m-%d"),
            "description": mod_info.get("description", ""),
            "categories": mod_info.get("categories", []),
            "minecraft_versions": mod_info.get("minecraft_versions", {}),
        }
        
        # 更新或新增
        if mod_id in mods:
            # 合并更新
            existing = mods[mod_id]
            # 保留原有的手动添加内容，合并新获取的版本信息
            for mc_ver, loader_data in new_entry["minecraft_versions"].items():
                if mc_ver not in existing.get("minecraft_versions", {}):
                    existing.setdefault("minecraft_versions", {})[mc_ver] = loader_data
                else:
                    # 更新版本信息
                    for loader, ver_info in loader_data.items():
                        if ver_info.get("recommended"):
                            existing["minecraft_versions"][mc_ver][loader] = ver_info
            
            # 更新元数据
            existing["last_updated"] = new_entry["last_updated"]
            existing["source"] = "auto_updated_merged"
            mods[mod_id] = existing
        else:
            # 新增
            mods[mod_id] = new_entry
            logger.info(f"新增模组到兼容规则库: {mod_id} ({mod_name_cn})")
        
        # 更新元信息
        if "_meta" not in data:
            data["_meta"] = {}
        data["_meta"]["last_updated"] = time.strftime("%Y-%m-%d")
        data["_meta"]["total_mods"] = len(mods)
        data["_meta"]["auto_update"] = True
        
        # 保存
        data["mods"] = mods
        return save_recommendations(data)
        
    except Exception as e:
        logger.error(f"更新兼容规则库失败 ({mod_id}): {e}")
        return False


def auto_update_recommendations_from_search(
    search_results: List[Dict],
    mc_version: str,
    loader: str
) -> int:
    """根据搜索结果自动更新兼容规则库

    Args:
        search_results: 搜索结果列表
        mc_version: MC版本
        loader: 加载器

    Returns:
        更新的模组数量
    """
    updated_count = 0
    
    for mod in search_results:
        slug = mod.get("slug", "")
        title = mod.get("title", slug)
        categories = mod.get("categories", [])
        
        # 获取版本信息
        versions = get_version_info(slug, loader, mc_version)
        
        # 构建版本信息
        version_info = {}
        if versions:
            latest = versions[0]
            version_info = {
                mc_version: {
                    loader: {
                        "recommended": latest.get("version_number", ""),
                        "minimum": latest.get("version_number", ""),
                        "notes": f"自动获取于 {time.strftime('%Y-%m-%d')}",
                    }
                }
            }
        
        # 更新兼容规则库
        mod_info = {
            "name_en": title,
            "description": mod.get("description", ""),
            "categories": categories,
            "minecraft_versions": version_info,
        }
        
        if update_mod_recommendations(slug, title, mod_info):
            updated_count += 1
    
    if updated_count > 0:
        logger.info(f"自动更新了 {updated_count} 个模组的兼容规则")
    
    return updated_count


# === V1.0.1 新增: 分类搜索和推荐功能 ===

def get_categories_list(include_dynamic: bool = False) -> List[Dict[str, Any]]:
    """获取所有可用的模组分类列表

    Args:
        include_dynamic: 是否包含动态分类（从API获取）

    Returns:
        分类列表 [{"id": "create", "name_cn": "机械动力系列", "description": "...", "source": "preset"}]
    """
    categories = []
    
    # 预定义分类
    for cat_id, cat in MOD_CATEGORIES.items():
        categories.append({
            "id": cat_id,
            "name_cn": cat["name_cn"],
            "description": cat["description"],
            "mod_count": len(cat["mod_ids"]),
            "source": "preset",
        })
    
    # 动态分类（可选）
    if include_dynamic:
        dynamic = fetch_dynamic_categories()
        for cat in dynamic:
            categories.append({
                "id": cat["id"],
                "name_cn": cat["name"],
                "description": cat["description"],
                "mod_count": 0,
                "source": "dynamic",
            })
    
    return categories


def search_by_category(
    category: str, mc_version: str, loader: str, platform: str = "both"
) -> Dict[str, Any]:
    """按分类搜索模组（支持预定义分类和动态分类）

    Args:
        category: 分类ID (预定义: create/fun/tech/... 或动态: modrinth分类名)
        mc_version: MC版本
        loader: 加载器
        platform: 平台偏好

    Returns:
        分类搜索结果，包含分类信息和所有匹配的模组
    """
    # 检查是否是预定义分类
    if category in MOD_CATEGORIES:
        cat_info = MOD_CATEGORIES[category]
        all_results = []
        search_cache = {}

        # 逐个搜索分类中的关键词
        for keyword in cat_info["keywords"][:3]:  # 限制搜索数量，避免API限流
            if keyword in search_cache:
                continue

            results = []
            if platform in ("modrinth", "both"):
                results.extend(search_modrinth(keyword, mc_version, loader, limit=5))
            if platform in ("curseforge", "both"):
                results.extend(search_curseforge(keyword, mc_version, loader))

            # 按slug去重
            seen_slugs = set()
            unique_results = []
            for r in results:
                slug = r.get("slug", "")
                if slug and slug not in seen_slugs:
                    seen_slugs.add(slug)
                    unique_results.append(r)

            search_cache[keyword] = unique_results
            all_results.extend(unique_results)
            time.sleep(0.5)  # 避免API限流

        # 按下载量排序
        all_results.sort(key=lambda x: x.get("downloads", 0), reverse=True)

        return {
            "success": True,
            "category": {
                "id": category,
                "name_cn": cat_info["name_cn"],
                "description": cat_info["description"],
                "source": "preset",
            },
            "results": all_results,
            "total": len(all_results),
            "search_mode": "preset_keyword_search",
        }
    
    # 检查是否是动态分类（从Modrinth分类API）
    dynamic_categories = fetch_dynamic_categories()
    dynamic_ids = [cat["id"] for cat in dynamic_categories]
    
    if category in dynamic_ids:
        # 使用Modrinth API的categories过滤进行搜索
        cat_info = next((c for c in dynamic_categories if c["id"] == category), None)
        
        results = []
        if platform in ("modrinth", "both"):
            # 使用分类过滤搜索
            try:
                client = get_modrinth_client()
                facets = [["project_type:mod"], [f"categories:{category}"]]
                if mc_version:
                    facets.append([f"versions:{mc_version}"])
                if loader:
                    facets.append([f"categories:{loader}"])
                
                params = {
                    "query": "",
                    "facets": json.dumps(facets),
                    "limit": 20,
                }
                response = client.get("search", params=params)
                hits = response.get("hits", [])
                
                for hit in hits:
                    results.append({
                        "slug": hit.get("project_id", ""),
                        "title": hit.get("title", ""),
                        "description": hit.get("description", ""),
                        "source": "modrinth",
                        "downloads": hit.get("downloads", 0),
                        "categories": hit.get("categories", []),
                        "project_type": hit.get("project_type", "mod"),
                    })
            except Exception as e:
                logger.error(f"动态分类搜索失败: {e}")
        
        # 按下载量排序
        results.sort(key=lambda x: x.get("downloads", 0), reverse=True)
        
        return {
            "success": True,
            "category": {
                "id": category,
                "name_cn": cat_info["name"] if cat_info else category,
                "description": cat_info["description"] if cat_info else "",
                "source": "dynamic",
            },
            "results": results,
            "total": len(results),
            "search_mode": "dynamic_category_filter",
        }
    
    # 未知分类
    all_categories = get_categories_list(include_dynamic=True)
    return {
        "success": False,
        "error": f"未知分类: {category}",
        "available_preset": [c["id"] for c in all_categories if c["source"] == "preset"],
        "available_dynamic_count": len([c for c in all_categories if c["source"] == "dynamic"]),
        "hint": "使用 get_categories_list(include_dynamic=True) 查看所有可用分类",
    }


def batch_search(
    queries: List[str],
    mc_version: str,
    loader: str,
    platform: str = "both",
    download: bool = False,
    with_deps: bool = False,
) -> Dict[str, Any]:
    """批量搜索多个关键词

    Args:
        queries: 关键词列表
        mc_version: MC版本
        loader: 加载器
        platform: 平台偏好
        download: 是否下载
        with_deps: 是否下载依赖

    Returns:
        批量搜索结果汇总
    """
    if not queries:
        return {"success": False, "error": "搜索关键词列表不能为空"}

    batch_results = []
    all_downloaded = []
    all_failed = []

    for query in queries:
        query = query.strip()
        if not query:
            continue

        logger.info(f"[批量] 搜索: {query}")

        # 搜索
        modrinth_results = []
        curseforge_results = []

        if platform in ("modrinth", "both"):
            modrinth_results = search_modrinth(query, mc_version, loader, limit=3)

        if platform in ("curseforge", "both"):
            curseforge_results = search_curseforge(query, mc_version, loader)

        merged = merge_results(modrinth_results, curseforge_results)

        query_result = {
            "query": query,
            "results_count": len(merged),
            "results": merged[:3],
        }

        # 下载（如果需要）
        if download and merged:
            top_mod = merged[0]
            slug = top_mod["slug"]
            source = top_mod["source"]
            versions = get_version_info(slug, loader, mc_version, source)

            if versions:
                latest = versions[0]
                if latest.get("download_url"):
                    dl_dir = config.DOWNLOADS_DIR
                    dl_dir.mkdir(parents=True, exist_ok=True)
                    file_name = latest.get("file_name", f"{slug}.jar")
                    result = download_mod(latest["download_url"], dl_dir, file_name)

                    if result:
                        all_downloaded.append({
                            "query": query,
                            "title": top_mod["title"],
                            "slug": slug,
                            "version": latest["version_number"],
                            "file_name": result.name,
                            "file_size": result.stat().st_size,
                        })
                        query_result["downloaded"] = True
                    else:
                        all_failed.append({
                            "query": query,
                            "title": top_mod["title"],
                            "slug": slug,
                            "error": "下载失败",
                        })
                        query_result["downloaded"] = False

        batch_results.append(query_result)
        time.sleep(0.3)  # 避免API限流

    return {
        "success": True,
        "batch_size": len(queries),
        "processed_count": len(batch_results),
        "results": batch_results,
        "downloaded": all_downloaded,
        "failed": all_failed,
    }


def find_similar_mods(
    query: str, mc_version: str, loader: str, limit: int = 5
) -> List[Dict]:
    """根据模组推荐同类/相关模组

    Args:
        query: 模组名称或关键词
        mc_version: MC版本
        loader: 加载器
        limit: 返回数量

    Returns:
        相关模组列表
    """
    # 1. 先确定模组所属分类
    matched_categories = []
    query_lower = query.lower()

    for cat_id, cat_info in MOD_CATEGORIES.items():
        for keyword in cat_info["keywords"]:
            if keyword.lower() in query_lower or query_lower in keyword.lower():
                matched_categories.append(cat_id)
                break

    # 2. 从匹配的分类中推荐模组
    recommendations = []
    seen_slugs = set()

    for cat_id in matched_categories:
        cat_info = MOD_CATEGORIES[cat_id]
        for mod_id in cat_info["mod_ids"]:
            if mod_id not in seen_slugs:
                seen_slugs.add(mod_id)
                recommendations.append({
                    "mod_id": mod_id,
                    "category": cat_id,
                    "category_name": cat_info["name_cn"],
                })

    # 3. 如果没有匹配分类，尝试搜索推荐
    if not recommendations:
        search_results = search_modrinth(f"{query} mod", mc_version, loader, limit=limit*2)
        for r in search_results:
            recommendations.append({
                "mod_id": r.get("slug", ""),
                "category": "search",
                "category_name": "搜索推荐",
                "title": r.get("title", ""),
                "description": r.get("description", ""),
                "downloads": r.get("downloads", 0),
            })

    return recommendations[:limit]


def generate_category_html(
    category_result: Dict[str, Any],
) -> str:
    """生成分类搜索结果HTML

    Args:
        category_result: 分类搜索结果

    Returns:
        HTML内容
    """
    gen = ReportGenerator(feature="mod_searcher")
    content = ""

    if category_result.get("success"):
        cat = category_result["category"]
        results = category_result["results"]

        # 分类信息
        info_rows = [
            ["分类名称", cat["name_cn"]],
            ["分类描述", cat["description"]],
            ["搜索关键词", ", ".join(category_result.get("keywords_used", []))],
            ["找到模组数", category_result.get("total_found", 0)],
        ]
        content += gen.render_section("分类信息", gen.render_table(["参数", "值"], info_rows))

        # 模组列表
        if results:
            result_rows = []
            for r in results:
                result_rows.append([
                    r.get("title", "N/A"),
                    r.get("source", ""),
                    r.get("slug", ""),
                    f"{r.get('downloads', 0):,}",
                ])
            content += gen.render_section(
                f"模组列表 (共{len(results)}个)",
                gen.render_table(["模组名", "来源", "Slug", "下载量"], result_rows)
            )
    else:
        content = gen.render_callout(
            "错误",
            f"<p>{category_result.get('error', '未知错误')}</p>",
            level="red"
        )
        if category_result.get("categories"):
            cat_rows = [[c["id"], c["name_cn"], str(c["mod_count"])] for c in category_result["categories"]]
            content += gen.render_section(
                "可用分类",
                gen.render_table(["ID", "名称", "模组数量"], cat_rows)
            )

    return content


def generate_batch_html(
    batch_result: Dict[str, Any],
) -> str:
    """生成批量搜索结果HTML

    Args:
        batch_result: 批量搜索结果

    Returns:
        HTML内容
    """
    gen = ReportGenerator(feature="mod_searcher")
    content = ""

    if batch_result.get("success"):
        # 批量信息
        info_rows = [
            ["批量大小", batch_result.get("batch_size", 0)],
            ["已处理", batch_result.get("processed_count", 0)],
            ["成功搜索", sum(1 for r in batch_result.get("results", []) if r.get("results_count", 0) > 0)],
            ["下载成功", len(batch_result.get("downloaded", []))],
            ["下载失败", len(batch_result.get("failed", []))],
        ]
        content += gen.render_section("批量搜索统计", gen.render_table(["参数", "值"], info_rows))

        # 结果列表
        results = batch_result.get("results", [])
        if results:
            result_rows = []
            for r in results:
                result_rows.append([
                    r["query"],
                    str(r.get("results_count", 0)),
                    "✅" if r.get("downloaded") else "—",
                    r.get("results", [{}])[0].get("title", "N/A") if r.get("results") else "N/A",
                ])
            content += gen.render_section(
                "批量搜索结果",
                gen.render_table(["关键词", "结果数", "已下载", "首个结果"], result_rows)
            )

        # 下载清单
        downloaded = batch_result.get("downloaded", [])
        if downloaded:
            dl_rows = [
                [d["query"], d["title"], d["version"], d["file_name"]]
                for d in downloaded
            ]
            content += gen.render_section(
                "下载清单",
                gen.render_table(["搜索词", "模组", "版本", "文件名"], dl_rows)
            )
    else:
        content = gen.render_callout(
            "错误",
            f"<p>{batch_result.get('error', '未知错误')}</p>",
            level="red"
        )

    return content


# === 原有搜索函数 ===

def search_modrinth(
    query: str, mc_version: str, loader: str, limit: int = 10
) -> List[Dict]:
    """从Modrinth搜索模组

    Args:
        query: 搜索关键词
        mc_version: MC版本
        loader: 加载器
        limit: 返回数量

    Returns:
        标准化后的模组列表
    """
    try:
        client = get_modrinth_client()
        raw = client.search(query, mc_version, loader, limit)

        results = []
        for hit in raw.get("hits", []):
            results.append({
                "source": "modrinth",
                "project_id": hit.get("project_id", ""),
                "slug": hit.get("slug", ""),
                "title": hit.get("title", ""),
                "description": hit.get("description", ""),
                "author": hit.get("author", ""),
                "categories": hit.get("categories", []),
                "versions": hit.get("versions", []),
                "downloads": hit.get("downloads", 0),
                "follows": hit.get("follows", 0),
                "date_created": hit.get("date_created", ""),
                "logo_url": hit.get("icon_url", ""),
            })

        logger.info(f"Modrinth搜索: {query} -> {len(results)} 个结果")
        return results

    except Exception as e:
        logger.error(f"Modrinth搜索失败: {e}")
        return []


def search_curseforge(
    query: str, mc_version: str, loader: str
) -> List[Dict]:
    """从CurseForge搜索模组

    Args:
        query: 搜索关键词
        mc_version: MC版本
        loader: 加载器

    Returns:
        标准化后的模组列表
    """
    try:
        client = get_curseforge_client()
        if not client.is_available():
            logger.warning("CurseForge API Key未配置，跳过CurseForge搜索")
            return []

        loader_type = LOADER_TO_CURSEFORGE.get(loader)
        raw = client.search(query, mc_version, loader_type)

        results = []
        for item in raw.get("data", []):
            results.append({
                "source": "curseforge",
                "project_id": str(item.get("id", "")),
                "slug": item.get("slug", ""),
                "title": item.get("name", ""),
                "description": item.get("summary", ""),
                "author": item.get("author", {}).get("name", "") if item.get("author") else "",
                "categories": [c.get("name", "") for c in item.get("categories", [])],
                "versions": [],
                "downloads": item.get("downloadCount", 0),
                "follows": 0,
                "date_created": item.get("dateCreated", ""),
                "logo_url": item.get("logoThumbnail", ""),
                "cf_mod_id": item.get("id"),
            })

        logger.info(f"CurseForge搜索: {query} -> {len(results)} 个结果")
        return results

    except Exception as e:
        logger.error(f"CurseForge搜索失败: {e}")
        return []


def merge_results(
    modrinth_results: List[Dict], curseforge_results: List[Dict]
) -> List[Dict]:
    """合并两个平台的搜索结果，按slug去重

    Args:
        modrinth_results: Modrinth结果
        curseforge_results: CurseForge结果

    Returns:
        合并后的结果列表
    """
    seen_slugs = set()
    merged = []

    for r in modrinth_results + curseforge_results:
        slug = r.get("slug", "")
        if slug and slug not in seen_slugs:
            seen_slugs.add(slug)
            merged.append(r)

    # 按下载量排序
    merged.sort(key=lambda x: x.get("downloads", 0), reverse=True)
    return merged


def get_version_info(
    slug: str, loader: str, mc_version: str, source: str = "modrinth"
) -> List[Dict]:
    """获取模组版本列表和依赖信息

    Args:
        slug: 模组slug
        loader: 加载器
        mc_version: MC版本
        source: 数据来源

    Returns:
        版本列表
    """
    try:
        if source == "modrinth":
            client = get_modrinth_client()
            versions = client.get_versions(slug, mc_version, loader)

            result = []
            for v in versions:
                files = v.get("files", [])
                primary_file = files[0] if files else {}
                result.append({
                    "version_id": v.get("id", ""),
                    "version_number": v.get("version_number", ""),
                    "date_published": v.get("date_published", ""),
                    "download_url": primary_file.get("url", ""),
                    "file_name": primary_file.get("filename", ""),
                    "file_size": primary_file.get("size", 0),
                    "dependencies": v.get("dependencies", []),
                    "game_versions": v.get("game_versions", []),
                    "loaders": v.get("loaders", []),
                    "release_type": v.get("version_type", ""),
                })

            return result

    except Exception as e:
        logger.error(f"获取版本信息失败 ({source}): {e}")
        return []


def resolve_dependencies(
    version_info: Dict, all_versions: Dict[str, List[Dict]]
) -> List[Dict]:
    """递归解析前置依赖

    Args:
        version_info: 版本信息
        all_versions: 已获取的所有版本信息缓存

    Returns:
        依赖列表
    """
    deps = []
    seen = set()

    def _resolve(dep_list, depth=0):
        if depth > 5:
            return  # 防止无限递归
        for dep in dep_list:
            dep_id = dep.get("project_id", "")
            if dep_id and dep_id not in seen:
                seen.add(dep_id)
                deps.append(dep)
                # 递归查找该依赖的依赖
                if dep_id in all_versions:
                    for v in all_versions[dep_id]:
                        if v.get("dependencies"):
                            _resolve(v["dependencies"], depth + 1)

    if version_info.get("dependencies"):
        _resolve(version_info["dependencies"])

    return deps


def download_mod(
    download_url: str, dest_dir: Path, file_name: str = None
) -> Optional[Path]:
    """下载模组JAR文件

    Args:
        download_url: 下载URL
        dest_dir: 目标目录
        file_name: 文件名（可选，从URL推断）

    Returns:
        下载文件的Path对象，失败返回None
    """
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        if not file_name:
            file_name = download_url.split("/")[-1].split("?")[0]
            if not file_name.endswith(".jar"):
                file_name += ".jar"

        dest_path = dest_dir / file_name
        client = get_modrinth_client()
        result = client.download(download_url, dest_path)
        return result

    except Exception as e:
        logger.error(f"下载失败: {file_name} - {e}")
        return None


def generate_search_html(
    query: str,
    mc_version: str,
    loader: str,
    results: List[Dict],
    downloaded: List[Dict],
    failed: List[Dict],
) -> str:
    """生成搜索结果HTML报告

    Args:
        query: 搜索关键词
        mc_version: MC版本
        loader: 加载器
        results: 搜索结果
        downloaded: 已下载模组
        failed: 下载失败模组

    Returns:
        HTML内容
    """
    gen = ReportGenerator(feature="mod_searcher")

    # 搜索参数
    info_rows = [
        ["搜索关键词", query],
        ["MC版本", mc_version],
        ["加载器", loader],
        ["结果数量", len(results)],
        ["已下载", len(downloaded)],
        ["下载失败", len(failed)],
    ]
    info_html = gen.render_table(["参数", "值"], info_rows)

    # 搜索结果列表
    if results:
        result_rows = []
        for r in results[:20]:
            result_rows.append([
                r["title"],
                r["source"],
                r["slug"],
                f"{r.get('downloads', 0):,}",
                r.get("description", "")[:80],
            ])
        results_html = gen.render_table(
            ["模组名", "来源", "Slug", "下载量", "描述"], result_rows
        )
    else:
        results_html = "<p class='muted'>未找到匹配的模组</p>"

    # 下载列表
    if downloaded:
        dl_rows = []
        for d in downloaded:
            dl_rows.append([
                d.get("title", ""),
                d.get("version", ""),
                d.get("file_name", ""),
                str(d.get("file_size", 0)),
                "✅",
            ])
        dl_html = gen.render_table(
            ["模组", "版本", "文件名", "大小", "状态"], dl_rows
        )
    else:
        dl_html = "<p class='muted'>未下载任何模组</p>"

    # 失败列表
    if failed:
        fail_rows = [
            [f["title"], f["error"]]
            for f in failed
        ]
        fail_html = gen.render_table(["模组", "错误信息"], fail_rows)
    else:
        fail_html = ""

    # 依赖关系提示
    dep_warning = ""
    if downloaded:
        dep_warning = gen.render_callout(
            "依赖关系",
            "<p>已下载的模组可能需要额外的前置依赖。"
            "请检查下载目录中的所有JAR文件，确保没有遗漏。"
            "如需自动解析依赖，请使用 --with-deps 参数。</p>",
            level="info",
        )

    content = gen.render_section("搜索参数", info_html, tag="search_info")
    content += gen.render_section("搜索结果", results_html, tag="results")
    if downloaded:
        content += gen.render_section("下载清单", dl_html, tag="downloaded")
    if fail_html:
        content += gen.render_section("下载失败", fail_html, tag="failed")
    if dep_warning:
        content += dep_warning

    return content


def run(args) -> Dict[str, Any]:
    """F2 模组检索下载主入口 (V1.0.1 增强版)

    支持三种搜索模式:
        1. 关键词搜索 (query) - 原有功能
        2. 分类搜索 (category) - V1.0.1 新增
        3. 批量搜索 (batch_mode + queries) - V1.0.1 新增

    Args:
        args: argparse.Namespace，需包含:
            - query: 搜索关键词（单条搜索）
            - category: 分类ID（分类搜索）
            - queries: 关键词列表（批量搜索）
            - batch_mode: 是否启用批量模式
            - mc_version: MC版本
            - loader: 加载器类型
            - download: 是否下载（默认True）
            - with_deps: 是否下载依赖（默认True）
            - platform: 平台偏好（modrinth/curseforge/both）
            - output: 输出目录

    Returns:
        统一返回结构字典
    """
    query = getattr(args, 'query', '')
    category = getattr(args, 'category', None)
    batch_mode = getattr(args, 'batch_mode', False)
    queries = getattr(args, 'queries', None)
    mc_version = args.mc_version
    loader = args.loader
    do_download = getattr(args, "download", True)
    with_deps = getattr(args, "with_deps", True)
    platform = getattr(args, "platform", "modrinth")
    output = getattr(args, "output", None)

    # === V1.0.1 新增: 分类搜索模式 ===
    if category:
        if loader not in config.LOADERS:
            return config.build_result(
                feature="mod_searcher",
                status="error",
                input_summary={"category": category, "loader": loader},
                result={},
                errors=[f"无效的加载器类型: {loader}，支持: {', '.join(config.LOADERS)}"],
            )

        logger.info(f"分类搜索: {category} (MC={mc_version}, Loader={loader})")
        category_result = search_by_category(category, mc_version, loader, platform)

        # V1.0.1 新增: 自动更新兼容规则库
        auto_update_recommendations_from_search(
            category_result.get("results", []),
            mc_version,
            loader
        )

        html_content = generate_category_html(category_result)

        return config.build_result(
            feature="mod_searcher",
            status="success" if category_result.get("success") else "error",
            input_summary={
                "mode": "category",
                "category": category,
                "mc_version": mc_version,
                "loader": loader,
            },
            result={
                "category_info": category_result.get("category", {}),
                "results_count": len(category_result.get("results", [])),
                "results": category_result.get("results", []),
            },
            output_files=generate_unified_output(
                feature="mod_searcher",
                status="success" if category_result.get("success") else "error",
                input_summary={"mode": "category", "category": category},
                result=category_result,
                title=f"分类搜索报告 - {category_result.get('category', {}).get('name_cn', category)}",
                html_content=html_content,
            ),
        )

    # === V1.0.1 新增: 批量搜索模式 ===
    if batch_mode or (queries and len(queries) > 1):
        if loader not in config.LOADERS:
            return config.build_result(
                feature="mod_searcher",
                status="error",
                input_summary={"batch_size": len(queries or []), "loader": loader},
                result={},
                errors=[f"无效的加载器类型: {loader}，支持: {', '.join(config.LOADERS)}"],
            )

        logger.info(f"批量搜索: {len(queries or [])} 个关键词 (MC={mc_version}, Loader={loader})")
        batch_result = batch_search(
            queries=queries or [query],
            mc_version=mc_version,
            loader=loader,
            platform=platform,
            download=do_download,
            with_deps=with_deps,
        )

        # V1.0.1 新增: 自动更新兼容规则库
        all_batch_results = []
        for r in batch_result.get("results", []):
            all_batch_results.extend(r.get("mods", []))
        auto_update_recommendations_from_search(
            all_batch_results,
            mc_version,
            loader
        )

        html_content = generate_batch_html(batch_result)

        return config.build_result(
            feature="mod_searcher",
            status="success" if batch_result.get("success") else "error",
            input_summary={
                "mode": "batch",
                "batch_size": batch_result.get("batch_size", 0),
                "mc_version": mc_version,
                "loader": loader,
            },
            result={
                "batch_size": batch_result.get("batch_size", 0),
                "processed_count": batch_result.get("processed_count", 0),
                "downloaded_count": len(batch_result.get("downloaded", [])),
                "failed_count": len(batch_result.get("failed", [])),
                "results": batch_result.get("results", []),
            },
            output_files=generate_unified_output(
                feature="mod_searcher",
                status="success" if batch_result.get("success") else "error",
                input_summary={"mode": "batch", "batch_size": batch_result.get("batch_size", 0)},
                result=batch_result,
                title=f"批量搜索报告 - {batch_result.get('batch_size', 0)}个模组",
                html_content=html_content,
            ),
        )

    # === 原有: 单条关键词搜索模式 ===
    # 1. 输入验证
    if not query:
        return config.build_result(
            feature="mod_searcher",
            status="error",
            input_summary={"query": query},
            result={},
            errors=["搜索关键词不能为空"],
        )

    if loader not in config.LOADERS:
        return config.build_result(
            feature="mod_searcher",
            status="error",
            input_summary={"query": query, "loader": loader},
            result={},
            errors=[f"无效的加载器类型: {loader}，支持: {', '.join(config.LOADERS)}"],
        )

    warnings = []
    logger.info(f"开始搜索: {query} (MC={mc_version}, Loader={loader})")

    # 2. 调用Modrinth搜索
    modrinth_results = []
    curseforge_results = []

    if platform in ("modrinth", "both"):
        modrinth_results = search_modrinth(query, mc_version, loader)

    if platform in ("curseforge", "both"):
        curseforge_results = search_curseforge(query, mc_version, loader)
        if not curseforge_results and not config.APIConfig.has_curseforge_key():
            warnings.append("CurseForge API Key未配置，仅使用Modrinth搜索")

    # 3. 合并结果
    all_results = merge_results(modrinth_results, curseforge_results)

    if not all_results:
        return config.build_result(
            feature="mod_searcher",
            status="error",
            input_summary={
                "query": query,
                "mc_version": mc_version,
                "loader": loader,
            },
            result={},
            warnings=warnings + ["两个平台均无匹配结果，建议更换关键词或版本"],
            errors=["无匹配结果"],
        )

    logger.info(f"合并后结果: {len(all_results)} 个模组")

    # 4. 获取版本信息（取前5个最相关的）
    top_results = all_results[:5]
    version_cache = {}
    downloaded = []
    failed = []
    dep_queue = []

    for mod in top_results:
        slug = mod["slug"]
        source = mod["source"]
        versions = get_version_info(slug, loader, mc_version, source)

        if versions:
            version_cache[slug] = versions
            latest = versions[0]

            if do_download and latest.get("download_url"):
                # 确定输出目录
                if output:
                    dl_dir = Path(output)
                else:
                    dl_dir = config.DOWNLOADS_DIR
                dl_dir.mkdir(parents=True, exist_ok=True)

                # 下载
                file_name = latest.get("file_name", f"{slug}.jar")
                result = download_mod(latest["download_url"], dl_dir, file_name)

                if result:
                    downloaded.append({
                        "title": mod["title"],
                        "slug": slug,
                        "version": latest["version_number"],
                        "file_name": result.name,
                        "file_size": result.stat().st_size,
                        "source": source,
                        "download_url": latest["download_url"],
                    })
                    logger.info(f"已下载: {file_name}")

                    # 收集依赖
                    if with_deps and latest.get("dependencies"):
                        dep_queue.extend(latest["dependencies"])
                else:
                    failed.append({
                        "title": mod["title"],
                        "slug": slug,
                        "error": "下载失败",
                    })

    # 5. 处理依赖下载（最多下载10个依赖）
    if with_deps and dep_queue:
        logger.info(f"发现 {len(dep_queue)} 个依赖需要处理")
        seen_dep_ids = set()
        dep_downloaded = 0

        for dep in dep_queue[:20]:
            dep_id = dep.get("project_id", "")
            if not dep_id or dep_id in seen_dep_ids:
                continue
            seen_dep_ids.add(dep_id)

            # 跳过Minecraft本身和加载器
            if dep_id.lower() in ("minecraft", "fabricloader", "forge", "neoforge", "quilt_loader"):
                continue

            if dep_downloaded >= 10:
                break

            # 尝试从Modrinth获取依赖的版本
            dep_versions = get_version_info(dep_id, loader, mc_version, "modrinth")
            if dep_versions and dep_versions[0].get("download_url"):
                dl_dir = config.DOWNLOADS_DIR
                dep_file = dep_versions[0].get("file_name", f"{dep_id}.jar")
                result = download_mod(dep_versions[0]["download_url"], dl_dir, dep_file)
                if result:
                    downloaded.append({
                        "title": dep_id,
                        "slug": dep_id,
                        "version": dep_versions[0]["version_number"],
                        "file_name": result.name,
                        "file_size": result.stat().st_size,
                        "source": "modrinth",
                        "is_dependency": True,
                    })
                    dep_downloaded += 1
                    logger.info(f"已下载依赖: {dep_file}")

        if dep_downloaded == 0 and with_deps:
            warnings.append("部分依赖可能需要手动下载，请查看报告中的依赖列表")

    # 6. V1.0.1 新增: 自动更新兼容规则库
    auto_update_recommendations_from_search(
        all_results,
        mc_version,
        loader
    )

    # 7. 生成报告
    html_content = generate_search_html(
        query, mc_version, loader, all_results, downloaded, failed
    )

    # 7. 依赖清单（用于HTML展示）
    dependency_list = []
    for d in downloaded:
        if d.get("is_dependency"):
            dependency_list.append({
                "mod_id": d["slug"],
                "version": d["version"],
                "file": d["file_name"],
            })

    output_files = generate_unified_output(
        feature="mod_searcher",
        status="success",
        input_summary={
            "query": query,
            "mc_version": mc_version,
            "loader": loader,
            "platform": platform,
        },
        result={
            "search_results": all_results,
            "downloaded": downloaded,
            "failed": failed,
            "dependencies": dependency_list,
        },
        title=f"模组检索报告 - {query}",
        html_content=html_content,
        warnings=warnings,
    )

    return config.build_result(
        feature="mod_searcher",
        status="success" if not failed else "partial",
        input_summary={
            "query": query,
            "mc_version": mc_version,
            "loader": loader,
        },
        result={
            "search_results": all_results,
            "search_results_count": len(all_results),
            "downloaded_count": len(downloaded),
            "failed_count": len(failed),
            "downloaded": downloaded,
            "failed": failed,
        },
        warnings=warnings,
        output_files=output_files,
    )
