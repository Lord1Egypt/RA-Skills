# -*- coding: utf-8 -*-
"""模组移植可行性评估报告 (F9)

分析模组从一个环境（MC版本+加载器）移植到另一个环境的可行性，
生成包含API兼容性、Mixin目标类、依赖模组、加载器迁移、资源格式
等维度的完整评估报告。

使用方式:
    from core.migration_assessor import run
    import argparse
    args = argparse.Namespace(
        jar_path="mod.jar",
        from_mc_version="1.20.1",
        to_mc_version="1.21.1",
        from_loader="forge",
        to_loader="neoforge",
        output=None,
    )
    result = run(args)
"""

import sys
import json
import os
import zipfile
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# 项目根目录
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from core.i18n import t
from utils.logger import get_logger
from utils.jar_utils import extract_jar, create_temp_dir, cleanup_temp_dir, parse_toml, read_jar_file
from utils.report_gen import ReportGenerator, generate_unified_output
from core.modrinth_client import get_latest_recommended_version

logger = get_logger("migration_assessor")

# === 加载器迁移兼容性矩阵 ===
LOADER_MIGRATION_MAP = {
    # (源加载器, 目标加载器): 兼容性等级
    ("forge", "neoforge"): {
        "level": "medium",
        "score": 60,
        "desc": "Forge 1.20.1 到 NeoForge 1.21.x 迁移",
        "key_changes": [
            "包名从 net.minecraftforge 改为 net.neoforged",
            "事件系统简化，部分事件签名变更",
            "注册系统从 RegistryObject 改为 DeferredRegister",
            "Mixin 目标类部分变更",
            "资源加载方式调整",
        ],
        "estimated_effort": "中等 (3-7天)",
    },
    ("forge", "fabric"): {
        "level": "low",
        "score": 30,
        "desc": "Forge 到 Fabric 迁移（跨加载器）",
        "key_changes": [
            "注解系统完全不同",
            "事件系统完全不同",
            "需要重写整个 Mod 类",
            "资源加载方式完全不同",
            "依赖管理方式不同",
        ],
        "estimated_effort": "高 (7-14天)",
    },
    ("forge", "quilt"): {
        "level": "low",
        "score": 25,
        "desc": "Forge 到 Quilt 迁移（跨加载器）",
        "key_changes": [
            "同 Fabric，需要完全重写",
            "Quilt API 与 Fabric 略有差异",
        ],
        "estimated_effort": "高 (7-14天)",
    },
    ("neoforge", "forge"): {
        "level": "low",
        "score": 20,
        "desc": "NeoForge 到 Forge（通常不推荐）",
        "key_changes": [
            "NeoForge 特有的 API 需要迁移",
            "部分新特性在 Forge 中不可用",
        ],
        "estimated_effort": "高 (7-14天)",
    },
    ("neoforge", "fabric"): {
        "level": "low",
        "score": 25,
        "desc": "NeoForge 到 Fabric 迁移",
        "key_changes": [
            "跨加载器迁移",
            "需要重写 Mod 类和事件系统",
        ],
        "estimated_effort": "高 (7-14天)",
    },
    ("fabric", "forge"): {
        "level": "low",
        "score": 30,
        "desc": "Fabric 到 Forge 迁移",
        "key_changes": [
            "注解系统完全不同",
            "事件系统完全不同",
            "需要重写整个 Mod 类",
        ],
        "estimated_effort": "高 (7-14天)",
    },
    ("fabric", "neoforge"): {
        "level": "low",
        "score": 35,
        "desc": "Fabric 到 NeoForge 迁移",
        "key_changes": [
            "跨加载器迁移",
            "需要重写 Mod 类和事件系统",
        ],
        "estimated_effort": "高 (7-14天)",
    },
    ("fabric", "quilt"): {
        "level": "high",
        "score": 85,
        "desc": "Fabric 到 Quilt 迁移（同系加载器）",
        "key_changes": [
            "大部分代码可直接迁移",
            "少量 API 差异需要调整",
        ],
        "estimated_effort": "低 (1-3天)",
    },
    ("quilt", "fabric"): {
        "level": "high",
        "score": 85,
        "desc": "Quilt 到 Fabric 迁移（同系加载器）",
        "key_changes": [
            "大部分代码可直接迁移",
            "少量 API 差异需要调整",
        ],
        "estimated_effort": "低 (1-3天)",
    },
    # 同加载器迁移（版本升级）
    ("forge", "forge"): {
        "level": "high",
        "score": 90,
        "desc": "Forge 版本升级",
        "key_changes": [
            "主要关注 API 变更",
            "Mixin 目标类可能变化",
            "依赖版本需更新",
        ],
        "estimated_effort": "低 (1-3天)",
    },
    ("neoforge", "neoforge"): {
        "level": "high",
        "score": 90,
        "desc": "NeoForge 版本升级",
        "key_changes": [
            "主要关注 API 变更",
            "Mixin 目标类可能变化",
            "依赖版本需更新",
        ],
        "estimated_effort": "低 (1-3天)",
    },
    ("fabric", "fabric"): {
        "level": "high",
        "score": 92,
        "desc": "Fabric 版本升级",
        "key_changes": [
            "API 相对稳定",
            "Mixin 目标类可能变化",
        ],
        "estimated_effort": "低 (0.5-2天)",
    },
    ("quilt", "quilt"): {
        "level": "high",
        "score": 90,
        "desc": "Quilt 版本升级",
        "key_changes": [
            "API 相对稳定",
            "Mixin 目标类可能变化",
        ],
        "estimated_effort": "低 (0.5-2天)",
    },
}

