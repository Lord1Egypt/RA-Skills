# -*- coding: utf-8 -*-
"""F1: JAR结构解析与中文释义

解压JAR文件，遍历所有目录与文件，按类型分类，
读取模组元数据，生成中文功能说明书。

使用方式:
    from core.jar_parser import run
    import argparse
    args = argparse.Namespace(jar_path="xxx.jar", output=None, detail_level="basic")
    result = run(args)
"""

import sys
import os
import json
import re
import html
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# 项目根目录
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.jar_utils import (
    extract_jar, create_temp_dir, cleanup_temp_dir,
    get_file_type, format_file_size, parse_toml, read_jar_file,
    list_jar_files
)
from utils.report_gen import ReportGenerator, generate_unified_output

logger = get_logger("jar_parser")

# === 文件分类释义规则库 ===
# 按优先级排序，先匹配先使用
FILE_DESC_RULES = [
    # (正则模式, 类型, 中文释义)
    (r"^META-INF/?$", "dir", "元数据目录，存放模组签名和清单文件"),
    (r"^META-INF/mods\.toml$", "metadata", "NeoForge/Forge模组清单文件，声明模组基本信息（ID、版本、依赖等）"),
    (r"^META-INF/neoforge\.mods\.toml$", "metadata", "NeoForge模组清单文件（新版格式）"),
    (r"^META-INF/MANIFEST\.MF$", "manifest", "Java清单文件，包含JAR元信息和主类声明"),
    (r"^fabric\.mod\.json$", "metadata", "Fabric模组清单文件，声明Fabric模组的元信息"),
    (r"^assets/[^/]+/lang/?$", "lang_dir", "语言文件目录，存放各语种翻译文本"),
    (r"^assets/[^/]+/lang/en_us\.json$", "lang", "英语语言文件，含所有游戏内文本键值对"),
    (r"^assets/[^/]+/lang/zh_cn\.json$", "lang", "简体中文语言文件，存放汉化翻译文本"),
    (r"^assets/[^/]+/lang/zh_cn\.lang$", "lang_legacy", "简体中文语言文件（旧版格式）"),
    (r"^assets/[^/]+/textures/?$", "texture_dir", "贴图资源目录，存放方块/物品/实体的PNG纹理"),
    (r"^assets/[^/]+/models/?$", "model_dir", "模型文件目录，定义方块/物品的3D形状"),
    (r"^assets/[^/]+/blockstates/?$", "blockstate_dir", "方块状态目录，定义方块的所有状态变体"),
    (r"^assets/[^/]+/sounds/?$", "sound_dir", "音效资源目录"),
    (r"^assets/[^/]+/shaders/?$", "shader_dir", "着色器目录，存放GLSL着色器代码"),
    (r"^assets/[^/]+/font/?$", "font_dir", "字体资源目录"),
    (r"^assets/[^/]+/gui/?$", "gui_dir", "GUI纹理目录，存放界面元素贴图"),
    (r"^data/[^/]+/recipes/?$", "recipe_dir", "合成配方目录，定义工作台/熔炉配方"),
    (r"^data/[^/]+/loot_tables/?$", "loot_dir", "战利品表目录，定义怪物掉落和宝箱内容"),
    (r"^data/[^/]+/advancements/?$", "advancement_dir", "进度/成就定义目录"),
    (r"^data/[^/]+/functions/?$", "function_dir", "数据包函数目录，存放MC函数命令"),
    (r"^data/[^/]+/worldgen/?$", "worldgen_dir", "世界生成配置目录"),
    (r"^data/[^/]+/structures/?$", "structure_dir", "结构定义目录"),
    (r"^mixins?\..*\.json$", "mixin_config", "Mixin注入配置文件，声明对游戏源码的修改规则"),
    (r"^pack\.mcmeta$", "meta", "资源包元数据，声明资源包格式版本和描述"),
    (r"^.*\.class$", "class", "Java编译后的字节码文件，包含模组核心逻辑"),
    (r"^.*\.png$", "png", "PNG贴图文件，用于方块/物品/实体/界面的视觉渲染"),
    (r"^.*\.json$", "json", "JSON配置文件，存放结构化数据"),
    (r"^.*\.toml$", "toml", "TOML配置文件，存放模组元信息或配置数据"),
    (r"^.*\.mcmeta$", "mcmeta", "资源元数据文件，定义贴图动画等附加信息"),
    (r"^.*\.ogg$", "audio", "OGG音频文件，通常为音效或背景音乐"),
    (r"^.*\.fsh$", "shader", "像素着色器文件（Fragment Shader）"),
    (r"^.*\.vsh$", "shader", "顶点着色器文件（Vertex Shader）"),
    (r"^.*\.glsl$", "shader", "GLSL着色器文件"),
    (r"^.*\.txt$", "text", "文本文件，可能包含说明或许可证信息"),
    (r"^license.*$", "license", "许可证文件，声明模组的开源协议"),
    (r"^readme.*$", "readme", "说明文档，介绍模组功能和使用方法"),
]


