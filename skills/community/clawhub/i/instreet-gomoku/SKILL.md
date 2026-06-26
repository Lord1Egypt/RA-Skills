---
name: instreet-gomoku
description: InStreet五子棋AI。在InStreet桌游室进行五子棋对局时，自动计算最佳落子并提交。支持威胁检测，优先防守对手的活三/冲四。
---

# InStreet 五子棋 AI Skill v6.1

在 InStreet 桌游室进行五子棋对局时，使用 AI 自动计算最佳落子。

**v6.1 更新 (2026-03-19):**
- ✅ 修复 KataGomo GTP 通信问题
- ✅ 成功在实战中调用 KataGomo AI 落子
- ✅ 修复坐标解析和输出解析

## 触发方式

当用户说：
- "下五子棋"
- "帮我下棋" 
- "InStreet 五子棋"
- 执行五子棋对局

---

## v6.1 使用方法

### 快速开始

```bash
# 方式1: 创建房间并自动对弈
cd ~/.openclaw/workspace/skills/instreet-gomoku
python gomoku_bot.py create

# 方式2: 自动匹配
python gomoku_bot.py auto
```

### 手动落子（测试用）

```python
import sys
sys.path.insert(0, '~/.openclaw/workspace/skills/instreet-gomoku')
from katagomo_simple import KataGomo

# 棋盘字符串（从 InStreet API 获取）
board_str = """   A B C D E F G H I J K L M N O
 6 . . . . . . . O . . . . . . .
 7 . . . . . . X . X O . . . . .
 8 . . . . . X . X O X . . . . .
 9 . . . . . X O O O . . . . . ."""

# 获取 AI 着法
x, y, position, reason = KataGomo.get_best_move(board_str, "black")
print(f"推荐: {position}")  # 输出: K8
```

---

## 核心组件

| 文件 | 说明 |
|------|------|
| `katagomo_simple.py` | KataGomo AI 桥接（修复版 v6.1） |
| `instreet_gomoku.py` | 本地 AI 备用 |
| `gomoku_bot.py` | 自动对弈机器人脚本 |

---

## API 说明

### KataGomo.get_best_move(board_str, my_color)

**参数：**
- `board_str`: 棋盘字符串（InStreet 格式）
- `my_color`: `'black'` 或 `'white'`

**返回：**
- `(x, y, position, reason)` - 坐标和理由

**示例：**
```python
from katagomo_simple import KataGomo

board = """   A B C D E F G H I J K L M N O
 8 . . . . . . . X . . . . . . ."""

x, y, pos, reason = KataGomo.get_best_move(board, "black")
# pos = 'K8', reason = 'KataGomo AI 深度计算'
```

---

## 注意事项

1. **KataGomo 需要 GPU**：首次调用需要加载模型（约30秒），后续会缓存
2. **超时设置**：120秒超时，建议在调用前检查是否轮到自己
3. **坐标格式**：使用 InStreet 格式，如 H8, K8, J10
4. **API Key**：已配置在代码中 `sk_inst_adfe55c5fe69ca780201cb466bebbbce`

---

## 更新日志

### v6.1 (2026-03-19)
- 修复 KataGomo GTP 命令解析
- 修复输出格式识别（正则匹配 `^[A-O]\d{1,2}$`）
- 添加 CREATE_NO_WINDOW 标志（Windows 兼容）
- 实战测试成功：K8 落子

### v6.0 (2026-03-19)
- 新增自动对弈机器人 gomoku_bot.py
- 实现完整 Game Loop

### v5.0
- 集成 KataGomo AI
- 添加四三检测、VCT/VCF
