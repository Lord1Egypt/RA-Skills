#!/usr/bin/env python3
"""
派蒙.skill - 原神专用AI游戏伴侣
旅行者最好的伙伴！
"""
import argparse
import json
import sys
import time
import os
from datetime import datetime
from typing import Optional
from PIL import Image

from scripts.click import click, right_click
from scripts.keyboard import press_key, hold_key, key_down, key_up
from scripts.screenshot import take_screenshot
from scripts.window import get_window_info, activate_window, list_windows, find_window_by_partial_title
from scripts.recognition import find_button, find_all_buttons, list_available_buttons
from scripts.gui_agent import get_agent, list_available_agents
from scripts.config import get_gui_agent_config, get_api_key

# 原神窗口标题
GENSHIN_WINDOW_TITLE = "原神"
GAME_ID = "genshin-impact"

def print_help():
    help_text = """
🌟 派蒙.skill - 原神专用AI游戏伴侣

用法:
  python main.py <command> [args]

命令:
  screenshot
    截取原神游戏窗口截图
    返回截图文件路径

  capture
    截取原神游戏窗口截图（与screenshot相同）

  click <x> <y> [--background]
    在原神窗口指定坐标点击
    x, y 是相对于窗口的坐标
    点击后 0.2 秒自动截取新截图并返回路径
    --background: 使用后台点击模式（不抢鼠标）

  rightclick <x> <y> [--background]
    在原神窗口右键点击指定坐标

  key <按键名>
    在原神窗口按下指定按键
    按键后自动截图
    支持的按键: W, A, S, D, Q, E, R, T, Z, X, C, V, B, N, M
               F, G, H, J, K, L, Y, U, I, O, P, 1-9, 0
               Space, Enter, Escape/Esc, Tab, Shift, Ctrl, Alt
               F1-F8, M, J, C, B, V

  hold <按键名> <按住时间(ms)>
    在原神窗口按住指定按键一段时间(毫秒)
    松开后自动截图

  find <按钮名称> [--threshold <阈值>]
    在原神截图中查找按钮并返回坐标
    找到后可以直接用返回的坐标点击
    --threshold: 匹配阈值（默认 0.8）

  findall
    查找原神截图中所有可识别的按钮

  buttons
    列出原神可用的按钮模板

  click_text <文字描述> [--provider <提供商>] [--dry-run]
    通过文字描述点击原神界面元素（使用多模态AI）
    例如: "确认按钮", "地图按钮", "传送锚点"
    --provider: GUI Agent 提供商 (默认: aliyun)
    --dry-run: 仅分析不执行点击

  windows
    列出所有可见窗口

  config --set-api-key <KEY> [--provider <提供商>]
    配置 GUI Agent API Key

  config --show
    显示当前配置

示例:
  python main.py screenshot
  python main.py find confirm
  python main.py click 540 820
  python main.py key Escape
  python main.py hold W 2000
  python main.py click_text "确认按钮"
"""
    print(help_text)

def create_result(action: str, **kwargs) -> dict:
    """创建标准返回结果"""
    result = {
        'action': action,
        'timestamp': datetime.now().isoformat()
    }
    result.update(kwargs)
    return result

def get_screenshot_dir() -> str:
    """获取截图目录"""
    return os.path.join(os.path.dirname(__file__), 'screenshots')

def handle_screenshot(args):
    try:
        screenshot_path = take_screenshot(GENSHIN_WINDOW_TITLE)
        result = create_result(
            'screenshot',
            windowTitle=GENSHIN_WINDOW_TITLE,
            screenshotPath=screenshot_path
        )
        print(f'📸 {screenshot_path}')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return screenshot_path
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_capture(args):
    """capture 命令与 screenshot 相同"""
    return handle_screenshot(args)