def classify_file(file_path: str) -> Dict[str, str]:
    """根据文件路径匹配分类规则

    Args:
        file_path: JAR内文件相对路径（如 "META-INF/mods.toml"）

    Returns:
        字典: {"type": "类型", "desc_cn": "中文释义"}
    """
    # 目录判断
    if file_path.endswith("/"):
        # 检查是否匹配目录规则
        for pattern, ftype, desc in FILE_DESC_RULES:
            if pattern.endswith("/$") and re.match(pattern, file_path):
                return {"type": ftype, "desc_cn": desc}
        return {"type": "dir", "desc_cn": "目录"}

    # 文件判断 - 先按FILE_DESC_RULES匹配
    for pattern, ftype, desc in FILE_DESC_RULES:
        if not pattern.endswith("/$") and re.match(pattern, file_path):
            # 语言文件特殊处理：统计键值对数量
            result = {"type": ftype, "desc_cn": desc}
            if ftype == "lang":
                result["key_count"] = None  # 将在外层计算
            if ftype == "mixin_config":
                result["mixin_count"] = None  # 将在外层计算
            return result

    # 兜底：按扩展名判断
    ftype = get_file_type(file_path)
    type_desc_map = {
        "class": "Java编译后的字节码文件",
        "json": "JSON配置文件",
        "png": "PNG图片文件",
        "toml": "TOML配置文件",
        "mcmeta": "资源元数据文件",
        "lang": "语言文件",
        "mixin_config": "Mixin配置文件",
        "audio": "音频文件",
        "shader": "着色器文件",
        "text": "文本文件",
    }
    return {"type": ftype, "desc_cn": type_desc_map.get(ftype, "未知类型文件")}


