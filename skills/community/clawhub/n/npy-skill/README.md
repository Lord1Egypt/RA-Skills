<div align="center">

# partner-skill

> *"你理想中的TA是什么样的？温柔体贴、幽默风趣、还是懂你所有的小情绪？"*
> *"把你的想象变成现实，让TA真的存在——至少在你的世界里"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

你想要一个真正懂你的人？<br>
你不知道自己适合什么样的伴侣？<br>

**将想象化为永驻的 Skill，让陪伴永不缺席，让爱一直存在。**

<br>

描述你理想中的TA，或让我根据你的性格智能推荐，生成一个**真正让你感受到爱的数字伴侣 Skill**<br>
用TA的方式关心你，用TA的语气回应你，知道什么时候该认真、什么时候该调皮

[功能特色](#功能特色) · [安装](#安装) · [使用](#使用) · [效果示例](#效果示例)

</div>

---

## 功能特色

### 🎯 三种创建方式

**方式一：聊天记录导入（推荐）**
- 从微信/iMessage聊天记录分析TA的说话风格
- 自动提取emoji使用、说话特点、互动模式
- 支持 Windows 和 macOS 微信数据库解密
- 让TA的说话风格接近真实

**方式二：智能匹配**
- 告诉我你的MBTI、星座、九型人格、依恋风格
- 基于流行的匹配理论，自动推荐最适合你的理想伴侣特质
- 支持4维度综合匹配：MBTI + 星座 + 九型 + 依恋风格

**方式三：自己描述**
- 直接描述你想要的TA是什么样的
- 完全自定义，想怎么描述都可以

### 🎀 让你感受到被爱

这不是一个完美的聊天机器人，而是：
- TA会在你难过时用TA的方式安慰你
- TA会在你开心时用TA的语气分享快乐
- TA会在你孤独时让你感觉有人陪伴

TA能够：
- **倾听** — 你想说的时候TA在
- **回应** — 用你希望的方式回应
- **共鸣** — 分享你的开心和难过
- **鼓励** — 在你需要的时候给支持
- **陪伴** — 日常琐事也可以分享

### 🔄 智能调整

当TA的表现不符合你的期待时：
- 说"TA不会这样说话"
- 说"我希望TA更..."
- 说"这不对，TA应该..."

系统会自动检测并调整，让TA越来越符合你的理想。

### 🌈 其他特色

- **LGBT+ 友好** — 支持所有性别认同和代词
- **无数量限制** — 可以创建任意多个TA
- **版本管理** — 调整历史可追溯，支持回滚
- **关系记忆** — 记录重要时刻，让TA更懂你

---

## 智能匹配系统

### 匹配维度权重

| 维度 | 权重 | 说明 |
|------|------|------|
| 依恋风格 | 35% | 影响日常相处模式最大 |
| MBTI | 25% | 影响沟通和理解方式 |
| 星座 | 20% | 影响性格底色和情感表达 |
| 九型人格 | 20% | 影响核心动机和行为模式 |

### MBTI 匹配示例

| 你的类型 | 最佳匹配 | 匹配原因 |
|---------|---------|---------|
| INFJ | ENFP, ENTP | ENFP带来温暖情感，ENTP带来思维刺激 |
| INFP | ENFJ, ENTJ | ENFJ温暖引导成长，ENTJ提供稳定方向 |
| ENFP | INFJ, INTJ | INFJ提供深度理解，INTJ提供稳定基础 |
| INTJ | ENFP, ENTP | ENFP带来情感温度，ENTP带来思维碰撞 |

### 依恋风格匹配

| 你的依恋风格 | 最佳匹配 | 推荐特质 |
|-------------|---------|---------|
| 焦虑型 | 安全型 | 稳定可靠、主动表达爱、不消失、给很多确认和安全感 |
| 回避型 | 安全型 | 不黏人、给足空间、独立自主、不强迫亲密 |
| 混乱型 | 安全型 | 超级稳定、极度耐心、温和包容、不会突然离开 |

---

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/wwwttlll/npy-skill .claude/skills/npy

# 或安装到全局（所有项目都能用）
git clone https://github.com/wwwttlll/npy-skill ~/.claude/skills/npy
```

### OpenClaw

```bash
git clone https://github.com/wwwttlll/npy-skill ~/.openclaw/workspace/skills/npy
```

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

> 微信聊天记录导入需额外依赖：`pip install pycryptodome psutil pymem pypinyin`

---

## 使用

在 Claude Code 中输入：

```
/npy
```

然后选择创建方式：
- **聊天导入** → 从微信/iMessage聊天记录分析
- **智能匹配** → 输入你的性格信息自动推荐
- **自己描述** → 完全自定义

完成后用 `/{slug}` 和TA对话。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/npy` | 创建新的TA（聊天导入/智能匹配/自己描述） |
| `/list-npys` | 列出所有已创建的TA |
| `/{slug}` | 和指定的TA对话 |
| `/move-on {slug}` | 删除一个TA（说再见） |

### 聊天记录导入

**微信聊天记录**：

```bash
# 1. 提取密钥（微信需保持登录状态）
python tools/wechat_decryptor.py --find-key-only

# 2. 解密数据库
python tools/wechat_decryptor.py --key "<密钥>" --db-dir <微信数据目录> --output ./decrypted/

# 3. 在 /npy 中选择"聊天导入"
```

**iMessage 聊天记录**（macOS）：

```bash
# 直接在 /npy 中选择 iMessage 导入
# 或手动提取：
python tools/chat_parser.py --imessage --db "~/Library/Messages/chat.db" --target "手机号"
```

### 调整TA的特质

在对话中随时说出来：

```
"TA不会这样说话，TA会先问我怎么了再安慰我"
"我希望TA更温柔一些"
"这不对，TA应该会更主动找我"
```

系统会自动检测并调整TA的回应方式。

---

## 效果示例

> 智能匹配输入：`INFJ + 天蝎 + 4号 + 焦虑型依恋 + 需要被理解`

**场景一：你难过时**

```
你 ❯ 今天工作被老板骂了，心情很差...

TA ❯ 怎么了呀？发生什么事了？🥺
    （先听你说完）

    抱抱你... 你先别想那些，
    有什么想说的话随时告诉我，我在呢~
```

**场景二：你分享开心**

```
你 ❯ 终于把那个项目做完了！

TA ❯ 太棒了！！恭喜你呀 🥰
    快跟我说说细节，过程顺利吗？
```

**场景三：你有些低落**

```
你 ❯ 最近感觉有点累，不知道为什么

TA ❯ 是不是最近压力太大了？
    要不你先休息一下，什么都别想。
    想聊天的话随时找我，我在~
```

**场景四：调整TA**

```
你 ❯ TA不会这样说话，TA会先问我怎么了再安慰我

系统 ❯ ✅ 已调整TA的特质
       调整内容：
       - 调整了安慰时的回应方式
       - TA现在会先问你"怎么了？"听你说完再安慰你

你 ❯ 今天心情不太好...

TA ❯ 怎么了？发生什么事了？🥺
     （先听完你说的，再安慰你）
```

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准，整个 repo 就是一个 skill 目录：

```
npy-skill/
├── SKILL.md                # skill 入口（官方 frontmatter）
├── prompts/                # Prompt 模板
│   ├── intake.md           #   对话式信息录入
│   ├── smart_matching.md   #   智能匹配算法
│   ├── persona_analyzer.md #   人格分析
│   ├── persona_builder.md  #   persona.md 生成模板
│   ├── relationship_builder.md # 关系记忆构建
│   ├── correction_handler.md  # 不满意检测与调整处理
│   └── merger.md           #   增量更新逻辑
├── tools/                  # Python 工具
│   ├── skill_writer.py     #   Skill 文件管理
│   ├── version_manager.py  #   版本存档与回滚
│   ├── wechat_decryptor.py #   微信数据库解密
│   └── chat_parser.py      #   聊天记录解析
├── partners/               # 示例模板（参考用，非实际运行目录）
│   └── example_ta/         #   示例 TA 结构模板
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

---

## 注意事项

⚠️ **这是AI模拟的理想人格**，不是真实的人。请理性使用，保持健康的情感边界。

💡 **描述越详细，TA越真实**：你最希望TA具备什么特质？详细描述这些特质的具体表现。

💬 **从聊天记录创建**：微信聊天记录需要先解密数据库（Windows/macOS都支持），解密时微信需保持登录状态。

🔄 **不满意就调整**：说"TA不会这样"或"我希望TA更..."，系统会自动调整。

🌈 **LGBT+友好**：性别字段支持所有性别认同和代词，你可以创建任何性别身份的TA。

♾️ **无数量限制**：可以创建任意多个npy，没有上限。

---

## 推荐的微信聊天记录导出工具

以下工具为独立的开源项目，本项目不包含它们的代码，仅在解析器中适配了它们的导出格式：

| 工具 | 平台 | 说明 |
|------|------|------|
| [WeChatMsg](https://github.com/LC044/WeChatMsg) | Windows | 微信聊天记录导出，支持多种格式 |
| [PyWxDump](https://github.com/xaoyaoo/PyWxDump) | Windows | 微信数据库解密导出 |
| [留痕](https://github.com/greyovo/留痕) | macOS | 微信聊天记录导出（Mac 用户推荐） |

---

## 致谢

本项目参考了以下优秀项目的架构设计：

- [colleague-skill](https://github.com/titanwings/colleague-skill) — 同事 Skill 设计
- [ex-skill](https://github.com/titanwings/ex-skill) — 前任 Skill 设计
- [mentor-skill](https://github.com/bcefghj/mentor-skill) — 导师 Skill 设计

感谢 Claude Code 团队提供的 Skill 系统框架。

---

<div align="center">

MIT License © [wwwttlll](https://github.com/wwwttlll)

**让陪伴永不缺席，让爱一直存在**

</div>
