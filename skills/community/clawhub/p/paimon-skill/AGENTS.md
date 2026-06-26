# 项目规则 - Play Any Game

## 项目定位

**Play Any Game 是一个 AI 游戏伴侣助手技能，不是游戏代肝工具。**

当玩家在游戏中遇到困难、卡关、不知道怎么操作时：
- 🤔 AI 可以截图分析游戏画面，理解当前状态
- 💡 AI 可以解答玩家的问题，告诉玩家该怎么解决
- 🖱️ AI 可以简单操作界面，帮玩家点击按钮、解决问题

**核心理念**：AI 是玩家的游戏伙伴，在玩家需要时伸出援手，而不是全自动挂机代肝。

## 核心设计理念

**每次操作都有截图，让 AI 能看到操作后的效果，然后继续下一步操作。**

这是本项目的核心设计原则：

1. **可视化反馈循环** - 每次点击、按键等操作后，自动截图并返回给 AI
2. **AI 决策驱动** - AI 通过分析截图来判断下一步操作，而非预设脚本
3. **闭环控制** - 操作 → 截图 → AI 分析 → 下一步操作，形成完整的控制闭环

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   AI 分析截图 ──→ 执行操作 ──→ 自动截图 ──→ 返回给 AI      │
│        ↑                                           │        │
│        └───────────────────────────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

这种设计使得：
- AI 能够实时看到操作效果
- AI 能够根据游戏状态做出智能决策
- 无需预设复杂的脚本逻辑
- 支持各种游戏场景的灵活应对

## 按钮识别方案

使用多模态大模型（如阿里云 GUI-Plus）直接识别界面元素：

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

**配置方式：**
```bash
# 设置 API Key
python main.py config --set-api-key YOUR_API_KEY

# 或设置环境变量
set DASHSCOPE_API_KEY=YOUR_API_KEY
```

## 核心功能

- 🤔 **画面分析** - AI 通过截图理解游戏当前状态
- 💡 **问题解答** - 告诉玩家该怎么解决遇到的困难
- 🖱️ **简单操作** - 帮玩家点击界面、解决问题
- 🎮 **多游戏支持** - 原神、崩坏星穹铁道等各类游戏
- 🔍 **AI 识图点击** - 通过自然语言描述定位并点击按钮

## 工作原理

```
玩家遇到困难 → AI截图分析画面 → 理解当前状态 → 解答问题/简单操作 → 解决问题
```

## OpenClaw 集成要求

### 1. 技能调用方式

OpenClaw 应通过以下方式调用本技能：

```bash
# 截图
python main.py screenshot

# 截取指定窗口
python main.py capture "游戏窗口标题"

# AI 识图点击（主要方式）
python main.py click_text "按钮描述" "原神"

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

# 配置管理
python main.py config --set-api-key YOUR_KEY
python main.py config --show
python main.py config --list-agents

# 游戏会话管理（SOUL 切换）
python main.py game list
python main.py game start 原神
python main.py game end
python main.py game current
```

### 2. 输出格式处理

技能返回标准JSON格式，OpenClaw 应解析以下字段：

- `action`: 操作类型（screenshot、capture、click、click_text）
- `screenshotPath`: 截图文件路径（相对于skill目录）
- `afterScreenshotPath`: 点击后的截图路径
- `timestamp`: 操作时间戳
- 其他操作特定字段（如 click 的 x、y 坐标）

### 3. 游戏SOUL使用

OpenClaw 应支持加载和使用 `games/` 目录下的游戏定制SOUL文件：

```
games/
├── games.json            # 游戏配置文件
├── default/              # 默认 SOUL（退出游戏时恢复）
│   └── SOUL.md          # OpenClaw 默认人设
├── genshin-impact/       # 原神
│   ├── SOUL.md          # 派蒙角色设定
│   └── SKILL.md         # 原神子技能说明
└── honkai-starrail/     # 崩坏：星穹铁道
    ├── SOUL.md          # 三月七角色设定
    └── SKILL.md         # 星铁子技能说明
```

#### SOUL 切换流程

