---
name: paimon-skill
description: 派蒙 - 原神特化 AI 游戏伴侣。让你的 OpenClaw 直接化身派蒙，实时看到你的游戏截图，给你实时指引，甚至能点击游戏按钮帮你操作。再也不用手动截图到百度贴吧问了——打开圣遗物等培养界面，让派蒙看到你的数值，给你培养建议。此模块为 play-any-game 子模块，依赖父模块核心能力。
version: 1.1.1
---

# 🌟 派蒙.skill - 原神特化 AI 游戏伴侣

> **play-any-game 已有 88+ 下载量，现推出原神特化版本！让你的 OpenClaw 直接化身派蒙，实时看到你的游戏画面，给你实时指引，甚至能点击游戏按钮帮你操作。再也不用手动截图到百度贴吧问了！**

## 🎯 项目定位

**派蒙是旅行者在提瓦特大陆最好的伙伴～**

当你在提瓦特冒险时遇到困难：
- 🤔 这个机关怎么解呀？
- 😵 这个Boss打不过怎么办？
- 🤷 找不到NPC在哪里？
- 😕 不知道这个界面怎么操作？
- 🎯 想刷材料但不知道去哪里？

派蒙可以：
1. **截图分析** - 看到你的游戏画面，理解当前状态
2. **解答问题** - 告诉你该怎么解决
3. **简单操作** - 帮你点击界面、解决问题
4. **提供建议** - 角色培养、圣遗物搭配、任务攻略

## 🔄 核心设计理念

**每次操作都有截图，让派蒙能看到操作后的效果，然后继续下一步操作。**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   派蒙分析截图 ──→ 执行操作 ──→ 自动截图 ──→ 返回给派蒙    │
│        ↑                                           │        │
│        └───────────────────────────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📝 OpenClaw 集成说明

### 🌈 SOUL 替换提示

**重要提示！** 本模块为 play-any-game 的原神特化版本，加载 SOUL 后替换父模块的对应游戏设定：

```bash
# 加载派蒙的 SOUL 设定（paimon-skill 子模块）
.trae/skills/paimon-skill/games/genshin-impact/SOUL.md
```

派蒙的角色设定就在 `games/genshin-impact/SOUL.md` 文件里哦～ 加载后替换OpenClaw原有的SOUL.md，AI 会化身为可爱的派蒙，用派蒙的语气与你交流！

### 🎮 技能调用方式

OpenClaw 应通过以下方式调用本技能：

```bash
# 截图（自动截取原神窗口）
python main.py screenshot

# 截取指定窗口（如果需要）
python main.py capture "原神"

# 点击坐标（相对于窗口）
python main.py click 540 820 "原神"

# 后台点击（不抢鼠标）
python main.py click 540 820 "原神" --background

# 按键
python main.py key Space "原神"

# 按住按键
python main.py hold W 1000 "原神"

# 列出所有窗口
python main.py windows

# 查找按钮
python main.py find confirm "原神"

# 通过文字描述点击
python main.py click_text "确认按钮" "原神"
```

### 📊 输出格式处理

技能返回标准JSON格式，OpenClaw 应解析以下字段：

- `action`: 操作类型（screenshot、capture、click、find 等）
- `screenshotPath`: 截图文件路径（相对于skill目录）
- `timestamp`: 操作时间戳
- 其他操作特定字段（如 click 的 x、y 坐标）

## 🎮 使用方式

### 基础命令

```bash
# 截图
python main.py screenshot

# 截取原神窗口
python main.py capture "原神"

# 点击坐标（相对于窗口）
python main.py click 540 820 "原神"

# 后台点击（不抢鼠标）
python main.py click 540 820 "原神" --background

# 按键
python main.py key Space "原神"

# 按住按键
python main.py hold W 1000 "原神"

# 列出所有窗口
python main.py windows
```

### 按钮识别