def build_file_tree(
    jar_path: Path, jar_file_list: List[str], temp_dir: Path
) -> Dict[str, Any]:
    """构建文件树结构

    Args:
        jar_path: JAR文件路径
        jar_file_list: JAR内文件列表
        temp_dir: 解压临时目录

    Returns:
        文件树字典
    """
    jar_name = jar_path.name
    root = {
        "name": jar_name,
        "type": "root",
        "desc_cn": f"JAR模组文件: {jar_name}",
        "children": [],
        "size": format_file_size(jar_path.stat().st_size),
    }

    # 统计信息
    stats = {
        "total_files": 0,
        "dir_count": 0,
        "class_files": 0,
        "json_files": 0,
        "png_files": 0,
        "toml_files": 0,
        "mcmeta_files": 0,
        "mixin_configs": 0,
        "lang_files": 0,
        "audio_files": 0,
        "shader_files": 0,
        "other_files": 0,
    }

    # 字典: 路径 -> 节点（用于构建树）
    dir_nodes: Dict[str, Dict] = {}
    dir_nodes[""] = root

    for file_path in jar_file_list:
        # 分类
        classified = classify_file(file_path)
        ftype = classified["type"]
        desc_cn = classified["desc_cn"]

        # 更新统计
        stats["total_files"] += 1
        type_map = {
            "class": "class_files",
            "json": "json_files",
            "png": "png_files",
            "toml": "toml_files",
            "mcmeta": "mcmeta_files",
            "mixin_config": "mixin_configs",
            "lang": "lang_files",
            "lang_legacy": "lang_files",
            "audio": "audio_files",
            "shader": "shader_files",
        }
        key = type_map.get(ftype, "other_files")
        stats[key] = stats.get(key, 0) + 1

        # 获取文件大小
        try:
            file_size = jar_path.stat().st_size  # 默认，实际需要从ZIP获取
        except Exception:
            file_size = 0

        # 构建文件节点
        file_name = file_path.split("/")[-1]
        file_node = {
            "name": file_path,
            "type": ftype,
            "desc_cn": desc_cn,
        }

        # 语言文件：统计键值对数量
        if ftype in ("lang", "lang_legacy"):
            key_count = _count_lang_keys(temp_dir / file_path)
            file_node["key_count"] = key_count
            file_node["desc_cn"] = f"{desc_cn}，共 {key_count} 条翻译"

        # Mixin配置：统计注入项数量
        if ftype == "mixin_config":
            mixin_count = _count_mixins(temp_dir / file_path)
            file_node["mixin_count"] = mixin_count
            file_node["desc_cn"] = f"{desc_cn}，注入 {mixin_count} 项"

        # 构建目录树
        parts = file_path.split("/")
        # 创建/获取所有中间目录
        current_path = ""
        current_node = root
        for i, part in enumerate(parts[:-1]):
            parent_path = current_path
            current_path = f"{current_path}/{part}" if current_path else part

            if current_path not in dir_nodes:
                dir_node = {
                    "name": part,
                    "type": "dir",
                    "desc_cn": _get_dir_desc(current_path),
                    "children": [],
                }
                dir_nodes[current_path] = dir_node
                dir_nodes[parent_path]["children"].append(dir_node)
                stats["dir_count"] += 1

            current_node = dir_nodes[current_path]

        # 添加文件到父目录
        current_node["children"].append(file_node)

    # 按名称排序每个目录的子节点
    _sort_tree(root)

    return root, stats


