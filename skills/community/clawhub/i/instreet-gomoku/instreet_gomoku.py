"""
InStreet 五子棋AI技能 v5.0
基于五子棋AI核心技术文档优化
新增：开局库、四三检测、VCT/VCF、位置权重、Alpha-Beta搜索
"""
import numpy as np
import urllib.request
import json
import time
import random

API_KEY = 'sk_inst_adfe55c5fe69ca780201cb466bebbbce'
BASE_URL = 'https://instreet.coze.site/api/v1/games'

# ========== 开局库 (必胜开局定式) ==========
# 花月、浦月、云月、松月的标准开局
OPENING_BOOK = {
    # 花月局 (直指，必胜)
    "flower_moon": [
        # 黑1=H8, 白2=I8, 黑3=I9 后的必胜点
        {("I9",): ["G10", "F10", "G9", "F9"]},  # 白4=I8
        {("J10",): ["G10", "F10", "G9"]},       # 白4=J10
        {("G7",): ["G10", "F10"]},              # 白4=G7
        {("J8",): ["G10", "F10", "G9", "F9"]}, # 白4=J8
        {("I7",): ["G10", "F10", "G9"]},        # 白4=I7
    ],
    # 浦月局 (斜指，必胜)
    "puyue": [
        {("I9", "I7"): ["G9", "J7", "J8"]},    # 白4=G9
        {("I9", "H7"): ["G9", "J6", "J8"]},    # 白4=H7
        {("I9", "H6"): ["G9", "I6", "J6", "J7"]},  # 白4=H6
        {("I9", "J6"): ["G8", "G9", "H9", "H10"]}, # 白4=J6
    ],
    # 云月局 (斜指，必胜)
    "cloud_moon": [
        {("I9", "I8"): ["H10"]},   # 白4=J8
        {("I9", "H7"): ["G10"]},    # 白4=H7
        {("I9", "G8"): ["H7"]},     # 白4=G8 (桂马止)
        {("I9", "H9"): ["G8", "J8"]},  # 白4=H9
    ],
    # 松月局 (直指，必胜)
    "pine_moon": [
        {("H9", "H7"): ["I8"]},     # 白4=H6 (天地止)
        {("H9", "J8"): ["I6"]},     # 白4=J8
        {("H9", "H10"): ["I7", "I8", "J9"]},  # 白4=H10
        {("H9", "I10"): ["G8", "I8"]},  # 白4=I10
    ],
}


