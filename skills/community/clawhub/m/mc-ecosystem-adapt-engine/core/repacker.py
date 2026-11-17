# -*- coding: utf-8 -*-
"""F5: 资源级全自动重新打包固化

解压JAR文件，替换汉化资源、修改配置文件、校验格式完整性，
重新打包为可用JAR。仅处理资源、文本、配置类文件，
不涉及源码编译与代码层级修改。

使用方式:
    from core.repacker import run
    import argparse
    args = argparse.Namespace(
        jar_path="xxx.jar",
        resources_dir="modified_resources/",
        output=None,
        validate=True
    )
    result = run(args)
"""

import sys
import os
import json
import shutil
import zipfile
import struct
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.jar_utils import (
    extract_jar, create_jar, validate_jar,
    create_temp_dir, cleanup_temp_dir,
    is_file_locked, format_file_size
)
from utils.report_gen import ReportGenerator, generate_unified_output

logger = get_logger("repacker")

# === 支持的资源文件类型 ===
SUPPORTED_RESOURCE_EXTS = {
    ".json", ".png", ".jpg", ".jpeg", ".toml", ".mcmeta",
    ".lang", ".txt", ".ogg", ".fsh", ".vsh", ".glsl",
    ".nbt", ".mcfunction",
}

# === PNG文件头魔数 ===
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def validate_json_file(file_path: Path) -> tuple:
    """验证JSON文件格式

    Args:
        file_path: 文件路径

    Returns:
        (is_valid, error_message) 元组
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        json.loads(content)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"JSON语法错误: {e}"
    except Exception as e:
        return False, f"读取文件失败: {e}"


def validate_png_file(file_path: Path) -> tuple:
    """验证PNG文件格式（检查魔数）

    Args:
        file_path: 文件路径

    Returns:
        (is_valid, error_message) 元组
    """
    try:
        with open(file_path, "rb") as f:
            header = f.read(8)
        if len(header) < 8:
            return False, "PNG文件过小，可能已损坏"
        if header[:8] != PNG_MAGIC:
            return False, "不是有效的PNG文件（魔数不匹配）"
        return True, ""
    except Exception as e:
        return False, f"读取PNG文件失败: {e}"


def validate_toml_file(file_path: Path) -> tuple:
    """验证TOML文件格式

    Args:
        file_path: 文件路径

    Returns:
        (is_valid, error_message) 元组
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        import tomllib
        tomllib.loads(content)
        return True, ""
    except ImportError:
        try:
            import tomli as tomllib
            tomllib.loads(content)
            return True, ""
        except Exception as e:
            return False, f"TOML解析失败: {e}"
    except Exception as e:
        return False, f"TOML语法错误: {e}"


def validate_resource_file(file_path: Path) -> tuple:
    """根据扩展名验证资源文件格式

    Args:
        file_path: 文件路径

    Returns:
        (is_valid, error_message) 元组
    """
    ext = file_path.suffix.lower()

    validators = {
        ".json": validate_json_file,
        ".mcmeta": validate_json_file,  # .mcmeta 也是JSON
        ".lang": validate_json_file,  # .lang 也是JSON格式
        ".toml": validate_toml_file,
        ".png": validate_png_file,
    }

    validator = validators.get(ext)
    if validator:
        return validator(file_path)

    # 其他类型文件默认通过（如.txt, .ogg, .mcfunction等）
    return True, ""


def build_resource_mapping(
    resources_dir: Path, temp_dir: Path
) -> Dict[str, Dict[str, Any]]:
    """构建资源文件映射关系

    将 resources_dir 中的文件映射到JAR内部对应路径，
    并检查该路径是否存在于解压后的JAR中。

    Args:
        resources_dir: 修改后的资源目录
        temp_dir: JAR解压临时目录

    Returns:
        映射字典: {相对路径: {"source": 源文件路径, "exists_in_jar": 是否存在于JAR}}
    """
    mapping = {}
    resources_dir = resources_dir.resolve()

    for root, dirs, files in os.walk(resources_dir):
        for file_name in files:
            source_file = Path(root) / file_name
            rel_path = source_file.relative_to(resources_dir).as_posix()

            # 检查该路径在JAR中是否存在
            jar_target = temp_dir / rel_path
            exists_in_jar = jar_target.exists()

            mapping[rel_path] = {
                "source": source_file,
                "exists_in_jar": exists_in_jar,
                "size": source_file.stat().st_size,
            }

    return mapping


