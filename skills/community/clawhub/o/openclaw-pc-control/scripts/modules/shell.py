"""
Shell 命令执行模块 - 提供 PowerShell、CMD 命令执行功能
支持直接执行命令和执行脚本文件
"""
import subprocess
import shlex
import os

from modules.security import check_shell_command, check_file_path, log_operation


def shell_run(command: str, shell: str = "powershell", timeout: int = 30):
    """
    执行 PowerShell 或 CMD 命令

    Args:
        command: 要执行的命令
        shell: 使用的 shell 类型 ("powershell" 或 "cmd")
        timeout: 超时时间(秒)

    Returns:
        执行结果字典
    """
    allowed, reason = check_shell_command(command, shell)
    if not allowed:
        return {"success": False, "data": None, "error": f"命令被安全策略拦截: {reason}"}

    try:
        if shell == "cmd":
            cmd = ["cmd", "/c", command]
        elif shell == "powershell":
            cmd = ["powershell", "-NoProfile", "-Command", command]
        elif shell == "pwsh":
            cmd = ["pwsh", "-NoProfile", "-Command", command]
        else:
            return {"success": False, "data": None, "error": f"不支持的shell类型: {shell}"}

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd()
        )

        return {
            "success": True,
            "data": {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            },
            "error": None
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "data": None, "error": f"命令执行超时({timeout}秒)"}
    except FileNotFoundError:
        return {"success": False, "data": None, "error": f"未找到 {shell} 可执行文件"}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def shell_run_file(script_path: str, shell: str = "powershell", timeout: int = 60):
    """
    执行 PowerShell 或 CMD 脚本文件

    Args:
        script_path: 脚本文件路径
        shell: 使用的 shell 类型 ("powershell" 或 "cmd")
        timeout: 超时时间(秒)

    Returns:
        执行结果字典
    """
    allowed_path, path_reason = check_file_path(script_path, "execute")
    if not allowed_path:
        return {"success": False, "data": None, "error": f"脚本执行被安全策略拦截: {path_reason}"}

    allowed_cmd, cmd_reason = check_shell_command(script_path, shell)
    if not allowed_cmd:
        return {"success": False, "data": None, "error": f"脚本执行被安全策略拦截: {cmd_reason}"}

    if not os.path.exists(script_path):
        return {"success": False, "data": None, "error": f"脚本文件不存在: {script_path}"}

    try:
        if shell == "cmd":
            cmd = ["cmd", "/c", script_path]
        elif shell == "powershell":
            cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path]
        elif shell == "pwsh":
            cmd = ["pwsh", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path]
        else:
            return {"success": False, "data": None, "error": f"不支持的shell类型: {shell}"}

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(script_path) or os.getcwd()
        )

        return {
            "success": True,
            "data": {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            },
            "error": None
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "data": None, "error": f"脚本执行超时({timeout}秒)"}
    except FileNotFoundError:
        return {"success": False, "data": None, "error": f"未找到 {shell} 可执行文件"}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def get_shell_info():
    """
    获取当前系统可用的 Shell 信息

    Returns:
        Shell 信息字典
    """
    shells = []

    powershell_path = subprocess.run(
        ["where", "powershell"],
        capture_output=True,
        text=True
    )
    if powershell_path.returncode == 0:
        shells.append({"type": "powershell", "path": powershell_path.stdout.strip().split('\n')[0]})

    pwsh_path = subprocess.run(
        ["where", "pwsh"],
        capture_output=True,
        text=True
    )
    if pwsh_path.returncode == 0:
        shells.append({"type": "pwsh", "path": pwsh_path.stdout.strip().split('\n')[0]})

    return {
        "success": True,
        "data": {
            "available_shells": shells,
            "default": "powershell" if shells else None
        },
        "error": None
    }