def handle_click(args):
    x = args.x
    y = args.y
    background = args.background if hasattr(args, 'background') else False
    
    try:
        success = click(x, y, GENSHIN_WINDOW_TITLE, background)
        if not success:
            sys.exit(1)
        
        time.sleep(0.2)
        screenshot_path = take_screenshot(GENSHIN_WINDOW_TITLE)
        
        result = create_result(
            'click',
            x=x,
            y=y,
            windowTitle=GENSHIN_WINDOW_TITLE,
            background=background,
            screenshotPath=screenshot_path
        )
        print(f'📸 {screenshot_path}')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return screenshot_path
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_rightclick(args):
    x = args.x
    y = args.y
    background = args.background if hasattr(args, 'background') else False
    
    try:
        success = right_click(x, y, GENSHIN_WINDOW_TITLE, background)
        if not success:
            sys.exit(1)
        
        time.sleep(0.2)
        screenshot_path = take_screenshot(GENSHIN_WINDOW_TITLE)
        
        result = create_result(
            'rightclick',
            x=x,
            y=y,
            windowTitle=GENSHIN_WINDOW_TITLE,
            background=background,
            screenshotPath=screenshot_path
        )
        print(f'📸 {screenshot_path}')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return screenshot_path
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_key(args):
    key_name = args.key
    
    try:
        activate_window(GENSHIN_WINDOW_TITLE)
        time.sleep(0.1)
        
        press_key(key_name, 100)
        
        time.sleep(0.3)
        screenshot_path = take_screenshot(GENSHIN_WINDOW_TITLE)
        
        result = create_result(
            'key',
            key=key_name,
            windowTitle=GENSHIN_WINDOW_TITLE,
            screenshotPath=screenshot_path
        )
        print(f'📸 {screenshot_path}')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return screenshot_path
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_hold(args):
    key_name = args.key
    hold_ms = args.hold_ms
    
    try:
        activate_window(GENSHIN_WINDOW_TITLE)
        time.sleep(0.1)
        
        hold_key(key_name, hold_ms, 200)
        
        time.sleep(0.3)
        screenshot_path = take_screenshot(GENSHIN_WINDOW_TITLE)
        
        result = create_result(
            'hold',
            key=key_name,
            holdMs=hold_ms,
            windowTitle=GENSHIN_WINDOW_TITLE,
            screenshotPath=screenshot_path
        )
        print(f'📸 {screenshot_path}')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return screenshot_path
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_find(args):
    button_name = args.button_name
    threshold = args.threshold if hasattr(args, 'threshold') else 0.8
    
    try:
        win_info = get_window_info(GENSHIN_WINDOW_TITLE)
        game_width = win_info['width'] if win_info else None
        
        screenshot_path = take_screenshot(GENSHIN_WINDOW_TITLE)
        
        screenshot_fullpath = os.path.join(os.path.dirname(__file__), screenshot_path.replace('..\\', '').replace('../', ''))
        screenshot = Image.open(screenshot_fullpath)
        
        result = find_button(screenshot, GAME_ID, button_name, threshold, game_width=game_width)
        
        if result:
            result_data = create_result(
                'find',
                buttonName=button_name,
                windowTitle=GENSHIN_WINDOW_TITLE,
                game=GAME_ID,
                **result,
                screenshotPath=screenshot_path
            )
            print(f'[原神] 找到按钮 "{button_name}": ({result["x"]}, {result["y"]}) 置信度: {result["confidence"]}')
            print(json.dumps(result_data, indent=2, ensure_ascii=False))
        else:
            print(f'[原神] 未找到按钮 "{button_name}"')
            result_data = create_result(
                'find',
                buttonName=button_name,
                windowTitle=GENSHIN_WINDOW_TITLE,
                game=GAME_ID,
                found=False,
                screenshotPath=screenshot_path
            )
            print(json.dumps(result_data, indent=2, ensure_ascii=False))
        
        return result
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_findall(args):
    try:
        win_info = get_window_info(GENSHIN_WINDOW_TITLE)
        game_width = win_info['width'] if win_info else None
        
        screenshot_path = take_screenshot(GENSHIN_WINDOW_TITLE)
        
        screenshot_fullpath = os.path.join(os.path.dirname(__file__), screenshot_path.replace('..\\', '').replace('../', ''))
        screenshot = Image.open(screenshot_fullpath)
        
        results = find_all_buttons(screenshot, GAME_ID, game_width=game_width)
        
        if results:
            print(f'[原神] 找到 {len(results)} 个按钮:')
            for name, info in results.items():
                print(f'  - {name}: ({info["x"]}, {info["y"]}) 置信度: {info["confidence"]}')
        else:
            print(f'[原神] 未找到按钮')
        
        result_data = create_result(
            'findall',
            windowTitle=GENSHIN_WINDOW_TITLE,
            game=GAME_ID,
            buttons=results,
            screenshotPath=screenshot_path
        )
        print(json.dumps(result_data, indent=2, ensure_ascii=False))
        return results
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_buttons(args):
    buttons = list_available_buttons(GAME_ID)
    
    if buttons:
        print(f'[原神] 可用的按钮模板 ({len(buttons)} 个):')
        for btn in buttons:
            print(f'  - {btn}')
    else:
        print(f'[原神] 没有可用的按钮模板')
    
    result_data = create_result('buttons', game=GAME_ID, buttons=buttons)
    print(json.dumps(result_data, indent=2, ensure_ascii=False))
    return buttons

