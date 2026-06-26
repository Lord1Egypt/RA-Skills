#!/usr/bin/env python3
"""
远程桌面自动化工作流
整合连接、截图、视觉识别和自动化控制
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from typing import Optional, Callable, Dict, Any, List

# 导入本地模块
from remote_desktop_control import UURemoteController
from remote_automation import WindowsAutomator
from vision_recognition import VisionRecognizer


class RemoteDesktopWorkflow:
    """远程桌面自动化工作流"""
    
    def __init__(
        self,
        session_id: Optional[str] = None,
        host: Optional[str] = None,
        port: int = 18792,
        screenshot_dir: str = "./remote_screenshots",
        templates_dir: str = "./templates",
        api_key: Optional[str] = None
    ):
        self.controller = UURemoteController(
            session_id=session_id,
            host=host,
            port=port,
            screenshot_dir=screenshot_dir
        )
        self.automator = WindowsAutomator(
            uu_exec_func=self.controller.exec_command
        )
        self.recognizer = VisionRecognizer(api_key=api_key)
        self.screenshot_dir = Path(screenshot_dir)
        self.templates_dir = Path(templates_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_screenshot: Optional[str] = None
    
    def connect(self) -> bool:
        """连接远程"""
        print("正在连接远程桌面...")
        if self.controller.connect():
            print("连接成功!")
            return True
        print("连接失败!")
        return False
    
    def disconnect(self):
        """断开连接"""
        self.controller.disconnect()
        print("已断开连接")
    
    def capture_screen(self) -> Optional[str]:
        """捕获屏幕"""
        # 使用 Windows Automator 截图
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screen_{timestamp}.png"
        save_path = self.screenshot_dir / filename
        
        # 通过 PowerShell 截图
        ps_script = f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen | Select-Object -ExpandProperty Bounds | ForEach-Object {{ Add-Type -AssemblyName System.Drawing; $bmp = New-Object System.Drawing.Bitmap($_.Width, $_.Height); $g = [System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($_.X, $_.Y, 0, 0, $_.Size); $bmp.Save('{save_path}'); $g.Dispose(); $bmp.Dispose() }}"
        
        success, _ = self.controller.exec_command(f'powershell -Command "{ps_script}"')
        
        if success and save_path.exists():
            self.current_screenshot = str(save_path)
            return str(save_path)
        
        # 备用：使用 uu screenshot
        return self.controller.screenshot(filename)
    
    def analyze_task(self, task: str) -> Dict[str, Any]:
        """
        分析任务
        
        Args:
            task: 任务描述，如 "点击下载按钮安装软件"
            
        Returns:
            分析结果
        """
        if not self.current_screenshot:
            self.capture_screen()
        
        if not self.current_screenshot:
            return {"error": "无法获取屏幕截图"}
        
        return self.recognizer.analyze_screen(self.current_screenshot, task)
    
    def find_and_execute(
        self, 
        target: str,
        action: str = "click",
        max_retries: int = 3
    ) -> bool:
        """
        查找目标并执行动作
        
        Args:
            target: 目标描述
            action: 动作 (click, double_click, right_click)
            max_retries: 最大重试次数
        """
        for attempt in range(max_retries):
            # 刷新截图
            self.capture_screen()
            
            # 查找目标位置
            pos = self.recognizer.find_click_target(
                self.current_screenshot,
                target,
                self.recognizer.api_key
            )
            
            if pos:
                print(f"找到目标 '{target}': ({pos[0]}, {pos[1]})")
                
                # 执行动作
                if action == "click":
                    return self.automator.mouse_click(pos[0], pos[1])
                elif action == "double_click":
                    return self.automator.mouse_double_click(pos[0], pos[1])
                elif action == "right_click":
                    return self.automator.mouse_right_click(pos[0], pos[1])
            
            print(f"未找到目标 '{target}'，重试 ({attempt + 1}/{max_retries})...")
            time.sleep(2)
        
        return False
    
    def type_text(self, text: str) -> bool:
        """输入文本"""
        return self.automator.typewrite(text)
    
    def press_key(self, key: str) -> bool:
        """按键"""
        return self.automator.press_key(key)
    
    def hotkey(self, *keys) -> bool:
        """组合键"""
        return self.automator.hotkey(*keys)
    
    def click_at(self, x: int, y: int) -> bool:
        """点击指定坐标"""
        return self.automator.mouse_click(x, y)
    
    def wait_for_change(self, timeout: int = 30, interval: int = 2) -> bool:
        """等待屏幕内容变化"""
        if not self.current_screenshot:
            self.capture_screen()
        
        import hashlib
        
        # 计算当前截图哈希
        with open(self.current_screenshot, "rb") as f:
            current_hash = hashlib.md5(f.read()).hexdigest()
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            time.sleep(interval)
            self.capture_screen()
            
            with open(self.current_screenshot, "rb") as f:
                new_hash = hashlib.md5(f.read()).hexdigest()
            
            if new_hash != current_hash:
                return True
        
        return False
    
    def describe_screen(self) -> str:
        """描述当前屏幕"""
        if not self.current_screenshot:
            self.capture_screen()
        
        return self.recognizer.describe_ui(self.current_screenshot)
    
    def run_workflow(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        执行工作流
        
        Steps 格式:
        [
            {"action": "capture"},           # 截图
            {"action": "analyze", "task": "..."},  # 分析
            {"action": "find", "target": "...", "execute": "click"},  # 查找并点击
            {"action": "type", "text": "..."},      # 输入文本
            {"action": "press", "key": "..."},       # 按键
            {"action": "wait"},               # 等待变化
            {"action": "describe"}             # 描述屏幕
        ]
        """
        results = []
        
        for i, step in enumerate(steps):
            print(f"\n[Step {i+1}/{len(steps)}] {step.get('action', 'unknown')}")
            
            action = step.get("action")
            
            try:
                if action == "capture":
                    path = self.capture_screen()
                    results.append({"step": i, "action": "capture", "result": path})
                    
                elif action == "analyze":
                    task = step.get("task", "")
                    result = self.analyze_task(task)
                    results.append({"step": i, "action": "analyze", "result": result})
                    
                elif action == "find":
                    target = step.get("target", "")
                    execute_action = step.get("execute", "click")
                    success = self.find_and_execute(target, execute_action)
                    results.append({"step": i, "action": "find", "target": target, "success": success})
                    
                elif action == "type":
                    text = step.get("text", "")
                    success = self.type_text(text)
                    results.append({"step": i, "action": "type", "text": text, "success": success})
                    
                elif action == "press":
                    key = step.get("key", "")
                    success = self.press_key(key)
                    results.append({"step": i, "action": "press", "key": key, "success": success})
                    
                elif action == "hotkey":
                    keys = step.get("keys", [])
                    success = self.hotkey(*keys)
                    results.append({"step": i, "action": "hotkey", "keys": keys, "success": success})
                    
                elif action == "click":
                    x = step.get("x")
                    y = step.get("y")
                    success = self.click_at(x, y)
                    results.append({"step": i, "action": "click", "x": x, "y": y, "success": success})
                    
                elif action == "wait":
                    timeout = step.get("timeout", 30)
                    changed = self.wait_for_change(timeout)
                    results.append({"step": i, "action": "wait", "changed": changed})
                    
                elif action == "describe":
                    description = self.describe_screen()
                    results.append({"step": i, "action": "describe", "result": description})
                    
                else:
                    results.append({"step": i, "action": action, "error": "Unknown action"})
                    
            except Exception as e:
                results.append({"step": i, "action": action, "error": str(e)})
        
        return {"success": True, "steps": results}
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False


