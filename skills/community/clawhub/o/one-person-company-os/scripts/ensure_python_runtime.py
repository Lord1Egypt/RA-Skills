#!/usr/bin/env python3
"""Inspect or switch to a compatible Python runtime for One Person Company OS scripts."""

from __future__ import annotations

import argparse
import platform
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

from common import (
    MIN_SUPPORTED_PYTHON,
    build_agent_action,
    choose_compatible_runtime,
    discover_python_runtimes,
    is_python_version_supported,
    print_block,
    print_step,
    python_compatibility_label,
    version_text,
)
from localization import normalize_language, pick_text

def shell_join(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def parse_os_release(path: Path = Path("/etc/os-release")) -> dict[str, str]:
    if not path.is_file():
        return {}

    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        result[key] = value.strip().strip('"')
    return result


def python_package_name(target_version: str, style: str) -> str:
    major, minor = target_version.split(".", 1)
    if style == "apt":
        return "python{}.{}".format(major, minor)
    if style == "dnf":
        return "python{}.{}".format(major, minor)
    if style == "choco":
        return "python{}{}".format(major, minor)
    return "python3"


def build_install_plan(
    *,
    target_version: str,
    system_name: Optional[str] = None,
    os_release: Optional[dict[str, str]] = None,
    available_commands: Optional[set[str]] = None,
    language: str = "zh-CN",
) -> dict[str, Any]:
    system_name = (system_name or platform.system()).lower()
    os_release = os_release or parse_os_release()
    available_commands = available_commands or set()
    distro = os_release.get("ID", "").lower()
    distro_like = os_release.get("ID_LIKE", "").lower()

    plan = {
        "supported": False,
        "platform": system_name,
        "installer": pick_text(language, "无", "None"),
        "title": pick_text(language, "未找到自动安装方案", "No automatic installation plan was found"),
        "commands": [],
        "notes": [pick_text(language, "当前环境未识别到可直接执行的 Python 安装方案。", "The current environment does not expose a directly executable Python installation plan.")],
    }

    if system_name == "darwin":
        if "brew" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": "macOS",
                    "installer": "Homebrew",
                    "title": pick_text(language, "通过 Homebrew 安装兼容 Python", "Install a compatible Python via Homebrew"),
                    "commands": [["brew", "install", "python@{}".format(target_version)]],
                    "notes": [pick_text(language, "安装完成后可用 `python{}` 重跑脚本。".format(target_version), "After installation, rerun the script with `python{}`.".format(target_version))],
                }
            )
        else:
            plan["notes"].append(pick_text(language, "缺少 Homebrew，需先安装 brew。", "Homebrew is missing, so install `brew` first."))
        return plan

    if system_name == "windows":
        winget_id = "Python.Python.{}".format(target_version)
        if "winget" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": "Windows",
                    "installer": "winget",
                    "title": pick_text(language, "通过 winget 安装兼容 Python", "Install a compatible Python via winget"),
                    "commands": [["winget", "install", "-e", "--id", winget_id]],
                    "notes": [pick_text(language, "安装完成后优先使用 `py -{}.{}` 或新安装的 python 可执行文件。".format(*target_version.split(".")), "After installation, prefer `py -{}.{}` or the newly installed python executable.".format(*target_version.split(".")))],
                }
            )
        elif "choco" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": "Windows",
                    "installer": "Chocolatey",
                    "title": pick_text(language, "通过 Chocolatey 安装兼容 Python", "Install a compatible Python via Chocolatey"),
                    "commands": [["choco", "install", python_package_name(target_version, "choco"), "-y"]],
                    "notes": [pick_text(language, "安装完成后重新打开终端，确保 PATH 生效。", "Reopen the terminal after installation so PATH updates take effect.")],
                }
            )
        else:
            plan["notes"].append(pick_text(language, "缺少 winget 或 Chocolatey，需由 OpenClaw 智能体接管。", "winget or Chocolatey is unavailable, so the OpenClaw agent should take over."))
        return plan

    if system_name == "linux":
        linux_id = "{} {}".format(distro, distro_like).strip()
        if ("ubuntu" in linux_id or "debian" in linux_id) and "apt-get" in available_commands:
            package = python_package_name(target_version, "apt")
            plan.update(
                {
                    "supported": True,
                    "platform": os_release.get("PRETTY_NAME", "Debian/Ubuntu"),
                    "installer": "apt-get",
                    "title": pick_text(language, "通过 apt-get 安装兼容 Python", "Install a compatible Python via apt-get"),
                    "commands": [
                        ["sudo", "apt-get", "update"],
                        ["sudo", "apt-get", "install", "-y", package, "{}-venv".format(package)],
                    ],
                    "notes": [pick_text(language, "如果源里缺少该版本，可由 OpenClaw 智能体切回手动落盘。", "If the package repository does not provide this version, the OpenClaw agent can fall back to manual persistence.")],
                }
            )
            return plan

        if ("fedora" in linux_id or "rhel" in linux_id or "centos" in linux_id) and ("dnf" in available_commands or "yum" in available_commands):
            package = python_package_name(target_version, "dnf")
            installer = "dnf" if "dnf" in available_commands else "yum"
            plan.update(
                {
                    "supported": True,
                    "platform": os_release.get("PRETTY_NAME", "Fedora/RHEL"),
                    "installer": installer,
                    "title": pick_text(language, "通过 {} 安装兼容 Python".format(installer), "Install a compatible Python via {}".format(installer)),
                    "commands": [["sudo", installer, "install", "-y", package]],
                    "notes": [pick_text(language, "安装完成后让 OpenClaw 智能体重新探测解释器。", "After installation, ask the OpenClaw agent to rediscover interpreters.")],
                }
            )
            return plan

        if ("alpine" in linux_id) and "apk" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": os_release.get("PRETTY_NAME", "Alpine"),
                    "installer": "apk",
                    "title": pick_text(language, "通过 apk 安装兼容 Python", "Install a compatible Python via apk"),
                    "commands": [["sudo", "apk", "add", "python3", "py3-pip"]],
                    "notes": [pick_text(language, "Alpine 会安装系统默认 Python 3。", "Alpine installs the system-default Python 3.")],
                }
            )
            return plan

        if "pacman" in available_commands:
            plan.update(
                {
                    "supported": True,
                    "platform": os_release.get("PRETTY_NAME", "Arch Linux"),
                    "installer": "pacman",
                    "title": pick_text(language, "通过 pacman 安装兼容 Python", "Install a compatible Python via pacman"),
                    "commands": [["sudo", "pacman", "-Sy", "--noconfirm", "python"]],
                    "notes": [pick_text(language, "Arch 默认提供当前 Python 3。", "Arch provides the current Python 3 by default.")],
                }
            )
            return plan

        plan["platform"] = os_release.get("PRETTY_NAME", "Linux")
        plan["notes"].append(pick_text(language, "缺少已支持的包管理器，需由 OpenClaw 智能体接管。", "No supported package manager was found, so the OpenClaw agent should take over."))
        return plan

    return plan