def replace_resources(
    temp_dir: Path,
    mapping: Dict[str, Dict[str, Any]],
    do_validate: bool = True,
) -> Dict[str, Any]:
    """执行资源替换

    Args:
        temp_dir: JAR解压临时目录
        mapping: 资源映射
        do_validate: 是否校验文件格式

    Returns:
        替换结果统计
    """
    stats = {
        "replaced": 0,
        "added": 0,
        "skipped_not_found": 0,
        "validation_errors": [],
        "replaced_files": [],
        "added_files": [],
    }

    for rel_path, info in mapping.items():
        source_file = info["source"]
        target_file = temp_dir / rel_path

        # 格式校验
        if do_validate:
            is_valid, error_msg = validate_resource_file(source_file)
            if not is_valid:
                stats["validation_errors"].append({
                    "file": rel_path,
                    "error": error_msg,
                })
                logger.warning(f"文件校验失败，跳过: {rel_path} - {error_msg}")
                continue

        # 执行替换或新增
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)

        if info["exists_in_jar"]:
            stats["replaced"] += 1
            stats["replaced_files"].append(rel_path)
            logger.info(f"替换: {rel_path}")
        else:
            stats["added"] += 1
            stats["added_files"].append(rel_path)
            logger.info(f"新增: {rel_path}")

    return stats


def generate_repack_html(
    jar_path: Path,
    output_jar: Path,
    stats: Dict[str, Any],
    validate: bool,
) -> str:
    """生成重打包报告HTML

    Args:
        jar_path: 原始JAR路径
        output_jar: 输出JAR路径
        stats: 替换统计
        validate: 是否启用校验

    Returns:
        HTML内容
    """
    gen = ReportGenerator(feature="repacker")

    # 基本信息
    info_rows = [
        ["原始JAR", str(jar_path)],
        ["输出JAR", str(output_jar)],
        ["原始大小", format_file_size(jar_path.stat().st_size)],
        ["输出大小", format_file_size(output_jar.stat().st_size)],
        ["校验模式", "开启" if validate else "关闭"],
    ]
    info_html = gen.render_table(["项目", "值"], info_rows)

    # 替换统计
    stat_rows = [
        ["替换文件数", stats["replaced"]],
        ["新增文件数", stats["added"]],
        ["校验失败数", len(stats["validation_errors"])],
    ]
    stats_html = gen.render_table(["类别", "数量"], stat_rows)

    # 校验错误详情
    validation_html = ""
    if stats["validation_errors"]:
        error_rows = [
            [e["file"], e["error"]]
            for e in stats["validation_errors"]
        ]
        validation_html = gen.render_table(
            ["文件", "错误信息"], error_rows
        )

    # 替换文件列表（最多显示50个）
    replaced_html = ""
    if stats["replaced_files"]:
        files_to_show = stats["replaced_files"][:50]
        file_rows = [[f] for f in files_to_show]
        if len(stats["replaced_files"]) > 50:
            file_rows.append([f"... 还有 {len(stats['replaced_files']) - 50} 个文件未显示"])
        replaced_html = gen.render_table(
            ["已替换文件"], file_rows
        )

    added_html = ""
    if stats["added_files"]:
        files_to_show = stats["added_files"][:50]
        file_rows = [[f] for f in files_to_show]
        if len(stats["added_files"]) > 50:
            file_rows.append([f"... 还有 {len(stats['added_files']) - 50} 个文件未显示"])
        added_html = gen.render_table(
            ["新增文件"], file_rows
        )

    # 组装
    content = gen.render_section("重打包信息", info_html, tag="info")
    content += gen.render_section("替换统计", stats_html, tag="statistics")

    if validation_html:
        content += gen.render_section(
            "校验错误（已跳过这些文件）", validation_html, tag="errors"
        )

    if replaced_html:
        content += gen.render_section("已替换文件列表", replaced_html, tag="replaced")

    if added_html:
        content += gen.render_section("新增文件列表", added_html, tag="added")

    # 提示
    tip_html = gen.render_callout(
        "使用提示",
        "<p>重打包完成！新的JAR文件已保存。"
        "将新JAR放入 mods 文件夹即可使用。"
        "如有游戏崩溃，请使用 F8(报错修复) 分析错误日志。</p>",
        level="green" if not stats["validation_errors"] else "yellow",
    )
    content += tip_html

    return content