```bash
# 查找按钮位置
python main.py find confirm "原神"

# 查找所有可识别按钮
python main.py findall "原神"

# 列出可用按钮模板
python main.py buttons genshin-impact

# 通过文字描述点击（使用多模态AI）
python main.py click_text "确认按钮" "原神"
```

## 🎯 支持的操作

### 基础操作

| 操作 | 命令 | 说明 |
|------|------|------|
| 截图 | `python main.py capture "原神"` | 截取游戏窗口 |
| 点击 | `python main.py click <x> <y> "原神"` | 点击指定坐标 |
| 后台点击 | `python main.py click <x> <y> "原神" --background` | 不抢鼠标 |
| 按键 | `python main.py key <按键> "原神"` | 按下按键 |
| 按住 | `python main.py hold <按键> <毫秒> "原神"` | 按住按键 |

### 原神常用按键

| 按键 | 功能 |
|------|------|
| `W/A/S/D` | 移动 |
| `Space` | 跳跃/攀爬 |
| `LeftShift` | 冲刺 |
| `E` | 元素战技 |
| `Q` | 元素爆发 |
| `R` | 瞄准模式 |
| `F` | 交互/拾取 |
| `Escape` | 打开菜单 |
| `M` | 打开地图 |
| `J` | 打开任务 |
| `C` | 打开角色 |
| `B` | 打开背包 |
| `Tab` | 切换角色 |
| `V` | 追踪任务 |
| `T` | 查看教程 |
| `L` | 打开队伍配置 |
| `1-4` | 切换队伍角色 |
| `Alt` | 显示鼠标 |

## 🌟 典型使用场景

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
```

### 场景4：战斗操作

```bash
# 释放元素战技
python main.py key E "原神"

# 释放元素爆发
python main.py key Q "原神"
```

## 📁 目录结构

```
.trae/skills/paimon-skill/
├── scripts/               # Python 核心模块
│   ├── __init__.py        # 模块入口
│   ├── click.py           # 点击功能（参考 BetterGI 实现）
│   ├── keyboard.py        # 键盘功能
│   ├── screenshot.py      # 截图功能
│   ├── window.py          # 窗口管理
│   ├── recognition.py     # 图像识别
│   ├── config.py          # 配置管理
│   └── gui_agent/         # 多模态 AI 识图模块
│       ├── base.py        # 抽象基类
│       ├── aliyun.py      # 阿里云 GUI-Plus 实现
│       └── factory.py     # 工厂模式
├── games/                 # 游戏配置
│   ├── genshin-impact/    # 原神
│   │   ├── SOUL.md        # 派蒙角色设定 🌟 重要！
│   │   ├── SKILL.md       # 原神子技能说明
│   │   └── assets/        # 图像资源
│   │       └── buttons/   # 按钮图片
│   └── games.json         # 游戏配置
├── screenshots/           # 截图存储目录
├── main.py                # CLI 入口
├── requirements.txt       # Python 依赖
├── SKILL.md               # 本文件
└── README.md              # 项目说明
```

## 🔍 按钮识别

### 可用按钮模板

项目包含大量原神游戏按钮模板，存放在 `games/genshin-impact/assets/buttons/` 目录：

- `confirm.png` - 确认按钮
- `cancel.png` - 取消按钮
- `map.png` - 地图按钮
- `teleport.png` - 传送按钮
- `paimon_menu.png` - 派蒙菜单
- `inventory.png` - 背包按钮
- `character_guide.png` - 角色按钮
- ... 等200+个按钮模板

### 使用按钮识别

```python
from scripts.recognition import find_button
from PIL import Image

# 加载截图
screenshot = Image.open('screenshot.png')

# 查找按钮
result = find_button(screenshot, 'genshin-impact', 'confirm')
if result:
    print(f"按钮位置: ({result['x']}, {result['y']})")
    print(f"置信度: {result['confidence']}")
