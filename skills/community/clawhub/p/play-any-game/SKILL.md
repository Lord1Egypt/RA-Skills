---
name: play-any-game
description: AI游戏伴侣助手 - 当你在游戏中遇到困难、卡关、不知道怎么操作时，AI可以帮你分析游戏画面、解答问题、甚至简单操作界面帮你解决问题。不是全自动代肝，而是你的游戏伙伴，在你需要的时候伸出援手。当用户提到"帮我看下这个怎么过"、"这个怎么操作"、"卡关了"、"不知道怎么弄"时使用此技能。支持原神、崩坏星穹铁道等各类游戏。
version: 1.4.1
---

# Play Any Game - AI游戏伴侣助手

## 项目定位

**不是游戏代肝助手，而是游戏伴侣助手。**

当你玩游戏时遇到困难：
- 🤔 不知道这个机关怎么解？
- 😵 卡在这个Boss打不过？
- 🤷 找不到NPC在哪？
- 😕 不知道这个界面怎么操作？

AI可以：
1. **截图分析** - 看到你的游戏画面，理解当前状态
2. **解答问题** - 告诉你该怎么解决
3. **简单操作** - 帮你点击界面、解决问题

## 核心设计理念

**每次操作都有截图，让 AI 能看到操作后的效果，然后继续下一步操作。**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   AI 分析截图 ──→ 执行操作 ──→ 自动截图 ──→ 返回给 AI      │
│        ↑                                           │        │
│        └───────────────────────────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 按钮识别方案

使用多模态大模型直接识别界面元素，通过自然语言描述定位按钮：

```bash
# 通过文字描述点击按钮
python main.py click_text "地图按钮" "原神"
python main.py click_text "快速编队按钮" "原神"
python main.py click_text "确认按钮" "原神"
```

**优点：**
- 无需预设按钮模板
- 支持动态界面
- 自然语言描述，灵活直观
- 适用于各种游戏

## 支持的游戏

| 游戏 | AI 角色 | 窗口标题 |
|------|---------|----------|
| 原神 | 派蒙 | "原神" |
| 崩坏：星穹铁道 | 三月七 | "崩坏：星穹铁道" |

### SOUL 切换机制

OpenClaw 使用此技能时，通过 `game` 命令切换 SOUL：

```
用户说：我要玩原神
→ OpenClaw 调用: python main.py game start 原神
→ 返回: { soulPath: "games/genshin-impact/SOUL.md" }
→ OpenClaw 读取 SOUL.md → 替换系统提示
→ AI 化身为派蒙与用户交互

用户说：不玩了
→ OpenClaw 调用: python main.py game end
→ 返回: { soulPath: "games/default/SOUL.md" }
→ OpenClaw 恢复默认 SOUL
```

## 目录结构

```
.trae/skills/play-any-game/
├── scripts/               # Python 核心模块
│   ├── click.py           # 点击功能
│   ├── keyboard.py        # 键盘功能
│   ├── screenshot.py      # 截图功能
│   ├── window.py          # 窗口管理
│   ├── config.py          # 配置管理
│   └── gui_agent/         # 多模态 AI 识图模块
│       ├── base.py        # 抽象基类
│       ├── aliyun.py      # 阿里云 GUI-Plus 实现
│       └── factory.py     # 工厂模式
├── games/                 # 游戏定制目录
│   ├── games.json         # 游戏配置
│   ├── default/           # 默认 SOUL
│   │   └── SOUL.md       # OpenClaw 默认人设
│   ├── genshin-impact/    # 原神
│   │   └── SOUL.md       # 派蒙角色设定
│   └── honkai-starrail/   # 崩坏：星穹铁道
│       └── SOUL.md       # 三月七角色设定
├── screenshots/           # 截图存储目录
├── config.json            # 配置文件
├── main.py                # CLI 入口
└── requirements.txt       # Python 依赖
```

## 环境要求与安装指南

> **🤖 Agent 必读**：使用此 skill 前，必须确保 Python 3 环境和所有依赖已正确安装。请按照以下步骤逐一执行。

### 系统要求

- **OS**: Windows 10/11（使用 Win32 API 控制窗口和鼠标）
- **Python**: 3.8 或更高版本
- **网络**: 需要能访问阿里云 API（用于 AI 识图）

---