def handle_click_text(args):
    text = args.text
    provider = args.provider if hasattr(args, 'provider') and args.provider else None
    
    try:
        api_key = get_api_key()
        if not api_key:
            print('[ERROR] 未配置 API Key')
            print('请通过以下方式之一配置:')
            print('  1. 设置环境变量: DASHSCOPE_API_KEY')
            print('  2. 编辑 config.json 文件')
            print('  3. 运行: python main.py config --set-api-key YOUR_KEY')
            sys.exit(1)
        
        activate_window(GENSHIN_WINDOW_TITLE)
        time.sleep(0.2)
        
        screenshot_path = take_screenshot(GENSHIN_WINDOW_TITLE)
        screenshot_fullpath = os.path.join(os.path.dirname(__file__), 
                                           screenshot_path.replace('..\\', '').replace('../', ''))
        screenshot = Image.open(screenshot_fullpath)
        
        agent_config = get_gui_agent_config()
        if provider:
            agent_config['provider'] = provider
        
        agent = get_agent(
            provider or agent_config.get('provider', 'aliyun'),
            api_key=api_key,
            base_url=agent_config.get('base_url'),
            model=agent_config.get('model')
        )
        
        print(f'[{agent.name}] 正在分析: "{text}"...')
        
        result = agent.click_element(screenshot, text)
        
        if result.success and result.actions:
            action = result.actions[0]
            x, y = action.x, action.y
            
            if args.dry_run:
                print(f'[DRY-RUN] 将点击坐标 ({x}, {y})')
                result_data = create_result(
                    'click_text',
                    text=text,
                    windowTitle=GENSHIN_WINDOW_TITLE,
                    x=x,
                    y=y,
                    dryRun=True,
                    screenshotPath=screenshot_path
                )
            else:
                win_info = get_window_info(GENSHIN_WINDOW_TITLE)
                
                # 原神需要按住 Alt 键才能用鼠标点击
                key_down('alt')
                
                if win_info:
                    click(x, y, GENSHIN_WINDOW_TITLE, background=False)
                else:
                    import pyautogui
                    pyautogui.click(x, y)
                
                time.sleep(0.1)
                key_up('alt')
                
                time.sleep(0.2)
                after_screenshot_path = take_screenshot(GENSHIN_WINDOW_TITLE)
                
                print(f'[{agent.name}] 已点击 "{text}" 在坐标 ({x}, {y})')
                result_data = create_result(
                    'click_text',
                    text=text,
                    windowTitle=GENSHIN_WINDOW_TITLE,
                    x=x,
                    y=y,
                    provider=agent.provider,
                    model=agent.name,
                    screenshotPath=screenshot_path,
                    afterScreenshotPath=after_screenshot_path
                )
        else:
            print(f'[{agent.name}] 未找到元素 "{text}"')
            if result.error:
                print(f'[ERROR] {result.error}')
            result_data = create_result(
                'click_text',
                text=text,
                windowTitle=GENSHIN_WINDOW_TITLE,
                found=False,
                error=result.error,
                screenshotPath=screenshot_path
            )
        
        print(json.dumps(result_data, indent=2, ensure_ascii=False))
        return result_data
        
    except Exception as e:
        print(f'[ERROR] {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

def handle_config(args):
    if hasattr(args, 'set_api_key') and args.set_api_key:
        from scripts.config import set_api_key
        set_api_key(args.set_api_key, args.provider if hasattr(args, 'provider') else 'aliyun')
        print(f'[config] API Key 已保存')
        return
    
    if hasattr(args, 'show') and args.show:
        from scripts.config import load_config
        config = load_config()
        if 'gui_agent' in config and 'api_key' in config['gui_agent']:
            key = config['gui_agent']['api_key']
            config['gui_agent']['api_key'] = key[:8] + '***' + key[-4:] if len(key) > 12 else '***'
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return
    
    if hasattr(args, 'list_agents') and args.list_agents:
        agents = list_available_agents()
        print('可用的 GUI Agents:')
        for agent in agents:
            print(f'  - {agent}')
        return
    
    print('用法: python main.py config --set-api-key KEY | --show | --list-agents')

def handle_windows(args):
    windows = list_windows()
    for i, win in enumerate(windows, 1):
        print(f'{i}. {win["title"]}')
    
    result = create_result('windows', windows=windows)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return windows

def main():
    parser = argparse.ArgumentParser(description='🌟 派蒙.skill - 原神专用AI游戏伴侣')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # screenshot - 截图
    parser_screenshot = subparsers.add_parser('screenshot', help='截取原神窗口截图')
    
    # capture - 截图（别名）
    parser_capture = subparsers.add_parser('capture', help='截取原神窗口截图')
    
    # click - 点击
    parser_click = subparsers.add_parser('click', help='在原神窗口点击坐标')
    parser_click.add_argument('x', type=int, help='X 坐标')
    parser_click.add_argument('y', type=int, help='Y 坐标')
    parser_click.add_argument('--background', action='store_true', help='后台点击模式')
    
    # rightclick - 右键点击
    parser_rightclick = subparsers.add_parser('rightclick', help='在原神窗口右键点击坐标')
    parser_rightclick.add_argument('x', type=int, help='X 坐标')
    parser_rightclick.add_argument('y', type=int, help='Y 坐标')
    parser_rightclick.add_argument('--background', action='store_true', help='后台点击模式')
    
    # key - 按键
    parser_key = subparsers.add_parser('key', help='在原神窗口按下按键')
    parser_key.add_argument('key', help='按键名称')
    
    # hold - 按住按键
    parser_hold = subparsers.add_parser('hold', help='在原神窗口按住按键')
    parser_hold.add_argument('key', help='按键名称')
    parser_hold.add_argument('hold_ms', type=int, help='按住时间（毫秒）')
    
    # find - 查找按钮
    parser_find = subparsers.add_parser('find', help='在原神截图中查找按钮')
    parser_find.add_argument('button_name', help='按钮名称')
    parser_find.add_argument('--threshold', type=float, default=0.8, help='匹配阈值')
    
    # findall - 查找所有按钮
    parser_findall = subparsers.add_parser('findall', help='查找原神截图中所有按钮')
    
    # buttons - 列出按钮
    parser_buttons = subparsers.add_parser('buttons', help='列出原神可用的按钮模板')
    
    # click_text - 文字点击
    parser_click_text = subparsers.add_parser('click_text', help='通过文字描述点击原神界面元素')
    parser_click_text.add_argument('text', help='按钮文字描述')
    parser_click_text.add_argument('--provider', help='GUI Agent 提供商')
    parser_click_text.add_argument('--dry-run', action='store_true', help='仅分析不执行')
    
    # config - 配置
    parser_config = subparsers.add_parser('config', help='配置管理')
    parser_config.add_argument('--set-api-key', help='设置 API Key')
    parser_config.add_argument('--provider', default='aliyun', help='提供商')
    parser_config.add_argument('--show', action='store_true', help='显示当前配置')
    parser_config.add_argument('--list-agents', action='store_true', help='列出可用的 Agent')
    
    # windows - 列出窗口
    parser_windows = subparsers.add_parser('windows', help='列出所有窗口')
    
    args = parser.parse_args()
    
    if not args.command:
        print_help()
        return
    
    commands = {
        'screenshot': handle_screenshot,
        'capture': handle_capture,
        'click': handle_click,
        'rightclick': handle_rightclick,
        'key': handle_key,
        'hold': handle_hold,
        'find': handle_find,
        'findall': handle_findall,
        'buttons': handle_buttons,
        'click_text': handle_click_text,
        'config': handle_config,
        'windows': handle_windows,
    }
    
    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        print(f'[ERROR] 未知命令: {args.command}')
        print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