```

## ⚙️ 配置说明

### 配置 GUI Agent API Key

```bash
# 设置阿里云 API Key（用于 click_text 功能）
python main.py config --set-api-key YOUR_API_KEY --provider aliyun

# 查看当前配置
python main.py config --show
```

### 环境变量

```bash
# 设置 API Key
set DASHSCOPE_API_KEY=your_api_key_here
```

## 🛠️ 技术规范

### 环境要求

- Python 3.8+
- Windows 操作系统（使用 Win32 API 实现截图和点击）
- **本机运行**：技能需要在本机直接运行，不能在沙箱环境中运行

### 安装步骤

```bash
# 安装依赖
pip install -r requirements.txt

# 测试运行
python main.py screenshot
python main.py capture "原神"
```

### 点击实现方式

参考 BetterGI 开源项目实现了两种点击模式：

1. **前台点击模式** (默认)
   - 使用 `mouse_event` API 模拟真实鼠标操作
   - 需要窗口在前台
   - 会移动真实鼠标光标
   - 适用于大多数游戏

2. **后台点击模式** (`--background` 参数)
   - 使用 `PostMessage` 发送窗口消息
   - 不抢夺鼠标，可在后台运行
   - 部分游戏可能拦截此类消息

## 🔒 安全注意事项

- **游戏窗口可见**：派蒙需要游戏窗口在可见状态才能分析画面
- **辅助性质**：派蒙只是辅助旅行者解决问题，不是全自动挂机
- **策略判断**：需要真正策略判断的高难度内容仍需旅行者自己操作

## 🐛 故障排除

### 常见问题

1. **截图失败**：确保游戏窗口在可见状态
2. **点击无反应**：
   - 前台模式：检查坐标是否正确，确保游戏窗口在前台
   - 后台模式：部分游戏可能拦截 PostMessage，尝试使用前台模式
3. **坐标偏移**：确保使用的是窗口相对坐标，而非屏幕绝对坐标
4. **性能问题**：减少截图频率，优化循环逻辑
5. **Python 依赖问题**：确保已安装 `pywin32` 和 `Pillow`

### 日志和调试

- 查看控制台输出获取详细信息
- 检查 `screenshots/` 目录的截图文件
- 使用 `python main.py windows` 查看所有可用窗口

## 📚 技术参考

本项目点击功能参考了 [BetterGI](https://github.com/babalae/better-genshin-impact) 开源项目的实现方式：

- **前台点击**：使用 `mouse_event` API 模拟真实鼠标操作
- **后台点击**：使用 `PostMessage` 发送窗口消息

感谢 BetterGI 项目的开源贡献！

## 🌐 开源仓库

- **派蒙.skill**：[https://github.com/CGandGameEngineLearner/paimon-skill.git](https://github.com/CGandGameEngineLearner/paimon-skill.git)
- **play-any-game**：[https://github.com/CGandGameEngineLearner/play-any-game.git](https://github.com/CGandGameEngineLearner/play-any-game.git)

---

## 🔗 与 play-any-game 的关系

本模块是 **[play-any-game](https://clawhub.com/skills/play-any-game)** 的**原神特化子模块**，依赖父模块的核心能力：

- **父模块** `play-any-game`：通用游戏伴侣，支持多款游戏（崩坏：星穹铁道等），提供截图、点击、键盘等基础操作能力
- **本模块** `paimon-skill`：原神专精，定制了派蒙 SOUL 角色设定、原神按钮模板、游戏特定逻辑（Alt 键等）

### 激活方式

当用户明确提到原神相关场景时（如"帮我过这个原神任务"、"派蒙帮我"），使用本模块；其他游戏场景使用父模块 `play-any-game`。

### SOUL 路径

```
.trae/skills/paimon-skill/games/genshin-impact/SOUL.md
```

---

**派蒙会一直在你身边，旅行者！让我们一起探索提瓦特大陆吧！** 🌟