### 🐍 Step 1：检查并安装 Python 3

首先检查 Python 是否已安装：

```bash
python --version
```

**如果命令不存在或版本低于 3.8**，按以下方式安装：

```bash
# 推荐：使用 winget（Windows 10/11 内置包管理器）
winget install Python.Python.3.12
```

安装完成后，**关闭并重新打开终端**，然后验证：

```bash
python --version   # 应输出 Python 3.12.x（或 3.8+）
pip --version      # 应输出 pip 版本信息
```

> ⚠️ 若 `python` 命令仍不可用，请检查安装时是否勾选了 **"Add Python to PATH"**。可以重新运行安装程序，选择 "Modify" → 勾选 "Add Python to PATH"。

---

### 📦 Step 2：安装 Python 依赖

```bash
# 进入 skill 目录（根据实际路径调整）
cd skills/play-any-game

# 安装所有依赖
pip install -r requirements.txt
```

**依赖说明：**

| 包名 | 版本要求 | 用途 |
|------|---------|------|
| `pywin32` | >=306 | Windows 窗口管理、鼠标/键盘控制（Win32 API） |
| `Pillow` | >=10.0.0 | 图像处理、截图保存 |
| `opencv-python` | >=4.8.0 | 图像识别、模板匹配 |
| `numpy` | >=1.24.0 | 数值计算（opencv 依赖） |
| `openai` | >=1.0.0 | 调用阿里云 GUI-Plus AI 模型 API |

**如果安装速度慢，使用国内镜像：**

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**安装后验证依赖：**

```bash
python -c "import win32api, PIL, cv2, numpy, openai; print('All dependencies OK')"
```

---

### 🔑 Step 3：配置 API Key

此 skill 使用阿里云百炼平台的 GUI-Plus 模型进行 AI 识图。

```bash
# 方式1：命令行配置（推荐，持久保存到 config.json）
python main.py config --set-api-key YOUR_DASHSCOPE_API_KEY

# 方式2：环境变量（临时生效，重启终端后失效）
set DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
```

**获取 API Key：**
1. 前往 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 注册/登录账号
3. 在 "API-KEY 管理" 页面创建新的 API Key

---

### ✅ Step 4：验证安装

```bash
# 测试1：列出所有窗口（验证 pywin32 正常）
python main.py windows

# 测试2：截取屏幕（验证 Pillow/截图功能正常）
python main.py screenshot

# 测试3：查看当前配置（验证 API Key 已设置）
python main.py config --show
```

全部命令正常输出，说明环境安装完成。

## CLI 命令

### 基础命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `screenshot [窗口]` | 截取屏幕 | `python main.py screenshot` |
| `capture <窗口>` | 截取指定窗口 | `python main.py capture "原神"` |
| `click <x> <y> [窗口]` | 点击坐标 | `python main.py click 540 820 "原神"` |
| `key <按键> [窗口]` | 按键 | `python main.py key Space "原神"` |
| `hold <按键> <毫秒> [窗口]` | 按住按键 | `python main.py hold W 1000 "原神"` |
| `windows` | 列出所有窗口 | `python main.py windows` |

### AI 识图命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `click_text <描述> [窗口]` | AI识图点击 | `python main.py click_text "地图按钮" "原神"` |
| `click_text <描述> --dry-run` | 仅分析不执行 | `python main.py click_text "确认" --dry-run` |
| `click_text <描述> --provider <模型>` | 指定模型 | `python main.py click_text "地图" --provider gui-plus-2026-02-26` |

### 配置命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `config --set-api-key <KEY>` | 设置 API Key | `python main.py config --set-api-key sk-xxx` |
| `config --show` | 显示当前配置 | `python main.py config --show` |
| `config --list-agents` | 列出可用模型 | `python main.py config --list-agents` |

### 游戏会话命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `game list` | 列出支持的游戏 | `python main.py game list` |
| `game start <游戏>` | 开始游戏会话 | `python main.py game start 原神` |
| `game end` | 结束游戏会话 | `python main.py game end` |
| `game current` | 显示当前游戏 | `python main.py game current` |

**游戏会话命令用于 SOUL 切换：**