# === MC 版本兼容性矩阵 ===
MC_VERSION_COMPATIBILITY = {
    # (源版本, 目标版本): 兼容性信息
    ("1.20.1", "1.21.1"): {
        "api_stability": "medium",
        "common_changes": [
            "方块实体 API 变更",
            "数据包格式升级",
            "部分注册方法签名变化",
            "资源路径规范调整",
        ],
    },
    ("1.20.4", "1.21.1"): {
        "api_stability": "medium",
        "common_changes": [
            "同上，跨版本跨度更大",
        ],
    },
    ("1.20.1", "1.20.4"): {
        "api_stability": "high",
        "common_changes": [
            "小版本补丁，API 基本稳定",
            "可能有少量废弃方法",
        ],
    },
    ("1.19.4", "1.20.1"): {
        "api_stability": "low",
        "common_changes": [
            "大版本更新，API 有显著变化",
            "新的注册系统",
            "数据生成器重写",
        ],
    },
}


def _parse_mod_metadata(jar_path: str) -> Dict[str, Any]:
    """解析模组元数据"""
    metadata = {
        "mod_id": "",
        "mod_name": "",
        "mod_version": "",
        "description": "",
        "authors": "",
        "dependencies": [],
        "loader": "",
    }
    
    # 尝试读取各种元数据文件
    metadata_files = [
        "META-INF/mods.toml",
        "META-INF/neoforge.mods.toml",
        "fabric.mod.json",
    ]
    
    for meta_file in metadata_files:
        try:
            content = read_jar_file(jar_path, meta_file)
            if not content:
                continue
            
            if meta_file.endswith("mods.toml") or meta_file.endswith("neoforge.mods.toml"):
                # Forge/NeoForge TOML 格式
                data = parse_toml(content)
                if data:
                    mods = data.get("mods", [{}])
                    if mods:
                        mod = mods[0]
                        metadata["mod_id"] = mod.get("modId", "")
                        metadata["mod_name"] = mod.get("displayName", "")
                        metadata["mod_version"] = mod.get("version", "")
                        metadata["description"] = mod.get("description", "")
                        metadata["authors"] = mod.get("authors", "")
                    dependencies = data.get("dependencies", {})
                    if dependencies:
                        metadata["dependencies"] = list(dependencies.keys())
                    metadata["loader"] = "forge" if "neoforge" not in meta_file else "neoforge"
                    
            elif meta_file == "fabric.mod.json":
                # Fabric JSON 格式
                data = json.loads(content)
                metadata["mod_id"] = data.get("id", "")
                metadata["mod_name"] = data.get("name", "")
                metadata["mod_version"] = data.get("version", "")
                metadata["description"] = data.get("description", "")
                metadata["authors"] = ", ".join(data.get("authors", []))
                metadata["dependencies"] = list(data.get("depends", {}).keys())
                metadata["loader"] = "fabric"
                
            if metadata["mod_id"]:
                break
                
        except Exception as e:
            logger.warning(f"解析 {meta_file} 失败: {e}")
            continue
    
    return metadata