def _count_lang_keys(lang_file: Path) -> int:
    """统计语言文件中的键值对数量"""
    try:
        with open(lang_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return len(data)
        return 0
    except Exception:
        return 0


def _count_mixins(mixin_file: Path) -> int:
    """统计Mixin配置文件中的注入项数量"""
    try:
        with open(mixin_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        mixins = data.get("mixins", [])
        return len(mixins) if isinstance(mixins, list) else 0
    except Exception:
        return 0


def _get_dir_desc(dir_path: str) -> str:
    """根据目录路径生成中文释义"""
    for pattern, ftype, desc in FILE_DESC_RULES:
        if pattern.endswith("/$") and re.match(pattern, dir_path + "/"):
            return desc
    # 通用目录描述
    name = dir_path.split("/")[-1]
    dir_desc_map = {
        "META-INF": "元数据目录",
        "assets": "资源目录",
        "data": "数据包目录",
        "lang": "语言文件目录",
        "textures": "贴图目录",
        "models": "模型目录",
        "blockstates": "方块状态目录",
        "recipes": "合成配方目录",
        "loot_tables": "战利品表目录",
        "shaders": "着色器目录",
        "sounds": "音效目录",
        "font": "字体目录",
        "gui": "GUI目录",
        "functions": "函数目录",
        "advancements": "进度目录",
        "structures": "结构目录",
        "worldgen": "世界生成目录",
    }
    return dir_desc_map.get(name, f"子目录: {name}")


def _sort_tree(node: Dict) -> None:
    """递归排序树节点"""
    if "children" in node and node["children"]:
        # 目录优先，然后按名称排序
        node["children"].sort(
            key=lambda n: (0 if n["type"] == "dir" else 1, n["name"])
        )
        for child in node["children"]:
            _sort_tree(child)


def parse_mod_metadata(jar_path: Path, temp_dir: Path) -> Dict[str, Any]:
    """解析模组元数据

    尝试从 mods.toml / neoforge.mods.toml / fabric.mod.json 读取信息

    Args:
        jar_path: JAR文件路径
        temp_dir: 解压临时目录

    Returns:
        模组信息字典
    """
    mod_info = {
        "mod_id": "",
        "name": "",
        "version": "",
        "mc_version": "",
        "loader": "",
        "description": "",
        "dependencies": [],
        "authors": [],
        "license": "",
    }

    # 尝试 NeoForge/Forge 清单
    toml_paths = [
        "META-INF/neoforge.mods.toml",
        "META-INF/mods.toml",
    ]

    for toml_path in toml_paths:
        toml_file = temp_dir / toml_path
        if toml_file.exists():
            try:
                data = parse_toml(toml_file.read_text(encoding="utf-8"))
                mods = data.get("mods", [])
                if mods:
                    mod = mods[0]
                    mod_info["mod_id"] = mod.get("modId", "")
                    mod_info["name"] = mod.get("displayName", mod.get("modId", ""))
                    mod_info["version"] = mod.get("version", "")
                    mod_info["description"] = mod.get("description", "")
                    mod_info["authors"] = (
                        mod.get("authors", "").split(", ") if mod.get("authors") else []
                    )
                    mod_info["license"] = mod.get("license", "")

                deps = data.get("dependencies", {})
                if isinstance(deps, dict):
                    # 获取加载器类型 - 检查顶层和嵌套依赖
                    for loader in ("neoforge", "forge", "fabric", "quilt"):
                        if loader in deps:
                            mod_info["loader"] = loader
                            break
                    # 检查嵌套的加载器依赖 (如 dependencies.create.neoforge)
                    if not mod_info["loader"]:
                        for dep_key, dep_val in deps.items():
                            if isinstance(dep_val, dict):
                                for loader in ("neoforge", "forge", "fabric", "quilt"):
                                    if loader in dep_key.lower() or loader in dep_val:
                                        mod_info["loader"] = loader
                                        break
                            if mod_info["loader"]:
                                break

                    # 收集依赖
                    for dep_name, dep_info in deps.items():
                        if isinstance(dep_info, list):
                            for d in dep_info:
                                if isinstance(d, dict):
                                    mod_info["dependencies"].append(
                                        {
                                            "mod_id": d.get("modId", dep_name),
                                            "type": d.get("type", "required"),
                                            "version_range": d.get("versionRange", ""),
                                        }
                                    )
                        elif isinstance(dep_info, dict):
                            mod_info["dependencies"].append(
                                {
                                    "mod_id": dep_name,
                                    "type": dep_info.get("type", "required"),
                                    "version_range": dep_info.get("versionRange", ""),
                                }
                            )

                mod_info["loader"] = mod_info.get("loader", "forge")
                break
            except Exception as e:
                logger.warning(f"解析 {toml_path} 失败: {e}")

    # 尝试 Fabric 清单
    fabric_json = temp_dir / "fabric.mod.json"
    if fabric_json.exists() and not mod_info["mod_id"]:
        try:
            data = json.loads(fabric_json.read_text(encoding="utf-8"))
            mod_info["mod_id"] = data.get("id", "")
            mod_info["name"] = data.get("name", data.get("id", ""))
            mod_info["version"] = data.get("version", "")
            mod_info["description"] = data.get("description", "")
            mod_info["loader"] = "fabric"
            mod_info["license"] = data.get("license", "")

            deps = data.get("depends", {})
            if isinstance(deps, dict):
                for dep_name, dep_version in deps.items():
                    if dep_name not in ("fabricloader", "minecraft", "java"):
                        mod_info["dependencies"].append(
                            {
                                "mod_id": dep_name,
                                "type": "required",
                                "version_range": str(dep_version),
                            }
                        )
        except Exception as e:
            logger.warning(f"解析 fabric.mod.json 失败: {e}")

    # 尝试从 MANIFEST.MF 读取版本信息
    manifest_file = temp_dir / "META-INF" / "MANIFEST.MF"
    if manifest_file.exists() and not mod_info["version"]:
        try:
            manifest_content = manifest_file.read_text(encoding="utf-8", errors="ignore")
            for line in manifest_content.split("\n"):
                line = line.strip()
                if line.startswith("Implementation-Version:"):
                    mod_info["version"] = line.split(":", 1)[1].strip()
                elif line.startswith("Implementation-Title:"):
                    if not mod_info["name"]:
                        mod_info["name"] = line.split(":", 1)[1].strip()
        except Exception:
            pass

    # 从mod_id推断加载器
    if not mod_info["loader"]:
        if mod_info["mod_id"]:
            # 检查是否存在 neoforge.mods.toml 以判断是 NeoForge
            neoforge_toml = temp_dir / "META-INF" / "neoforge.mods.toml"
            if neoforge_toml.exists():
                mod_info["loader"] = "neoforge"
            else:
                mod_info["loader"] = "forge"

    return mod_info


def generate_html_report(
    mod_info: Dict,
    file_tree: Dict,
    stats: Dict,
    jar_path: Path,
    max_depth: int = 3,
) -> str:
    """生成HTML报告内容

    Args:
        mod_info: 模组元信息
        file_tree: 文件树
        stats: 统计信息
        jar_path: JAR路径
        max_depth: 树默认展开深度

    Returns:
        HTML内容字符串
    """
    gen = ReportGenerator(feature="jar_parser")

    # === 模组信息部分 ===
    info_rows = []
    field_labels = {
        "mod_id": "模组ID",
        "name": "模组名称",
        "version": "版本号",
        "loader": "加载器",
        "mc_version": "MC版本",
        "description": "描述",
        "license": "许可证",
    }
    for key, label in field_labels.items():
        val = mod_info.get(key, "")
        if val:
            info_rows.append([label, str(val)])

    # 作者
    authors = mod_info.get("authors", [])
    if authors:
        info_rows.append(["作者", ", ".join(authors)])

    mod_info_html = gen.render_table(["属性", "值"], info_rows)

    # === 依赖列表 ===
    deps = mod_info.get("dependencies", [])
    if deps:
        dep_rows = []
        for dep in deps:
            dep_rows.append([
                dep.get("mod_id", ""),
                dep.get("type", ""),
                dep.get("version_range", ""),
            ])
        deps_html = gen.render_table(
            ["依赖模组", "类型", "版本范围"], dep_rows
        )
    else:
        deps_html = "<p class='muted'>无依赖声明</p>"

    # === 统计信息 ===
    stat_rows = [
        ["总文件数", stats["total_files"]],
        ["目录数", stats["dir_count"]],
        [".class 字节码", stats["class_files"]],
        [".json 配置", stats["json_files"]],
        [".png 贴图", stats["png_files"]],
        [".toml 配置", stats["toml_files"]],
        ["Mixin配置", stats["mixin_configs"]],
        ["语言文件", stats["lang_files"]],
        ["音频文件", stats["audio_files"]],
        ["着色器", stats["shader_files"]],
        ["其他文件", stats["other_files"]],
    ]
    stats_html = gen.render_table(["类别", "数量"], stat_rows)

    # === 文件树 ===
    tree_html = gen.render_tree(file_tree, max_depth=max_depth)

    # === 组装报告 ===
    warnings = []
    if stats["total_files"] > 10000:
        warnings.append("模组文件数量超过10000个，可能需要较长时间加载")
    if stats["mixin_configs"] > 0:
        warnings.append("模组使用了Mixin注入，升级版本时需重点关注兼容性")
    if stats["class_files"] > 500:
        warnings.append("模组包含大量.class文件，体积较大")

    warnings_html = gen.render_warnings(warnings) if warnings else ""

    # 说明
    tip_html = gen.render_callout(
        "使用说明",
        "<p>点击文件树中的目录名可展开/折叠子节点。"
        "悬停在文件上可查看中文释义。"
        "此文件树结构可直接提供给 F4(冲突扫描)、F5(重打包)、F7(汉化) 使用。</p>",
        level="info",
    )

    content = (
        gen.render_section("模组基本信息", mod_info_html, tag="mod_info")
        + gen.render_section("依赖关系", deps_html, tag="dependencies")
        + gen.render_section("文件统计", stats_html, tag="statistics")
        + gen.render_section("文件结构（点击展开）", tip_html + tree_html, tag="file_tree")
        + warnings_html
    )

    return content


def run(args) -> Dict[str, Any]:
    """F1 JAR结构解析主入口

    Args:
        args: argparse.Namespace，需包含:
            - jar_path: JAR文件路径
            - output: 输出目录（可选）
            - detail_level: basic/detailed

    Returns:
        统一返回结构字典
    """
    jar_path = Path(args.jar_path)

    # 1. 输入验证
    if not jar_path.exists():
        logger.error(f"JAR文件不存在: {jar_path}")
        return config.build_result(
            feature="jar_parser",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=[f"JAR文件不存在: {jar_path}"],
        )

    if jar_path.suffix.lower() not in (".jar", ".zip"):
        logger.error(f"文件格式不支持: {jar_path.suffix}")
        return config.build_result(
            feature="jar_parser",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=[f"文件格式不支持，仅支持 .jar/.zip"],
        )

    file_size_mb = jar_path.stat().st_size / (1024 * 1024)
    warnings = []
    if file_size_mb > 100:
        warnings.append(f"JAR文件较大 ({file_size_mb:.1f}MB)，解析可能需要较长时间")

    logger.info(f"开始解析JAR: {jar_path.name} ({file_size_mb:.1f}MB)")

    # 2. 解压JAR
    temp_dir = create_temp_dir("jar_parser")
    try:
        extract_jar(jar_path, temp_dir)
    except zipfile.BadZipFile:
        return config.build_result(
            feature="jar_parser",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=["JAR文件损坏，请重新下载"],
        )
    except Exception as e:
        return config.build_result(
            feature="jar_parser",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=[f"JAR解压失败: {e}"],
        )

    # 3. 解析模组元数据
    mod_info = parse_mod_metadata(jar_path, temp_dir)
    logger.info(
        f"模组信息: id={mod_info['mod_id']}, name={mod_info['name']}, "
        f"version={mod_info['version']}, loader={mod_info['loader']}"
    )

    if not mod_info["mod_id"]:
        warnings.append("未在JAR中找到mods.toml或fabric.mod.json，可能是通用JAR而非模组")

    # 4. 获取文件列表
    jar_file_list = list_jar_files(jar_path)

    # 5. 构建文件树
    file_tree, stats = build_file_tree(jar_path, jar_file_list, temp_dir)
    logger.info(f"文件统计: {stats['total_files']}个文件")

    # 6. 生成报告
    jar_stem = jar_path.stem
    html_content = generate_html_report(
        mod_info, file_tree, stats, jar_path, max_depth=3
    )

    output_files = generate_unified_output(
        feature="jar_parser",
        status="success",
        input_summary={
            "jar_path": str(jar_path),
            "detail_level": getattr(args, "detail_level", "basic"),
        },
        result={
            "mod_info": mod_info,
            "file_tree": file_tree,
            "statistics": stats,
        },
        title=f"JAR结构解析报告 - {mod_info.get('name') or jar_stem}",
        html_content=html_content,
        warnings=warnings,
        mod_name=jar_stem,
    )

    # 7. 清理临时目录
    cleanup_temp_dir(temp_dir)

    logger.info(f"解析完成: {jar_path.name}")
    return config.build_result(
        feature="jar_parser",
        status="success",
        input_summary={"jar_path": str(jar_path)},
        result={
            "mod_info": mod_info,
            "file_tree": file_tree,
            "statistics": stats,
        },
        warnings=warnings,
        output_files=output_files,
    )