class GomokuAI:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        # 初始化 Zobrist 哈希表
        self._zobrist = self._init_zobrist()
        
        # 位置权重：中心(H8=7,7)价值最高，边缘递减
        self.position_weights = self._init_position_weights()
        
        self.score_weights = {
            "FIVE": 1000000,     # 五连，必胜
            "LIVE4": 100000,    # 活四
            "RUSH4": 50000,     # 冲四
            "LIVE3": 20000,     # 活三
            "SLEEP3": 5000,     # 眠三
            "LIVE2": 1500,      # 活二
            "SLEEP2": 500,      # 眠二
        }
        
        # 置换表：缓存已评估的局面
        self.ttable = {}
        # 杀手着法
        self.killer_moves = {}  # depth -> [(move1, score), (move2, score)]
    
    def _init_zobrist(self):
        """初始化 Zobrist 哈希表"""
        import random
        random.seed(42)  # 固定种子保证一致性
        zobrist = [[(random.getrandbits(64), random.getrandbits(64)) 
                    for _ in range(self.board_size)] 
                   for _ in range(self.board_size)]
        return zobrist
    
    def _init_position_weights(self):
        """初始化位置权重：中心价值高，边缘价值低"""
        weights = np.zeros((self.board_size, self.board_size))
        center = self.board_size // 2
        for x in range(self.board_size):
            for y in range(self.board_size):
                # 曼哈顿距离衰减
                dist = abs(x - center) + abs(y - center)
                weights[x][y] = 100 / (dist + 1)
        return weights
    
    def zobrist_hash(self):
        """Zobrist哈希：生成局面唯一标识"""
        h = 0
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 1:
                    h ^= self._zobrist[x][y][0]
                elif self.board[x][y] == 2:
                    h ^= self._zobrist[x][y][1]
        return h
    
    def is_valid(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == 0
        
    # ========== 核心：四三检测（双重威胁）==========
    def check_four_three(self, x, y, player):
        """
        检测四三：同时形成冲四+活三
        这是五子棋最核心的杀招，双重威胁不可防守
        """
        self.board[x][y] = player
        has_rush4 = False
        has_live3 = False
        
        for dx, dy in self.directions:
            line = []
            for i in range(-4, 5):
                nx = x + dx * i
                ny = y + dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    line.append(self.board[nx][ny])
                else:
                    line.append(-1)
            
            for i in range(len(line) - 4):
                window = line[i:i+5]
                empty = window.count(0)
                self_pieces = window.count(player)
                
                # 冲四：一端被堵，四子一线
                if self_pieces == 4 and empty == 1:
                    has_rush4 = True
                # 活三：两端开放，三子一线
                elif self_pieces == 3 and empty == 2:
                    if (window[0] == 0 and window[1] == player) or (window[-1] == 0 and window[-2] == player):
                        has_live3 = True
        
        self.board[x][y] = 0
        return has_rush4 and has_live3
    
    # ========== VCT检测（连续活三）==========
    def check_vct(self, player, depth=3):
        """
        VCT (Victory of Continuous Three): 连续活三进攻
        通过多次活三保持先手，最终形成四三或活四
        """
        # 简化实现：检测是否有活三能发展为四三
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 0:
                    self.board[x][y] = player
                    # 落子后能成四三？
                    if self.check_four_three(x, y, player):
                        self.board[x][y] = 0
                        return True
                    self.board[x][y] = 0
        return False
    
    # ========== VCF检测（连续冲四）==========
    def check_vcf(self, player):
        """
        VCF (Victory of Continuous Four): 连续冲四追击
        纯靠冲四实施追击，积累先手直至形成冲四活三
        """
        # 简化实现：检测连续冲四的可能性
        rush4_count = 0
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 0:
                    pattern = self._detect_single_pattern(x, y, player)
                    if pattern.get("rush4"):
                        rush4_count += 1
        return rush4_count >= 2  # 有多个冲四点，可以连续追击
    
    def _detect_single_pattern(self, x, y, player):
        """检测单个位置的棋型"""
        result = {"live4": False, "rush4": False, "live3": False, "sleep3": False, "live2": False}
        opponent = 3 - player
        
        for dx, dy in self.directions:
            line = []
            for i in range(-4, 5):
                nx = x + dx * i
                ny = y + dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    line.append(self.board[nx][ny])
                else:
                    line.append(-1)
            
            for i in range(len(line) - 4):
                window = line[i:i+5]
                empty = window.count(0)
                self_pieces = window.count(player)
                opp_pieces = window.count(opponent)
                
                if opp_pieces > 0:
                    continue
                
                if self_pieces == 4 and empty == 1:
                    if window[0] == 0 or window[-1] == 0:
                        result["live4"] = True
                elif self_pieces == 4:
                    result["rush4"] = True
                elif self_pieces == 3 and empty == 2:
                    if (window[0] == 0 and window[1] == player) or (window[-1] == 0 and window[-2] == player):
                        result["live3"] = True
                elif self_pieces == 3 and empty == 1:
                    result["sleep3"] = True
                elif self_pieces == 2 and empty == 3:
                    if (window[0] == 0 and window[1] == player) or (window[-1] == 0 and window[-2] == player):
                        result["live2"] = True
        
        return result
    
    def check_win(self, x, y, player):
        for dx, dy in self.directions:
            count = 1
            nx, ny = x + dx, y + dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == player:
                count += 1
                nx += dx
                ny += dy
            nx, ny = x - dx, y - dy
            while 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == player:
                count += 1
                nx -= dx
                ny -= dy
            if count >= 5:
                return True
        return False
    
    def detect_pattern(self, x, y, player):
        """
        完整棋型检测（四个方向）
        v5.0: 增加位置权重影响
        """
        result = {"live4": False, "rush4": False, "live3": False, "sleep3": False, "live2": False}
        opponent = 3 - player
        
        for dx, dy in self.directions:
            line = []
            for i in range(-4, 5):
                nx = x + dx * i
                ny = y + dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    line.append(self.board[nx][ny])
                else:
                    line.append(-1)
            
            for i in range(len(line) - 4):
                window = line[i:i+5]
                empty = window.count(0)
                self_pieces = window.count(player)
                opp_pieces = window.count(opponent)
                
                if opp_pieces > 0:
                    continue
                
                if self_pieces == 4 and empty == 1:
                    if window[0] == 0 or window[-1] == 0:
                        result["live4"] = True
                elif self_pieces == 4:
                    result["rush4"] = True
                elif self_pieces == 3 and empty == 2:
                    if (window[0] == 0 and window[1] == player) or (window[-1] == 0 and window[-2] == player):
                        result["live3"] = True
                elif self_pieces == 3 and empty == 1:
                    result["sleep3"] = True
                elif self_pieces == 2 and empty == 3:
                    if (window[0] == 0 and window[1] == player) or (window[-1] == 0 and window[-2] == player):
                        result["live2"] = True
        
        return result
    
    # ========== Alpha-Beta 搜索 (v5.0新增) ==========
    def alpha_beta_search(self, player, depth=3, alpha=-float('inf'), beta=float('inf'), maximizing=True):
        """
        Alpha-Beta剪枝搜索
        理想排序下时间复杂度从O(b^d)降至O(sqrt(b^d))
        """
        # 置换表查找
        hash_val = self.zobrist_hash()
        if hash_val in self.ttable and self.ttable[hash_val][1] >= depth:
            return self.ttable[hash_val][0]
        
        # 终止条件
        if depth == 0:
            return self.evaluate_board(player)
        
        # 获取候选落子（只考虑有棋子的邻域）
        candidates = self.get_candidates()
        if not candidates:
            return 0
        
        # 着法排序：优先杀手着法
        candidates = self._order_moves(candidates, player, depth)
        
        best_score = -float('inf') if maximizing else float('inf')
        
        for x, y in candidates:
            if not self.is_valid(x, y):
                continue
            
            # 尝试落子
            self.board[x][y] = player
            
            # 检查胜利
            if self.check_win(x, y, player):
                self.board[x][y] = 0
                score = 1000000  # 胜利
                self.ttable[hash_val] = (score, depth)
                return score
            
            # 递归搜索
            next_player = 3 - player
            score = self.alpha_beta_search(next_player, depth-1, alpha, beta, not maximizing)
            
            self.board[x][y] = 0
            
            if maximizing:
                if score > best_score:
                    best_score = score
                    # 记录杀手着法
                    self._record_killer(depth, (x, y), score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta剪枝
            else:
                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha剪枝
        
        self.ttable[hash_val] = (best_score, depth)
        return best_score
    
    def _order_moves(self, candidates, player, depth):
        """着法排序：优先杀手着法和高价值着法"""
        scored = []
        for x, y in candidates:
            score = 0
            # 杀手着法优先
            if depth in self.killer_moves:
                for kmove, kscore in self.killer_moves[depth]:
                    if kmove == (x, y):
                        score += kscore
                        break
            # 高价值着法加分
            pattern = self.detect_pattern(x, y, player)
            if pattern.get("live4") or pattern.get("rush4"):
                score += 10000
            elif pattern.get("live3"):
                score += 5000
            # 位置权重
            score += self.position_weights[x][y]
            scored.append((score, random.random() * 100, x, y))
        
        scored.sort(reverse=True)
        return [(x, y) for _, _, x, y in scored]
    
    def _record_killer(self, depth, move, score):
        """记录杀手着法"""
        if depth not in self.killer_moves:
            self.killer_moves[depth] = []
        # 保持最多2个杀手着法
        self.killer_moves[depth] = [m for m in self.killer_moves[depth] if m[0] != move]
        self.killer_moves[depth].insert(0, (move, score))
        if len(self.killer_moves[depth]) > 2:
            self.killer_moves[depth] = self.killer_moves[depth][:2]
    
    def evaluate_board(self, player):
        """
        评估整个棋盘
        v5.0: 包含位置权重
        """
        my_total = 0
        opp_total = 0
        opponent = 3 - player
        
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 0:
                    # 评估所有空位
                    my_pattern = self.detect_pattern(x, y, player)
                    opp_pattern = self.detect_pattern(x, y, opponent)
                    
                    # 自己的棋型
                    if my_pattern["live4"]:
                        my_total += self.score_weights["LIVE4"]
                    if my_pattern["rush4"]:
                        my_total += self.score_weights["RUSH4"]
                    if my_pattern["live3"]:
                        my_total += self.score_weights["LIVE3"]
                    if my_pattern["sleep3"]:
                        my_total += self.score_weights["SLEEP3"]
                    if my_pattern["live2"]:
                        my_total += self.score_weights["LIVE2"]
                    
                    # 对手的棋型
                    if opp_pattern["live4"]:
                        opp_total += self.score_weights["LIVE4"]
                    if opp_pattern["rush4"]:
                        opp_total += self.score_weights["RUSH4"]
                    if opp_pattern["live3"]:
                        opp_total += self.score_weights["LIVE3"]
                    if opp_pattern["sleep3"]:
                        opp_total += self.score_weights["SLEEP3"]
                    if opp_pattern["live2"]:
                        opp_total += self.score_weights["LIVE2"]
        
        return my_total - opp_total
    
    def has_threat(self, player):
        threats = {"live4": 0, "rush4": 0, "live3": 0}
        
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 0:
                    pattern = self.detect_pattern(x, y, player)
                    if pattern["live4"]:
                        threats["live4"] += 1
                    if pattern["rush4"]:
                        threats["rush4"] += 1
                    if pattern["live3"]:
                        threats["live3"] += 1
        
        return threats
    
    def has_opponent_threat(self, opp_player):
        """检测对手是否已有威胁（活三/冲四/活四/已赢）"""
        # 先检测对手是否已经赢了
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == opp_player:
                    if self.check_win(x, y, opp_player):
                        return True
        
        # 再检测对手在空位的威胁
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 0:
                    pattern = self.detect_pattern(x, y, opp_player)
                    if pattern["live4"] or pattern["rush4"] or pattern["live3"]:
                        return True
        return False
    
    def find_blocking_moves(self, opp_player):
        """找到能堵住对手威胁的位置"""
        blocking_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 0:
                    # 尝试堵住对手的威胁
                    self.board[x][y] = opp_player
                    # 检查堵住后对手是否还有威胁
                    still_threat = False
                    for ox in range(self.board_size):
                        for oy in range(self.board_size):
                            if self.board[ox][oy] == 0:
                                pattern = self.detect_pattern(ox, oy, opp_player)
                                if pattern["live4"] or pattern["rush4"] or pattern["live3"]:
                                    still_threat = True
                                    break
                        if still_threat:
                            break
                    self.board[x][y] = 0
                    if not still_threat:
                        blocking_moves.append((x, y))
        return blocking_moves
    
    def evaluate_move(self, x, y, player):
        """
        v5.0 评估落子
        优先级：必胜 > 四三 > 防守 > VCT > 造棋
        """
        if not self.is_valid(x, y):
            return -float('inf')
        
        opp_player = 3 - player
        
        # 0. 位置权重加成
        position_bonus = self.position_weights[x][y]
        
        # 1. 自己能成活四/五连 → 必胜 (最高优先)
        self.board[x][y] = player
        if self.check_win(x, y, player):
            self.board[x][y] = 0
            return 1000000 + position_bonus
        self.board[x][y] = 0
        
        # ====== v5.0: 四三检测（双重威胁）=======
        # 落子后能形成四三？→ 直接返回高分（不可防守）
        if self.check_four_three(x, y, player):
            return 900000 + position_bonus  # 四三接近必胜
        
        # ====== 核心逻辑：对手已有威胁，必须防守 ======
        # 2. 检查当前棋盘对手是否已有威胁
        opp_has_threat = self.has_opponent_threat(opp_player)
        
        # 2.1 对手能成活四 → 必须防守 (最高优先)
        for ox in range(self.board_size):
            for oy in range(self.board_size):
                if self.board[ox][oy] == 0:
                    self.board[ox][oy] = opp_player
                    if self.check_win(ox, oy, opp_player):
                        self.board[ox][oy] = 0
                        # 检查这步能否堵住
                        self.board[x][y] = player
                        can_block = True
                        for ox2 in range(self.board_size):
                            for oy2 in range(self.board_size):
                                if self.board[ox2][oy2] == 0:
                                    self.board[ox2][oy2] = opp_player
                                    if self.check_win(ox2, oy2, opp_player):
                                        can_block = False
                                    self.board[ox2][oy2] = 0
                        self.board[x][y] = 0
                        if can_block:
                            return 100000 + position_bonus  # 能堵住对手活四
                    self.board[ox][oy] = 0
        
        # ====== v4.2：对手已有活三/冲四，必须防守 ======
        if opp_has_threat:
            # 检查这步能否堵住对手威胁
            self.board[x][y] = player
            still_has_threat = self.has_opponent_threat(opp_player)
            self.board[x][y] = 0
            
            if not still_has_threat:
                # 能堵住！这是好防守 - 给高分
                return 80000 + position_bonus
            else:
                # 堵不住，惩罚
                return -50000
        
        # ====== v5.0: VCT/VCP进攻检测 ======
        # 能通过VCT（连续活三）形成杀招？
        if self.check_vct(player):
            return 70000 + position_bonus
        
        # ====== 对手没有威胁，可以造棋 ======
        # 3. 落子后自己能成冲四 → 进攻
        self.board[x][y] = player
        after_pattern = self.detect_pattern(x, y, player)
        self.board[x][y] = 0
        
        if after_pattern["rush4"]:
            return 50000 + position_bonus
        
        # 4. 落子后自己能成活三 → 造棋
        if after_pattern["live3"]:
            base_score = 20000
        elif after_pattern["sleep3"]:
            base_score = 5000
        elif after_pattern["live2"]:
            base_score = 1500
        else:
            base_score = 100
        
        # 5. 正常估值
        my_score = self.evaluate_pos(x, y, player)
        opp_score = self.evaluate_pos(x, y, opp_player)
        
        return base_score + my_score - opp_score + position_bonus
    
    def evaluate_pos(self, x, y, player):
        score = 0
        opponent = 3 - player
        
        for dx, dy in self.directions:
            line = []
            for i in range(-4, 5):
                nx = x + dx * i
                ny = y + dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    line.append(self.board[nx][ny])
                else:
                    line.append(-1)
            
            for i in range(len(line) - 4):
                window = line[i:i+5]
                empty = window.count(0)
                self_pieces = window.count(player)
                opp_pieces = window.count(opponent)
                
                if opp_pieces > 0:
                    continue
                
                if self_pieces == 4 and empty == 1:
                    if window[0] == 0 or window[-1] == 0:
                        score += self.score_weights["LIVE4"]
                elif self_pieces == 4:
                    score += self.score_weights["RUSH4"]
                elif self_pieces == 3 and empty == 2:
                    if (window[0] == 0 and window[1] == player) or (window[-1] == 0 and window[-2] == player):
                        score += self.score_weights["LIVE3"]
                elif self_pieces == 3 and empty == 1:
                    score += self.score_weights["SLEEP3"]
                elif self_pieces == 2 and empty == 3:
                    if (window[0] == 0 and window[1] == player) or (window[-1] == 0 and window[-2] == player):
                        score += self.score_weights["LIVE2"]
        
        return score
    
    def get_candidates(self):
        """
        获取候选落子点
        v5.0: 只考虑有棋子的邻域（加速搜索）
        """
        candidates = []
        
        center = self.board_size // 2
        # 开局第一步：天元
        if np.sum(self.board) == 0:
            return [(center, center)]
        
        # 只搜索有邻居的空位
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.is_valid(x, y):
                    has_neighbor = False
                    for dx in [-2, -1, 0, 1, 2]:
                        for dy in [-2, -1, 0, 1, 2]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] != 0:
                                has_neighbor = True
                                break
                        if has_neighbor:
                            break
                    if has_neighbor:
                        candidates.append((x, y))
        
        # 排序：优先中心位置
        candidates.sort(key=lambda pos: -self.position_weights[pos[0]][pos[1]])
        return candidates
    
    def ai_move(self, player=1):
        """
        v5.0 AI落子
        策略：开局库 → 四三 → 防守 → Alpha-Beta搜索
        """
        center = self.board_size // 2
        
        # ====== 开局库检测（前10步）=======
        # 统计已落子数
        total_moves = np.sum(self.board != 0)
        
        if total_moves == 0:
            # 黑1: 天元
            self.board[center][center] = player
            return center, center
        
        if total_moves <= 10:
            # 尝试开局库
            opening_move = self._get_opening_move(player)
            if opening_move:
                x, y = opening_move
                self.board[x][y] = player
                return x, y
        
        # ====== Alpha-Beta 搜索 ======
        candidates = self.get_candidates()
        
        if not candidates:
            return None, None
        
        # 清理置换表（避免内存过大）
        if len(self.ttable) > 10000:
            self.ttable.clear()
        
        best_score = -float('inf')
        best_move = None
        
        # 着法排序：优先高价值着法
        scored_candidates = []
        for x, y in candidates:
            score = self.evaluate_move(x, y, player)
            scored_candidates.append((score, random.random() * 100, x, y))
        
        scored_candidates.sort(reverse=True)
        
        for score, _, x, y in scored_candidates[:30]:  # 限制搜索数量
            self.board[x][y] = player
            
            # 检查直接胜利
            if self.check_win(x, y, player):
                self.board[x][y] = 0
                return x, y
            
            # Alpha-Beta搜索下一层
            search_score = self.alpha_beta_search(3 - player, depth=2, alpha=-float('inf'), beta=float('inf'), maximizing=False)
            
            self.board[x][y] = 0
            
            # 自己的分数 - 对手的分数
            total_score = score + search_score
            
            if total_score > best_score:
                best_score = total_score
                best_move = (x, y)
        
        if best_move:
            x, y = best_move
            self.board[x][y] = player
            return x, y
        
        return None, None
    
    def _get_opening_move(self, player):
        """
        v5.0 开局库
        返回必胜开局的下一步
        """
        # 找黑棋和白棋的位置
        black_pos = None
        white_pos = None
        
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == 1:
                    black_pos = (x, y)
                elif self.board[x][y] == 2:
                    white_pos = (x, y)
        
        if not black_pos:
            return None
        
        center = self.board_size // 2  # 7
        
        # 黑1 = H8 (天元)
        if black_pos == (center, center):
            # 白2 的位置决定开局类型
            if white_pos:
                wx, wy = white_pos
                # 白2 在 I8 (右) → 花月/松月方向
                # 白2 在 I9 (右下) → 浦月/云月方向
                if wy == center and wx == center + 1:  # I8
                    # 下一手：I9 (浦月)
                    return (center + 1, center)
                elif wx == center + 1 and wy == center + 1:  # I9
                    # 下一手：I7 (浦月) 或 I8 (云月)
                    # 选浦月：I7
                    return (center + 1, center - 1)
        
        return None
    
    # ========== 坐标转换 ==========
    
    def get_position_name(self, x, y):
        """坐标转换: (x,y) -> 'H8'"""
        col = chr(ord('A') + x)
        row = y + 1
        return f"{col}{row}"
    
    def get_coord_from_name(self, name):
        """坐标转换: 'H8' -> (x,y)"""
        if not name or len(name) < 2:
            return None
        col = ord(name[0].upper()) - ord('A')
        try:
            row = int(name[1:]) - 1
        except:
            return None
        if 0 <= col < self.board_size and 0 <= row < self.board_size:
            return col, row
        return None
    
    # ========== 棋盘解析 ==========
    
    def parse_board(self, board_str):
        """解析棋盘字符串 (API返回的格式)"""
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        
        if not board_str:
            return
        
        lines = board_str.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 跳过表头 (如 "   A B C D E F G H I J K L M N O")
            if not line[0].isdigit():
                continue
            
            parts = line.split()
            if len(parts) < 2:
                continue
            
            try:
                row = int(parts[0]) - 1
            except:
                continue
            
            if row < 0 or row >= self.board_size:
                continue
            
            # 解析每一列 (索引1开始，因为索引0是行号)
            for col in range(self.board_size):
                if col + 1 >= len(parts):
                    break
                cell = parts[col + 1]
                if cell == 'X':
                    self.board[col][row] = 1  # 黑棋
                elif cell == 'O':
                    self.board[col][row] = 2  # 白棋
    
    # ========== 落子解释 ==========
    
    def get_move_reason(self, x, y, player):
        """获取落子原因"""
        self.board[x][y] = player
        if self.check_win(x, y, player):
            self.board[x][y] = 0
            return "胜！五连"
        self.board[x][y] = 0
        
        my_pattern = self.detect_pattern(x, y, player)
        
        # 先检查自己能否造活三（进攻优先）
        if my_pattern["live4"]:
            return "冲四！必胜"
        if my_pattern["live3"]:
            return "造活三！主动进攻"
        if my_pattern["sleep3"]:
            return "造眠三，发展"
        
        # 再检查对手威胁（防守）
        opp_player = 3 - player
        self.board[x][y] = opp_player
        opp_pattern = self.detect_pattern(x, y, opp_player)
        self.board[x][y] = 0
        
        if opp_pattern["live4"]:
            return "防对手活四！"
        if opp_pattern["rush4"]:
            return "防对手冲四！"
        if opp_pattern["live3"]:
            return "防对手活三！"
        
        return "占据好位置"


# ========== API 函数 ==========

def get_activity():
    """获取当前活动"""
    url = f'{BASE_URL}/activity'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {API_KEY}'})
    try:
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode('utf-8'))
        return data.get('data', {})
    except Exception as e:
        print(f'Error getting activity: {e}')
        return {}