def _analyze_mixin_configs(jar_path: str) -> List[Dict[str, Any]]:
    """分析 Mixin 配置"""
    mixin_info = []
    mixin_patterns = [
        "mixins",
        "Mixin",
        "mixin",
    ]
    
    try:
        with zipfile.ZipFile(jar_path, 'r') as zf:
            all_files = zf.namelist()
            
            # 查找 Mixin 配置文件
            for fname in all_files:
                if not fname.endswith(".json"):
                    continue
                if not any(p in fname.lower() for p in mixin_patterns):
                    continue
                
                try:
                    content = zf.read(fname).decode('utf-8', errors='ignore')
                    data = json.loads(content)
                    
                    targets = data.get("targets", [])
                    mixins = data.get("mixins", [])
                    
                    if targets or mixins:
                        mixin_info.append({
                            "config_file": fname,
                            "targets": targets,
                            "mixins": [m.get("mixinClass", "") for m in mixins if isinstance(m, dict)],
                            "count": len(targets) + len(mixins),
                        })
                        
                except Exception as e:
                    logger.debug(f"解析 Mixin 配置 {fname} 失败: {e}")
                    
    except Exception as e:
        logger.error(f"分析 Mixin 配置失败: {e}")
    
    return mixin_info


def _analyze_dependencies(
    mod_id: str,
    from_mc: str,
    to_mc: str,
    from_loader: str,
    to_loader: str,
    local_deps: List[str],
) -> Dict[str, Any]:
    """分析依赖兼容性"""
    dep_analysis = {
        "total_deps": len(local_deps),
        "deps_checked": [],
        "deps_incompatible": [],
        "deps_missing": [],
        "online_checks": [],
    }
    
    # 获取本地版本推荐数据库
    try:
        db = config.get_mod_version_recommendations()
    except Exception:
        db = {"mods": {}}
    
    # 检查每个依赖
    for dep_id in local_deps:
        dep_info = {
            "mod_id": dep_id,
            "source": "local",
            "status": "unknown",
        }
        
        # 先查本地数据库
        if dep_id in db.get("mods", {}):
            mod_data = db["mods"][dep_id]
            versions = mod_data.get("versions", {})
            
            # 检查目标版本是否支持
            target_versions = versions.get(to_mc, {})
            if target_versions:
                # 检查目标加载器是否有对应版本
                if to_loader in target_versions:
                    recommended = target_versions[to_loader].get("recommended", "")
                    min_ver = target_versions[to_loader].get("min", "")
                    
                    dep_info["status"] = "compatible"
                    dep_info["recommended_version"] = recommended
                    dep_info["min_version"] = min_ver
                else:
                    dep_info["status"] = "loader_incompatible"
                    dep_info["note"] = f"目标加载器 {to_loader} 暂无支持版本"
            else:
                dep_info["status"] = "version_incompatible"
                dep_info["note"] = f"目标MC版本 {to_mc} 暂无支持版本"
        else:
            # 本地数据库未命中，标记为需要联网查询
            dep_info["status"] = "needs_online_check"
            dep_analysis["online_checks"].append(dep_id)
        
        dep_analysis["deps_checked"].append(dep_info)
    
    # 汇总不兼容的依赖
    for dep in dep_analysis["deps_checked"]:
        if dep["status"] in ("loader_incompatible", "version_incompatible"):
            dep_analysis["deps_incompatible"].append(dep)
        elif dep["status"] == "needs_online_check":
            dep_analysis["deps_missing"].append(dep)
    
    return dep_analysis


