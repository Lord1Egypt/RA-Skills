# Matter Day Reminder - 个人社交助理

---

## 中文简介

**Matter Day Reminder** 是一个智能个人社交助理 Skill，专为管理亲友重要日期而生。无论你是经常忘记朋友生日的"健忘星人"，还是想给亲友惊喜的"贴心达人"，这个 Skill 都能帮你轻松搞定。

### 核心功能

🎯 **智能提醒系统**
- 双节点提醒：提前7天准备礼物 + 当天推送祝福
- 支持农历/阳历双历日期
- 自动处理闰月，准确计算每年对应的阳历日期

📝 **联系人管理**
- 对话式交互录入，像聊天一样添加联系人
- Markdown + YAML Frontmatter 本地存储，数据完全掌控
- 支持标签系统，记录兴趣爱好和礼物偏好

🤖 **AI 智能生成**
- 自适应祝福语：根据关系亲疏（父母/密友/普通朋友）调整语气
- 智能礼物建议：自动推断预算（朋友≤300元，家人弹性）
- 个性化推荐：基于人物特征和兴趣爱好

🌙 **农历完美支持**
- 支持11种农历日期输入格式（农历/阴历/旧历/数字格式等）
- 自动统一为标准格式存储
- 使用 lunar-javascript 库，转换精准可靠

### 适用场景

- 🎂 **生日提醒**：再也不会忘记亲朋好友的生日
- 💕 **纪念日管理**：恋爱纪念日、结婚纪念日一键记录
- 🎁 **礼物规划**：提前7天提醒，有充足时间准备惊喜
- ✍️ **祝福生成**：AI生成走心祝福语，告别复制粘贴

---

## English Introduction

**Matter Day Reminder** is an intelligent personal social assistant Skill designed for managing important dates of your family and friends. Whether you're someone who often forgets birthdays or a thoughtful person who loves to surprise loved ones, this Skill has got you covered.

### Core Features

🎯 **Smart Reminder System**
- Dual-node reminders: 7-day advance gift preparation + same-day blessing push
- Support for both lunar and solar calendars
- Automatic leap month handling with accurate solar date calculation

📝 **Contact Management**
- Conversational interaction for adding contacts like chatting
- Local storage with Markdown + YAML Frontmatter, full data control
- Tag system for tracking hobbies and gift preferences

🤖 **AI-Powered Generation**
- Adaptive blessing messages: Adjust tone based on relationship closeness
- Smart gift suggestions: Auto-inferred budget (friends ≤¥300, family flexible)
- Personalized recommendations based on personal characteristics

🌙 **Perfect Lunar Calendar Support**
- Supports 11 lunar date input formats (lunar/yinli/jiuli/numeric, etc.)
- Automatic standardization to uniform format
- Powered by lunar-javascript library for accurate conversion

### Use Cases

- 🎂 **Birthday Reminders**: Never forget friends' and family's birthdays again
- 💕 **Anniversary Management**: Track relationship and wedding anniversaries
- 🎁 **Gift Planning**: 7-day advance reminder for thoughtful preparation
- ✍️ **Blessing Generation**: AI-generated heartfelt messages, no more copy-paste

---

## 技术亮点 / Technical Highlights

### 中文
- **零外部依赖**：除邮件服务外，所有数据本地存储，隐私安全
- **全平台支持**：基于 Node.js，跨平台运行
- **数据可移植**：Markdown 格式，可用任何文本编辑器查看和编辑
- **Git 友好**：结构化文本，天然支持版本控制

### English
- **Zero External Dependencies**: All data stored locally except email service
- **Cross-Platform**: Node.js-based, runs on any platform
- **Data Portability**: Markdown format, viewable in any text editor
- **Git-Friendly**: Structured text, naturally supports version control

---

## 快速开始 / Quick Start

### 中文
1. 安装 `matter-day-reminder.skill` 到 OpenCode
2. 初始化数据目录：`mkdir -p reminder-data/contacts`
3. 开始对话："帮我添加一个朋友"

### English
1. Install `matter-day-reminder.skill` to OpenCode
2. Initialize data directory: `mkdir -p reminder-data/contacts`
3. Start conversation: "Help me add a friend"

---

## 一句话描述 / One-Liner

**中文**：你的私人社交秘书，让重要日子不再错过，让每一份祝福都恰到好处。

**English**: Your personal social secretary ensuring you never miss important dates and every blessing is perfectly timed.

---

*Version 1.0.0 | Built with ❤️ for better social connections*