def run(args) -> Dict[str, Any]:
    """F5 资源级重打包主入口

    Args:
        args: argparse.Namespace，需包含:
            - jar_path: 原始JAR文件路径
            - resources_dir: 修改后的资源目录
            - output: 输出JAR路径（可选）
            - validate: 是否校验文件格式

    Returns:
        统一返回结构字典
    """
    jar_path = Path(args.jar_path)
    resources_dir = Path(args.resources_dir)
    do_validate = getattr(args, "validate", True)

    # 1. 输入验证
    if not jar_path.exists():
        return config.build_result(
            feature="repacker",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=[f"原始JAR不存在: {jar_path}"],
        )

    if not resources_dir.exists():
        return config.build_result(
            feature="repacker",
            status="error",
            input_summary={
                "jar_path": str(jar_path),
                "resources_dir": str(resources_dir),
            },
            result={},
            errors=[f"资源目录不存在: {resources_dir}"],
        )

    if not jar_path.is_file():
        return config.build_result(
            feature="repacker",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=[f"路径不是文件: {jar_path}"],
        )

    if not resources_dir.is_dir():
        return config.build_result(
            feature="repacker",
            status="error",
            input_summary={"resources_dir": str(resources_dir)},
            result={},
            errors=[f"路径不是目录: {resources_dir}"],
        )

    # 检查文件锁
    if is_file_locked(jar_path):
        return config.build_result(
            feature="repacker",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=[
                "JAR文件被占用！请关闭正在运行的游戏或其他占用该文件的程序后重试。"
            ],
        )

    # 2. 确定输出路径
    output_path = getattr(args, "output", None)
    jar_stem = jar_path.stem

    if output_path and not Path(output_path).is_dir():
        output_jar = Path(output_path)
    else:
        output_dir = config.OUTPUT_DIR / "downloads"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_jar = output_dir / f"{jar_stem}_patched.jar"

    logger.info(f"开始重打包: {jar_path.name} -> {output_jar.name}")

    # 3. 解压原JAR
    temp_dir = create_temp_dir("repacker")
    try:
        extract_jar(jar_path, temp_dir)
    except zipfile.BadZipFile:
        cleanup_temp_dir(temp_dir)
        return config.build_result(
            feature="repacker",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=["JAR文件损坏，无法解压"],
        )
    except Exception as e:
        cleanup_temp_dir(temp_dir)
        return config.build_result(
            feature="repacker",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=[f"JAR解压失败: {e}"],
        )

    # 4. 构建资源映射
    mapping = build_resource_mapping(resources_dir, temp_dir)
    logger.info(f"发现 {len(mapping)} 个资源文件待处理")

    if not mapping:
        cleanup_temp_dir(temp_dir)
        return config.build_result(
            feature="repacker",
            status="error",
            input_summary={
                "jar_path": str(jar_path),
                "resources_dir": str(resources_dir),
            },
            result={},
            errors=[
                f"资源目录中没有可替换的文件。"
                f"请确认资源目录结构与JAR内部路径一致"
                f"（如 resources/assets/create/lang/zh_cn.json 对应JAR内 assets/create/lang/zh_cn.json）。"
            ],
        )

    # 5. 执行替换
    replace_stats = replace_resources(temp_dir, mapping, do_validate)

    # 6. 重新打包
    try:
        create_jar(temp_dir, output_jar)
    except Exception as e:
        cleanup_temp_dir(temp_dir)
        return config.build_result(
            feature="repacker",
            status="error",
            input_summary={"jar_path": str(jar_path)},
            result={},
            errors=[f"JAR打包失败: {e}"],
        )

    # 7. 验证新JAR
    try:
        is_valid = validate_jar(output_jar)
        if not is_valid:
            cleanup_temp_dir(temp_dir)
            return config.build_result(
                feature="repacker",
                status="error",
                input_summary={"jar_path": str(jar_path)},
                result={
                    "output_jar": str(output_jar),
                    "replace_stats": replace_stats,
                },
                errors=[
                    "新JAR完整性校验失败！"
                    f"临时目录保留在: {temp_dir}，请检查后手动清理"
                ],
            )
    except Exception as e:
        logger.warning(f"JAR校验异常: {e}")

    # 8. 生成报告
    html_content = generate_repack_html(jar_path, output_jar, replace_stats, do_validate)

    output_files = generate_unified_output(
        feature="repacker",
        status="success",
        input_summary={
            "jar_path": str(jar_path),
            "resources_dir": str(resources_dir),
            "validate": do_validate,
        },
        result={
            "output_jar": str(output_jar),
            "replace_stats": replace_stats,
        },
        title=f"重打包报告 - {jar_path.stem}",
        html_content=html_content,
        warnings=[e["error"] for e in replace_stats["validation_errors"]],
        mod_name=jar_path.stem,
    )

    # 9. 清理临时目录
    cleanup_temp_dir(temp_dir)

    logger.info(
        f"重打包完成: {output_jar.name} "
        f"(替换{replace_stats['replaced']}个, 新增{replace_stats['added']}个)"
    )

    return config.build_result(
        feature="repacker",
        status="success",
        input_summary={
            "jar_path": str(jar_path),
            "resources_dir": str(resources_dir),
        },
        result={
            "output_jar": str(output_jar),
            "replace_stats": replace_stats,
        },
        warnings=[e["error"] for e in replace_stats["validation_errors"]],
        output_files=output_files,
    )