def _online_check_dependencies(
    dep_ids: List[str],
    to_mc: str,
    to_loader: str,
) -> List[Dict[str, Any]]:
    """联网查询依赖版本信息"""
    online_results = []
    
    for dep_id in dep_ids:
        try:
            # 尝试通过 Modrinth 查询
            result = get_latest_recommended_version(
                dep_id, to_mc, to_loader, max_cache_age=3600
            )
            
            if result:
                online_results.append({
                    "mod_id": dep_id,
                    "source": "online",
                    "status": "found",
                    "version": result.get("version", ""),
                    "download_url": result.get("download_url", ""),
                    "note": f"通过 Modrinth 联网查询获取",
                })
            else:
                online_results.append({
                    "mod_id": dep_id,
                    "source": "online",
                    "status": "not_found",
                    "note": "Modrinth 未找到匹配版本",
                })
        except Exception as e:
            logger.warning(f"联网查询 {dep_id} 失败: {e}")
            online_results.append({
                "mod_id": dep_id,
                "source": "online",
                "status": "query_failed",
                "note": f"查询失败: {str(e)}",
            })
    
    return online_results


def _calculate_feasibility_score(
    loader_compat: int,
    mc_version_compat: int,
    dep_compat: float,
    mixin_complexity: int,
) -> Tuple[int, str, str]:
    """计算可行性评分"""
    # 加权计算总分
    score = (
        loader_compat * 0.35 +          # 加载器迁移占35%
        mc_version_compat * 0.25 +      # 版本兼容性占25%
        dep_compat * 0.30 +             # 依赖兼容性占30%
        (100 - mixin_complexity) * 0.10  # Mixin复杂度占10%（越低越好）
    )
    
    score = max(0, min(100, int(score)))
    
    # 风险等级
    if score >= 80:
        level = "low"
        level_name = "低风险"
        desc = "移植可行性高，主要是常规更新"
    elif score >= 60:
        level = "medium"
        level_name = "中等风险"
        desc = "移植需要一定工作量，部分功能需要调整"
    elif score >= 40:
        level = "high"
        level_name = "高风险"
        desc = "移植难度较大，需要较多改动"
    else:
        level = "very_high"
        level_name = "极高风险"
        desc = "移植非常困难，建议寻找替代方案"
    
    return score, level, f"{level_name} - {desc}"


def _generate_assessment_report(
    metadata: Dict[str, Any],
    loader_migration: Dict[str, Any],
    mc_version_info: Dict[str, Any],
    dep_analysis: Dict[str, Any],
    online_results: List[Dict[str, Any]],
    mixin_analysis: List[Dict[str, Any]],
    score: int,
    risk_level: str,
    risk_desc: str,
    from_mc: str,
    to_mc: str,
    from_loader: str,
    to_loader: str,
) -> Dict[str, Any]:
    """生成完整评估报告"""
    
    # 整合在线查询结果到依赖分析
    all_dep_results = dep_analysis["deps_checked"]
    for online in online_results:
        for i, local in enumerate(all_dep_results):
            if local["mod_id"] == online["mod_id"] and local["status"] == "needs_online_check":
                all_dep_results[i] = online
                break
    
    # 计算依赖兼容率
    if all_dep_results:
        compatible_count = sum(1 for d in all_dep_results if d["status"] == "compatible")
        dep_rate = (compatible_count / len(all_dep_results)) * 100
    else:
        dep_rate = 100
    
    # 生成移植建议
    suggestions = []
    if loader_migration.get("level") == "low":
        suggestions.append("跨加载器迁移，建议仔细检查所有注解和事件系统")
    if dep_rate < 80:
        suggestions.append(f"依赖兼容率仅 {dep_rate:.0f}%，部分依赖需要升级或替换")
    if mixin_analysis:
        total_mixins = sum(m["count"] for m in mixin_analysis)
        if total_mixins > 10:
            suggestions.append(f"Mixin 注入点较多（{total_mixins}个），需重点验证目标类是否存在")
    
    # 综合建议
    if score >= 80:
        suggestions.append("✅ 总体可行，建议按步骤执行移植")
    elif score >= 60:
        suggestions.append("⚠️ 有一定风险，建议先在测试环境验证关键功能")
    else:
        suggestions.append("❌ 风险较高，建议谨慎考虑是否进行移植")
    
    report = {
        "report_type": "migration_assessment",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": {
            "mod_id": metadata.get("mod_id", ""),
            "mod_name": metadata.get("mod_name", ""),
            "from_mc_version": from_mc,
            "to_mc_version": to_mc,
            "from_loader": from_loader,
            "to_loader": to_loader,
        },
        "score": {
            "total": score,
            "level": risk_level,
            "description": risk_desc,
        },
        "mod_metadata": metadata,
        "loader_migration": loader_migration,
        "mc_version_compatibility": mc_version_info,
        "dependency_analysis": {
            "total_deps": dep_analysis["total_deps"],
            "compatible_rate": dep_rate,
            "results": all_dep_results,
        },
        "mixin_analysis": {
            "total_configs": len(mixin_analysis),
            "total_injections": sum(m["count"] for m in mixin_analysis),
            "details": mixin_analysis,
        },
        "suggestions": suggestions,
        "effort_estimate": {
            "loader_migration": loader_migration.get("estimated_effort", "未知"),
            "overall": "根据实际情况评估",
        },
    }
    
    return report


