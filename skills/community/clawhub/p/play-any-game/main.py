#!/usr/bin/env python3
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

GAME_ALIASES = {
    '原神': 'genshin-impact',
    'genshin': 'genshin-impact',
    '崩坏：星穹铁道': 'honkai-starrail',
    '星铁': 'honkai-starrail',
    'starrail': 'honkai-starrail',
}

def get_game_id(game_name: str) -> str:
    """获取游戏ID（处理别名）"""
    return GAME_ALIASES.get(game_name, game_name)

def print_help():
    help_text = """
🎮 AI 游戏代肝工具 - CLI (Python 版)

用法:
  python main.py <command> [args]

命令:
  screenshot [窗口标题]
    截取屏幕截图。
    如果指定窗口标题，则截取指定窗口；否则截取主屏幕。
    返回截图文件路径。

  capture <窗口标题>
    截取指定窗口的截图。
    返回截图文件路径。

  click <x> <y> [窗口标题] [--background]
    在指定坐标点击。
    如果提供了窗口标题，则 x, y 是相对于窗口的坐标。
    点击后 0.2 秒自动截取新截图并返回路径。
    --background: 使用后台点击模式（不抢鼠标）

  rightclick <x> <y> [窗口标题] [--background]
    右键点击指定坐标。

  key <按键名> [窗口标题]
    按下指定按键。
    按键后自动截图。
    支持的按键: W, A, S, D, Q, E, R, T, Z, X, C, V, B, N, M
               F, G, H, J, K, L, Y, U, I, O, P, 1-9, 0
               Space, Enter, Escape/Esc, Tab, Shift, Ctrl, Alt
               F1-F8

  hold <按键名> <按住时间(ms)> [窗口标题]
    按住指定按键一段时间(毫秒)。
    松开后自动截图。

  find <按钮名称> <窗口标题> [--game <游戏名>] [--threshold <阈值>]
    在截图中查找按钮并返回坐标。
    找到后可以直接用返回的坐标点击。
    --game: 指定游戏名称（默认根据窗口标题自动识别）
    --threshold: 匹配阈值（默认 0.8）

  findall <窗口标题> [--game <游戏名>]
    查找截图中所有可识别的按钮。

  buttons <游戏名>
    列出游戏可用的按钮模板。

  windows
    列出所有可见窗口。

示例:
  python main.py screenshot
  python main.py capture "原神"
  python main.py find feedback "原神"
  python main.py click 540 820 "原神"
  python main.py key Escape "原神"
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

def load_latest_screenshot(window_title: Optional[str] = None) -> Optional[Image.Image]:
    """加载最新的截图"""
    screenshots_dir = get_screenshot_dir()
    
    if window_title:
        safe_title = window_title.replace(' ', '_').replace(':', '_')
        for c in '<>"\\/|?*':
            safe_title = safe_title.replace(c, '_')
        game_dir = os.path.join(screenss_dir, safe_title)
        if os.path.exists(game_dir):
            screenshots_dir = game_dir
    
    if not os.path.exists(screenshots_dir):
        return None
    
    files = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
    if not files:
        return None
    
    files.sort(reverse=True)
    latest = os.path.join(screenshots_dir, files[0])
    return Image.open(latest)

def handle_screenshot(args):
    window_title = args.window_title if hasattr(args, 'window_title') and args.window_title else None
    
    try:
        screenshot_path = take_screenshot(window_title)
        result = create_result(
            'screenshot',
            windowTitle=window_title,
            screenshotPath=screenshot_path
        )
        print(f'📸 {screenshot_path}')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return screenshot_path
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_capture(args):
    window_title = args.window_title
    if not window_title:
        print('[ERROR] 请指定窗口标题')
        sys.exit(1)
    
    try:
        screenshot_path = take_screenshot(window_title)
        result = create_result(
            'capture',
            windowTitle=window_title,
            screenshotPath=screenshot_path
        )
        print(f'📸 {screenshot_path}')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return screenshot_path
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_click(args):
    x = args.x
    y = args.y
    window_title = args.window_title if hasattr(args, 'window_title') and args.window_title else None
    background = args.background if hasattr(args, 'background') else False
    
    try:
        success = click(x, y, window_title, background)
        if not success:
            sys.exit(1)
        
        time.sleep(0.2)
        screenshot_path = take_screenshot(window_title)
        
        result = create_result(
            'click',
            x=x,
            y=y,
            windowTitle=window_title,
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
    window_title = args.window_title if hasattr(args, 'window_title') and args.window_title else None
    background = args.background if hasattr(args, 'background') else False
    
    try:
        success = right_click(x, y, window_title, background)
        if not success:
            sys.exit(1)
        
        time.sleep(0.2)
        screenshot_path = take_screenshot(window_title)
        
        result = create_result(
            'rightclick',
            x=x,
            y=y,
            windowTitle=window_title,
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
    window_title = args.window_title if hasattr(args, 'window_title') and args.window_title else None
    
    try:
        if window_title:
            activate_window(window_title)
            time.sleep(0.1)
        
        press_key(key_name, 100)
        
        time.sleep(0.3)
        screenshot_path = take_screenshot(window_title)
        
        result = create_result(
            'key',
            key=key_name,
            windowTitle=window_title,
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
    window_title = args.window_title if hasattr(args, 'window_title') and args.window_title else None
    
    try:
        if window_title:
            activate_window(window_title)
            time.sleep(0.1)
        
        hold_key(key_name, hold_ms, 200)
        
        time.sleep(0.3)
        screenshot_path = take_screenshot(window_title)
        
        result = create_result(
            'hold',
            key=key_name,
            holdMs=hold_ms,
            windowTitle=window_title,
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
    window_title = args.window_title
    game_name = args.game if hasattr(args, 'game') and args.game else get_game_id(window_title)
    threshold = args.threshold if hasattr(args, 'threshold') else 0.8
    
    try:
        game_width = None
        if window_title:
            win_info = get_window_info(window_title)
            if win_info:
                game_width = win_info['width']
        
        screenshot_path = take_screenshot(window_title)
        
        screenshot_fullpath = os.path.join(os.path.dirname(__file__), screenshot_path.replace('..\\', '').replace('../', ''))
        screenshot = Image.open(screenshot_fullpath)
        
        result = find_button(screenshot, game_name, button_name, threshold, game_width=game_width)
        
        if result:
            result_data = create_result(
                'find',
                buttonName=button_name,
                windowTitle=window_title,
                game=game_name,
                **result,
                screenshotPath=screenshot_path
            )
            print(f'[{game_name}] Found button "{button_name}": ({result["x"]}, {result["y"]}) confidence: {result["confidence"]}')
            print(json.dumps(result_data, indent=2, ensure_ascii=False))
        else:
            print(f'[{game_name}] Button "{button_name}" not found')
            result_data = create_result(
                'find',
                buttonName=button_name,
                windowTitle=window_title,
                game=game_name,
                found=False,
                screenshotPath=screenshot_path
            )
            print(json.dumps(result_data, indent=2, ensure_ascii=False))
        
        return result
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_findall(args):
    window_title = args.window_title
    game_name = args.game if hasattr(args, 'game') and args.game else get_game_id(window_title)
    
    try:
        game_width = None
        if window_title:
            win_info = get_window_info(window_title)
            if win_info:
                game_width = win_info['width']
        
        screenshot_path = take_screenshot(window_title)
        
        screenshot_fullpath = os.path.join(os.path.dirname(__file__), screenshot_path.replace('..\\', '').replace('../', ''))
        screenshot = Image.open(screenshot_fullpath)
        
        results = find_all_buttons(screenshot, game_name, game_width=game_width)
        
        if results:
            print(f'[{game_name}] Found {len(results)} buttons:')
            for name, info in results.items():
                print(f'  - {name}: ({info["x"]}, {info["y"]}) confidence: {info["confidence"]}')
        else:
            print(f'[{game_name}] No buttons found')
        
        result_data = create_result(
            'findall',
            windowTitle=window_title,
            game=game_name,
            buttons=results,
            screenshotPath=screenshot_path
        )
        print(json.dumps(result_data, indent=2, ensure_ascii=False))
        return results
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

def handle_buttons(args):
    game_name = get_game_id(args.game_name)
    
    buttons = list_available_buttons(game_name)
    
    if buttons:
        print(f'[{game_name}] Available button templates:')
        for btn in buttons:
            print(f'  - {btn}')
    else:
        print(f'[{game_name}] No button templates available')
    
    result_data = create_result('buttons', game=game_name, buttons=buttons)
    print(json.dumps(result_data, indent=2, ensure_ascii=False))
    return buttons

def handle_click_text(args):
    text = args.text
    window_title = args.window_title
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
        
        if window_title:
            activate_window(window_title)
            time.sleep(0.2)
        
        screenshot_path = take_screenshot(window_title)
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
        
        print(f'[{agent.name}] Analyzing: "{text}"...')
        
        result = agent.click_element(screenshot, text)
        
        if result.success and result.actions:
            action = result.actions[0]
            x, y = action.x, action.y
            
            if args.dry_run:
                print(f'[DRY-RUN] Would click at ({x}, {y})')
                result_data = create_result(
                    'click_text',
                    text=text,
                    windowTitle=window_title,
                    x=x,
                    y=y,
                    dryRun=True,
                    screenshotPath=screenshot_path
                )
            else:
                win_info = get_window_info(window_title) if window_title else None
                
                is_genshin = window_title and ('原神' in window_title or 'genshin' in window_title.lower())
                
                if is_genshin:
                    key_down('alt')
                
                if win_info:
                    click(x, y, window_title, background=False)
                else:
                    import pyautogui
                    pyautogui.click(x, y)
                
                if is_genshin:
                    time.sleep(0.1)
                    key_up('alt')
                
                time.sleep(0.2)
                after_screenshot_path = take_screenshot(window_title)
                
                print(f'[{agent.name}] Clicked "{text}" at ({x}, {y})')
                result_data = create_result(
                    'click_text',
                    text=text,
                    windowTitle=window_title,
                    x=x,
                    y=y,
                    provider=agent.provider,
                    model=agent.name,
                    screenshotPath=screenshot_path,
                    afterScreenshotPath=after_screenshot_path
                )
        else:
            print(f'[{agent.name}] Element "{text}" not found')
            if result.error:
                print(f'[ERROR] {result.error}')
            result_data = create_result(
                'click_text',
                text=text,
                windowTitle=window_title,
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
        print(f'[config] API Key saved')
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
        print('Available GUI Agents:')
        for agent in agents:
            print(f'  - {agent}')
        return
    
    print('Usage: python main.py config --set-api-key KEY | --show | --list-agents')

def handle_windows(args):
    windows = list_windows()
    for i, win in enumerate(windows, 1):
        print(f'{i}. {win["title"]}')
    
    result = create_result('windows', windows=windows)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return windows

def load_games_config() -> dict:
    """加载游戏配置"""
    config_path = os.path.join(os.path.dirname(__file__), 'games', 'games.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'games': {}, 'default': {}}

def find_game_by_keyword(keyword: str) -> Optional[str]:
    """通过关键词查找游戏ID"""
    config = load_games_config()
    keyword_lower = keyword.lower()
    
    for game_id, game_info in config.get('games', {}).items():
        if keyword_lower == game_id.lower():
            return game_id
        if keyword_lower == game_info.get('name', '').lower():
            return game_id
        if keyword_lower == game_info.get('nameEn', '').lower():
            return game_id
        for kw in game_info.get('keywords', []):
            if keyword_lower == kw.lower():
                return game_id
    
    return None

def handle_game(args):
    """处理游戏相关命令"""
    subcommand = args.subcommand
    
    config = load_games_config()
    
    if subcommand == 'list':
        games = config.get('games', {})
        print('Supported games:')
        for game_id, game_info in games.items():
            print(f'  - {game_id}: {game_info.get("name", game_id)} ({game_info.get("character", "Unknown")})')
        
        result = create_result(
            'game',
            subaction='list',
            games={gid: {'name': g.get('name'), 'character': g.get('character')} for gid, g in games.items()}
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    
    elif subcommand == 'start':
        game_name = args.game_name
        game_id = find_game_by_keyword(game_name)
        
        if not game_id:
            print(f'[ERROR] Unknown game: {game_name}')
            print('Use "python main.py game list" to see supported games')
            sys.exit(1)
        
        game_info = config['games'][game_id]
        soul_path = game_info.get('soulPath', f'games/{game_id}/SOUL.md')
        
        print(f'[game] Starting: {game_info.get("name", game_id)}')
        print(f'[game] Character: {game_info.get("character", "Unknown")}')
        print(f'[game] SOUL: {soul_path}')
        
        result = create_result(
            'game',
            subaction='start',
            gameId=game_id,
            gameName=game_info.get('name', game_id),
            character=game_info.get('character'),
            windowTitle=game_info.get('windowTitle'),
            soulPath=soul_path
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    
    elif subcommand == 'end':
        default_info = config.get('default', {})
        soul_path = default_info.get('soulPath', 'games/default/SOUL.md')
        
        print(f'[game] Ending game session')
        print(f'[game] Restoring default SOUL: {soul_path}')
        
        result = create_result(
            'game',
            subaction='end',
            soulPath=soul_path,
            character=default_info.get('character', 'OpenClaw')
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    
    elif subcommand == 'current':
        print('[game] Current game session info:')
        print('  Note: Game session state is managed by OpenClaw')
        print('  This command returns available games for reference')
        
        games = config.get('games', {})
        result = create_result(
            'game',
            subaction='current',
            games=list(games.keys())
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    
    else:
        print(f'[ERROR] Unknown game subcommand: {subcommand}')
        print('Usage: python main.py game <list|start|end|current>')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='🎮 AI 游戏代肝工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    parser_screenshot = subparsers.add_parser('screenshot', help='截取屏幕截图')
    parser_screenshot.add_argument('window_title', nargs='?', help='窗口标题（可选）')
    
    parser_capture = subparsers.add_parser('capture', help='截取指定窗口')
    parser_capture.add_argument('window_title', help='窗口标题')
    
    parser_click = subparsers.add_parser('click', help='点击坐标')
    parser_click.add_argument('x', type=int, help='X 坐标')
    parser_click.add_argument('y', type=int, help='Y 坐标')
    parser_click.add_argument('window_title', nargs='?', help='窗口标题（可选）')
    parser_click.add_argument('--background', action='store_true', help='后台点击模式')
    
    parser_rightclick = subparsers.add_parser('rightclick', help='右键点击坐标')
    parser_rightclick.add_argument('x', type=int, help='X 坐标')
    parser_rightclick.add_argument('y', type=int, help='Y 坐标')
    parser_rightclick.add_argument('window_title', nargs='?', help='窗口标题（可选）')
    parser_rightclick.add_argument('--background', action='store_true', help='后台点击模式')
    
    parser_key = subparsers.add_parser('key', help='按下按键')
    parser_key.add_argument('key', help='按键名称')
    parser_key.add_argument('window_title', nargs='?', help='窗口标题（可选）')
    
    parser_hold = subparsers.add_parser('hold', help='按住按键')
    parser_hold.add_argument('key', help='按键名称')
    parser_hold.add_argument('hold_ms', type=int, help='按住时间（毫秒）')
    parser_hold.add_argument('window_title', nargs='?', help='窗口标题（可选）')
    
    parser_find = subparsers.add_parser('find', help='查找按钮')
    parser_find.add_argument('button_name', help='按钮名称')
    parser_find.add_argument('window_title', help='窗口标题')
    parser_find.add_argument('--game', help='游戏名称')
    parser_find.add_argument('--threshold', type=float, default=0.8, help='匹配阈值')
    
    parser_findall = subparsers.add_parser('findall', help='查找所有按钮')
    parser_findall.add_argument('window_title', help='窗口标题')
    parser_findall.add_argument('--game', help='游戏名称')
    
    parser_buttons = subparsers.add_parser('buttons', help='列出可用按钮')
    parser_buttons.add_argument('game_name', help='游戏名称')
    
    parser_click_text = subparsers.add_parser('click_text', help='通过文字描述点击按钮')
    parser_click_text.add_argument('text', help='按钮文字描述')
    parser_click_text.add_argument('window_title', nargs='?', help='窗口标题（可选）')
    parser_click_text.add_argument('--provider', help='GUI Agent 提供商')
    parser_click_text.add_argument('--dry-run', action='store_true', help='仅分析不执行')
    
    parser_config = subparsers.add_parser('config', help='配置管理')
    parser_config.add_argument('--set-api-key', help='设置 API Key')
    parser_config.add_argument('--provider', default='aliyun', help='提供商')
    parser_config.add_argument('--show', action='store_true', help='显示当前配置')
    parser_config.add_argument('--list-agents', action='store_true', help='列出可用的 Agent')
    
    parser_windows = subparsers.add_parser('windows', help='列出所有窗口')
    
    parser_game = subparsers.add_parser('game', help='游戏会话管理')
    game_subparsers = parser_game.add_subparsers(dest='subcommand', help='子命令')
    
    parser_game_list = game_subparsers.add_parser('list', help='列出支持的游戏')
    parser_game_start = game_subparsers.add_parser('start', help='开始游戏会话')
    parser_game_start.add_argument('game_name', help='游戏名称或ID')
    parser_game_end = game_subparsers.add_parser('end', help='结束游戏会话')
    parser_game_current = game_subparsers.add_parser('current', help='显示当前游戏')
    
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
        'game': handle_game,
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
