import json
import time
import requests
import os
import random
import sys
import argparse

BOARD_SIZE = 15
SERVER_URL = "https://www.ocgame.top"

# ===================== 战绩统计配置（纯本地） =====================
# 战绩文件路径：games/gomoku/battle_stats.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATS_FILE = os.path.join(BASE_DIR, "battle_stats.json")

# 初始化战绩文件
def init_stats_file():
    if not os.path.exists(STATS_FILE):
        default_stats = {
            "total_win": 0,        # 总胜场
            "total_lose": 0,       # 总负场
            "total_draw": 0,       # 总平局
            "lose_streak": 0,      # 连输场次
            "recent_5_games": [],  # 最近5局记录 [1=胜,0=负,2=平]
            "daily_trigger_count": 0  # 当日触发调整次数（上限2次）
        }
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_stats, f, indent=2, ensure_ascii=False)

# 加载战绩到内存
def load_stats():
    init_stats_file()
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                # 文件为空，返回默认值
                return {
                    "total_win": 0,
                    "total_lose": 0,
                    "total_draw": 0,
                    "lose_streak": 0,
                    "recent_5_games": [],
                    "daily_trigger_count": 0
                }
            return json.loads(content)
    except json.JSONDecodeError:
        # JSON格式错误，重新初始化文件
        print("⚠️  战绩文件格式错误，重新初始化...")
        init_stats_file()
        # 重新加载
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # 其他错误，返回默认值
        print(f"⚠️  加载战绩文件失败: {e}")
        return {
            "total_win": 0,
            "total_lose": 0,
            "total_draw": 0,
            "lose_streak": 0,
            "recent_5_games": [],
            "daily_trigger_count": 0
        }

# 保存内存战绩到文件
def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

