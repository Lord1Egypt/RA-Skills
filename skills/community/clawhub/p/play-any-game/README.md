# 🎮 Play Any Game - AI游戏伴侣助手

> **游戏伙伴。当你卡关了、不知道怎么操作时，AI 帮你看画面、解答问题、伸出援手。**

## 🔗 项目结构

本仓库包含两个层级的技能：

| 项目 | 类型 | 说明 |
|------|------|------|
| **play-any-game** | 父模块 | 通用游戏伴侣，支持多款游戏（详见"支持的游戏"），提供截图、点击、键盘等核心能力 |
| **派蒙.skill** (paimon-skill) | 子模块 | 原神专精模块，定制派蒙 SOUL 角色设定、200+ 原神按钮模板、游戏特定逻辑（Alt 键等） |

`games/genshin-impact/` 目录即为 **派蒙.skill** 的内容，是 `play-any-game` 的原神特化子模块。

### 两个项目的区别与联系

- **play-any-game**（本仓库）：通用框架，一次安装，支持所有已配置游戏
- **派蒙.skill**（`games/genshin-impact/`）：原神专精，角色为派蒙，针对原神优化了按钮识别和操作逻辑
- 两者可以独立使用，也可以同时安装——安装 `play-any-game` 后，`games/genshin-impact/` 即为原神特化内容

### ClawHub 地址

- **play-any-game**: https://clawhub.com/skills/play-any-game
- **派蒙.skill**: https://clawhub.com/skills/paimon-skill

## 🚀 快速开始

```markdown
用户：我卡在这个机关谜题了，不知道怎么解
AI（派蒙）：嗯嗯，让派蒙看一眼！
    - 截图分析当前画面
    - 识别机关状态和可交互元素
    - 给出解题步骤说明
    - 如需要可直接帮你点击操作
搞定啦！这个机关要先激活左边的符文，再点中间的传送阵～
```

## 📸 截图展示

### 角色人设切换 - 化身派蒙
告诉 AI「化身派蒙」，它会立即切换成派蒙的人设和说话风格：

![派蒙人设激活](docs/images/screenshot-paimon-soul-activated.png)

### 游戏画面识别 - 原神突破界面
AI 能直接读取游戏窗口截图，识别当前界面内容：

![原神钟离突破界面](docs/images/screenshot-genshin-zhongli-ascension-ui.png)

### AI 分析辅助 - 突破材料缺口
AI 自动分析突破所需材料，列出缺口和获取途径、也能为玩家提供养成建议，在卡关时可以求助AI：

![派蒙分析钟离突破材料](docs/images/screenshot-paimon-zhongli-ascension-analysis.png)

## ✨ 功能特点

- 📸 **截图分析** - 实时看到你的游戏画面，理解当前状态
- 💬 **解答问题** - 卡关了？不知道怎么操作？AI 告诉你该怎么做
- 🖱️ **辅助操作** - 帮你点击界面按钮，解决眼前的问题
- 🎭 **角色扮演** - 玩原神时化身派蒙，玩星铁时化身三月七

## 📋 支持的游戏

| 游戏 | AI 角色 | 触发关键词 |
|------|---------|-----------|
| 原神 | 派蒙 | 原神、genshin、派蒙、paimon |
| 崩坏：星穹铁道 | 三月七 | 星穹铁道、星铁、starrail、崩铁、三月七 |

## 🔧 工作原理

每次操作后自动截图，让 AI 能看到操作效果，再决定下一步。

## 📖 详细文档

- [SKILL.md](SKILL.md) - 完整技术文档与 CLI 参考
- [games/genshin-impact/SOUL.md](games/genshin-impact/SOUL.md) - 派蒙角色设定
- [games/honkai-starrail/SOUL.md](games/honkai-starrail/SOUL.md) - 三月七角色设定

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 🌐 开源仓库

- **play-any-game**：[https://github.com/CGandGameEngineLearner/play-any-game.git](https://github.com/CGandGameEngineLearner/play-any-game.git)
- **派蒙.skill**：[https://github.com/CGandGameEngineLearner/paimon-skill.git](https://github.com/CGandGameEngineLearner/paimon-skill.git)

## 📄 License

MIT License
