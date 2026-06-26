# 崩坏：星穹铁道 - 子技能说明

## 游戏信息

- **游戏名称**: 崩坏：星穹铁道 (Honkai: Star Rail)
- **窗口标题**: "崩坏：星穹铁道"
- **AI 角色**: 三月七 (SOUL.md)

## 支持的操作

### 基础操作

| 操作 | 命令 | 说明 |
|------|------|------|
| 截图 | `python main.py capture "崩坏：星穹铁道"` | 截取游戏窗口 |
| 点击 | `python main.py click <x> <y> "崩坏：星穹铁道"` | 点击指定坐标 |
| 后台点击 | `python main.py click <x> <y> "崩坏：星穹铁道" --background` | 不抢鼠标 |
| 按键 | `python main.py key <按键> "崩坏：星穹铁道"` | 按下按键 |
| 按住 | `python main.py hold <按键> <毫秒> "崩坏：星穹铁道"` | 按住按键 |

### 常用按键

| 按键 | 功能 |
|------|------|
| `W/A/S/D` | 移动 |
| `Space` | 跳跃/确认 |
| `LeftShift` | 冲刺 |
| `E` | 秘技 |
| `R` | 进入战斗 |
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
games/honkai-starrail/scripts/
├── __init__.py      # 模块入口
├── simulated.py     # 模拟宇宙相关
├── forgotten.py     # 忘却之庭相关
└── exploration.py   # 探索相关
```

## 图像资源

### assets/buttons/ 目录

存放星铁游戏的按钮图片，用于图像识别：

```
games/honkai-starrail/assets/buttons/
├── confirm.png      # 确认按钮
├── cancel.png       # 取消按钮
├── map.png          # 地图按钮
└── ...
```

## 典型使用场景

### 场景1：查看角色信息

```bash
# 1. 打开角色界面
python main.py key C "崩坏：星穹铁道"

# 2. 截图分析
python main.py capture "崩坏：星穹铁道"
```

### 场景2：打开地图查看位置

```bash
# 1. 打开地图
python main.py key M "崩坏：星穹铁道"

# 2. 截图分析
python main.py capture "崩坏：星穹铁道"
```

### 场景3：移动探索

```bash
# 向前走2秒
python main.py hold W 2000 "崩坏：星穹铁道"

# 交互
python main.py key F "崩坏：星穹铁道"
```

## 注意事项

1. **窗口标题**: 确保游戏窗口标题为 "崩坏：星穹铁道"
2. **前台模式**: 部分操作需要游戏在前台
3. **后台模式**: 使用 `--background` 参数可在后台操作
4. **坐标系统**: 坐标为窗口相对坐标，左上角为 (0, 0)