def run(args) -> int:
    """执行模组移植可行性评估

    Args:
        args: 命令行参数，需包含:
            - jar_path: 模组JAR文件路径
            - from_mc_version: 源MC版本
            - to_mc_version: 目标MC版本
            - from_loader: 源加载器
            - to_loader: 目标加载器
            - output: 输出目录
    
    Returns:
        退出码 0=成功 1=失败
    """
    print(t("migration.assess_title"), flush=True)
    
    # === 参数校验 ===
    jar_path = getattr(args, "jar_path", "")
    from_mc = getattr(args, "from_mc_version", "")
    to_mc = getattr(args, "to_mc_version", "")
    from_loader = getattr(args, "from_loader", "")
    to_loader = getattr(args, "to_loader", "")
    output_dir = getattr(args, "output", None) or str(config.REPORTS_DIR)
    
    if not jar_path or not Path(jar_path).exists():
        print(t("error.invalid_jar"), flush=True)
        return 1
    if not from_mc or not to_mc:
        print(t("error.missing_mc_versions"), flush=True)
        return 1
    if not from_loader or not to_loader:
        print(t("error.missing_loaders"), flush=True)
        return 1
    
    print(t("migration.jar_info", path=jar_path), flush=True)
    print(t("migration.migration_info", from_mc=from_mc, from_loader=from_loader, to_mc=to_mc, to_loader=to_loader), flush=True)
    
    # === 1. 解析模组元数据 ===
    print("\n" + t("migration.parsing_metadata"), flush=True)
    metadata = _parse_mod_metadata(jar_path)
    print(t("migration.mod_id", id=metadata['mod_id']), flush=True)
    print(t("migration.mod_name", name=metadata['mod_name']), flush=True)
    print(t("migration.mod_version", version=metadata['mod_version']), flush=True)
    print(t("migration.dependency_count", count=len(metadata['dependencies'])), flush=True)
    
    # === 2. 分析加载器迁移兼容性 ===
    print("\n" + t("migration.analyzing_loader"), flush=True)
    loader_key = (from_loader, to_loader)
    loader_info = LOADER_MIGRATION_MAP.get(loader_key, {
        "level": "unknown",
        "score": 50,
        "desc": f"{from_loader} → {to_loader}",
        "key_changes": ["未知迁移路径，需手动评估"],
        "estimated_effort": "未知",
    })
    print(t("migration.compat_level", level=loader_info['level']), flush=True)
    print(t("migration.key_changes", count=len(loader_info.get('key_changes', []))), flush=True)
    
    # === 3. 分析 MC 版本兼容性 ===
    print("\n" + t("migration.analyzing_mc"), flush=True)
    version_key = (from_mc, to_mc)
    mc_info = MC_VERSION_COMPATIBILITY.get(version_key, {
        "api_stability": "unknown",
        "common_changes": ["版本兼容性信息未知，建议手动测试"],
    })
    print(t("migration.api_stability", stability=mc_info.get('api_stability', 'unknown')), flush=True)
    
    # === 4. 分析依赖兼容性 ===
    print("\n" + t("migration.analyzing_deps"), flush=True)
    dep_analysis = _analyze_dependencies(
        metadata["mod_id"], from_mc, to_mc,
        from_loader, to_loader, metadata["dependencies"]
    )
    print(t("migration.local_check", count=len(dep_analysis['deps_checked'])), flush=True)
    print(t("migration.online_check", count=len(dep_analysis['online_checks'])), flush=True)
    
    # 联网查询
    online_results = []
    if dep_analysis["online_checks"]:
        print(t("migration.querying_online"), flush=True)
        online_results = _online_check_dependencies(
            dep_analysis["online_checks"], to_mc, to_loader
        )
        found = sum(1 for r in online_results if r["status"] == "found")
        print(t("migration.online_result", total=len(online_results), found=found), flush=True)
    
    # === 5. 分析 Mixin 配置 ===
    print("\n" + t("migration.analyzing_mixin"), flush=True)
    mixin_analysis = _analyze_mixin_configs(jar_path)
    total_mixins = sum(m["count"] for m in mixin_analysis)
    print(t("migration.mixin_config", count=len(mixin_analysis)), flush=True)
    print(t("migration.mixin_injections", count=total_mixins), flush=True)
    
    # === 6. 计算可行性评分 ===
    print("\n" + t("migration.calculating_score"), flush=True)
    loader_score = loader_info.get("score", 50)
    version_score = 70 if mc_info.get("api_stability") == "high" else \
                    50 if mc_info.get("api_stability") == "medium" else \
                    30 if mc_info.get("api_stability") == "low" else 40
    dep_compat = 100 if not dep_analysis["deps_checked"] else \
        (sum(1 for d in dep_analysis["deps_checked"] if d["status"] == "compatible") / len(dep_analysis["deps_checked"])) * 100
    mixin_complexity = min(100, total_mixins * 5)  # 5个注入点增加10%复杂度
    
    score, risk_level, risk_desc = _calculate_feasibility_score(
        loader_score, version_score, dep_compat, mixin_complexity
    )
    print(t("migration.total_score", score=score), flush=True)
    print(t("migration.risk_level_display", level=risk_level, desc=risk_desc), flush=True)
    
    # === 7. 生成报告 ===
    print("\n" + t("migration.generating_report"), flush=True)
    report = _generate_assessment_report(
        metadata, loader_info, mc_info,
        dep_analysis, online_results, mixin_analysis,
        score, risk_level, risk_desc,
        from_mc, to_mc, from_loader, to_loader
    )
    
    # 保存报告
    report_path = Path(output_dir)
    report_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_mod_id = metadata["mod_id"] or "unknown_mod"
    
    # 生成 JSON 报告
    json_path = report_path / f"migration_assessment_{safe_mod_id}_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(t("migration.json_report", path=json_path), flush=True)
    
    # 生成 HTML 报告
    html_path = report_path / f"migration_assessment_{safe_mod_id}_{timestamp}.html"
    html_content = _generate_html_report(report)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(t("migration.html_report", path=html_path), flush=True)
    
    # === 8. 输出摘要 ===
    print(f"\n{'='*60}", flush=True)
    print(t("migration.completed"), flush=True)
    print(f"{'='*60}", flush=True)
    print(t("migration.jar_info", path=f"{metadata['mod_name']} ({metadata['mod_id']})"), flush=True)
    print(t("migration.migration_info", from_mc=from_mc, from_loader=from_loader, to_mc=to_mc, to_loader=to_loader), flush=True)
    print(t("migration.score_display", score=score, desc=risk_desc), flush=True)
    print(t("migration.dep_compat", rate=f"{dep_compat:.0f}"), flush=True)
    print(t("migration.mixin_count", count=total_mixins), flush=True)
    
    if report["suggestions"]:
        print("\n" + t("migration.suggestions"), flush=True)
        for suggestion in report["suggestions"]:
            print(f"    {suggestion}", flush=True)
    
    print("\n" + t("migration.report_saved_path"), flush=True)
    print(f"    {json_path}", flush=True)
    print(f"    {html_path}", flush=True)
    
    return 0


