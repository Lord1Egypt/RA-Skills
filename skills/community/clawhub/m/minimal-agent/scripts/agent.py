#!/usr/bin/env python3
# ═══════════════════════════════════════════
# Minimal Agent — 极简 AI 操作系统控制代理（Python Skill 版）
# ═══════════════════════════════════════════
#
# 职责：接收指令 → 选择 system-controller 脚本 → 执行 → 返回结果
# LLM 和对话管理由 WorkBuddy 提供，本脚本只做"手脚"工作。
#
# **支持智能模式选择**：
# - function (V2) 模式：限制在55个预定义工具内，只能调用system-controller脚本
# - text (V1) 模式：无限制，可执行任何系统命令（包括文件修改、脚本执行等）
# - auto 模式：自动检测system-controller可用性，有则用V2，无则用V1
# - force_text/force_function 模式：强制指定模式
#
# **模式优先级**：
# 1. 命令行参数（--text, --function, --auto）
# 2. 配置文件 mode 字段
# 3. 自动检测（auto模式）
#
# 用法（WorkBuddy 自动调用，也可独立运行）：
#   python agent.py "帮我打开记事本"
#   python agent.py --interactive
#   python agent.py --text --interactive       # 强制V1模式
#   python agent.py --function "列出窗口"       # 强制V2模式
#   python agent.py --auto --interactive       # 自动检测模式

import subprocess
import sys
import os
import json
import shutil
import io
import tomllib
from pathlib import Path
from typing import Literal

# 修复 Windows 控制台 UTF-8 编码
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ═══════════════════════════════════════════
# 类型定义
# ═══════════════════════════════════════════

ModeType = Literal["function", "text", "auto", "mixed", "force_text", "force_function"]

# ═══════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════

class Config:
    """配置类"""
    
    def __init__(self):
        self.skill_path = ""
        self.python_path = ""
        self.mode: ModeType = "auto"
        self.timeout_seconds = 30
        self._load_config()
    
    def _load_config(self):
        """从配置文件加载配置"""
        config_file = Path(__file__).parent / "config.toml"
        
        if not config_file.exists():
            # 使用默认配置
            self._set_defaults()
            return
        
        try:
            with open(config_file, "rb") as f:
                config_data = tomllib.load(f)
            
            # system_controller 配置
            sys_ctrl = config_data.get("system_controller", {})
            self.skill_path = sys_ctrl.get("skill_path", "~/.workbuddy/skills/system-controller")
            self.python_path = sys_ctrl.get("python_path", "python")
            
            # execution 配置
            exec_config = config_data.get("execution", {})
            self.mode = exec_config.get("mode", "auto")
            self.timeout_seconds = exec_config.get("timeout_seconds", 30)
            
            # 扩展 ~ 为绝对路径
            if self.skill_path.startswith("~"):
                self.skill_path = str(Path.home() / self.skill_path[2:])
                
        except Exception as e:
            print(f"⚠️ 配置文件加载失败: {e}，使用默认配置")
            self._set_defaults()
    
    def _set_defaults(self):
        """设置默认配置"""
        self.skill_path = str(Path.home() / ".workbuddy" / "skills" / "system-controller")
        self.python_path = "python"
        self.mode = "auto"
        self.timeout_seconds = 30

CONFIG = Config()

# ═══════════════════════════════════════════
# 路径配置
# ═══════════════════════════════════════════

HOME = Path.home()
SKILL_BASE = HOME / ".workbuddy" / "skills"
SYSTEM_CONTROLLER = Path(CONFIG.skill_path) / "scripts"

# Python 运行时路径（根据配置）
PYTHON = CONFIG.python_path
PYTHON_VENV = r"C:\Users\wave\.workbuddy\binaries\python\envs\default\Scripts\python.exe"  # 备用venv路径


# ═══════════════════════════════════════════
# System-controller 检测与模式选择
# ═══════════════════════════════════════════