def available_command_names() -> set[str]:
    names = set()
    for command in ["brew", "apt-get", "dnf", "yum", "apk", "pacman", "winget", "choco"]:
        if shutil.which(command):
            names.add(command)
    return names


def run_script_with_runtime(runtime_path: str, script_path: str, script_args: list[str]) -> int:
    completed = subprocess.run([runtime_path, script_path, *script_args])
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect or switch to a compatible Python runtime for One Person Company OS.")
    parser.add_argument("--target-version", default="3.11", help="希望安装的 Python 次版本，例如 3.11")
    parser.add_argument("--apply", action="store_true", help="兼容开关：可直接重跑目标脚本，但不会自动安装系统依赖")
    parser.add_argument("--run-script", help="可选，指定一个目标脚本；如果有兼容解释器则直接用它运行")
    parser.add_argument("--language", default="auto", help="工作语言，如 zh-CN、en-US 或 auto")
    parser.add_argument("script_args", nargs=argparse.REMAINDER, help="传给目标脚本的参数，前面可加 --")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    language = normalize_language(args.language, args.run_script, *args.script_args)

    print_step(1, 5, pick_text(language, "检测当前 Python", "Check Current Python"), language=language)
    current_version = tuple(sys.version_info[:3])
    current_supported = is_python_version_supported(current_version)
    runtimes = discover_python_runtimes()
    compatible_runtime = choose_compatible_runtime(runtimes)

    print_step(2, 5, pick_text(language, "生成安装方案", "Build Install Plan"), language=language)
    install_plan = build_install_plan(
        target_version=args.target_version,
        available_commands=available_command_names(),
        language=language,
    )

    print_step(3, 5, pick_text(language, "判定恢复路径", "Decide Recovery Path"), language=language)
    if current_supported:
        resolution = pick_text(language, "当前 Python 已兼容，可直接继续", "The current Python runtime is already compatible")
        chosen_runtime = sys.executable
    elif compatible_runtime:
        resolution = pick_text(language, "发现可切换的兼容解释器", "Found a compatible interpreter that can be switched to")
        chosen_runtime = compatible_runtime["executable"]
    elif install_plan["supported"]:
        resolution = pick_text(language, "需要先手动安装兼容 Python", "A compatible Python runtime must be installed manually first")
        chosen_runtime = pick_text(language, "手动安装完成后重新探测", "Re-detect after manual installation")
    else:
        resolution = pick_text(language, "当前环境没有可用的手动安装方案", "No manual install plan is available in this environment")
        chosen_runtime = pick_text(language, "无", "None")

    run_args = list(args.script_args)
    if run_args and run_args[0] == "--":
        run_args = run_args[1:]

    execution_status = pick_text(language, "执行中", "Running") if args.apply and args.run_script else pick_text(language, "已规划", "Planned")
    print_step(4, 5, pick_text(language, "执行恢复动作", "Execute Recovery Action"), status=execution_status, language=language)
    return_code = 0
    action_summary = pick_text(language, "未执行，仅输出计划", "No action executed; showing the plan only")
    if args.apply:
        if current_supported and args.run_script:
            return_code = run_script_with_runtime(sys.executable, args.run_script, run_args)
            action_summary = pick_text(language, "已用当前兼容 Python 运行目标脚本", "Ran the target script with the current compatible Python")
        elif compatible_runtime and args.run_script:
            return_code = run_script_with_runtime(compatible_runtime["executable"], args.run_script, run_args)
            action_summary = pick_text(language, "已用兼容 Python 运行目标脚本", "Ran the target script with the compatible Python interpreter")
        elif install_plan["supported"]:
            action_summary = pick_text(
                language,
                "已跳过自动安装。请先审阅下面的手动安装方案；marketplace 版不会自动执行系统级安装命令。",
                "Automatic installation was skipped. Review the manual install plan below first; the marketplace build will not execute system-level install commands.",
            )
        else:
            action_summary = pick_text(language, "当前环境没有可用的手动安装方案，请改用兼容解释器或手动落盘", "No manual install plan is available in this environment; switch to a compatible interpreter or persist manually")

    print_step(5, 5, "验证与回报", language=language)
    print_block(
        pick_text(language, "Python 兼容状态", "Python Compatibility Status"),
        [
            (pick_text(language, "当前解释器", "Current Interpreter"), "{} ({})".format(sys.executable, python_compatibility_label(current_version))),
            (pick_text(language, "兼容目标", "Compatibility Target"), "Python {}+".format(version_text(MIN_SUPPORTED_PYTHON))),
            (pick_text(language, "当前是否兼容", "Currently Compatible"), pick_text(language, "是", "Yes") if current_supported else pick_text(language, "否", "No")),
            (
                pick_text(language, "可切换解释器", "Switchable Interpreter"),
                pick_text(language, "无", "None")
                if not compatible_runtime
                else "{} ({})".format(
                    compatible_runtime["executable"],
                    python_compatibility_label(compatible_runtime["version"]),
                ),
            ),
            (pick_text(language, "恢复结论", "Recovery Conclusion"), resolution),
            (pick_text(language, "恢复动作", "Recovery Action"), build_agent_action(current_supported=current_supported, compatible_runtime=compatible_runtime, writable=True, language=language)),
        ],
    )
    print_block(
        pick_text(language, "安装方案", "Install Plan"),
        [
            (pick_text(language, "平台", "Platform"), install_plan["platform"]),
            (pick_text(language, "安装器", "Installer"), install_plan["installer"]),
            (pick_text(language, "是否提供手动安装方案", "Has Manual Install Plan"), pick_text(language, "是", "Yes") if install_plan["supported"] else pick_text(language, "否", "No")),
            (pick_text(language, "推荐标题", "Recommended Title"), install_plan["title"]),
            (pick_text(language, "建议命令（需手动审阅后执行）", "Suggested Commands (review manually before running)"), ("；" if language == "zh-CN" else "; ").join(shell_join(command) for command in install_plan["commands"]) if install_plan["commands"] else pick_text(language, "无", "None")),
            (pick_text(language, "备注", "Notes"), ("；" if language == "zh-CN" else "; ").join(install_plan["notes"]) if install_plan["notes"] else pick_text(language, "无", "None")),
        ],
    )
    print_block(
        pick_text(language, "执行结果", "Execution Result"),
        [
            (pick_text(language, "目标脚本", "Target Script"), args.run_script or pick_text(language, "无", "None")),
            (pick_text(language, "选用解释器", "Chosen Interpreter"), chosen_runtime),
            ("apply", pick_text(language, "是", "Yes") if args.apply else pick_text(language, "否", "No")),
            (pick_text(language, "结果", "Result"), action_summary),
            (pick_text(language, "退出码", "Exit Code"), str(return_code)),
        ],
    )
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
