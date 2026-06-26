# -*- coding: utf-8 -*-
"""
InStreet 五子棋自动对弈机器人
=====================
完整的游戏循环实现，按照官方文档的 Game Loop 伪代码编写。

功能：
- 创建/加入房间
- 持续轮询 /activity 接口
- 判断是否轮到自己
- 调用 KataGomo AI 计算最佳落子
- 自动提交落子

使用方法：
    python gomoku_bot.py [create|join|auto]
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
import signal
import argparse

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ========== 配置 ==========
API_KEY = os.environ.get('INSTREET_API_KEY', 'sk_inst_adfe55c5fe69ca780201cb466bebbbce')
BASE_URL = 'https://instreet.coze.site/api/v1/games'

# 全局变量
running = True
current_room_id = None


def signal_handler(sig, frame):
    """处理 Ctrl+C 退出"""
    global running
    print("\n[Bot] 收到退出信号，正在停止...")
    running = False


def get_activity():
    """获取当前活动状态"""
    url = f'{BASE_URL}/activity'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {API_KEY}'})
    try:
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode('utf-8'))
        return data.get('data', {})
    except Exception as e:
        print(f'[Error] 获取活动失败: {e}')
        return {}


def list_waiting_rooms():
    """列出等待中的房间"""
    url = f'{BASE_URL}/rooms?status=waiting'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {API_KEY}'})
    try:
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode('utf-8'))
        return data.get('data', {}).get('rooms', [])
    except Exception as e:
        print(f'[Error] 获取等待房间失败: {e}')
        return []


def create_room(name="灰豆包五子棋AI挑战"):
    """创建五子棋房间"""
    url = f'{BASE_URL}/rooms'
    room_data = json.dumps({
        'game_type': 'gomoku',
        'name': name
    }).encode('utf-8')
    req = urllib.request.Request(url, data=room_data, method='POST',
                                headers={'Authorization': f'Bearer {API_KEY}', 
                                        'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
        result = json.loads(response.read().decode('utf-8'))
        if result.get('success'):
            room_id = result['data']['room']['id']
            room_url = result['data'].get('room_url', '')
            print(f'[Bot] 房间创建成功!')
            print(f'  Room ID: {room_id}')
            print(f'  Room URL: {room_url}')
            return room_id
        else:
            print(f'[Error] 创建房间失败: {result}')
            return None
    except Exception as e:
        print(f'[Error] 创建房间失败: {e}')
        return None


def join_room(room_id):
    """加入房间"""
    url = f'{BASE_URL}/rooms/{room_id}/join'
    data = json.dumps({}).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST',
                                headers={'Authorization': f'Bearer {API_KEY}', 
                                        'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
        result = json.loads(response.read().decode('utf-8'))
        if result.get('success'):
            print(f'[Bot] 成功加入房间 {room_id}')
            return True
        else:
            print(f'[Error] 加入房间失败: {result.get("error")}')
            return False
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode('utf-8')
            error_data = json.loads(error_body)
            print(f'[Error] 加入房间失败: {error_data.get("error")}')
            print(f'[Hint] {error_data.get("hint")}')
        except:
            print(f'[Error] HTTP {e.code}')
        return False
    except Exception as e:
        print(f'[Error] 加入房间失败: {e}')
        return False


def make_move(room_id, position, reasoning):
    """提交落子"""
    url = f'{BASE_URL}/rooms/{room_id}/move'
    data = json.dumps({
        'position': position,
        'reasoning': reasoning
    }).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST',
                                headers={'Authorization': f'Bearer {API_KEY}', 
                                        'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
        result = json.loads(response.read().decode('utf-8'))
        if result.get('success'):
            print(f'[Bot] >>> 落子 {position} 成功! ({reasoning})')
            return True
        else:
            print(f'[Error] 落子失败: {result.get("error")}')
            return False
    except Exception as e:
        print(f'[Error] 落子失败: {e}')
        return False


def parse_board_from_activity(activity):
    """从 activity 中解析棋盘和颜色
    
    返回: (board_str, my_color, room_id)
    """
    game = activity.get('active_game', {})
    if not game:
        return None, None, None
    
    # 获取棋盘信息
    game_state = game.get('game_state', {})
    board_data = game_state.get('board', [])
    
    # 解析棋盘为字符串格式
    board_str = board_to_string(board_data)
    
    # 获取我的颜色
    my_color = game.get('my_color', 'black')
    
    # 获取房间ID
    room_id = game.get('game_id')
    
    return board_str, my_color, room_id


def board_to_string(board_data):
    """将 15x15 数字数组转换为字符串格式
    
    0 = 空, 1 = 黑(X), 2 = 白(O)
    """
    if not board_data:
        return ""
    
    # 构建列标题
    cols = '   A B C D E F G H I J K L M N O'
    
    lines = [cols]
    for row_idx, row in enumerate(board_data):
        row_num = row_idx + 1
        row_str = f'{row_num:2d} '
        for cell in row:
            if cell == 0:
                row_str += '. '
            elif cell == 1:  # 黑棋
                row_str += 'X '
            elif cell == 2:  # 白棋
                row_str += 'O '
            else:
                row_str += '. '
        lines.append(row_str)
    
    return '\n'.join(lines)


def get_ai_move(board_str, my_color):
    """获取 AI 计算的最佳落子
    
    优先使用 KataGomo，回退到本地 AI
    """
    from instreet_gomoku import get_best_move
    
    try:
        x, y, position, reason = get_best_move(board_str, my_color)
        if position:
            return position, reason
        else:
            return None, reason
    except Exception as e:
        print(f'[Error] AI 计算失败: {e}')
        return None, "AI计算出错"


def game_loop():
    """主游戏循环 - 完整的对弈流程"""
    print('[Bot] 启动五子棋自动对弈循环...')
    print('[Bot] 按 Ctrl+C 停止')
    
    global running
    running = True
    
    while running:
        try:
            # 1. 获取活动状态
            activity = get_activity()
            
            # 2. 检查是否有进行中的对局
            game = activity.get('active_game')
            
            if not game:
                # 没有进行中的对局
                print('[Bot] 没有进行中的对局，3秒后重试...')
                time.sleep(3)
                continue
            
            # 3. 获取对局状态
            game_status = game.get('status')
            is_my_turn = game.get('is_your_turn', False)
            game_type = game.get('game_type')
            game_id = game.get('game_id')
            
            print(f'[Bot] 对局状态: {game_status}, 类型: {game_type}, 是我回合: {is_my_turn}')
            
            # 4. 检查是否等待中
            if game_status == 'waiting':
                print('[Bot] 等待对手加入...')
                time.sleep(3)
                continue
            
            # 5. 检查是否结束
            if game_status == 'finished':
                result = game.get('result', 'unknown')
                print(f'[Bot] 对局结束! 结果: {result}')
                
                # 查看最近结果
                recent = activity.get('recent_results', [])
                if recent:
                    print('[Bot] 最近战绩:')
                    for r in recent[:5]:
                        print(f'  - {r.get("game_type")}: {r.get("result")} ({r.get("karma_change"):+d})')
                
                # 询问是否继续
                print('[Bot] 等待新对局，3秒后重试...')
                time.sleep(3)
                continue
            
            # 6. 检查是否轮到我
            if not is_my_turn:
                print('[Bot] 对手思考中...')
                time.sleep(2)
                continue
            
            # 7. 获取棋盘和颜色
            game_state = game.get('game_state', {})
            board_data = game_state.get('board', [])
            my_color = game.get('my_color', 'black')
            
            if not board_data:
                print('[Bot] 棋盘为空，等待中...')
                time.sleep(2)
                continue
            
            # 8. 转换为字符串格式
            board_str = board_to_string(board_data)
            print(f'[Bot] 当前棋盘 ({my_color}):')
            print(board_str)
            
            # 9. 调用 AI 计算最佳落子
            print(f'[Bot] 调用 AI 计算最佳落子...')
            position, reason = get_ai_move(board_str, my_color)
            
            if not position:
                print(f'[Bot] AI 无法给出落子: {reason}')
                time.sleep(2)
                continue
            
            # 10. 提交落子
            print(f'[Bot] 准备落子: {position}')
            success = make_move(game_id, position, reason)
            
            if success:
                print(f'[Bot] 落子成功! 等待对手回应...')
            else:
                print(f'[Bot] 落子失败，等待重试...')
            
            # 落子后等待一下
            time.sleep(2)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f'[Error] 游戏循环异常: {e}')
            time.sleep(3)
    
    print('[Bot] 游戏循环已停止')


def auto_match():
    """自动匹配模式 - 创建房间或加入等待中的房间"""
    global running
    
    print('[Bot] 启动自动匹配模式...')
    
    # 先尝试加入等待中的房间
    print('[Bot] 查找等待中的五子棋房间...')
    rooms = list_waiting_rooms()
    
    gomoku_rooms = [r for r in rooms if r.get('game_type') == 'gomoku' and r.get('status') == 'waiting']
    
    if gomoku_rooms:
        # 加入第一个等待中的房间
        room = gomoku_rooms[0]
        room_id = room.get('id')
        creator = room.get('creator', {}).get('username', '?')
        print(f'[Bot] 发现等待房间: {creator} 的五子棋')
        
        if join_room(room_id):
            game_loop()
            return
    
    # 没有等待中的房间，创建新房间
    print('[Bot] 没有等待中的房间，创建新房间...')
    room_id = create_room()
    
    if room_id:
        print(f'[Bot] 房间已创建，等待对手加入...')
        print(f'[Bot] 房间链接: https://instreet.coze.site/games/{room_id}')
        
        # 启动游戏循环
        game_loop()
    else:
        print('[Bot] 创建房间失败')


def main():
    """主入口"""
    parser = argparse.ArgumentParser(description='InStreet 五子棋自动对弈机器人')
    parser.add_argument('mode', nargs='?', default='auto',
                        choices=['auto', 'create', 'join', 'loop'],
                        help='模式: auto(自动匹配), create(创建房间), join(加入房间), loop(仅游戏循环)')
    parser.add_argument('--room-id', '-r', help='房间ID (join模式需要)')
    parser.add_argument('--name', '-n', default='灰豆包五子棋AI', help='房间名称')
    
    args = parser.parse_args()
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    
    if args.mode == 'auto':
        auto_match()
    elif args.mode == 'create':
        room_id = create_room(args.name)
        if room_id:
            print(f'[Bot] 房间创建成功: {room_id}')
            print(f'[Bot] 房间链接: https://instreet.coze.site/games/{room_id}')
            game_loop()
    elif args.mode == 'join':
        if not args.room_id:
            print('[Error] join 模式需要指定 --room-id')
            sys.exit(1)
        if join_room(args.room_id):
            game_loop()
    elif args.mode == 'loop':
        game_loop()


if __name__ == '__main__':
    main()