def _generate_html_report(report: Dict[str, Any]) -> str:
    """生成 HTML 评估报告"""
    target = report["target"]
    score = report["score"]
    metadata = report["mod_metadata"]
    loader_info = report["loader_migration"]
    dep_analysis = report["dependency_analysis"]
    mixin_info = report["mixin_analysis"]
    
    html_parts = [
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>模组移植可行性评估报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            backdrop-filter: blur(10px);
        }
        .header h1 {
            font-size: 28px;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header .subtitle { color: #888; font-size: 14px; }
        .score-section {
            display: flex;
            align-items: center;
            gap: 40px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            margin-bottom: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .score-circle {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            font-weight: bold;
            color: white;
            position: relative;
            flex-shrink: 0;
        }
        .score-circle::before {
            content: '';
            position: absolute;
            inset: -4px;
            border-radius: 50%;
            padding: 4px;
            background: linear-gradient(135deg, """
    ]
    
    # 根据评分选择颜色
    if score["total"] >= 80:
        score_color = "#4ade80"
        score_gradient = "#22c55e, #16a34a"
    elif score["total"] >= 60:
        score_color = "#fbbf24"
        score_gradient = "#f59e0b, #d97706"
    elif score["total"] >= 40:
        score_color = "#fb923c"
        score_gradient = "#f97316, #ea580c"
    else:
        score_color = "#f87171"
        score_gradient = "#ef4444, #dc2626"
    
    html_parts.append(score_gradient + """);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
        }
        .score-info h2 { font-size: 24px; margin-bottom: 8px; }
        .score-info p { color: #aaa; line-height: 1.6; }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .info-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
        }
        .info-card h3 {
            font-size: 16px;
            margin-bottom: 12px;
            color: #a0a0a0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .info-card .value {
            font-size: 20px;
            color: #e0e0e0;
        }
        .section {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .section h2 {
            font-size: 20px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .table { width: 100%; border-collapse: collapse; }
        .table th, .table td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .table th { color: #888; font-weight: 500; font-size: 14px; }
        .table td { font-size: 14px; }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        .badge-success { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
        .badge-warning { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
        .badge-danger { background: rgba(239, 68, 68, 0.2); color: #f87171; }
        .badge-info { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
        .suggestion-list { list-style: none; }
        .suggestion-list li {
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            margin-bottom: 8px;
            line-height: 1.6;
        }
        .meta-info {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 12px;
        }
        .meta-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 13px;
        }
        .meta-item span { color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>模组移植可行性评估报告</h1>
            <p class="subtitle">生成时间: """ + report["generated_at"] + """</p>
        </div>
        
        <div class="score-section">
            <div class="score-circle" style="background: linear-gradient(135deg, """ + score_gradient + """); color: white;">
                """ + str(score["total"]) + """
            </div>
            <div class="score-info">
                <h2 style="color: """ + score_color + """;">风险等级: """ + score["level"].upper() + """</h2>
                <p>""" + score["description"] + """</p>
            </div>
        </div>
        
        <div class="info-grid">
            <div class="info-card">
                <h3>源环境</h3>
                <div class="value">""" + target["from_mc_version"] + """</div>
                <div style="color: #888; margin-top: 4px;">加载器: """ + target["from_loader"].upper() + """</div>
            </div>
            <div class="info-card">
                <h3>目标环境</h3>
                <div class="value">""" + target["to_mc_version"] + """</div>
                <div style="color: #888; margin-top: 4px;">加载器: """ + target["to_loader"].upper() + """</div>
            </div>
            <div class="info-card">
                <h3>模组信息</h3>
                <div class="value">""" + (metadata.get("mod_name") or metadata.get("mod_id", "")) + """</div>
                <div style="color: #888; margin-top: 4px;">版本: """ + metadata.get("mod_version", "") + """</div>
            </div>
            <div class="info-card">
                <h3>依赖统计</h3>
                <div class="value">""" + str(dep_analysis["total_deps"]) + """ 个</div>
                <div style="color: #888; margin-top: 4px;">兼容率: """ + f"{dep_analysis['compatible_rate']:.0f}%" + """</div>
            </div>
        </div>
""")
    
    # 加载器迁移信息
    if loader_info:
        html_parts.append("""
        <div class="section">
            <h2>🔀 加载器迁移兼容性</h2>
            <div style="margin-bottom: 16px;">
                <span class="badge """ + ("badge-success" if loader_info.get("level") == "high" else "badge-warning" if loader_info.get("level") == "medium" else "badge-danger") + """>
                    兼容性: """ + loader_info.get("level", "unknown").upper() + """
                </span>
                <span style="margin-left: 16px; color: #888;">预估工作量: """ + loader_info.get("estimated_effort", "未知") + """</span>
            </div>
            <p style="margin-bottom: 12px; color: #ccc;">""" + loader_info.get("desc", "") + """</p>
            <h3 style="font-size: 14px; color: #a0a0a0; margin-bottom: 8px;">关键变更点:</h3>
            <ul style="padding-left: 20px; line-height: 1.8; color: #ccc;">
""")
        for change in loader_info.get("key_changes", []):
            html_parts.append(f"                <li>{change}</li>\n")
        html_parts.append("""
            </ul>
        </div>
""")
    
    # 依赖分析
    if dep_analysis.get("results"):
        html_parts.append("""
        <div class="section">
            <h2>📦 依赖兼容性分析</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>依赖模组</th>
                        <th>状态</th>
                        <th>推荐版本</th>
                        <th>来源</th>
                    </tr>
                </thead>
                <tbody>
""")
        for dep in dep_analysis["results"]:
            status = dep.get("status", "unknown")
            if status == "compatible" or status == "found":
                badge_class = "badge-success"
                status_text = "✓ 兼容"
            elif status == "loader_incompatible" or status == "version_incompatible":
                badge_class = "badge-danger"
                status_text = "✗ 不兼容"
            elif status == "not_found" or status == "query_failed":
                badge_class = "badge-warning"
                status_text = "⚠ 未找到"
            else:
                badge_class = "badge-info"
                status_text = "? 待查询"
            
            html_parts.append(f"""                <tr>
                    <td>{dep.get('mod_id', '')}</td>
                    <td><span class="badge {badge_class}">{status_text}</span></td>
                    <td>{dep.get('recommended_version', dep.get('version', '—'))}</td>
                    <td>{dep.get('source', 'local')}</td>
                </tr>
""")
        html_parts.append("""                </tbody>
            </table>
        </div>
""")
    
    # Mixin 分析
    if mixin_info.get("details"):
        html_parts.append(f"""
        <div class="section">
            <h2>🔧 Mixin 注入分析</h2>
            <p style="color: #888; margin-bottom: 16px;">共发现 {mixin_info['total_configs']} 个配置文件，{mixin_info['total_injections']} 个注入点</p>
            <table class="table">
                <thead>
                    <tr>
                        <th>配置文件</th>
                        <th>注入目标数</th>
                    </tr>
                </thead>
                <tbody>
""")
        for m in mixin_info["details"]:
            html_parts.append(f"""                <tr>
                    <td>{m.get('config_file', '')}</td>
                    <td>{m.get('count', 0)} 个</td>
                </tr>
""")
        html_parts.append("""                </tbody>
            </table>
        </div>
""")
    
    # 建议
    if report.get("suggestions"):
        html_parts.append("""
        <div class="section">
            <h2>💡 迁移建议</h2>
            <ul class="suggestion-list">
""")
        for suggestion in report["suggestions"]:
            html_parts.append(f"                <li>{suggestion}</li>\n")
        html_parts.append("""            </ul>
        </div>
""")
    
    html_parts.append("""
    </div>
</body>
</html>
""")
    
    return "".join(html_parts)
