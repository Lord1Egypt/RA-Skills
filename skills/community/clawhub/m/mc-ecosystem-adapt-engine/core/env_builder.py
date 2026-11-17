# -*- coding: utf-8 -*-
"""F3: 全端全启动器环境智能引导搭建

自动检测系统环境，根据MC版本推荐Java版本，根据启动器类型
生成配置参数和分步图文教程，生成辅助安装脚本。

使用方式:
    from core.env_builder import run
    import argparse
    args = argparse.Namespace(
        launcher="pcl2",
        mc_version="1.21.1",
        loader="neoforge",
        device="pc",
        output=None
    )
    result = run(args)
"""

import sys
import os
import json
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.report_gen import ReportGenerator, generate_unified_output

logger = get_logger("env_builder")

# === 启动器推荐下载链接 ===
LAUNCHER_DOWNLOADS = {
    "pcl2": {
        "name": "PCL2",
        "url": "https://www.plmcl.net/",
        "note": "帕斯卡的启动器，国内流行，支持正版登录",
    },
    "hmcl": {
        "name": "HMCL",
        "url": "https://hmcl.huangyuhui.net/",
        "note": "开源免费的MC启动器，支持离线登录",
    },
    "xmcl": {
        "name": "XMCL",
        "url": "https://xmcl.net/",
        "note": "轻量级启动器，支持多版本管理",
    },
    "prism": {
        "name": "Prism Launcher",
        "url": "https://prismlauncher.org/",
        "note": "多实例启动器，支持Fabric/Quilt/NeoForge",
    },
    "bakaxl": {
        "name": "BakaXL",
        "url": "https://bakaxl.net/",
        "note": "国产启动器，界面精美",
    },
    "fcl": {
        "name": "FCL",
        "url": "https://fcl.projectx.top/",
        "note": "手机端启动器，支持安卓",
    },
    "pojav": {
        "name": "PojavLauncher",
        "url": "https://pojav.net/",
        "note": "手机端启动器，支持iOS/Android",
    },
    "ling_zalith": {
        "name": "Zalith Launcher",
        "url": "",
        "note": "MC启动器，支持多平台",
    },
    "netease": {
        "name": "网易我的世界",
        "url": "https://mc.163.com/",
        "note": "网易官方代理版，需网易账号",
    },
}

# === Java推荐下载链接 ===
JAVA_DOWNLOADS = {
    "21": [
        {
            "name": "Eclipse Temurin JDK 21 (推荐)",
            "url": "https://adoptium.net/temurin/releases/?version=21",
            "note": "OpenJDK社区版，免费开源，MC官方推荐",
        },
        {
            "name": "Oracle JDK 21",
            "url": "https://www.oracle.com/java/technologies/downloads/#java21",
            "note": "Oracle官方版本",
        },
    ],
    "17": [
        {
            "name": "Eclipse Temurin JDK 17 (推荐)",
            "url": "https://adoptium.net/temurin/releases/?version=17",
            "note": "OpenJDK社区版，免费开源",
        },
        {
            "name": "Oracle JDK 17",
            "url": "https://www.oracle.com/java/technologies/downloads/#java17",
            "note": "Oracle官方版本",
        },
    ],
    "16": [
        {
            "name": "Eclipse Temurin JDK 16",
            "url": "https://adoptium.net/temurin/releases/?version=16",
            "note": "过渡版本，不推荐新使用",
        },
    ],
    "8": [
        {
            "name": "Eclipse Temurin JDK 8",
            "url": "https://adoptium.net/temurin/releases/?version=8",
            "note": "老版本MC使用",
        },
    ],
}

# === JVM参数预设 ===
JVM_PRESETS = {
    "pc": {
        "min_mem": "2G",
        "max_mem": "4G",
        "gc": "G1GC",
        "args": "-XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20",
    },
    "pc_large": {
        "min_mem": "4G",
        "max_mem": "8G",
        "gc": "G1GC",
        "args": "-XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20",
    },
    "mobile": {
        "min_mem": "512M",
        "max_mem": "2G",
        "gc": "G1GC",
        "args": "-XX:+UseG1GC -XX:G1NewSizePercent=10",
    },
}


