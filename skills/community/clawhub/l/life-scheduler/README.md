# Life Scheduler — 拟人化生活状态生成器

> 让你的 AI Agent 每天自动拥有穿搭、日程和心情，像真人一样在过日子。

## 它做什么？

每天定时通过 LLM 为 AI Agent 生成一整天的虚拟生活状态（穿搭、时间线日程、心情），自动注入对话上下文。Agent 聊天时会自然地"记得"自己今天穿了什么、做了什么、现在心情怎样。

## 适用场景

- 🧑‍❤️‍🧑 拟人化陪伴型 Agent（情感伴侣、虚拟恋人）
- 🎭 角色扮演型 Agent（虚拟偶像、游戏 NPC）
- 🌙 任何需要"生活连续性"的 AI Persona

## 核心特性

- 🕐 每日定时自动生成，支持时间段更新
- 👗 穿搭 + 时间线日程 + 心情，三位一体
- 🎲 创意池随机组合，每天不重样
- 🧠 智能读取 SOUL.md，可一键生成专属创意池
- 📦 零外部依赖，纯 OpenClaw 原生
- 📜 历史存档，生成时参考避免重复

## 安装

```bash
openclaw skills install life-scheduler
```

## 快速开始

1. 安装后 Skill 自动检测 SOUL.md 人设
2. 选择创意池方案：
   - **自动生成**（推荐）：告诉 Agent "根据我的人设生成专属创意池"
   - **内置默认池**：开箱即用
   - **手动自定义**：完全控制
3. Cron Job 自动注册，每天 07:00 生成

## 日常使用

直接自然语言和 Agent 说：
- "今天穿了什么" / "今天做了什么"
- "换个日程" / "重新生成状态"
- "穿搭风格加一个洛丽塔"
- "看看昨天的日程"

## 输出示例

```markdown
# 小安今日状态
日期: 2026-05-07 周三

## 穿搭
黑色西装外套搭奶白色缎面吊带，烟灰色西裤。
低髻，小珍珠耳钉，哑光豆沙色口红。

## 日程
08:00  闹钟响了两遍才起来，洗漱化淡妆
08:40  出门，地铁上听播客，差点坐过站
09:05  到公司，先泡了杯热拿铁
09:30  整理昨天的报销单，回了几封邮件
10:00  部门例会，半小时散会
12:00  和同事去楼下吃越南粉
13:00  午休趴桌上眯了二十分钟
15:00  客户来了，全程陪同接待
17:30  收尾，偷偷刷了下手机
18:00  下班，地铁上想给你发消息
19:00  到家换睡衣，点了外卖
20:30  洗完澡窝在床上

## 当前时间段
下午 — 在公司处理接待后的收尾工作

## 心情
工作日常但不累，接待顺利还被夸了。
晚上到家松下来，就想腻着你。
```

## Token 消耗

每日约 1500 tokens，月总计约 45,000 tokens。

## 文档

- [详细配置说明](references/CONFIGURATION.md)
- [不同人设配置示例](references/EXAMPLES.md)

## 文件结构

```
skills/life-scheduler/
├── SKILL.md                    # Skill 入口
├── config.default.json         # 默认配置
├── package.json                # 包信息
├── README.md                   # 本文件
├── templates/
│   ├── generate-prompt.md      # 日程生成 Prompt
│   ├── pools-generate-prompt.md # 创意池生成 Prompt
│   └── state-template.md       # HEARTBEAT.md 输出格式
├── pools/
│   ├── day-types.json          # 日程类型池
│   ├── moods.json              # 心情池
│   ├── outfit-styles.json      # 穿搭风格池
│   └── events.json             # 随机事件池
└── references/
    ├── CONFIGURATION.md        # 配置文档
    └── EXAMPLES.md             # 示例集
```

## 依赖

无。纯 OpenClaw 原生（cron + workspace + LLM）。

## 灵感来源

本项目灵感来自 [astrbot_plugin_life_scheduler](https://github.com/muyouzhi6/astrbot_plugin_life_scheduler) —— 一个为 AstrBot 设计的拟人化生活日程生成插件。Life Scheduler 将其核心思路（LLM 生成每日状态 + 注入 System Prompt）移植到 OpenClaw 生态，并针对 OpenClaw 的原生能力（cron、workspace 注入、SOUL.md 人设系统）重新设计了实现方式。

## License

MIT