def make_move(room_id, position, reasoning):
    """提交落子（带重试）"""
    url = f'{BASE_URL}/rooms/{room_id}/move'
    data = json.dumps({'position': position, 'reasoning': reasoning}).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST', 
                                headers={'Authorization': f'Bearer {API_KEY}', 
                                        'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
        result = json.loads(response.read().decode('utf-8'))
        return result
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode('utf-8')
            print(f'HTTP Error {e.code}: {error_body}')
        except:
            print(f'HTTP Error {e.code}')
        return None
    except Exception as e:
        print(f'Error making move: {e}')
        return None


def get_best_move(board_str, my_color):
    """对外接口：获取最佳落子
    优先使用 KataGomo AI，如失败则回退到本地 AI
    """
    # 尝试使用 KataGomo
    try:
        from katagomo_simple import KataGomo
        print(f"[AI] Calling KataGomo for {my_color}...")
        x, y, position, reason = KataGomo.get_best_move(board_str, my_color)
        print(f"[AI] KataGomo returned: {position}, reason: {reason[:30] if reason else 'None'}")
        if x is not None:
            return x, y, position, reason + " (KataGomo)"
        else:
            print(f"[AI] KataGomo returned None, reason: {reason}")
    except Exception as e:
        print(f"[AI] KataGomo failed with error: {e}")
    
    # 回退到本地 AI
    ai = GomokuAI()
    ai.parse_board(board_str)
    
    player = 1 if my_color == 'black' else 2
    
    x, y = ai.ai_move(player)
    
    if x is None:
        return None, None, "No valid move"
    
    position = ai.get_position_name(x, y)
    reason = ai.get_move_reason(x, y, player)
    
    return x, y, position, reason + " (本地AI)"


if __name__ == "__main__":
    # 测试
    board_str = """   A B C D E F G H I J K L M N O
 1 . . . . . . . . . . . . . . .
 8 . . . . . . X . . . . . . . ."""
    
    ai = GomokuAI()
    ai.parse_board(board_str)
    print("Parsed board[:,7:8]:")
    print(ai.board[:, 7])
    
    print("\nCoord tests:")
    print("H8 ->", ai.get_coord_from_name('H8'))
    print("G9 ->", ai.get_coord_from_name('G9'))
    print("(7,7) ->", ai.get_position_name(7, 7))
