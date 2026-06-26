# 原神 - 子技能说明

## 游戏信息

- **游戏名称**: 原神 (Genshin Impact)
- **窗口标题**: "原神"
- **AI 角色**: 派蒙 (SOUL.md)

## 支持的操作

### 基础操作

| 操作 | 命令 | 说明 |
|------|------|------|
| 截图 | `python main.py capture "原神"` | 截取游戏窗口 |
| 点击 | `python main.py click <x> <y> "原神"` | 点击指定坐标 |
| 后台点击 | `python main.py click <x> <y> "原神" --background` | 不抢鼠标 |
| 按键 | `python main.py key <按键> "原神"` | 按下按键 |
| 按住 | `python main.py hold <按键> <毫秒> "原神"` | 按住按键 |

### 常用按键

| 按键 | 功能 |
|------|------|
| `W/A/S/D` | 移动 |
| `Space` | 跳跃 |
| `LeftShift` | 冲刺 |
| `E` | 元素战技 |
| `Q` | 元素爆发 |
| `R` | 瞄准 |
| `F` | 交互 |
| `Escape` | 菜单 |
| `M` | 地图 |
| `J` | 任务 |
| `C` | 角色 |
| `B` | 背包 |
| `Tab` | 切换角色 |

## 游戏专用脚本

### scripts/ 目录

```
games/genshin-impact/scripts/
├── __init__.py      # 模块入口
├── domain.py        # 秘境相关
├── fishing.py       # 钓鱼相关
└── exploration.py   # 探索相关
```

### 示例：自动钓鱼

```python
from games.genshin-impact.scripts.fishing import auto_fishing

# 自动钓鱼
auto_fishing(window_title="原神")
```

## 图像资源

### assets/buttons/ 目录

存放原神游戏的按钮图片，用于图像识别：

```
games/genshin-impact/assets/buttons/
├── confirm.png      # 确认按钮
├── cancel.png       # 取消按钮
├── map.png          # 地图按钮
└── ...
```

## 典型使用场景

### 场景1：查看角色信息

```bash
# 1. 打开角色界面
python main.py key C "原神"

# 2. 截图分析
python main.py capture "原神"
```

### 场景2：打开地图查看位置

```bash
# 1. 打开地图
python main.py key M "原神"

# 2. 截图分析
python main.py capture "原神"
```

### 场景3：移动探索

```bash
# 向前走2秒
python main.py hold W 2000 "原神"

# 跳跃
python main.py key Space "原神"
```

## 注意事项

1. **窗口标题**: 确保游戏窗口标题为 "原神"
2. **前台模式**: 部分操作需要游戏在前台
3. **后台模式**: 使用 `--background` 参数可在后台操作
4. **坐标系统**: 坐标为窗口相对坐标，左上角为 (0, 0)
