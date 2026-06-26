#!/usr/bin/env python3
"""
macOS 桌面控制 - 自然语言控制核心
解析用户的自然语言命令，转换为具体操作
"""

import sys
import subprocess
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 颜色输出
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_color(color, text):
    print(f"{color}{text}{Colors.NC}")

def show_help():
    """显示帮助"""
    print("macOS 自然语言控制")
    print("")
    print("用法：python3 natural_language.py [命令]")
    print("")
    print("示例:")
    print("  python3 natural_language.py \"帮我截个屏\"")
    print("  python3 natural_language.py \"把 Safari 放到左边\"")
    print("  python3 natural_language.py \"打开所有工作应用\"")
    print("  python3 natural_language.py \"关闭 Chrome\"")
    print("  python3 natural_language.py \"显示我的电脑配置\"")
    print("")
    print("支持的命令类型:")
    print("  - 截屏类：截屏、截图、拍个照")
    print("  - 窗口类：左边、右边、全屏、居中")
    print("  - 应用类：打开、关闭、切换")
    print("  - 系统类：配置、信息、进程")
    print("  - 自动化：晨会、专注、下班")

def parse_command(text):
    """
    解析自然语言命令
    返回：(动作，参数，置信度)
    """
    text_original = text.strip()
    text = text.lower()  # 只小写英文，保留中文
    
    # === 截屏类命令 ===
    screenshot_keywords = ['截屏', '截图', '拍个照', 'screenshot', 'capture', 'shot', '截个屏']
    if any(kw in text_original for kw in screenshot_keywords) or any(kw in text for kw in screenshot_keywords):
        # 检查是否有延迟
        delay_match = re.search(r'(\d+)\s*(秒 | 秒后|seconds?)', text_original)
        delay = int(delay_match.group(1)) if delay_match else 0
        
        # 检查是否区域截图
        if '区域' in text_original or 'region' in text or '选' in text_original:
            return ('screenshot_select', {'delay': delay}, 0.9)
        else:
            return ('screenshot', {'delay': delay}, 0.95)
    
    # === 窗口吸附类命令 ===
    window_keywords = ['放到', '移到', '移动到', '放在', '左边', '右边', '上边', '下边', '全屏', '居中', '四分之一']
    if any(kw in text for kw in window_keywords):
        # 提取应用名（简单匹配）
        app_match = re.search(r'(safari|chrome|firefox|vs.?code|iterm|terminal|qq|wechat|钉钉|dingtalk|企业微信|wecom)', text)
        app_name = app_match.group(1) if app_match else None
        
        # 判断方向
        if '左边' in text or '左侧' in text or 'left' in text:
            return ('window_left', {'app': app_name}, 0.85)
        elif '右边' in text or '右侧' in text or 'right' in text:
            return ('window_right', {'app': app_name}, 0.85)
        elif '上边' in text or '上方' in text or 'top' in text:
            return ('window_top', {'app': app_name}, 0.85)
        elif '下边' in text or '下方' in text or 'bottom' in text:
            return ('window_bottom', {'app': app_name}, 0.85)
        elif '全屏' in text or '最大化' in text or 'full' in text:
            return ('window_full', {'app': app_name}, 0.85)
        elif '居中' in text or '中间' in text or 'center' in text:
            return ('window_center', {'app': app_name}, 0.85)
        elif '四分之一' in text or '角落' in text or 'corner' in text:
            corner_match = re.search(r'([1234]|一 | 二 | 三 | 四 | 左上 | 右上 | 左下 | 右下)', text)
            corner = 1  # 默认左上
            if corner_match:
                c = corner_match.group(1)
                if c in ['1', '一', '左上']: corner = 1
                elif c in ['2', '二', '右上']: corner = 2
                elif c in ['3', '三', '左下']: corner = 3
                elif c in ['4', '四', '右下']: corner = 4
            return ('window_corner', {'app': app_name, 'corner': corner}, 0.8)
    
    # === 应用控制类命令 ===
    app_action_keywords = ['打开', '启动', '运行', 'open', 'launch', 'start']
    if any(kw in text for kw in app_action_keywords):
        # 提取应用名
        app_patterns = [
            r'(safari|浏览器)',
            r'(chrome|google.?chrome)',
            r'(firefox|火狐)',
            r'(vs.?code|visual.?studio.?code)',
            r'(iterm|iterm2|terminal|终端)',
            r'(qq|微信 |wechat|钉钉|dingtalk|企业微信)',
            r'(mail|邮件)',
            r'(calendar|日历)',
            r'(music|音乐)',
            r'(photos|照片)',
            r'(finder|访达)',
        ]
        app_name = None
        for pattern in app_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                app_name = match.group(1)
                break
        
        if app_name:
            return ('app_open', {'app': app_name}, 0.85)
        else:
            return ('app_open', {'app': None}, 0.6)
    
    # 关闭应用
    close_keywords = ['关闭', '退出', '关掉', 'close', 'quit', 'exit', 'kill']
    if any(kw in text for kw in close_keywords):
        # 提取应用名（同上）
        app_patterns = [
            r'(safari|浏览器)',
            r'(chrome|google.?chrome)',
            r'(firefox|火狐)',
            r'(vs.?code|visual.?studio.?code)',
            r'(iterm|iterm2|terminal|终端)',
            r'(qq|微信 |wechat|钉钉|dingtalk|企业微信)',
        ]
        app_name = None
        for pattern in app_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                app_name = match.group(1)
                break
        
        if app_name:
            return ('app_close', {'app': app_name}, 0.85)
        elif '所有' in text and ('娱乐' in text or '无关' in text):
            return ('app_close_entertainment', {}, 0.8)
        else:
            return ('app_close', {'app': None}, 0.6)
    
    # 切换应用
    switch_keywords = ['切换', '转到', '跳到', 'switch', 'go to']
    if any(kw in text for kw in switch_keywords):
        app_patterns = [r'(safari|chrome|firefox|vs.?code|terminal|qq|wechat)']
        app_name = None
        for pattern in app_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                app_name = match.group(1)
                break
        
        if app_name:
            return ('app_switch', {'app': app_name}, 0.85)
    
    # === QQ 消息发送 ===
    # 支持多种说法：用 QQ 发消息、QQ 发消息、发 QQ、用 QQ 给 xxx 发消息
    qq_send_keywords = ['QQ', 'qq']
    if any(kw in text_original for kw in qq_send_keywords) and ('消息' in text_original or '发' in text_original) and '给' in text_original:
        # 使用字符串方法提取（比正则更可靠）
        # 格式："用 QQ 给 [联系人] 发消息 [消息内容]"
        gei_idx = text_original.find('给')
        fa_idx = text_original.find('发')
        
        if gei_idx != -1 and fa_idx != -1 and fa_idx > gei_idx:
            buddy = text_original[gei_idx+1:fa_idx].strip()
            message = text_original[fa_idx+1:].strip()
            
            # 清理消息中的关键词
            if message.startswith('消息'):
                message = message[2:]
            
            # 常见问句模板处理
            if '几点' in message and not message.endswith('？'):
                message = message.replace('几点', '几点了？').rstrip('了？') + '了？'
            
            if buddy and message:
                return ('qq_send', {'buddy': buddy, 'message': message}, 0.9)
    
    # === 系统信息类命令 ===
    info_keywords = ['配置', '信息', '状态', '电脑', '系统', 'info', 'config', 'status', 'spec']
    if any(kw in text for kw in info_keywords):
        if '进程' in text or '运行' in text or 'app' in text:
            return ('system_processes', {}, 0.9)
        else:
            return ('system_info', {}, 0.95)
    
    # === 自动化工作流 ===
    workflow_keywords = ['晨会', '早上', '早晨', 'morning', '专注', '下班', 'cleanup', 'presentation']
    if any(kw in text for kw in workflow_keywords):
        if '晨会' in text or '早上' in text or '早晨' in text or 'morning' in text:
            return ('workflow_morning', {}, 0.9)
        elif '专注' in text or 'focus' in text:
            return ('workflow_focus', {}, 0.9)
        elif '下班' in text or 'cleanup' in text or '清理' in text:
            return ('workflow_cleanup', {}, 0.9)
        elif '演示' in text or 'presentation' in text:
            return ('workflow_presentation', {}, 0.9)
    
    # === 剪贴板 ===
    clipboard_keywords = ['复制', '粘贴', '剪贴板', 'clipboard', 'copy', 'paste']
    if any(kw in text for kw in clipboard_keywords):
        if '复制' in text or 'copy' in text:
            # 提取要复制的文字
            text_match = re.search(r'["\'](.+?)["\']', text)
            if text_match:
                return ('clipboard_set', {'text': text_match.group(1)}, 0.9)
        elif '粘贴' in text or 'paste' in text:
            return ('clipboard_get', {}, 0.9)
    
    # === 鼠标键盘 ===
    mouse_keywords = ['鼠标位置', 'mouse', 'click', '点击']
    if any(kw in text for kw in mouse_keywords):
        if '位置' in text or 'position' in text or 'where' in text:
            return ('mouse_position', {}, 0.9)
        elif '点击' in text or 'click' in text:
            return ('mouse_click', {}, 0.8)
    
    # 调试输出
    # print(f"DEBUG: 未匹配，text={text_original}")
    
    # 未匹配到命令
    return ('unknown', {'text': text_original}, 0.5)