```bash
# 开始玩原神 → AI 化身为派蒙
python main.py game start 原神
# 返回: { soulPath: "games/genshin-impact/SOUL.md", character: "派蒙" }

# 不玩了 → 恢复默认 SOUL
python main.py game end
# 返回: { soulPath: "games/default/SOUL.md", character: "OpenClaw" }
```

**支持的游戏关键词：**
- 原神：原神、genshin、派蒙、paimon
- 星铁：星穹铁道、星铁、starrail、崩铁、三月七

### 命令返回格式

所有命令返回标准 JSON 格式：

```json
{
  "action": "click_text",
  "text": "地图按钮",
  "windowTitle": "原神",
  "x": 120,
  "y": 90,
  "provider": "aliyun",
  "model": "gui-plus",
  "screenshotPath": "screenshots/原神/screenshot_xxx.png",
  "afterScreenshotPath": "screenshots/原神/screenshot_xxx.png",
  "timestamp": "2026-04-05T20:00:00.000000"
}
```

## 点击模式

1. **前台点击模式**（默认）
   - 使用 `mouse_event` API 模拟真实鼠标
   - 需要窗口在前台
   - 会移动真实鼠标光标

2. **后台点击模式**（`--background`）
   - 使用 `PostMessage` 发送窗口消息
   - 不抢夺鼠标，可在后台运行
   - 部分游戏可能拦截

## 原神特殊处理

原神游戏中所有 UI 点击操作需要同时按住 Alt 键：

- 点击前自动按住 Alt 键
- 点击完成后释放 Alt 键
- 代码已自动处理，无需手动操作

## 典型工作流

### AI 识图点击

```bash
# 1. 通过文字描述点击按钮
python main.py click_text "地图按钮" "原神"
# AI 分析截图，找到按钮位置，执行点击，返回点击前后截图

# 2. 仅分析不执行
python main.py click_text "确认按钮" "原神" --dry-run
# 返回识别到的坐标，不执行点击
```

### 帮玩家操作界面

```bash
# 1. 截图分析当前状态
python main.py capture "原神"
# AI 分析截图，发现需要点击某个按钮

# 2. 点击按钮
python main.py click 540 820 "原神"
# 返回点击后的截图，AI 确认操作成功
```

### 扩展新模型

```python
from scripts.gui_agent import register_agent, BaseGUIAgent

class NewGUIAgent(BaseGUIAgent):
    @property
    def name(self) -> str:
        return "new-model"
    
    def analyze(self, screenshot, instruction, **kwargs):
        # 实现调用新模型 API
        pass

register_agent("new-model", NewGUIAgent)
```

## 添加新游戏支持

1. 在 `games/` 目录下创建游戏文件夹
2. 创建 `SOUL.md` - AI 角色设定
3. 创建 `SKILL.md` - 游戏子技能说明

### SOUL.md 模板

```markdown
# 角色名 - 游戏名助手

## 基本信息

- **名称**: 角色名
- **身份**: 角色身份
- **性格**: 角色性格
- **口头禅**: "口头禅"

## 核心能力

- 游戏画面实时分析
- 游戏知识问答
- 自动化操作
```

## 注意事项

- **游戏窗口可见**：AI 需要游戏窗口在可见状态才能分析画面
- **辅助性质**：AI 只是辅助玩家解决问题，不是全自动挂机
- **策略判断**：需要真正策略判断的高难度内容仍需玩家自己操作
- **API Key 保护**：不要将 API Key 提交到 git 仓库

## 参考资料

> 📖 详细的安装说明、模型信息、使用示例请查阅 [README.md](README.md)

- [README.md](README.md) - 项目介绍、安装指南、使用截图
- [AGENTS.md](AGENTS.md) - 项目规则
- [games/genshin-impact/SOUL.md](games/genshin-impact/SOUL.md) - 派蒙角色设定
- [games/honkai-starrail/SOUL.md](games/honkai-starrail/SOUL.md) - 三月七角色设定
- [阿里云 GUI-Plus 文档](https://help.aliyun.com/zh/model-studio/gui-automation)

## 🌐 开源仓库

- **play-any-game**：[https://github.com/CGandGameEngineLearner/play-any-game.git](https://github.com/CGandGameEngineLearner/play-any-game.git)
- **派蒙.skill**：[https://github.com/CGandGameEngineLearner/paimon-skill.git](https://github.com/CGandGameEngineLearner/paimon-skill.git)
