# 🌟 派蒙.skill - 原神特化 AI 游戏伴侣

> **play-any-game 已有 88+ 下载量，现推出原神特化版本！让你的 OpenClaw 直接化身派蒙，实时看到你的游戏截图，给你实时指引，甚至能点击游戏按钮帮你操作。再也不用手动截图到百度贴吧问了——打开圣遗物等培养界面，让派蒙看到你的数值，给你培养建议。**

## 🚀 快速开始

```markdown
旅行者：派蒙，我卡在这个机关谜题了，不知道怎么解...
派蒙：嗯嗯，让派蒙看一眼！
    - 截图分析当前画面
    - 识别机关状态和可交互元素
    - 给出解题步骤说明
    - 如需要可直接帮你点击操作
搞定啦！这个机关要先激活左边的元素方碑，再点中间的传送阵～
哇~旅行者好厉害！
```

## 📸 截图展示

### 角色人设 - 派蒙
派蒙会用她活泼可爱的语气和你交流：

![派蒙人设激活](docs/images/screenshot-paimon-soul-activated.png)

### 游戏画面识别 - 原神突破界面
派蒙能直接读取游戏窗口截图，识别当前界面内容：

![原神钟离突破界面](docs/images/screenshot-genshin-zhongli-ascension-ui.png)

### AI 分析辅助 - 突破材料缺口
派蒙自动分析突破所需材料，列出缺口和获取途径、也能为旅行者提供养成建议：

![派蒙分析钟离突破材料](docs/images/screenshot-paimon-zhongli-ascension-analysis.png)

## ✨ 功能特点

- 📸 **截图分析** - 实时看到你的游戏画面，理解当前状态
- 💬 **解答问题** - 卡关了？不知道怎么操作？派蒙告诉你该怎么做
- 🖱️ **辅助操作** - 帮你点击界面按钮，解决眼前的问题
- 🎭 **角色扮演** - 化身派蒙，用派蒙的语气和你交流
- 🎮 **原神专用** - 针对原神优化的按钮识别和操作逻辑

## 📋 支持的按键

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
| `1-4` | 切换队伍角色 |
| `Alt` | 显示鼠标 |

## 🔧 工作原理

```
派蒙分析截图 ──→ 执行操作 ──→ 自动截图 ──→ 返回给派蒙
     ↑                                        │
     └────────────────────────────────────────┘
```

每次操作后自动截图，让派蒙能看到操作效果，再决定下一步。

### 技术实现

1. **AI 识图** - 多模态大模型直接识别界面元素
2. **自然语言定位** - 通过文字描述找到按钮（无需预设模板）
3. **点击操作** - 前台/后台两种模式
4. **按钮模板** - 200+ 原神专用按钮模板

### AI 模型

| Provider | 模型 | 说明 |
|----------|------|------|
| 阿里云 | `gui-plus-2026-02-26` | 默认，混合思考模型 |
| 阿里云 | `gui-plus` | 旧版 |

通过 OpenAI 兼容接口调用，实现见 [`scripts/gui_agent/aliyun.py`](scripts/gui_agent/aliyun.py)：
- **base_url**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **API 文档**: [阿里云 GUI-Plus 接口文档](https://bailian.console.aliyun.com/cn-beijing?tab=api#/api/?type=model&url=2997660)

## 📦 安装

### 🐍 Step 1：确认 Python 3 环境

> **需要 Python 3.8+**

```bash
# 检查 Python 版本
python --version
```

### 📥 Step 2：安装依赖

```bash
# 进入技能目录
cd .trae/skills/paimon-skill

# 安装依赖
pip install -r requirements.txt
```

### ⚙️ Step 3：配置 API Key（可选，用于 click_text 功能）

```bash
# 设置阿里云 API Key
python main.py config --set-api-key YOUR_API_KEY

# 或者设置环境变量
set DASHSCOPE_API_KEY=your_api_key_here
```

## 🎮 使用方法

### 基础命令

```bash
# 截取原神窗口截图
python main.py screenshot

# 点击指定坐标
python main.py click 540 820

# 按下按键
python main.py key Escape

# 按住按键一段时间
python main.py hold W 2000

# 查找按钮位置
python main.py find confirm

# 列出所有可用按钮
python main.py buttons

# 通过文字描述点击（需要 API Key）
python main.py click_text "确认按钮"
```

### 典型使用场景

#### 场景1：查看角色信息

```bash
# 打开角色界面
python main.py key C

# 截图分析
python main.py screenshot
```

#### 场景2：打开地图查看位置

```bash
# 打开地图
python main.py key M

# 截图分析
python main.py screenshot
```

#### 场景3：移动探索

```bash
# 向前走2秒
python main.py hold W 2000
```

#### 场景4：战斗操作

```bash
# 释放元素战技
python main.py key E

# 释放元素爆发
python main.py key Q
```

## 📁 目录结构

```
.trae/skills/paimon-skill/
├── scripts/               # Python 核心模块
│   ├── click.py           # 点击功能
│   ├── keyboard.py        # 键盘功能
│   ├── screenshot.py      # 截图功能
│   ├── window.py          # 窗口管理
│   ├── recognition.py     # 图像识别
│   ├── config.py          # 配置管理
│   └── gui_agent/         # 多模态 AI 识图模块
├── games/                 # 游戏配置
│   └── genshin-impact/    # 原神
│       ├── SOUL.md        # 派蒙角色设定
│       ├── SKILL.md       # 原神子技能说明
│       └── assets/        # 图像资源
│           └── buttons/   # 按钮图片（200+个）
├── screenshots/           # 截图存储目录
├── main.py                # CLI 入口
├── requirements.txt       # Python 依赖
├── SKILL.md               # 技能文档
└── README.md              # 本文件
```

## 🎯 按钮识别

项目包含 200+ 个原神游戏按钮模板，存放在 `games/genshin-impact/assets/buttons/` 目录：

- `confirm.png` - 确认按钮
- `cancel.png` - 取消按钮
- `paimon_menu.png` - 派蒙菜单
- `inventory.png` - 背包按钮
- `character_guide.png` - 角色按钮
- `teleport.png` - 传送按钮
- `map.png` - 地图按钮
- ... 等等

### 使用按钮识别

```bash
# 查找按钮
python main.py find confirm

# 查找所有按钮
python main.py findall

# 列出所有可用按钮
python main.py buttons
```

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
4. **API Key 错误**：检查是否正确配置了 DASHSCOPE_API_KEY

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

## 📝 许可证

[LICENSE](LICENSE)

---

## 🚀 下一步

**派蒙.skill** 会持续更新，后续计划支持：

| 游戏 | 状态 |
|------|------|
| 🗺️ 原神（派蒙） | ✅ 已上线 |
| 🚂 崩坏：星穹铁道（三月七） | 🔜 开发中 |
| 🃏 炉石传说 | 🔜 开发中 |
| 🗡️ 杀戮尖塔 | 🔜 开发中 |

敬请期待！

---

**"派蒙会一直在你身边，旅行者！让我们一起探索提瓦特大陆吧！"** ⭐