```
┌─────────────────────────────────────────────────────────────┐
│                    SOUL 切换流程                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  用户: "我要玩原神"                                          │
│       ↓                                                     │
│  OpenClaw 调用: python main.py game start 原神              │
│       ↓                                                     │
│  返回: { soulPath: "games/genshin-impact/SOUL.md" }         │
│       ↓                                                     │
│  OpenClaw 读取 SOUL.md → 替换自己的系统提示                   │
│       ↓                                                     │
│  AI 化身为派蒙与用户交互                                      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  用户: "不玩了" / "退出游戏"                                  │
│       ↓                                                     │
│  OpenClaw 调用: python main.py game end                     │
│       ↓                                                     │
│  返回: { soulPath: "games/default/SOUL.md" }                │
│       ↓                                                     │
│  OpenClaw 恢复默认 SOUL                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### game 命令

```bash
# 列出支持的游戏
python main.py game list

# 开始游戏会话（切换到对应 SOUL）
python main.py game start 原神
python main.py game start genshin-impact
python main.py game start 星铁

# 结束游戏会话（恢复默认 SOUL）
python main.py game end

# 显示当前游戏信息
python main.py game current
```

#### 返回格式

**game start 返回：**
```json
{
  "action": "game",
  "subaction": "start",
  "gameId": "genshin-impact",
  "gameName": "原神",
  "character": "派蒙",
  "windowTitle": "原神",
  "soulPath": "games/genshin-impact/SOUL.md"
}
```

**game end 返回：**
```json
{
  "action": "game",
  "subaction": "end",
  "soulPath": "games/default/SOUL.md",
  "character": "OpenClaw"
}
```

#### OpenClaw 实现要点

1. **监听用户意图**：当用户说"我要玩XX游戏"、"帮我在XX游戏里..."时，识别游戏名称
2. **调用 game start**：调用 `python main.py game start <游戏名>` 获取 SOUL 路径
3. **读取并替换 SOUL**：读取 `soulPath` 指向的 SOUL.md 文件内容，替换自己的系统提示
4. **保持角色**：在游戏会话期间，始终保持对应角色的语气和性格
5. **监听退出意图**：当用户说"不玩了"、"退出游戏"时，调用 `python main.py game end`
6. **恢复默认**：读取默认 SOUL.md 并恢复

#### 支持的游戏关键词

| 游戏 | 关键词 |
|------|--------|
| 原神 | 原神、genshin、派蒙、paimon、genshin-impact |
| 崩坏：星穹铁道 | 星穹铁道、星铁、starrail、崩铁、三月七、honkai-starrail |

### 4. 截图管理

- OpenClaw 应定期清理 `screenshots/` 目录，避免存储空间占用过大
- 应保留关键操作的截图用于调试和分析

### 5. API Key 管理

- API Key 存储在 `config.json` 中
- `config.json` 已添加到 `.gitignore`，不会泄露到 git
- 支持通过环境变量 `DASHSCOPE_API_KEY` 配置

## 安全注意事项

- **游戏窗口可见**：AI需要游戏窗口在可见状态才能分析画面
- **辅助性质**：AI只是辅助玩家解决问题，不是全自动挂机
- **策略判断**：需要真正策略判断的高难度内容仍需玩家自己操作
- **API Key 保护**：不要将 API Key 提交到 git 仓库

## 技术规范

### 环境要求

- Python 3.8+
- Windows 操作系统（使用 Win32 API 实现截图和点击）
- **本机运行**：技能需要在本机直接运行，不能在沙箱环境中运行，因为需要访问本机的窗口系统和进程

### 安装步骤

```bash
# 安装依赖
cd .trae/skills/play-any-game
pip install -r requirements.txt

# 配置 API Key
python main.py config --set-api-key YOUR_API_KEY