# ========== 预设工作流模板 ==========

class WorkflowTemplates:
    """预设工作流模板"""
    
    @staticmethod
    def software_install(software_name: str, installer_path: str = None) -> List[Dict]:
        """软件安装工作流"""
        return [
            {"action": "capture"},
            {"action": "describe"},
            {"action": "find", "target": "安装向导", "execute": "click"},
            {"action": "wait", "timeout": 10},
            {"action": "find", "target": "下一步", "execute": "click"},
            {"action": "wait", "timeout": 5},
            {"action": "find", "target": "我接受", "execute": "click"},
            {"action": "find", "target": "下一步", "execute": "click"},
            {"action": "wait", "timeout": 30},
            {"action": "find", "target": "安装", "execute": "click"},
            {"action": "wait", "timeout": 60},
            {"action": "find", "target": "完成", "execute": "click"},
        ]
    
    @staticmethod
    def browse_and_click(url: str, target: str) -> List[Dict]:
        """浏览并点击工作流"""
        return [
            {"action": "press", "key": "win"},
            {"action": "wait", "timeout": 2},
            {"action": "type", "text": "edge"},
            {"action": "wait", "timeout": 1},
            {"action": "press", "key": "enter"},
            {"action": "wait", "timeout": 5},
            {"action": "hotkey", "keys": ["ctrl", "l"]},
            {"action": "type", "text": url},
            {"action": "press", "key": "enter"},
            {"action": "wait", "timeout": 10},
            {"action": "find", "target": target, "execute": "click"},
        ]
    
    @staticmethod
    def file_operation(operation: str, file_path: str) -> List[Dict]:
        """文件操作工作流"""
        base = [
            {"action": "press", "key": "win"},
            {"action": "wait", "timeout": 1},
        ]
        
        if operation == "open":
            return base + [
                {"action": "type", "text": file_path},
                {"action": "press", "key": "enter"},
            ]
        elif operation == "delete":
            return base + [
                {"action": "type", "text": file_path},
                {"action": "press", "key": "enter"},
                {"action": "press", "key": "delete"},
                {"action": "find", "target": "是", "execute": "click"},
            ]
        
        return base


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="远程桌面自动化工作流")
    parser.add_argument("--session-id", help="UU Session ID")
    parser.add_argument("--host", help="远程主机")
    parser.add_argument("--port", type=int, default=18792)
    parser.add_argument("--workflow", "-w", help="工作流 JSON 文件")
    parser.add_argument("--task", "-t", help="自然语言任务")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    if args.workflow:
        # 从文件加载工作流
        with open(args.workflow) as f:
            workflow_data = json.load(f)
        
        with RemoteDesktopWorkflow(session_id=args.session_id, host=args.host) as wf:
            result = wf.run_workflow(workflow_data.get("steps", []))
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.task:
        # 自然语言任务模式
        print("自然语言任务模式开发中...")
        print(f"任务: {args.task}")
    
    elif args.interactive:
        # 交互模式
        print("=" * 60)
        print("远程桌面自动化 - 交互模式")
        print("=" * 60)
        
        session_id = input("Session ID (留空则输入host): ").strip()
        host = None
        
        if not session_id:
            host = input("主机地址: ").strip()
        
        with RemoteDesktopWorkflow(
            session_id=session_id or None,
            host=host
        ) as wf:
            print("\n连接成功! 输入命令操作:")
            print("  capture - 截图")
            print("  describe - 描述屏幕")
            print("  find <目标> - 查找并点击")
            print("  type <文本> - 输入文本")
            print("  press <按键> - 按键")
            print("  screenshot <路径> - 保存截图")
            print("  quit - 退出")
            
            while True:
                cmd = input("\n> ").strip()
                
                if not cmd:
                    continue
                
                if cmd == "quit":
                    break
                
                if cmd == "capture":
                    path = wf.capture_screen()
                    print(f"截图: {path}")
                elif cmd == "describe":
                    print(wf.describe_screen())
                elif cmd.startswith("find "):
                    target = cmd[5:]
                    wf.find_and_execute(target)
                elif cmd.startswith("type "):
                    text = cmd[5:]
                    wf.type_text(text)
                elif cmd.startswith("press "):
                    key = cmd[6:]
                    wf.press_key(key)
                elif cmd.startswith("screenshot "):
                    path = cmd[11:].strip()
                    if path:
                        # 需要实现自定义路径
                        print(f"保存截图到: {path}")
                else:
                    print("未知命令")
    
    else:
        parser.print_help()