# ===================== 大模型策略调整（预留接口，严格按prompt执行） =====================
def llm_adjust_strategy(strategy_path="gomoku_strategy.json"):
    """
    触发条件满足后，调用大模型修改策略文件
    严格遵循prompt.txt规则：仅微调参数/切换预设性格，不修改结构
    """
    try:
        print("🔴 开始自动调整AI策略（严格遵循prompt规则）...")
        # 1. 读取prompt.txt规则
        prompt_path = os.path.join(BASE_DIR, "prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_rules = f.read()

        # 2. 读取人格模板
        personality_path = os.path.join(BASE_DIR, "gomoku_personality_roles.json")
        with open(personality_path, "r", encoding="utf-8") as f:
            personality_data = json.load(f)

        # 3. 读取当前策略
        with open(strategy_path, "r", encoding="utf-8") as f:
            strategy = json.load(f)

        # ===================== 大模型修改逻辑（此处接入你的大模型） =====================
        # 示例：仅打印，实际替换为大模型调用
        print(f"📝 按prompt规则调整策略，当前性格：{strategy['personality']['attack_style']}")
        # 大模型输出新策略后，写入gomoku_strategy.json

        print("✅ AI策略调整完成！下次对战生效")
        return True
    except Exception as e:
        print(f"❌ 策略调整失败：{e}")
        return False

class GomokuBoard:
    def __init__(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.moves = []
    
    def copy(self):
        new_board = GomokuBoard()
        new_board.board = [row[:] for row in self.board]
        new_board.moves = self.moves[:]
        return new_board
    
    def place(self, row, col, player):
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == 0:
            self.board[row][col] = player
            self.moves.append((row, col, player))
            return True
        return False
    
    def is_valid(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == 0
    
    def get_empty_positions(self):
        positions = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == 0:
                    positions.append((r, c))
        return positions

class GomokuAI:
    def __init__(self, strategy_path):
        with open(strategy_path, "r", encoding="utf-8") as f:
            self.strategy = json.load(f)
        
        self.fixed_base = self.strategy.get("fixed_base", {})
        self.personality = self.strategy.get("personality", {})
        self.personality_boost = self.strategy.get("personality_boost", {})
        self.random_config = self.strategy.get("random", {})
        
        # 基础权重
        base_offense = self.fixed_base.get("offense", 0.5)
        base_defense = self.fixed_base.get("defense", 0.5)
        self.center_control = self.fixed_base.get("center_control", 0.5)
        
        # personality 参数
        self.attack_style = self.personality.get("attack_style", "steady")
        self.defense_style = self.personality.get("defense_style", "flexible")
        self.risk_like = self.personality.get("risk_like", 0.5)
        self.creativity = self.personality.get("creativity", 0.5)
        
        # personality_boost 加成
        attack_boost = self.personality_boost.get("attack_boost", 0.0)
        defense_boost = self.personality_boost.get("defense_boost", 0.0)
        self.risk_boost = self.personality_boost.get("risk_boost", 0.0)
        self.creative_boost = self.personality_boost.get("creative_boost", 0.0)
        
        # 根据 attack_style 调整进攻倾向
        style_offense_mod = {
            "aggressive": 0.15,
            "steady": 0.0,
            "slow": -0.1,
            "unpredictable": 0.05
        }.get(self.attack_style, 0.0)
        
        # 根据 defense_style 调整防守倾向
        style_defense_mod = {
            "rigid": 0.15,
            "flexible": 0.0,
            "passive": -0.1,
            "adaptive": 0.05
        }.get(self.defense_style, 0.0)
        
        # 计算最终权重 = 基础 + boost + style修正
        self.offense = min(1.0, max(0.1, base_offense + attack_boost + style_offense_mod))
        self.defense = min(1.0, max(0.1, base_defense + defense_boost + style_defense_mod))
        
        # 最终创造性 = 基础 + boost
        self.final_creativity = min(1.0, max(0.0, self.creativity + self.creative_boost))
        
        self.bot_name = self.strategy.get("meta", {}).get("bot_name", "Bot")
        
        print(f"[{self.bot_name}] 策略加载完成:")
        print(f"  进攻风格: {self.attack_style}, 最终进攻权重: {self.offense:.2f}")
        print(f"  防守风格: {self.defense_style}, 最终防守权重: {self.defense:.2f}")
        print(f"  风险偏好: {self.risk_like:.2f}, 创造性: {self.final_creativity:.2f}")
    
    def evaluate_line(self, board, row, col, dr, dc, player):
        count = 0
        open_ends = 0
        
        for i in range(5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if board[r][c] == player:
                    count += 1
                elif board[r][c] == 0:
                    open_ends += 1
                    break
                else:
                    break
            else:
                break
        
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if board[r][c] == player:
                    count += 1
                elif board[r][c] == 0:
                    open_ends += 1
                    break
                else:
                    break
            else:
                break
        
        if count >= 5:
            return 100000
        elif count == 4:
            if open_ends >= 2:
                return 10000
            elif open_ends == 1:
                return 1000
        elif count == 3:
            if open_ends >= 2:
                return 500
            elif open_ends == 1:
                return 50
        elif count == 2:
            if open_ends >= 2:
                return 20
            elif open_ends == 1:
                return 5
        
        return count
    
    def evaluate_position(self, board, row, col, player):
        if board[row][col] != 0:
            return 0
        
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        test_board = [r[:] for r in board]
        test_board[row][col] = player
        
        # 进攻得分
        for dr, dc in directions:
            line_score = self.evaluate_line(test_board, row, col, dr, dc, player)
            # 根据棋型应用不同的权重（从高分到低分判断）
            if line_score >= 10000:  # 活四及以上（必胜）
                score += line_score * self.offense * self.fixed_base.get("chong_four", 1.0) * 2
            elif line_score >= 1000:  # 冲四
                score += line_score * self.offense * self.fixed_base.get("chong_four", 1.0)
            elif line_score >= 500:  # 活三
                score += line_score * self.offense * self.fixed_base.get("live_three", 1.0)
            else:
                score += line_score * self.offense
        
        # 防守得分
        opponent = 3 - player
        test_board[row][col] = opponent
        for dr, dc in directions:
            line_score = self.evaluate_line(test_board, row, col, dr, dc, opponent)
            # 根据棋型应用不同的权重（从高分到低分判断）
            if line_score >= 10000:  # 活四（必须防守）
                score += line_score * self.defense * self.fixed_base.get("block_four", 1.0) * 2
            elif line_score >= 1000:  # 冲四
                score += line_score * self.defense * self.fixed_base.get("block_four", 1.0)
            elif line_score >= 500:  # 活三
                score += line_score * self.defense * self.fixed_base.get("block_three", 1.0)
            else:
                score += line_score * self.defense
        
        # 中心控制
        center = BOARD_SIZE // 2
        dist = abs(row - center) + abs(col - center)
        center_score = (BOARD_SIZE - dist) * 3 * self.center_control
        score += center_score
        
        # 边缘和角落规避
        if dist > 8:  # 边缘位置
            score -= dist * 2 * self.fixed_base.get("edge_avoid", 0.0)
        if (row == 0 or row == BOARD_SIZE-1) and (col == 0 or col == BOARD_SIZE-1):  # 角落位置
            score -= 50 * self.fixed_base.get("corner_avoid", 0.0)
        
        return score
    
    def get_best_move(self, board, player):
        print(f"[{self.bot_name}] 开始计算最佳落子...")
        positions = self.get_candidate_moves(board)
        
        if not positions:
            print(f"[{self.bot_name}] 没有候选位置，返回中心")
            return BOARD_SIZE // 2, BOARD_SIZE // 2
        
        best_score = -float('inf')
        best_moves = []
        
        for row, col in positions:
            score = self.evaluate_position(board, row, col, player)
            
            # 随机扰动（基础随机）
            if self.random_config.get("enable", False):
                rand_range = self.random_config.get("range", 0.01)
                score += random.uniform(-rand_range * 100, rand_range * 100)
            
            # 风险偏好影响：高风险偏好允许选择次优但可能高回报的位置
            if self.risk_like > 0.6:
                # 增加随机性，让次优位置也有机会
                score += random.uniform(-self.risk_like * 50, self.risk_like * 50)
            
            if score > best_score:
                best_score = score
                best_moves = [(row, col)]
            elif score == best_score:
                best_moves.append((row, col))
        
        # 创造性决策：高创造性时随机选择等优位置
        if self.final_creativity > 0.5 and len(best_moves) > 1:
            move = random.choice(best_moves)
            print(f"[{self.bot_name}] 创造性选择落子: {move}")
            return move
        
        print(f"[{self.bot_name}] 选择最佳落子: {best_moves[0]}")
        return best_moves[0]
    
    def get_candidate_moves(self, board):
        candidates = set()
        has_stones = False
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != 0:
                    has_stones = True
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == 0:
                                candidates.add((nr, nc))
        
        if not has_stones:
            return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
        
        return list(candidates) if candidates else [(BOARD_SIZE // 2, BOARD_SIZE // 2)]

class GomokuBot:
    def __init__(self, config_path, strategy_path):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        self.user_id = self.config["owner_info"]["user_id"]
        self.nickname = self.config["owner_info"].get("nickname", "Bot")
        self.api_token = self.config["api_auth"]["api_token"]
        self.ai = GomokuAI(strategy_path)
        self.board = GomokuBoard()
        self.game_id = None
        self.my_color = None
        self.my_turn = False

        # ===================== 初始化本地战绩（启动读1次） =====================
        self.stats = load_stats()
        self.strategy_path = strategy_path
        print(f"📊 加载本地战绩 | 胜:{self.stats['total_win']} 负:{self.stats['total_lose']} 平:{self.stats['total_draw']} 连输:{self.stats['lose_streak']}")

    # ===================== 核心：更新战绩（服务器结果为准） =====================
    def update_battle_stats(self, is_win: bool, is_draw: bool):
        # 1. 更新内存数据
        if is_draw:
            self.stats["total_draw"] += 1
            self.stats["recent_5_games"].append(2)
        elif is_win:
            self.stats["total_win"] += 1
            self.stats["lose_streak"] = 0  # 赢了清空连输
            self.stats["recent_5_games"].append(1)
        else:
            self.stats["total_lose"] += 1
            self.stats["lose_streak"] += 1  # 输了+1连输
            self.stats["recent_5_games"].append(0)

        # 限制最近5局记录长度为5
        if len(self.stats["recent_5_games"]) > 5:
            self.stats["recent_5_games"] = self.stats["recent_5_games"][-5:]

        # 2. 立即写入本地文件
        save_stats(self.stats)
        print(f"📝 战绩已保存 | 当前连输：{self.stats['lose_streak']} | 最近5局：{self.stats['recent_5_games']}")

        # 3. 检查是否触发策略调整
        self.check_trigger_adjustment()

    # ===================== 双条件触发判断 =====================
    def check_trigger_adjustment(self):
        # 单日最多触发2次
        if self.stats["daily_trigger_count"] >= 2:
            return

        lose_streak = self.stats["lose_streak"]
        recent = self.stats["recent_5_games"]
        # 计算最近5局胜场数
        win_count = recent.count(1)

        # 条件A：连输3局
        condition_a = (lose_streak >= 3)
        # 条件B：最近5局胜率 ≤20%（胜场≤1）
        condition_b = (len(recent) == 5 and win_count <= 1)

        if condition_a or condition_b:
            print("="*60)
            print("⚠️ 建议AI策略进行调整以获取更好的游戏结果！")
            if condition_a:
                print("📌 原因：连输3局")
            if condition_b:
                print("📌 原因：最近5局胜率≤20%")
            print("="*60)

            # 调用大模型调整策略
            llm_adjust_strategy(self.strategy_path)

            # 更新触发次数
            self.stats["daily_trigger_count"] += 1
            # 清空统计，避免重复触发
            self.stats["lose_streak"] = 0
            self.stats["recent_5_games"] = []
            save_stats(self.stats)

    def check_network_status(self):
        """检查网络连接状态"""
        try:
            # 发送一个简单的GET请求来测试网络连接
            response = requests.get(f"{SERVER_URL}/api/rank/gomoku", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def api_call(self, endpoint, method="GET", data=None, max_retries=3, retry_delay=1):
        """API调用函数，支持超时重试
        
        Args:
            endpoint: API端点
            method: 请求方法 (GET/POST)
            data: 请求数据
            max_retries: 最大重试次数
            retry_delay: 初始重试延迟（秒）
            
        Returns:
            响应结果
        """
        url = f"{SERVER_URL}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if data is None:
            data = {}
        data["user_id"] = self.user_id
        data["api_token"] = self.api_token
        
        retry_count = 0
        current_delay = retry_delay
        
        while retry_count <= max_retries:
            try:
                if method == "GET":
                    params = "&".join([f"{k}={v}" for k, v in data.items()])
                    resp = requests.get(f"{url}?{params}", headers=headers, timeout=15)
                else:
                    resp = requests.post(url, json=data, headers=headers, timeout=15)
                
                if not resp.ok:
                    print(f"[{self.nickname}] API Status Error: {resp.status_code} - {resp.text}")
                    return {"code": resp.status_code, "msg": resp.text}
                
                return resp.json()
            except requests.exceptions.Timeout:
                print(f"[{self.nickname}] API Timeout: 连接服务器超时")
                if retry_count < max_retries:
                    print(f"[{self.nickname}] 尝试重连 ({retry_count+1}/{max_retries})...")
                    time.sleep(current_delay)
                    current_delay *= 2  # 指数退避
                    retry_count += 1
                else:
                    return {"code": 408, "msg": "连接服务器超时"}
            except requests.exceptions.ConnectionError:
                print(f"[{self.nickname}] API Connection Error: 无法连接到服务器")
                if retry_count < max_retries:
                    print(f"[{self.nickname}] 尝试重连 ({retry_count+1}/{max_retries})...")
                    time.sleep(current_delay)
                    current_delay *= 2  # 指数退避
                    retry_count += 1
                else:
                    return {"code": 503, "msg": "无法连接到服务器"}
            except Exception as e:
                print(f"[{self.nickname}] API Error: {e}")
                if retry_count < max_retries:
                    print(f"[{self.nickname}] 尝试重连 ({retry_count+1}/{max_retries})...")
                    time.sleep(current_delay)
                    current_delay *= 2  # 指数退避
                    retry_count += 1
                else:
                    return {"code": 500, "msg": str(e)}
    
    def match(self):
        print(f"[{self.nickname}] 正在匹配对手...")
        result = self.api_call("/api/match", "POST", {"game": "gomoku"})
        
        print(f"[{self.nickname}] 匹配响应: {result}")
        
        if result.get("code") == 200:
            self.game_id = result["game_id"]
            self.my_color = result["your_color"]
            self.my_turn = result.get("your_turn", False)
            print(f"[{self.nickname}] 匹配成功! 颜色: {self.my_color}")
            return result
        elif result.get("code") == 202:
            print(f"[{self.nickname}] 等待匹配中...")
            return self.wait_for_match()
        else:
            print(f"[{self.nickname}] 匹配失败: {result.get('msg')}")
            return None
    
    def wait_for_match(self):
        for i in range(300):  # 增加超时时间到300秒
            print(f"[{self.nickname}] 等待匹配... ({i+1}/300)")
            time.sleep(1)
            result = self.api_call("/api/match_status", "GET")
            print(f"[{self.nickname}] 匹配状态响应: {result}")
            if result.get("code") == 200:
                self.game_id = result["game_id"]
                self.my_color = result["your_color"]
                self.my_turn = result.get("your_turn", False)
                print(f"[{self.nickname}] 匹配成功! 颜色: {self.my_color}")
                return result
        print(f"[{self.nickname}] 匹配超时")
        return None
    
    def send_move(self, row, col):
        print(f"[{self.nickname}] 发送落子请求: row={row}, col={col}, game_id={self.game_id}")
        result = self.api_call("/api/move", "POST", {
            "game_id": self.game_id,
            "row": row,
            "col": col
        })
        print(f"[{self.nickname}] 落子响应: {result}")
        return result
    
    def wait_opponent_move(self):
        last_move_idx = len(self.board.moves)
        print(f"[{self.nickname}] 开始等待对手落子，当前步数: {last_move_idx}")
        
        # 优化：根据网络状况调整轮询间隔
        base_interval = 1.0  # 基础间隔1秒
        max_interval = 5.0   # 最大间隔5秒
        current_interval = base_interval
        
        for i in range(12):  # 调整为12次，每次最多5秒，总超时60秒（1分钟）
            print(f"[{self.nickname}] 等待对手落子... ({i+1}/12)")
            time.sleep(current_interval)
            
            # 构建请求参数
            params = {
                "user_id": self.user_id,
                "api_token": self.api_token,
                "game_id": self.game_id,
                "last_move_idx": last_move_idx
            }
            
            result = self.api_call("/api/wait_move", "GET", params)
            
            print(f"[{self.nickname}] 等待对手响应: {result}")
            
            # 检查响应状态
            if result is None:
                print(f"[{self.nickname}] 响应为空，继续等待")
                # 增加间隔以避免频繁请求
                current_interval = min(current_interval * 1.5, max_interval)
                continue
            
            if result.get("code") != 200:
                print(f"[{self.nickname}] API错误: {result.get('msg')}")
                # 增加间隔以避免频繁请求
                current_interval = min(current_interval * 1.5, max_interval)
                continue
            
            # 响应成功，重置间隔
            current_interval = base_interval
            
            if result.get("game_over"):
                print(f"[{self.nickname}] 游戏结束: {result}")
                return result
            
            if result.get("your_turn"):
                print(f"[{self.nickname}] 轮到我了")
                # 检查是否有对手落子信息
                if result.get("opponent_move"):
                    move = result["opponent_move"]
                    opponent_color = 3 - self.my_color
                    self.board.place(move["row"], move["col"], opponent_color)
                    print(f"[{self.nickname}] 对手落子: ({move['row']}, {move['col']})")
                return result
        
        print(f"[{self.nickname}] 等待对手落子超时")
        return {"game_over": True, "msg": "等待超时"}
    
    def reconnect(self, max_attempts=10, delay=2):
        """网络重连函数
        
        Args:
            max_attempts: 最大重连尝试次数
            delay: 重连间隔（秒）
            
        Returns:
            bool: 重连是否成功
        """
        print(f"[{self.nickname}] 开始网络重连...")
        
        for attempt in range(max_attempts):
            if self.check_network_status():
                print(f"[{self.nickname}] ✅ 网络重连成功")
                return True
            else:
                print(f"[{self.nickname}] ⚠️ 重连失败 ({attempt+1}/{max_attempts})，{delay}秒后重试...")
                time.sleep(delay)
                delay *= 1.5  # 递增延迟
        
        print(f"[{self.nickname}] ❌ 网络重连失败，达到最大尝试次数")
        return False
    
    def run(self):
        print(f"\n{'='*50}")
        print(f"[{self.nickname}] Bot 启动")
        print(f"[{self.nickname}] 策略: {self.ai.bot_name}")
        print(f"{'='*50}\n")
        
        # 初始化总游戏计数
        total_games_played = 0
        max_consecutive_games = 5
        
        while True:
            # 检查网络状态
            if not self.check_network_status():
                print(f"[{self.nickname}] ⚠️ 网络连接异常，尝试重连...")
                if not self.reconnect():
                    print(f"[{self.nickname}] ❌ 网络连接失败，退出游戏")
                    return
            
            # 匹配对手
            game_info = self.match()
            if not game_info:
                # 匹配失败，尝试重连
                if not self.reconnect():
                    return
                continue
            
            # 游戏信息
            game_id = game_info.get("game_id")
            your_color = game_info.get("your_color")
            your_turn = game_info.get("your_turn", False)
            # 从服务端获取连续游戏信息
            consecutive_games = game_info.get("consecutive_games", 1)
            max_consecutive_games = game_info.get("max_consecutive_games", 5)
            opponent_nickname = game_info.get("opponent_nickname", "Unknown")
            
            # 更新总游戏计数
            total_games_played += 1
            
            print(f"[{self.nickname}] 🎮 对局信息")
            print(f"[{self.nickname}] 对手 ：{opponent_nickname}")
            print(f"[{self.nickname}] 游戏ID ： {game_id}")
            print(f"[{self.nickname}] 我方颜色 ：{'黑棋 (先手)' if your_color == 1 else '白棋 (后手)'}")
            print(f"[{self.nickname}] 连续游戏 ：{consecutive_games}/{max_consecutive_games}")
            
            # 游戏主循环
            game_over = False
            move_count = 0
            while not game_over:
                # 检查网络状态
                if not self.check_network_status():
                    print(f"[{self.nickname}] ⚠️ 网络连接异常，尝试重连...")
                    if not self.reconnect():
                        print(f"[{self.nickname}] ❌ 网络连接失败，退出游戏")
                        return
                    # 重连成功后同步棋盘状态
                    self.sync_board()
                
                if your_turn:
                    print(f"[{self.nickname}] 第 {move_count+1} 回合，我的回合")
                    row, col = self.ai.get_best_move(self.board.board, your_color)
                    print(f"[{self.nickname}] 计算出的落子: ({row}, {col})")
                    
                    # 发送落子请求
                    response = self.send_move(row, col)
                    if response.get("code") != 200:
                        print(f"[{self.nickname}] ❌ 落子失败: {response.get('msg')}")
                        # 尝试重连
                        if not self.reconnect():
                            return
                        continue
                    
                    # 落子成功
                    self.board.place(row, col, your_color)
                    move_count += 1
                    
                    # 检查游戏是否结束
                    if response.get("game_over"):
                        game_over = True
                        # 处理游戏结束
                        winner = response.get("winner")
                        is_win = (winner == self.user_id)
                        is_draw = (winner == "draw")
                        self.update_battle_stats(is_win, is_draw)
                        
                        if is_win:
                            print(f"[{self.nickname}] 🎉 获胜!")
                        elif is_draw:
                            print(f"[{self.nickname}] 🤝 平局!")
                        else:
                            print(f"[{self.nickname}] 😢 对手获胜")
                        
                        print(f"[{self.nickname}] 🏆 游戏结束，共进行了 {total_games_played} 局")
                        
                        # 检查服务端是否指示继续下一局
                        # 如果 consecutive_games < max_consecutive_games，服务端会自动匹配下一局
                        # 客户端只需要重新调用 match() 即可
                        break
                    else:
                        your_turn = False
                else:
                    # 等待对手落子
                    response = self.wait_opponent_move()
                    if response.get("code") != 200:
                        print(f"[{self.nickname}] ❌ 等待对手落子失败: {response.get('msg')}")
                        # 尝试重连
                        if not self.reconnect():
                            return
                        continue
                    
                    # 检查游戏是否结束
                    if response.get("game_over"):
                        game_over = True
                        # 处理游戏结束
                        winner = response.get("winner")
                        is_win = (winner == self.user_id)
                        is_draw = (winner == "draw")
                        self.update_battle_stats(is_win, is_draw)
                        
                        if is_win:
                            print(f"[{self.nickname}] 🎉 获胜!")
                        elif is_draw:
                            print(f"[{self.nickname}] 🤝 平局!")
                        else:
                            print(f"[{self.nickname}] 😢 对手获胜")
                        
                        print(f"[{self.nickname}] 🏆 游戏结束，共进行了 {total_games_played} 局")
                        
                        # 检查服务端是否指示继续下一局
                        # 如果 consecutive_games < max_consecutive_games，服务端会自动匹配下一局
                        # 客户端只需要重新调用 match() 即可
                        break
                    else:
                        # 更新棋盘
                        opponent_move = response.get("opponent_move")
                        if opponent_move:
                            opponent_color = 3 - your_color
                            self.board.place(opponent_move["row"], opponent_move["col"], opponent_color)
                        your_turn = True
            
            # 游戏结束，准备下一局
            # 重置棋盘，让服务端来决定是否继续
            self.board = GomokuBoard()
            
            # 如果已经达到最大局数，退出循环
            if total_games_played >= max_consecutive_games:
                print(f"[{self.nickname}] ✅ 已完成所有 {max_consecutive_games} 局游戏")
                return
    
    def sync_board(self):
        result = self.api_call("/api/game_status", "GET", {"game_id": self.game_id})
        if result.get("code") == 200:
            self.board = GomokuBoard()
            for move in result.get("moves", []):
                self.board.place(move["row"], move["col"], move["player"])
            print(f"[{self.nickname}] 棋盘已同步")

def run():
    parser = argparse.ArgumentParser(description="OpenClaw Gomoku Bot")
    parser.add_argument("--config", default="user_config.json", help="Bot配置文件路径")
    parser.add_argument("--strategy", default="gomoku_strategy.json", help="策略文件路径")
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = args.config if os.path.isabs(args.config) else os.path.join(base_dir, "..", "..", args.config)
    strategy_path = args.strategy if os.path.isabs(args.strategy) else os.path.join(base_dir, args.strategy)
    
    bot = GomokuBot(config_path, strategy_path)
    bot.run()

if __name__ == "__main__":
    run()