def is_system_controller_available() -> bool:
    """
    检测 system-controller 是否可用
    1. 检查 skill 目录是否存在
    2. 检查主要脚本是否存在
    3. 检查 Python 环境是否可用
    """
    try:
        # 1. 检查 skill 目录
        skill_dir = Path(CONFIG.skill_path)
        if not skill_dir.exists() or not skill_dir.is_dir():
            print(f"⚠️ system-controller 目录不存在: {CONFIG.skill_path}")
            return False
        
        # 2. 检查 scripts 子目录
        scripts_dir = skill_dir / "scripts"
        if not scripts_dir.exists() or not scripts_dir.is_dir():
            print(f"⚠️ system-controller 脚本目录不存在: {scripts_dir}")
            return False
        
        # 3. 检查主要脚本文件
        required_scripts = ["window_manager.py", "process_manager.py", "hardware_controller.py"]
        for script in required_scripts:
            script_file = scripts_dir / script
            if not script_file.exists():
                print(f"⚠️ system-controller 缺少必要脚本: {script}")
                return False
        
        # 4. 测试 Python 环境
        try:
            result = subprocess.run(
                [CONFIG.python_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                print(f"⚠️ Python 环境不可用: {CONFIG.python_path}")
                return False
        except Exception as e:
            print(f"⚠️ Python 环境测试失败: {e}")
            return False
        
        print(f"✅ system-controller 可用: {CONFIG.skill_path}")
        return True
        
    except Exception as e:
        print(f"⚠️ system-controller 检测异常: {e}")
        return False


def analyze_task_type(task: str) -> str:
    """
    智能分析任务类型，决定使用V1还是V2模式
    
    规则：
    1. 如果任务可以通过预定义工具完成 → V2模式
    2. 如果任务需要文件操作、脚本执行等 → V1模式
    3. 复杂任务可以拆分为多个步骤，每个步骤单独选择模式
    """
    v2_keywords = [
        "窗口", "进程", "音量", "亮度", "电源", "网络", "鼠标", "键盘", "截图", "OCR", 
        "串口", "IoT", "homeassistant", "亮度", "屏幕", "显示器", "激活", "最小化", "最大化",
        "关闭窗口", "打开应用", "结束进程", "启动进程", "调整大小", "发送按键",
        "鼠标移动", "鼠标点击", "键盘输入", "截屏", "文字识别", "找图", "颜色",
        "串口发送", "串口接收", "智能家居", "HTTP请求"
    ]
    
    v1_keywords = [
        "文件", "编辑", "创建", "删除", "移动", "复制", "重命名", "脚本", "执行", "运行",
        "网络", "数据库", "查询", "导入", "导出", "系统", "配置", "注册表", "服务",
        "安装", "卸载", "更新", "安全", "防火墙", "权限", "编译", "构建", "测试",
        "CSV", "JSON", "XML", "处理", "转换", "打包", "部署", "备份", "恢复"
    ]
    
    task_lower = task.lower()
    v2_count = sum(1 for keyword in v2_keywords if keyword.lower() in task_lower)
    v1_count = sum(1 for keyword in v1_keywords if keyword.lower() in task_lower)
    
    if v2_count > v1_count and v2_count > 0:
        return "V2"
    elif v1_count > v2_count and v1_count > 0:
        return "V1"
    else:
        return "MIXED"  # 两者都有或无法判断


def determine_actual_mode(force_mode: ModeType | None = None) -> Literal["function", "text", "mixed"]:
    """
    智能选择运行模式
    根据配置和 system-controller 可用性自动选择最佳模式
    
    参数:
        force_mode: 强制模式（来自命令行参数）
    """
    # 优先级：命令行参数 > 配置文件 > 自动检测
    mode_to_use: ModeType = force_mode or CONFIG.mode
    
    if mode_to_use in ("function", "force_function"):
        print("📊 使用 function 模式 (V2)")
        return "function"
    
    if mode_to_use in ("text", "force_text"):
        print("📊 使用 text 模式 (V1)")
        return "text"
    
    if mode_to_use == "mixed":
        print("📊 使用 mixed 模式 (智能混合)")
        return "mixed"
    
    if mode_to_use == "auto":
        if is_system_controller_available():
            print("📊 自动选择：system-controller 可用 → 使用 function 模式 (V2)")
            return "function"
        else:
            print("📊 自动选择：system-controller 不可用 → 使用 text 模式 (V1)")
            return "text"
    
    # 默认情况
    print("📊 默认使用 function 模式 (V2)")
    return "function"


def get_python(script_name: str) -> str:
    """根据脚本选择合适的 Python 解释器"""
    # GUI 相关脚本需要 venv（含 pyautogui/pillow）
    gui_scripts = {"gui_controller.py"}
    if script_name in gui_scripts and os.path.exists(PYTHON_VENV):
        return PYTHON_VENV
    return PYTHON


def get_script_path(script_name: str) -> str:
    """获取 system-controller 脚本的完整路径"""
    path = SYSTEM_CONTROLLER / script_name
    if not path.exists():
        raise FileNotFoundError(f"脚本不存在: {path}，请确认 system-controller Skill 已安装")
    return str(path)


# ═══════════════════════════════════════════
# 命令执行
# ═══════════════════════════════════════════

class ExecutionResult:
    """脚本执行结果"""

    def __init__(self, success: bool, output: str, command: str):
        self.success = success
        self.output = output.strip()
        self.command = command

    def __repr__(self):
        status = "✅" if self.success else "❌"
        return f"{status} {self.output}"


def run_script(script_name: str, args: list[str], timeout: int = 30) -> ExecutionResult:
    """
    执行 system-controller 脚本

    参数:
        script_name: 脚本文件名，如 "window_manager.py"
        args: 命令行参数列表，如 ["list"]
        timeout: 超时秒数
    """
    python = get_python(script_name)
    script_path = get_script_path(script_name)
    cmd = [python, script_path] + args
    command_str = " ".join(cmd)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        output = result.stdout or result.stderr or "(无输出)"
        success = result.returncode == 0
        return ExecutionResult(success, output, command_str)

    except subprocess.TimeoutExpired:
        return ExecutionResult(False, f"⏰ 执行超时 ({timeout}s): {command_str}", command_str)

    except FileNotFoundError as e:
        return ExecutionResult(False, f"🔍 {e}", command_str)

    except Exception as e:
        return ExecutionResult(False, f"💥 执行异常: {e}", command_str)


# ═══════════════════════════════════════════
# 工具映射表（原子操作 → 脚本命令）
# ═══════════════════════════════════════════

# 每个工具定义：(脚本名, 默认参数模板)
# LLM/用户通过工具名调用，Agent 映射到实际脚本
TOOL_DEFS: dict[str, tuple[str, ...]] = {
    # ---- 窗口管理 (window_manager.py) ----
    "window_list":      ("window_manager.py", "list"),
    "window_activate":  ("window_manager.py", "activate"),
    "window_close":     ("window_manager.py", "close"),
    "window_minimize":  ("window_manager.py", "minimize"),
    "window_maximize":  ("window_manager.py", "maximize"),
    "window_resize":    ("window_manager.py", "resize"),
    "window_send_keys": ("window_manager.py", "send-keys"),

    # ---- 进程管理 (process_manager.py) ----
    "process_list":     ("process_manager.py", "list"),
    "process_kill":     ("process_manager.py", "kill"),
    "process_start":    ("process_manager.py", "start"),
    "process_info":     ("process_manager.py", "info"),
    "process_system":   ("process_manager.py", "system"),

    # ---- 硬件控制 (hardware_controller.py) ----
    "volume_get":       ("hardware_controller.py", "volume", "get"),
    "volume_set":       ("hardware_controller.py", "volume", "set"),
    "volume_mute":      ("hardware_controller.py", "volume", "mute"),
    "brightness_set":   ("hardware_controller.py", "screen", "brightness"),
    "screen_info":      ("hardware_controller.py", "screen", "info"),
    "power_lock":       ("hardware_controller.py", "power", "lock"),
    "power_sleep":      ("hardware_controller.py", "power", "sleep"),
    "power_hibernate":  ("hardware_controller.py", "power", "hibernate"),
    "power_shutdown":   ("hardware_controller.py", "power", "shutdown"),
    "power_restart":    ("hardware_controller.py", "power", "restart"),
    "power_cancel":     ("hardware_controller.py", "power", "cancel"),
    "network_list":     ("hardware_controller.py", "network", "adapters"),
    "network_enable":   ("hardware_controller.py", "network", "enable"),
    "network_disable":  ("hardware_controller.py", "network", "disable"),
    "wifi_info":        ("hardware_controller.py", "network", "wifi"),
    "usb_list":         ("hardware_controller.py", "usb", "list"),

    # ---- GUI 控制 (gui_controller.py) ----
    "mouse_move":           ("gui_controller.py", "mouse", "move"),
    "mouse_click":         ("gui_controller.py", "mouse", "click"),
    "mouse_right_click":    ("gui_controller.py", "mouse", "right-click"),
    "mouse_double_click":   ("gui_controller.py", "mouse", "double-click"),
    "mouse_drag":          ("gui_controller.py", "mouse", "drag"),
    "mouse_scroll":        ("gui_controller.py", "mouse", "scroll"),
    "mouse_position":      ("gui_controller.py", "mouse", "position"),
    "keyboard_type":       ("gui_controller.py", "keyboard", "type"),
    "keyboard_press":      ("gui_controller.py", "keyboard", "press"),
    "screenshot":          ("gui_controller.py", "screenshot"),
    "visual_ocr":          ("gui_controller.py", "visual", "ocr"),
    "visual_find":         ("gui_controller.py", "visual", "find"),
    "visual_click_image":  ("gui_controller.py", "visual", "click-image"),
    "visual_pixel":        ("gui_controller.py", "visual", "pixel"),

    # ---- 串口通信 (serial_comm.py) ----
    "serial_list":     ("serial_comm.py", "list"),
    "serial_send":     ("serial_comm.py", "send"),
    "serial_receive":  ("serial_comm.py", "receive"),
    "serial_chat":     ("serial_comm.py", "chat"),
    "serial_monitor":  ("serial_comm.py", "monitor"),

    # ---- IoT 控制 (iot_controller.py) ----
    "ha_list":         ("iot_controller.py", "homeassistant", "list"),
    "ha_state":        ("iot_controller.py", "homeassistant", "state"),
    "ha_on":           ("iot_controller.py", "homeassistant", "on"),
    "ha_off":          ("iot_controller.py", "homeassistant", "off"),
    "ha_toggle":       ("iot_controller.py", "homeassistant", "toggle"),
    "http_get":        ("iot_controller.py", "http", "get"),
    "http_post":       ("iot_controller.py", "http", "post"),
    "http_put":        ("iot_controller.py", "http", "put"),
}


def execute_tool(tool_name: str, params: dict | None = None) -> ExecutionResult:
    """
    通过工具名执行对应的 system-controller 脚本

    参数:
        tool_name: 工具名，如 "window_list"、"volume_set"
        params: 额外参数字典，如 {"level": 50, "--title": "Chrome"}
                 键名会直接作为命令行参数传入
    """
    if tool_name not in TOOL_DEFS:
        available = ", ".join(sorted(TOOL_DEFS.keys()))
        return ExecutionResult(
            False,
            f"未知工具: '{tool_name}'。可用工具: {available}",
            tool_name
        )

    params = params or {}
    # 从映射表获取基础参数
    base_args = list(TOOL_DEFS[tool_name])

    # 展开用户参数为命令行参数
    extra_args = []
    for key, value in params.items():
        # 以 -- 开头的键保留前缀，否则加上
        if key.startswith("--"):
            extra_args.append(key)
        else:
            extra_args.append(f"--{key}")
        if value is not None and value != "":
            extra_args.append(str(value))

    all_args = base_args + extra_args
    script_name = all_args[0]
    script_args = all_args[1:]

    return run_script(script_name, script_args)


# ═══════════════════════════════════════════
# 危险操作检查
# ═══════════════════════════════════════════

DANGEROUS_TOOLS = {
    "power_shutdown", "power_restart", "power_sleep", "power_hibernate",
    "process_kill", "window_close", "network_disable",
}


def is_dangerous(tool_name: str) -> bool:
    """判断是否为危险操作"""
    return tool_name in DANGEROUS_TOOLS


# ═══════════════════════════════════════════
# 交互模式（独立运行时使用）
# ═══════════════════════════════════════════

BANNER = """
╔══════════════════════════════════════╗
║   Minimal Agent — 操作系统控制代理    ║
║   输入自然语言或工具名即可操作系统    ║
║   输入 quit 或 exit 退出              ║
║   输入 tools 查看可用工具列表         ║
╚══════════════════════════════════════╝
"""


def print_tools():
    """打印工具分类清单"""
    categories: dict[str, list[str]] = {}
    for name, defn in TOOL_DEFS.items():
        category = defn[0].replace(".py", "")
        categories.setdefault(category, []).append(name)

    print("\n📋 可用工具列表：\n")
    for cat, tools in sorted(categories.items()):
        print(f"  📦 {cat}")
        for t in tools:
            print(f"    - {t}")
    print()


def interactive_mode():
    """交互式循环（独立运行）"""
    print(BANNER)

    while True:
        try:
            user_input = input("\n🫵 ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("👋 再见！")
            break
        if user_input.lower() == "tools":
            print_tools()
            continue

        # 尝试作为工具调用解析: 工具名 [参数...]
        parts = user_input.split()
        tool_name = parts[0]

        if tool_name in TOOL_DEFS:
            # 解析简单参数: --key value --key2 value2
            params = {}
            i = 1
            while i < len(parts):
                key = parts[i]
                if key.startswith("--"):
                    if i + 1 < len(parts) and not parts[i + 1].startswith("--"):
                        params[key] = parts[i + 1]
                        i += 2
                    else:
                        params[key] = True
                        i += 1
                else:
                    i += 1

            if is_dangerous(tool_name):
                confirm = input(f"  ⚠️  危险操作 [{tool_name}]，确认执行？(y/N): ")
                if confirm.lower() != "y":
                    print("  ❌ 已取消")
                    continue

            result = execute_tool(tool_name, params)
            print(f"\n  {result}")

        else:
            print(f"  ❓ 未知命令: '{tool_name}'")
            print(f"  💡 输入 'tools' 查看可用工具，或输入 'quit' 退出")


# ═══════════════════════════════════════════
# Mixed 模式支持（智能混合V1和V2）
# ═══════════════════════════════════════════

MIXED_MODE_PROMPT = """
你是一个智能的任务分析器，负责将复杂的多步骤任务分解为适合的执行模式。

**模式选择规则：**
1. **V2模式（Function Calling）**：用于以下类型的子任务：
   - 窗口管理（最小化、最大化、关闭、移动等）
   - 进程控制（启动、结束、列出等）
   - 硬件控制（音量、亮度、电源、网络等）
   - 鼠标键盘操作
   - 截图、OCR识别
   - 串口通信、IoT控制

2. **V1模式（文本命令）**：用于以下类型的子任务：
   - 文件操作（创建、删除、复制、移动等）
   - 脚本执行、程序运行
   - 数据库操作
   - 系统配置修改
   - 网络服务操作
   - 复杂数据处理

**任务分析流程：**
1. 分析用户输入的任务
2. 识别任务中的多个步骤
3. 为每个步骤选择最佳模式（V1或V2）
4. 生成执行序列

**输出格式：**
- 为每个步骤指定模式：[V1] 或 [V2]
- 提供执行命令或工具调用
- 按顺序排列

**示例：**
用户输入："帮我截屏，OCR识别文字，保存到文件，然后调整音量"

分析结果：
[V2] 截图：使用screenshot工具
[V2] OCR识别：使用visual_ocr工具，参数为截图文件
[V1] 保存到文件：使用文本命令复制OCR结果到文件
[V2] 调整音量：使用volume_set工具，参数level=50
"""

def split_mixed_task(task: str) -> list[tuple[str, str]]:
    """
    智能拆分混合任务为多个子步骤
    返回格式：[(模式, 命令/工具), ...]
    """
    # 简单基于标点符号拆分
    import re
    # 使用中文或英文标点作为分隔符
    separators = r'[，,。；;、]'
    steps = [step.strip() for step in re.split(separators, task) if step.strip()]
    
    result = []
    for step in steps:
        task_type = analyze_task_type(step)
        if task_type == "V2":
            # 尝试将自然语言转换为工具调用
            tool_name = translate_to_tool(step)
            if tool_name:
                result.append(("V2", tool_name))
            else:
                # 回退到V1模式
                result.append(("V1", step))
        elif task_type == "V1":
            result.append(("V1", step))
        else:
            # 默认使用V1
            result.append(("V1", step))
    
    return result

def translate_to_tool(step: str) -> str | None:
    """将自然语言转换为工具名"""
    step_lower = step.lower()
    
    # 简单的关键词匹配
    if "窗口" in step_lower or "window" in step_lower:
        if "列表" in step_lower or "list" in step_lower:
            return "window_list"
        elif "激活" in step_lower or "activate" in step_lower:
            return "window_activate"
        elif "关闭" in step_lower or "close" in step_lower:
            return "window_close"
    
    elif "进程" in step_lower or "process" in step_lower:
        if "列表" in step_lower or "list" in step_lower:
            return "process_list"
        elif "结束" in step_lower or "kill" in step_lower:
            return "process_kill"
    
    elif "音量" in step_lower or "volume" in step_lower:
        if "设置" in step_lower or "set" in step_lower:
            return "volume_set"
        elif "获取" in step_lower or "get" in step_lower:
            return "volume_get"
    
    elif "截图" in step_lower or "screenshot" in step_lower:
        return "screenshot"
    
    elif "ocr" in step_lower or "识别" in step_lower:
        return "visual_ocr"
    
    elif "鼠标" in step_lower or "mouse" in step_lower:
        if "移动" in step_lower or "move" in step_lower:
            return "mouse_move"
        elif "点击" in step_lower or "click" in step_lower:
            return "mouse_click"
    
    elif "键盘" in step_lower or "keyboard" in step_lower:
        if "输入" in step_lower or "type" in step_lower:
            return "keyboard_type"
    
    return None

def execute_mixed_task(task: str) -> list[tuple[str, ExecutionResult]]:
    """
    执行混合模式任务
    智能分析任务，自动选择V1或V2模式执行每个子步骤
    
    返回: [(模式, 执行结果), ...]
    """
    print("🤖 分析混合模式任务...")
    steps = split_mixed_task(task)
    
    if not steps:
        return [("error", ExecutionResult(False, "❌ 无法解析任务", ""))]
    
    results = []
    print(f"📋 任务分解为 {len(steps)} 个步骤:")
    for i, (mode, command) in enumerate(steps, 1):
        print(f"  {i}. [{mode}] {command}")
    
    for i, (mode, command) in enumerate(steps, 1):
        print(f"\n🚀 执行步骤 {i}/{len(steps)}: [{mode}] {command}")
        
        if mode == "V1":
            result = execute_raw_command(command)
        elif mode == "V2":
            # 解析工具调用参数
            tool_parts = command.split()
            tool_name = tool_parts[0] if tool_parts else ""
            params = {}
            
            # 简单参数解析（实际应用中应该更智能）
            for j in range(1, len(tool_parts), 2):
                if j + 1 < len(tool_parts):
                    key = tool_parts[j]
                    value = tool_parts[j + 1]
                    if key.startswith("--"):
                        params[key] = value
                    else:
                        params[f"--{key}"] = value
            
            result = execute_tool(tool_name, params)
        else:
            result = ExecutionResult(False, f"❌ 未知模式: {mode}", command)
        
        results.append((mode, result))
        print(f"  结果: {result}")
    
    return results

def run_mixed_mode():
    """Mixed 模式交互循环"""
    print("""
╔══════════════════════════════════════╗
║   Mixed 模式 — 智能混合执行          ║
║   自动分析任务，智能选择V1/V2模式    ║
║   支持复杂多步骤任务自由切换组合     ║
║   输入 quit 或 exit 退出             ║
║   输入 help 查看使用示例             ║
╚══════════════════════════════════════╝
""")
    
    while True:
        try:
            user_input = input("\n🫵 输入任务: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 退出 Mixed 模式")
            break
        
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("👋 退出 Mixed 模式")
            break
        if user_input.lower() == "help":
            print(MIXED_MODE_PROMPT)
            continue
        
        # 执行混合模式任务
        results = execute_mixed_task(user_input)
        
        # 显示总结
        print(f"\n📊 任务完成总结:")
        success_count = sum(1 for mode, result in results if result.success)
        print(f"  ✅ 成功: {success_count}/{len(results)}")
        if success_count < len(results):
            print(f"  ❌ 失败: {len(results) - success_count}")
            for i, (mode, result) in enumerate(results, 1):
                if not result.success:
                    print(f"    步骤{i}[{mode}]: {result.output}")


# ═══════════════════════════════════════════
# Text 模式支持（V1：任意命令执行）
# ═══════════════════════════════════════════

def execute_raw_command(command: str) -> ExecutionResult:
    """
    执行任意系统命令（text/V1 模式）
    
    参数:
        command: 完整的shell命令字符串
    """
    command_str = command.strip()
    if not command_str:
        return ExecutionResult(False, "❌ 命令为空", "")
    
    try:
        # 执行任意命令
        result = subprocess.run(
            command_str,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace",
        )
        output = result.stdout or result.stderr or "(无输出)"
        success = result.returncode == 0
        return ExecutionResult(success, output, command_str)
    
    except subprocess.TimeoutExpired:
        return ExecutionResult(False, f"⏰ 执行超时 (30s): {command_str}", command_str)
    
    except Exception as e:
        return ExecutionResult(False, f"💥 执行异常: {e}", command_str)


def run_text_mode():
    """Text 模式交互循环"""
    print("""
╔══════════════════════════════════════╗
║   Text 模式 — 任意命令执行           ║
║   可执行任何系统命令（包括文件修改）  ║
║   **警告：操作不可逆，风险自担**     ║
║   输入 quit 或 exit 退出             ║
╚══════════════════════════════════════╝
""")
    
    while True:
        try:
            user_input = input("\n🫵 输入命令: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 退出 Text 模式")
            break
        
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("👋 退出 Text 模式")
            break
        
        # 检查危险命令
        dangerous_keywords = ["rm -rf", "del /s /q", "format", "shutdown", "taskkill /f"]
        is_dangerous = any(keyword in user_input.lower() for keyword in dangerous_keywords)
        
        if is_dangerous:
            confirm = input(f"⚠️  **危险命令**：{user_input}\n   确认执行？(y/N): ")
            if confirm.lower() != "y":
                print("  ❌ 已取消")
                continue
        
        result = execute_raw_command(user_input)
        print(f"\n  {result}")


# ═══════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════

def parse_args() -> tuple[ModeType | None, bool, list[str]]:
    """
    解析命令行参数
    
    返回:
        (force_mode, is_interactive, remaining_args)
        force_mode: 强制模式（来自命令行参数）
        is_interactive: 是否交互模式
        remaining_args: 剩余参数（命令或工具名+参数）
    """
    args = sys.argv[1:]
    force_mode: ModeType | None = None
    is_interactive = False
    
    # 解析模式参数
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg == "--text":
            force_mode = "force_text"
            args.pop(i)
        elif arg == "--function":
            force_mode = "force_function"
            args.pop(i)
        elif arg == "--auto":
            force_mode = "auto"
            args.pop(i)
        elif arg == "--mixed":
            force_mode = "mixed"
            args.pop(i)
        elif arg == "--interactive":
            is_interactive = True
            args.pop(i)
        else:
            i += 1
    
    return force_mode, is_interactive, args


def main():
    """主入口：支持智能模式选择和多种运行方式"""
    print(f"📋 配置模式: {CONFIG.mode}")
    print(f"📋 路径检查: {CONFIG.skill_path}")
    
    # 解析命令行参数
    force_mode, is_interactive, remaining_args = parse_args()
    
    if force_mode:
        print(f"📋 命令行强制模式: {force_mode}")
    
    # 确定实际模式
    actual_mode = determine_actual_mode(force_mode)
    
    if is_interactive:
        # 交互模式
        if actual_mode == "text":
            run_text_mode()
        elif actual_mode == "mixed":
            run_mixed_mode()
        else:
            interactive_mode()
        return
    
    if not remaining_args:
        # 没有参数，默认进入交互模式
        print("ℹ️  没有提供命令，进入交互模式")
        if actual_mode == "text":
            run_text_mode()
        elif actual_mode == "mixed":
            run_mixed_mode()
        else:
            interactive_mode()
        return
    
    if actual_mode == "text":
        # Text 模式：直接执行命令
        command = " ".join(remaining_args)
        result = execute_raw_command(command)
        print(result)
        return
    elif actual_mode == "mixed":
        # Mixed 模式：智能分析任务
        task = " ".join(remaining_args)
        results = execute_mixed_task(task)
        
        # 显示总结
        print(f"\n📊 任务完成总结:")
        success_count = sum(1 for mode, result in results if result.success)
        print(f"  ✅ 成功: {success_count}/{len(results)}")
        if success_count < len(results):
            print(f"  ❌ 失败: {len(results) - success_count}")
            for i, (mode, result) in enumerate(results, 1):
                if not result.success:
                    print(f"    步骤{i}[{mode}]: {result.output}")
        return
    
    # Function 模式：工具调用
    tool_name = remaining_args[0]
    params = {}
    
    i = 1
    while i < len(remaining_args):
        key = remaining_args[i]
        if key.startswith("--"):
            if i + 1 < len(remaining_args) and not remaining_args[i + 1].startswith("--"):
                params[key] = remaining_args[i + 1]
                i += 2
            else:
                params[key] = True
                i += 1
        else:
            i += 1
    
    if is_dangerous(tool_name):
        confirm = input(f"⚠️  危险操作 [{tool_name}]，确认执行？(y/N): ")
        if confirm.lower() != "y":
            print("❌ 已取消")
            return
    
    result = execute_tool(tool_name, params)
    print(result)


if __name__ == "__main__":
    main()