# 测试运行
python main.py screenshot
python main.py click_text "测试按钮" "原神" --dry-run
```

### 目录结构

```
.trae/skills/play-any-game/
├── scripts/               # Python 核心模块
│   ├── __init__.py        # 模块入口
│   ├── click.py           # 点击功能
│   ├── keyboard.py        # 键盘功能
│   ├── screenshot.py      # 截图功能
│   ├── window.py          # 窗口管理
│   ├── config.py          # 配置管理
│   └── gui_agent/         # 多模态 AI 识图模块
│       ├── base.py        # 抽象基类
│       ├── aliyun.py      # 阿里云 GUI-Plus 实现
│       └── factory.py     # 工厂模式
├── games/                 # 游戏定制目录（按游戏分类）
│   ├── games.json         # 游戏配置文件
│   ├── default/           # 默认 SOUL（退出游戏时恢复）
│   │   └── SOUL.md       # OpenClaw 默认人设
│   ├── genshin-impact/    # 原神
│   │   ├── SOUL.md        # 派蒙角色设定
│   │   └── SKILL.md       # 原神子技能说明
│   └── honkai-starrail/   # 崩坏：星穹铁道
│       ├── SOUL.md        # 三月七角色设定
│       └── SKILL.md       # 星铁子技能说明
├── screenshots/           # 截图存储目录
├── config.json            # 配置文件（API Key 等）
├── main.py                # CLI 入口
├── requirements.txt       # Python 依赖
├── SKILL.md               # 技能详细文档
└── AGENTS.md              # 项目规则（本文件）
```

### 点击实现方式

本项目实现了两种点击模式：

1. **前台点击模式** (默认)
   - 使用 `mouse_event` API 模拟真实鼠标操作
   - 需要窗口在前台
   - 会移动真实鼠标光标
   - 适用于大多数游戏

2. **后台点击模式** (`--background` 参数)
   - 使用 `PostMessage` 发送窗口消息
   - 不抢夺鼠标，可在后台运行
   - 部分游戏可能拦截此类消息

### 原神特殊处理

原神游戏中所有 UI 点击操作需要同时按住 Alt 键：

- 点击前自动按住 Alt 键
- 点击完成后释放 Alt 键
- 代码已自动处理，无需手动操作

## GUI Agent 架构

### 抽象层设计

支持多种多模态模型，便于扩展：

```python
# 基类
class BaseGUIAgent(ABC):
    def analyze(self, screenshot, instruction) -> GUIAgentResult
    def click_element(self, screenshot, text) -> GUIAgentResult

# 实现
class AliyunGUIAgent(BaseGUIAgent):  # 阿里云 GUI-Plus
class OpenAIGUIAgent(BaseGUIAgent):  # 预留 OpenAI
class GoogleGUIAgent(BaseGUIAgent):  # 预留 Google
```

### 添加新的 GUI Agent

1. 继承 `BaseGUIAgent` 类
2. 实现 `analyze()` 方法
3. 在 `factory.py` 中注册

```python
from scripts.gui_agent import register_agent

class NewGUIAgent(BaseGUIAgent):
    @property
    def name(self) -> str:
        return "new-model"
    
    def analyze(self, screenshot, instruction, **kwargs):
        # 实现调用新模型 API
        pass

register_agent("new-model", NewGUIAgent)
```

## 扩展指南

### 添加新游戏支持

1. 在 `games/` 目录下创建游戏文件夹（如 `games/arknights/`）
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

## 故障排除

### 常见问题

1. **截图失败**：确保游戏窗口在可见状态
2. **点击无反应**：
   - 前台模式：检查坐标是否正确，确保游戏窗口在前台
   - 后台模式：部分游戏可能拦截 PostMessage，尝试使用前台模式
3. **坐标偏移**：确保使用的是窗口相对坐标，而非屏幕绝对坐标
4. **性能问题**：减少截图频率，优化循环逻辑
5. **Python 依赖问题**：确保已安装 `pywin32`、`Pillow` 和 `openai`
6. **API Key 未配置**：运行 `python main.py config --set-api-key YOUR_KEY`

### 日志和调试

- 查看控制台输出获取详细信息
- 检查 `screenshots/` 目录的截图文件
- 使用 `python main.py windows` 查看所有可用窗口
- 使用 `--dry-run` 参数仅分析不执行

## 版本兼容性

- 支持 OpenClaw v2.0+
- Python 3.8+
- Windows 10/11
- 与其他游戏自动化技能兼容
- 定期更新以支持新游戏和新功能

## 技术参考

- [阿里云 GUI-Plus 文档](https://help.aliyun.com/zh/model-studio/gui-automation)
