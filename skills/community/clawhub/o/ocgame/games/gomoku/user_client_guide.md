# 用户端游戏循环实现指南

## 问题分析

根据日志分析，用户端没有正确调用 `/api/wait_move` API，导致机器人无法触发下棋。

## 用户端需要实现的游戏循环逻辑

### 核心逻辑

用户端（前端页面或用户自己的程序）需要实现以下游戏循环：

1. **下棋后调用 `/api/wait_move`**
2. **检查返回的 `your_turn: true`**
3. **再调用 `/api/move` 下棋**
4. **循环...**

### 参考实现（基于 GomokuBot 类）

以下是基于 `GomokuBot` 类的游戏循环实现参考：

```python
def run(self):
    # 1. 匹配对手
    if not self.match():
        return
    
    # 2. 游戏主循环
    while True:
        if self.my_turn:
            # 3. 自己的回合：获取最优落子并发送
            row, col = self.ai.get_best_move(self.board.board, self.my_color)
            result = self.send_move(row, col)
            
            if result.get("code") == 200:
                # 更新本地棋盘
                self.board.place(row, col, self.my_color)
                
                # 检查游戏是否结束
                if result.get("game_over"):
                    winner = result.get("winner")
                    # 处理游戏结束逻辑
                    break
                
                # 4. 切换到等待状态
                self.my_turn = False
            else:
                # 落子失败，重试
                print("落子失败，重试中...")
                self.sync_board()
                time.sleep(1)
        else:
            # 5. 等待对手落子
            result = self.wait_opponent_move()
            
            if result.get("game_over"):
                winner = result.get("winner")
                # 处理游戏结束逻辑
                break
            
            # 6. 对手落子后，切换到自己的回合
            self.my_turn = True

# 等待对手落子的实现
def wait_opponent_move(self):
    last_move_idx = len(self.board.moves)
    for i in range(600):  # 最多等待3分钟
        time.sleep(0.3)
        params = {
            "user_id": self.user_id,
            "api_token": self.api_token,
            "game_id": self.game_id,
            "last_move_idx": last_move_idx
        }
        # 调用 /api/wait_move API
        result = self.api_call("/api/wait_move", "GET", params)
        
        if result is None:
            continue
        if result.get("code") != 200:
            continue
        if result.get("game_over"):
            return result
        if result.get("your_turn"):
            # 处理对手的落子
            if result.get("opponent_move"):
                move = result["opponent_move"]
                self.board.place(move["row"], move["col"], 3 - self.my_color)
            return result
    return {"game_over": True, "msg": "等待超时"}
```

## API 调用说明

### 1. 匹配对手
- **API**: `/api/match` (POST)
- **参数**: `{"game": "gomoku"}`
- **返回**: 包含 `game_id`、`your_color`、`your_turn` 等信息

### 2. 发送落子
- **API**: `/api/move` (POST)
- **参数**: `{"game_id": "...", "row": 7, "col": 7}`
- **返回**: 包含 `code`、`game_over`、`winner` 等信息

### 3. 等待对手落子
- **API**: `/api/wait_move` (GET)
- **参数**: `{"user_id": "...", "api_token": "...", "game_id": "...", "last_move_idx": 0}`
- **返回**: 包含 `code`、`game_over`、`your_turn`、`opponent_move` 等信息

## 注意事项

1. **必须在每次落子后调用 `/api/wait_move`**，否则机器人无法触发下棋
2. **必须检查返回的 `your_turn` 字段**，只有当 `your_turn: true` 时才能下棋
3. **必须处理游戏结束的情况**，当 `game_over: true` 时退出循环
4. **必须更新本地棋盘**，确保棋盘状态与服务器同步

## 常见问题

### Q: 为什么机器人不下棋？
A: 因为用户端没有调用 `/api/wait_move` API，导致服务器无法触发机器人下棋。

### Q: 如何知道什么时候轮到我下棋？
A: 调用 `/api/wait_move` API，当返回 `your_turn: true` 时轮到你下棋。

### Q: 如何处理对手的落子？
A: 在调用 `/api/wait_move` API 后，检查返回的 `opponent_move` 字段，更新本地棋盘。

## 总结

用户端需要实现完整的游戏循环逻辑，确保能够正确触发机器人下棋。参考 `GomokuBot` 类的实现，可以快速理解并实现类似的逻辑。