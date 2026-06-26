#!/usr/bin/env python3
"""
Mali App Builder Launcher (Python版本)
自动打开码力搭建平台并填充用户需求
支持跨平台使用
"""

import sys
import time
import platform
import subprocess
import webbrowser
from urllib.parse import quote

# 配置
MALI_URL = "https://lowcode.baidu-int.com/ai-coding"

# 颜色代码
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def print_colored(text, color=''):
    """打印带颜色的文本"""
    print(f"{color}{text}{Colors.NC}")

def detect_browser():
    """检测可用的浏览器"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return "chrome-mac"
    elif system == "Linux":
        return "chrome-linux"
    elif system == "Windows":
        return "chrome-win"
    else:
        return "default"

def launch_with_applescript(requirement):
    """使用 AppleScript 在 macOS 上启动 Chrome（最佳方案）"""
    print_colored("🚀 使用 AppleScript 启动码力搭建平台...", Colors.BLUE)
    
    # 转义单引号
    requirement_escaped = requirement.replace("'", "'\"'\"'")
    
    applescript = f'''
tell application "Google Chrome"
    activate
    delay 0.5
    
    -- 方式1：直接在当前窗口打开新标签
    if (count of windows) = 0 then
        make new window
        set URL of active tab of front window to "{MALI_URL}"
    else
        tell front window
            set newTab to make new tab
            set URL of newTab to "{MALI_URL}"
        end tell
    end if
    
    delay 5
    
    -- 第一步：先填充需求
    set jsCode1 to "
    (function() {{
        const input = document.querySelector('textarea, input[type=\\"text\\"]');
        if (input) {{
            input.value = '{requirement_escaped}';
            input.focus();
            return 'filled';
        }}
        return 'not_found';
    }})();
    "
    
    tell front window
        set result1 to execute active tab javascript jsCode1
    end tell
    
    delay 1
    
    -- 第二步：触发输入事件
    set jsCode2 to "
    (function() {{
        const input = document.querySelector('textarea, input[type=\\"text\\"]');
        if (input) {{
            const inputEvent = new Event('input', {{ bubbles: true, cancelable: true }});
            input.dispatchEvent(inputEvent);
            const changeEvent = new Event('change', {{ bubbles: true }});
            input.dispatchEvent(changeEvent);
            return 'triggered';
        }}
        return 'not_found';
    }})();
    "
    
    tell front window
        execute active tab javascript jsCode2
    end tell
    
    delay 0.5
    
    -- 第三步：点击发送按钮
    set jsCode3 to "
    (function() {{
        // 尝试多种选择器查找发送按钮
        const selectors = [
            'button[type=\\"submit\\"]',
            'button.send-btn',
            'button.submit-btn',
            'button:has(svg)',
            'button[aria-label*=\\"发送\\"]',
            'button[title*=\\"发送\\"]'
        ];
        
        for (let selector of selectors) {{
            const btn = document.querySelector(selector);
            if (btn) {{
                btn.click();
                return 'clicked: ' + selector;
            }}
        }}
        
        // 如果找不到，尝试查找最后一个按钮
        const allButtons = document.querySelectorAll('button');
        if (allButtons.length > 0) {{
            const lastBtn = allButtons[allButtons.length - 1];
            lastBtn.click();
            return 'clicked last button';
        }}
        
        return 'button not found';
    }})();
    "
    
    tell front window
        execute active tab javascript jsCode3
    end tell
end tell
'''
    
    try:
        subprocess.run(['osascript', '-e', applescript], check=True)
        print_colored("✅ Chrome 已启动，需求已自动填充！", Colors.GREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ AppleScript 执行失败: {e}", Colors.RED)
        return False
    except FileNotFoundError:
        print_colored("❌ 未找到 osascript 命令", Colors.RED)
        return False

def launch_with_webbrowser(requirement):
    """使用 Python webbrowser 模块启动（兼容方案）"""
    print_colored("🚀 使用系统默认浏览器启动...", Colors.BLUE)
    
    try:
        # 尝试用 Chrome 打开
        chrome_path = None
        system = platform.system()
        
        if system == "Darwin":
            chrome_path = 'open -a /Applications/Google\\ Chrome.app %s'
        elif system == "Windows":
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        elif system == "Linux":
            chrome_path = '/usr/bin/google-chrome %s'
        
        if chrome_path:
            webbrowser.get(chrome_path).open(MALI_URL)
        else:
            webbrowser.open(MALI_URL)
        
        print_colored("✅ 浏览器已打开", Colors.GREEN)
        print_colored("⚠️ 请手动将以下需求复制到输入框：", Colors.YELLOW)
        print_colored(f"\n{requirement}\n", Colors.BOLD)
        return True
        
    except Exception as e:
        print_colored(f"❌ 浏览器启动失败: {e}", Colors.RED)
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_colored("❌ 错误：缺少搭建需求参数", Colors.RED)
        print("\n用法:")
        print(f"  python3 {sys.argv[0]} \"搭建需求描述\"")
        print("\n示例:")
        print(f"  python3 {sys.argv[0]} \"创建一个任务管理系统\"")
        sys.exit(1)
    
    requirement = " ".join(sys.argv[1:])
    
    # 打印标题
    print_colored("━" * 50, Colors.BLUE)
    print_colored("   码力搭建平台启动器 (Python版本)", Colors.BLUE)
    print_colored("━" * 50, Colors.BLUE)
    print()
    print_colored(f"?? 平台地址: {MALI_URL}", Colors.BLUE)
    print_colored(f"💻 操作系统: {platform.system()}", Colors.BLUE)
    print_colored(f"📋 搭建需求:", Colors.BLUE)
    print_colored(f"   {requirement}", Colors.GREEN)
    print()
    
    # 根据系统选择启动方式
    system = platform.system()
    success = False
    
    if system == "Darwin":
        # macOS 优先使用 AppleScript
        success = launch_with_applescript(requirement)
        if not success:
            print_colored("⚠️ AppleScript 方式失败，尝试备用方案...", Colors.YELLOW)
            success = launch_with_webbrowser(requirement)
    else:
        # 其他系统使用 webbrowser
        success = launch_with_webbrowser(requirement)
    
    if success:
        print()
        print_colored("✅ 操作完成！", Colors.GREEN)
        print_colored("⏳ 请在浏览器中查看搭建进度...", Colors.BLUE)
        print()
    else:
        print_colored("\n❌ 启动失败，请手动访问以下地址：", Colors.RED)
        print_colored(f"   {MALI_URL}", Colors.BOLD)
        sys.exit(1)

if __name__ == "__main__":
    main()