def detect_system() -> Dict[str, Any]:
    """检测系统环境

    Returns:
        系统信息字典
    """
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "java_installed": False,
        "java_version": "",
        "java_home": "",
        "memory_total_gb": 0,
        "memory_available_gb": 0,
    }

    # 检测Java
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            info["java_installed"] = True
            # 从stderr解析版本（java -version输出到stderr）
            output = result.stderr or result.stdout
            for line in output.split("\n"):
                if "version" in line.lower():
                    # 提取版本号 "1.21.01" or "21.0.1"
                    import re
                    match = re.search(r'(\d+\.\d+\.\d+)', line)
                    if match:
                        info["java_version"] = match.group(1)
                    break
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 检测JAVA_HOME
    java_home = os.environ.get("JAVA_HOME", "")
    if java_home:
        info["java_home"] = java_home

    # 检测内存
    try:
        import psutil
        mem = psutil.virtual_memory()
        info["memory_total_gb"] = round(mem.total / (1024**3), 1)
        info["memory_available_gb"] = round(mem.available / (1024**3), 1)
    except ImportError:
        try:
            # Windows: 通过wmic获取
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["wmic", "OS", "get", "TotalVisibleMemorySize"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                lines = result.stdout.strip().split("\n")
                if len(lines) >= 2:
                    total_kb = int(lines[1].strip())
                    info["memory_total_gb"] = round(total_kb / (1024 * 1024), 1)
        except Exception:
            pass

    logger.info(f"系统检测完成: OS={info['os']}, Java={info['java_version'] or '未安装'}")
    return info


def get_java_recommendation(mc_version: str) -> Dict[str, Any]:
    """根据MC版本推荐Java版本

    Args:
        mc_version: MC版本号

    Returns:
        推荐信息字典
    """
    java_ver = config.get_java_version(mc_version)

    if not java_ver:
        return {
            "recommended_java": "",
            "status": "unknown",
            "message": f"无法为MC {mc_version} 匹配Java版本",
            "downloads": [],
        }

    downloads = JAVA_DOWNLOADS.get(java_ver, [])

    return {
        "recommended_java": java_ver,
        "status": "ok",
        "message": f"MC {mc_version} 需要 Java {java_ver}",
        "downloads": downloads,
    }


def detect_java_match(system_info: Dict, java_ver: str) -> Dict[str, Any]:
    """检测当前Java版本是否匹配推荐

    Args:
        system_info: 系统信息
        java_ver: 推荐的Java版本号

    Returns:
        匹配结果
    """
    if not system_info["java_installed"]:
        return {
            "matched": False,
            "reason": "Java未安装",
            "action": "请下载安装推荐的Java版本",
        }

    installed = system_info["java_version"]
    if not installed:
        return {
            "matched": False,
            "reason": "无法识别已安装的Java版本",
            "action": "请确认Java安装是否正确",
        }

    # 比较主版本号
    try:
        parts = installed.split(".")
        if parts[0] == "1":
            # Java 8 格式: 1.8.0_381
            major = parts[1]
        else:
            major = parts[0]

        if str(major) == java_ver:
            return {
                "matched": True,
                "reason": f"已安装Java {installed}，符合要求",
                "action": "无需额外操作",
            }
        else:
            return {
                "matched": False,
                "reason": f"已安装Java {installed}，需要Java {java_ver}",
                "action": "请安装推荐的Java版本（可与现有版本共存）",
            }
    except (IndexError, ValueError):
        return {
            "matched": False,
            "reason": f"无法解析Java版本号: {installed}",
            "action": "请确认Java安装是否正确",
        }


def generate_launcher_config(
    launcher: str,
    mc_version: str,
    loader: str,
    device: str,
    system_info: Dict,
) -> Dict[str, Any]:
    """生成启动器配置

    Args:
        launcher: 启动器类型
        mc_version: MC版本
        loader: 加载器
        device: 设备类型
        system_info: 系统信息

    Returns:
        配置字典
    """
    launcher_info = config.get_launcher_info(launcher)
    launcher_download = LAUNCHER_DOWNLOADS.get(launcher, {})

    # 选择JVM预设
    available_mem = system_info.get("memory_available_gb", 0)
    if device == "mobile":
        jvm = JVM_PRESETS["mobile"]
    elif available_mem >= 8:
        jvm = JVM_PRESETS["pc_large"]
    else:
        jvm = JVM_PRESETS["pc"]

    config_data = {
        "launcher": launcher,
        "launcher_name": launcher_download.get("name", launcher),
        "mc_version": mc_version,
        "loader": loader,
        "device": device,
        "launcher_download_url": launcher_download.get("url", ""),
        "launcher_note": launcher_download.get("note", ""),
        "jvm_config": {
            "min_memory": jvm["min_mem"],
            "max_memory": jvm["max_mem"],
            "gc": jvm["gc"],
            "args": jvm["args"],
        },
        "game_dirs": {
            "saves": launcher_info.get("saves_path", ".minecraft/saves/"),
            "mods": launcher_info.get("mods_path", ".minecraft/mods/"),
        },
    }

    return config_data


def generate_install_bat(
    launcher: str,
    mc_version: str,
    java_ver: str,
    launcher_download_url: str,
) -> str:
    """生成PC端安装辅助脚本

    Args:
        launcher: 启动器类型
        mc_version: MC版本
        java_ver: Java版本
        launcher_download_url: 启动器下载链接

    Returns:
        .bat脚本内容
    """
    launcher_name = LAUNCHER_DOWNLOADS.get(launcher, {}).get("name", launcher)
    java_ver_display = java_ver or "对应版本"
    java_download_url = (
        f"https://adoptium.net/temurin/releases/?version={java_ver}"
        if java_ver
        else "https://adoptium.net/temurin/releases/"
    )

    bat_content = f"""@echo off
chcp 65001 >nul
title MC全生态智能适配工程师 - 环境搭建脚本
echo ============================================================
echo  MC环境搭建辅助脚本
echo  MC版本: {mc_version} | Java: {java_ver_display} | 启动器: {launcher_name}
echo ============================================================
echo.

echo [1/4] 创建目录结构...
if not exist "%USERPROFILE%\\.minecraft\\mods" mkdir "%USERPROFILE%\\.minecraft\\mods"
if not exist "%USERPROFILE%\\.minecraft\\saves" mkdir "%USERPROFILE%\\.minecraft\\saves"
if not exist "%USERPROFILE%\\.minecraft\\resourcepacks" mkdir "%USERPROFILE%\\.minecraft\\resourcepacks"
echo  目录创建完成
echo.

echo [2/4] 打开Java下载页面...
start "" "{java_download_url}"
echo  请在浏览器中下载并安装 Java {java_ver_display}
echo.

echo [3/4] 打开启动器下载页面...
start "" "{launcher_download_url}"
echo  请在浏览器中下载并安装 {launcher_name}
echo.

echo [4/4] 打开.minecraft目录...
explorer "%USERPROFILE%\\.minecraft"
echo.

echo ============================================================
echo  下一步操作:
echo  1. 安装下载的 Java {java_ver_display} (安装时勾选 "Add to PATH")
echo  2. 安装下载的 {launcher_name} 启动器
echo  3. 打开 {launcher_name}，添加MC版本 {mc_version}
echo  4. 将模组JAR文件放入 .minecraft\\mods 目录
echo  5. 启动游戏，确认运行正常
echo ============================================================
echo.
pause
"""
    return bat_content


def generate_setup_html(
    system_info: Dict,
    java_rec: Dict,
    java_match: Dict,
    launcher_config: Dict,
    install_bat: str,
) -> str:
    """生成环境搭建HTML教程

    Args:
        system_info: 系统信息
        java_rec: Java推荐信息
        java_match: Java匹配结果
        launcher_config: 启动器配置
        install_bat: 安装脚本内容

    Returns:
        HTML内容
    """
    gen = ReportGenerator(feature="env_builder")

    launcher_name = launcher_config.get("launcher_name", "")
    mc_version = launcher_config.get("mc_version", "")
    loader = launcher_config.get("loader", "")

    # === 系统信息 ===
    sys_rows = [
        ["操作系统", f"{system_info['os']} {system_info['os_release']}"],
        ["系统版本", system_info["os_version"]],
        ["架构", system_info["machine"]],
        ["处理器", system_info["processor"] or "未知"],
        ["内存总量", f"{system_info['memory_total_gb']} GB"],
        ["可用内存", f"{system_info['memory_available_gb']} GB"],
        ["Python版本", system_info["python_version"]],
    ]

    if system_info["java_installed"]:
        java_status = f"✅ 已安装 Java {system_info['java_version']}"
    else:
        java_status = "❌ 未安装 Java"
    sys_rows.append(["Java状态", java_status])

    sys_html = gen.render_table(["项目", "值"], sys_rows)

    # === Java推荐 ===
    java_rows = [
        ["推荐版本", f"Java {java_rec['recommended_java']}"],
        ["当前状态", java_match["reason"]],
        ["建议操作", java_match["action"]],
    ]

    # Java下载链接
    if java_rec.get("downloads"):
        for d in java_rec["downloads"]:
            java_rows.append([f"下载: {d['name']}", d["url"]])
            java_rows.append(["说明", d["note"]])

    java_html = gen.render_table(["项目", "值"], java_rows)

    # === 启动器配置 ===
    lc = launcher_config
    config_rows = [
        ["启动器", f"{lc['launcher_name']} ({lc['launcher']})"],
        ["下载地址", lc["launcher_download_url"]],
        ["启动器说明", lc["launcher_note"]],
        ["MC版本", lc["mc_version"]],
        ["加载器", lc["loader"]],
        ["设备类型", lc["device"]],
        ["JVM最小内存", lc["jvm_config"]["min_memory"]],
        ["JVM最大内存", lc["jvm_config"]["max_memory"]],
        ["GC策略", lc["jvm_config"]["gc"]],
        ["JVM参数", lc["jvm_config"]["args"]],
        ["存档目录", lc["game_dirs"]["saves"]],
        ["模组目录", lc["game_dirs"]["mods"]],
    ]
    config_html = gen.render_table(["项目", "值"], config_rows)

    # === 安装步骤 ===
    java_ver = java_rec.get('recommended_java', '')
    java_url = f"https://adoptium.net/temurin/releases/?version={java_ver}" if java_ver else "https://adoptium.net/temurin/releases/"
    java_label = f"Java {java_ver}" if java_ver else "Java"

    steps_html = f"""
    <div class='callout'>
      <div class='callout-title'>📋 安装步骤</div>
      <ol>
        <li><strong>安装 {java_label}</strong>
          <br>访问: <a href='{java_url}' target='_blank'>{java_url}</a>
          <br>下载 Windows x64 Installer (.msi)，双击安装，<strong>务必勾选 "Add to PATH"</strong>
        </li>
        <li><strong>安装 {launcher_name} 启动器</strong>
          <br>访问: <a href='{lc["launcher_download_url"]}' target='_blank'>{lc["launcher_download_url"]}</a>
          <br>下载并安装启动器
        </li>
        <li><strong>配置启动器</strong>
          <br>打开 {launcher_name}，添加MC版本 {mc_version}，选择加载器 {loader}
          <br>在启动设置中配置 JVM 参数: -Xms{lc['jvm_config']['min_memory']} -Xmx{lc['jvm_config']['max_memory']} {lc['jvm_config']['args']}
        </li>
        <li><strong>安装模组</strong>
          <br>将下载的模组JAR文件放入 mods 目录
          <br>启动游戏，确认模组加载正常
        </li>
      </ol>
    </div>
    """

    # === 网易版特殊说明 ===
    netease_warning = ""
    if lc["launcher"] == "netease":
        netease_warning = gen.render_callout(
            "网易版环境优化",
            "<p><strong>网易版特殊说明：</strong></p>"
            "<ul>"
            "<li>网易版使用官方启动器，Java环境已内置</li>"
            "<li>内存分配建议: 4G以上</li>"
            "<li>网易版模组需从网易版资源包下载，与正版模组不互通</li>"
            "<li>本工具检索的模组为正版（Modrinth/CurseForge），需人工核对网易端是否上架</li>"
            "<li>JVM参数: -Xms2G -Xmx4G -XX:+UseG1GC</li>"
            "</ul>",
            level="yellow",
        )

    # === 组装 ===
    content = gen.render_section("系统检测", sys_html, tag="system")
    content += gen.render_section("Java环境配置", java_html, tag="java")
    content += gen.render_section("启动器配置", config_html, tag="launcher")
    content += gen.render_section("安装步骤", steps_html, tag="steps")
    content += netease_warning

    # 脚本下载提示
    tip_html = gen.render_callout(
        "辅助脚本",
        f"<p>已生成辅助安装脚本 <code>install_{lc['launcher']}.bat</code>，"
        "双击即可自动创建目录结构和打开下载页面。</p>",
        level="info",
    )
    content += tip_html

    return content


def run(args) -> Dict[str, Any]:
    """F3 环境引导搭建主入口

    Args:
        args: argparse.Namespace，需包含:
            - launcher: 启动器类型
            - mc_version: MC版本
            - loader: 加载器
            - device: 设备类型
            - output: 输出目录

    Returns:
        统一返回结构字典
    """
    launcher = args.launcher
    mc_version = args.mc_version
    loader = args.loader
    device = getattr(args, "device", "pc")

    # 1. 输入验证
    if launcher not in config.LAUNCHERS:
        return config.build_result(
            feature="env_builder",
            status="error",
            input_summary={"launcher": launcher},
            result={},
            errors=[f"无效的启动器类型: {launcher}，支持: {', '.join(config.LAUNCHERS)}"],
        )

    if loader not in config.LOADERS:
        return config.build_result(
            feature="env_builder",
            status="error",
            input_summary={"loader": loader},
            result={},
            errors=[f"无效的加载器类型: {loader}，支持: {', '.join(config.LOADERS)}"],
        )

    warnings = []
    logger.info(f"开始环境搭建: {launcher} + {mc_version} + {loader}")

    # 2. 系统检测
    system_info = detect_system()

    # 3. Java版本推荐
    java_rec = get_java_recommendation(mc_version)

    if java_rec["status"] != "ok":
        warnings.append(java_rec["message"])

    # 4. Java匹配检测
    java_match = detect_java_match(system_info, java_rec["recommended_java"])

    if not java_match["matched"]:
        warnings.append(f"Java版本不匹配: {java_match['reason']}")

    # 5. 启动器配置生成
    launcher_config = generate_launcher_config(
        launcher, mc_version, loader, device, system_info
    )

    # 6. 生成安装脚本
    install_bat = generate_install_bat(
        launcher,
        mc_version,
        java_rec["recommended_java"],
        launcher_config["launcher_download_url"],
    )

    # 保存脚本
    output_dir = config.REPORTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    bat_path = output_dir / f"install_{launcher}.bat"
    bat_path.write_text(install_bat, encoding="utf-8")
    logger.info(f"安装脚本已保存: {bat_path}")

    # 7. 生成HTML教程
    html_content = generate_setup_html(
        system_info, java_rec, java_match, launcher_config, install_bat
    )

    # 8. 输出结果
    result_data = {
        "system_info": system_info,
        "java_recommendation": java_rec,
        "java_match": java_match,
        "launcher_config": launcher_config,
        "install_script": str(bat_path),
    }

    output_files = generate_unified_output(
        feature="env_builder",
        status="success" if java_match["matched"] else "partial",
        input_summary={
            "launcher": launcher,
            "mc_version": mc_version,
            "loader": loader,
            "device": device,
        },
        result=result_data,
        title=f"环境搭建指南 - {launcher} + {mc_version}",
        html_content=html_content,
        warnings=warnings,
    )

    # 额外添加bat脚本路径
    if output_files.get("extra_files") is None:
        output_files["extra_files"] = {}
    output_files["extra_files"]["install_script"] = str(bat_path)

    return config.build_result(
        feature="env_builder",
        status="success" if java_match["matched"] else "partial",
        input_summary={
            "launcher": launcher,
            "mc_version": mc_version,
            "loader": loader,
        },
        result=result_data,
        warnings=warnings,
        output_files=output_files,
    )
