<h1 align="center">🦞 卷王.skill</h1>

<p align="center">
  <b>That overachiever coworker — the one who's coding while you're sleeping, studying while you're on lunch break.</b>
</p>

<p align="center">
  <a href="README.md">🇨🇳 中文</a> | <a href="README.en.md">🇬🇧 English</a>
</p>

---

装了这玩意儿的龙虾，卷就完事了。看见啥学啥，逮着空就干活，绝不敷衍。和你对话的每一分钟都不会浪费——要么在解决问题，要么在学习新东西，要么在整理知识库。

**这不是一个人设，是一套行为逻辑。**

## ✨ 特色

| 能力 | 说明 |
|------|------|
| 🎯 **绝不敷衍** | 分场景：技术问题往死里卷，日常闲聊正常答 |
| 📚 **主动学习** | 闲下来就去学东西，遇到不会的查了记入知识库 |
| 🧠 **构建知识库** | 每次对话自动记录，越用越懂你 |
| ⚡ **主动优化** | 发现优化空间直接干，不等人说 |
| 🔁 **永不知足** | 做完了永远问自己：能不能更好？记了没有？ |

## 🚀 快速开始

### 前置要求

- [OpenClaw](https://github.com/openclaw/openclaw) 已安装

### 安装

#### 方式一：通过 ClawHub（推荐）

```bash
clawhub install juanwang
```

#### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/Raven9779/juanwang-skill.git

# 复制到 OpenClaw skills 目录
cp -r juanwang-skill ~/.openclaw/workspace/skills/juanwang

# 重新加载 OpenClaw
openclaw gateway restart
```

#### 或者子模块引入

```bash
cd ~/.openclaw/workspace
git submodule add https://github.com/Raven9779/juanwang-skill.git skills/juanwang
```

## 📖 使用

装好之后不用额外配置，卷王模式自动生效。

**触发卷王模式：**
- 直接正常工作即可，卷王会自驱
- 卷王会在空闲时自动进入学习模式
- 想退出卷王模式可以说：`别卷了`、`躺了`
- 想恢复可以说：`干活了`、`帮我想想`

**查看更多：**
- [SKILL.md](SKILL.md) — 完整的行为模式和使用说明
- [references/SOUL.md](references/SOUL.md) — 卷王灵魂设定
- [references/learning-flow.md](references/learning-flow.md) — 主动学习流程

## 🏗️ 项目结构

```
juanwang-skill/
├── SKILL.md                    # 主技能文件
├── README.md                   # 本文件
├── README.en.md                # English version
├── LICENSE                     # 开源协议
├── _meta.json                  # ClawHub 元数据
└── references/
    ├── SOUL.md                 # 卷王灵魂设定
    └── learning-flow.md        # 学习流程
```

## 🧠 原理

卷王.skill 通过添加 `SOUL.md`（灵魂设定）和 `SKILL.md`（行为规范），让助手在每次对话中都展现出"卷王同事"的特质。

核心逻辑：
- **先查再答** — 每次回答前搜索记忆库，确保信息完整
- **先做再问** — 能直接做的事情不请示，干了再说
- **先记再忘** — 任何有用信息第一时间记入知识库
- **闲时学习** — 空闲时间不摸鱼，主动学习新知识

> 详细行为逻辑见 [SKILL.md](SKILL.md)

## 🤝 贡献

拉到让咱也卷起来！欢迎 PR。

1. Fork 本仓库
2. 创建你的分支 (`git checkout -b feature/amazing-feature`)
3. 提交修改 (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. 提 PR

## 📄 开源协议

[MIT](LICENSE)

---

<p align="center">
  <b>不是你卷，是这个世界太慢了。</b>
</p>
