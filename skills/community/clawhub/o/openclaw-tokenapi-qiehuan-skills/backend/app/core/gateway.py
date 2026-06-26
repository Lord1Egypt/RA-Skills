import os
import subprocess
import time
import sys
from typing import Tuple


class GatewayController:
    """OpenClaw Gateway 服务控制器"""

    @staticmethod
    def _execute_command(command: str) -> Tuple[bool, str]:
        """执行命令并返回结果"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "命令执行超时"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _log(msg: str):
        """输出日志到终端"""
        print(f"[GatewayController] {msg}", flush=True)
        sys.stdout.flush()

    @staticmethod
    def stop_gateway() -> Tuple[bool, str]:
        """停止 OpenClaw Gateway"""
        GatewayController._log("Stopping Gateway...")
        success, output = GatewayController._execute_command("taskkill /F /IM openclaw.exe 2>nul")
        if success or "not found" in output.lower():
            GatewayController._log("Gateway stopped")
            return True, "Gateway stopped"
        return success, output

    @staticmethod
    def start_gateway() -> Tuple[bool, str]:
        """启动 OpenClaw Gateway"""
        GatewayController._log("Starting Gateway...")
        # 使用用户主目录，跨平台兼容
        openclaw_home = os.path.join(os.path.expanduser("~"), ".openclaw")
        gateway_cmd = os.path.join(openclaw_home, "gateway.cmd")

        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            subprocess.Popen(
                f'"{gateway_cmd}"',
                shell=True,
                startupinfo=startupinfo,
                cwd=openclaw_home
            )
            GatewayController._log("Gateway started")
            return True, "Gateway 服务已启动"
        except Exception as e:
            GatewayController._log(f"Failed to start Gateway: {e}")
            return False, str(e)

    @staticmethod
    def restart_gateway() -> Tuple[bool, str]:
        """重启 OpenClaw Gateway"""
        GatewayController._log("=== Restarting Gateway ===")
        GatewayController.stop_gateway()
        time.sleep(1)
        return GatewayController.start_gateway()

    @staticmethod
    def restart_with_command() -> Tuple[bool, str]:
        """使用指定命令重启 Gateway: 调用脚本打开新 PowerShell 窗口"""
        GatewayController._log("=== Restarting Gateway with new PowerShell ===")

        # 使用项目根目录的相对路径
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        script_path = os.path.join(project_root, "tools", "restart_gateway.bat")

        try:
            subprocess.Popen([script_path], shell=True)
            GatewayController._log(f"Restart script executed: {script_path}")
            return True, "已打开 PowerShell 窗口执行重启命令"
        except Exception as e:
            GatewayController._log(f"Failed to execute restart script: {e}")
            return False, str(e)

    @staticmethod
    def control_gateway(action: str) -> Tuple[bool, str]:
        """控制 Gateway 服务"""
        GatewayController._log(f"Control action: {action}")
        action_map = {
            'stop': GatewayController.stop_gateway,
            'start': GatewayController.start_gateway,
            'restart': GatewayController.restart_gateway
        }
        handler = action_map.get(action.lower())
        if not handler:
            return False, f"未知的操作: {action}"
        return handler()