def execute_command(action, params, original_text=""):
    """
    执行解析后的命令
    
    Args:
        action: 动作
        params: 参数
        original_text: 原始用户输入
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 🎯 关键改进：先检索 ControlMemory
    print_color(Colors.BLUE, "🔍 检索 ControlMemory...")
    try:
        from operation_search import OperationSearcher
        searcher = OperationSearcher()
        
        if original_text:
            best_match = searcher.find_best_match(original_text, threshold=0.5)
            
            if best_match:
                print_color(Colors.GREEN, f"✅ 找到相似操作：{best_match['app']} - {best_match['name']}")
                print(f"   相似度：{best_match.get('similarity', 0):.0%}")
                print(f"   命令：{best_match['command']}")
                print(f"   脚本：{best_match['script']}")
                print(f"   成功率：{best_match['success_rate']}")
                
                # 分析是否能完成
                can_do, reason = searcher.can_complete_task(best_match, original_text)
                print(f"   📊 分析：{reason}")
                
                # 询问是否使用
                if can_do:
                    print("")
                    print_color(Colors.YELLOW, "💡 是否使用此操作？(y/n)")
                    # 实际使用中可以自动执行或询问用户
                    # 这里选择自动执行
                    print_color(Colors.BLUE, "🚀 使用已有操作执行...")
                    searcher.execute_operation(best_match)
                    
                    # 执行操作并记录成功/失败
                    from control_memory import ControlMemory
                    memory = ControlMemory()
                    
                    if searcher.execute_operation(best_match):
                        # 成功 - 增加借鉴次数
                        memory.increment_usage(
                            app_name=best_match['app'],
                            command=best_match['command']
                        )
                    else:
                        # 失败 - 增加失败次数
                        memory.increment_failure(
                            app_name=best_match['app'],
                            command=best_match['command']
                        )
                    return
    except Exception as e:
        print_color(Colors.YELLOW, f"⚠️  检索失败：{e}，继续执行...")
    
    # 如果没有找到匹配或执行失败，继续原有流程
    print_color(Colors.BLUE, f"🧠 解析结果：{action}")
    print_color(Colors.BLUE, f"📋 参数：{params}")
    print("")
    
    # 导入 ControlMemory（用于记录）
    control_memory_path = os.path.join(script_dir, "control_memory.py")
    
    if action == 'screenshot':
        print_color(Colors.GREEN, "📸 正在截屏...")
        delay = params.get('delay', 0)
        cmd = f"bash {SCRIPT_DIR}/screenshot.sh"
        if delay > 0:
            cmd += f" -d {delay}"
        subprocess.run(cmd, shell=True)
    
    elif action == 'screenshot_select':
        print_color(Colors.GREEN, "📸 请选择截图区域...")
        subprocess.run(f"bash {SCRIPT_DIR}/screenshot.sh -s", shell=True)
    
    elif action == 'window_left':
        app = params.get('app', 'Safari')
        print_color(Colors.GREEN, f"🪟 将 {app} 放到左半屏...")
        subprocess.run(f"bash {SCRIPT_DIR}/window_snap.sh left '{app}'", shell=True)
    
    elif action == 'window_right':
        app = params.get('app', 'Chrome')
        print_color(Colors.GREEN, f"🪟 将 {app} 放到右半屏...")
        subprocess.run(f"bash {SCRIPT_DIR}/window_snap.sh right '{app}'", shell=True)
    
    elif action == 'window_full':
        app = params.get('app', 'Safari')
        print_color(Colors.GREEN, f"🪟 将 {app} 全屏...")
        subprocess.run(f"bash {SCRIPT_DIR}/window_snap.sh full '{app}'", shell=True)
    
    elif action == 'window_center':
        app = params.get('app', 'Safari')
        print_color(Colors.GREEN, f"🪟 将 {app} 居中...")
        subprocess.run(f"bash {SCRIPT_DIR}/window_snap.sh center '{app}'", shell=True)
    
    elif action == 'app_open':
        app = params.get('app')
        if app:
            print_color(Colors.GREEN, f"🖥️  正在打开 {app}...")
            subprocess.run(f"bash {SCRIPT_DIR}/app_control.sh open '{app}'", shell=True)
        else:
            print_color(Colors.YELLOW, "⚠️  请指定要打开的应用名称")
    
    elif action == 'app_close':
        app = params.get('app')
        if app:
            print_color(Colors.GREEN, f"🖥️  正在关闭 {app}...")
            subprocess.run(f"bash {SCRIPT_DIR}/app_control.sh close '{app}'", shell=True)
        else:
            print_color(Colors.YELLOW, "⚠️  请指定要关闭的应用名称")
    
    elif action == 'app_close_entertainment':
        print_color(Colors.GREEN, "🖥️  正在关闭娱乐应用...")
        for app in ['Google Chrome', 'Safari', 'Music', 'TV']:
            subprocess.run(f"bash {SCRIPT_DIR}/app_control.sh close '{app}'", shell=True, capture_output=True)
        print_color(Colors.GREEN, "✅ 娱乐应用已关闭")
    
    elif action == 'qq_send':
        buddy = params.get('buddy', '')
        message = params.get('message', '')
        print_color(Colors.GREEN, f"🐧 正在用 QQ 发送消息...")
        print_color(Colors.BLUE, f"   联系人：{buddy}")
        print_color(Colors.BLUE, f"   消息：{message}")
        print("")
        subprocess.run(f"bash {SCRIPT_DIR}/../../../scripts/qq-send-auto.sh '{buddy}' '{message}'", shell=True)
    
    elif action == 'system_info':
        print_color(Colors.GREEN, "💻 系统信息:")
        subprocess.run(f"bash {SCRIPT_DIR}/system_info.sh --short", shell=True)
    
    elif action == 'system_processes':
        print_color(Colors.GREEN, "📋 运行的应用:")
        subprocess.run(f"bash {SCRIPT_DIR}/processes.sh -g", shell=True)
    
    elif action == 'workflow_morning':
        print_color(Colors.GREEN, "🌅 启动晨会准备工作流...")
        subprocess.run(f"bash {SCRIPT_DIR}/automation_workflows.sh morning", shell=True)
    
    elif action == 'workflow_focus':
        print_color(Colors.GREEN, "🎯 启动专注模式...")
        subprocess.run(f"bash {SCRIPT_DIR}/automation_workflows.sh focus", shell=True)
    
    elif action == 'workflow_cleanup':
        print_color(Colors.GREEN, "🏠 启动下班清理工作流...")
        subprocess.run(f"bash {SCRIPT_DIR}/automation_workflows.sh cleanup", shell=True)
    
    elif action == 'clipboard_set':
        text = params.get('text', '')
        print_color(Colors.GREEN, f"📋 复制文字到剪贴板...")
        subprocess.run(f"bash {SCRIPT_DIR}/clipboard.sh set \"{text}\"", shell=True)
    
    elif action == 'mouse_position':
        print_color(Colors.GREEN, "🖱️  鼠标位置:")
        subprocess.run(f"python3 {SCRIPT_DIR}/desktop_ctrl.py mouse position", shell=True)
    
    elif action == 'unknown':
        print_color(Colors.RED, "❌ 抱歉，我没理解这个命令")
        print_color(Colors.YELLOW, "💡 提示：可以说 '截个屏'、'把 Safari 放左边'、'打开 Chrome' 等")
        print("")
        show_help()
    
    else:
        print_color(Colors.YELLOW, f"⚠️  未知动作：{action}")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    # 获取用户输入（支持多词）
    command_text = ' '.join(sys.argv[1:])
    
    print_color(Colors.BLUE, "🗣️  收到命令:")
    print(f"   \"{command_text}\"")
    print("")
    
    # 解析命令
    action, params, confidence = parse_command(command_text)
    
    print_color(Colors.BLUE, f"🎯 置信度：{confidence:.0%}")
    print("")
    
    # 执行命令
    if confidence >= 0.6:
        execute_command(action, params)
    else:
        print_color(Colors.RED, "❌ 抱歉，我不太理解这个命令")
        print_color(Colors.YELLOW, "💡 请尝试更明确的说法，例如:")
        print("   - '帮我截个屏'")
        print("   - '把 Safari 放到左边'")
        print("   - '打开 Chrome 浏览器'")
        print("")
        show_help()

if __name__ == "__main__":
    main()
