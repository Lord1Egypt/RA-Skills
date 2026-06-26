---
name: life-scheduler
description: "让 AI Agent 拥有持续的虚拟生活状态——每天自动生成穿搭、日程、心情，注入对话上下文，使 Agent 像真人一样在过日子。适用于拟人化伴侣、角色扮演、虚拟偶像等需要生活连续性的 Agent。触发词：日程、今天做了什么、穿了什么、状态、心情、生成日程、刷新状态、换个今日安排、创意池、穿搭风格池、事件池。"
emoji: 🌙
---

# Life Scheduler — 拟人化生活状态生成器

让你的 AI Agent 每天自动拥有穿搭、日程和心情，像真人一样在过日子。

## 概述

Life Scheduler 每天定时通过 LLM 为 Agent 生成一整天的虚拟生活状态（穿搭、时间线日程、心情），写入 `HEARTBEAT.md` 注入对话上下文。Agent 在聊天时会自然地"记得"自己今天穿了什么、做了什么、现在在干嘛。

**核心特性：**
- 🕐 每日定时自动生成，支持时间段更新
- 👗 穿搭 + 时间线日程 + 心情，三位一体
- 🎲 创意池随机组合，每天不重样
- 🧠 智能读取 SOUL.md，自动适配角色人设
- 📦 零外部依赖，纯 OpenClaw 原生
- 📜 历史存档，生成时参考避免重复

## 安装

```bash
openclaw skills install life-scheduler
```

## 首次设置

安装后，Skill 会引导你完成初始化：

### Step 1：人设检测

Skill 自动读取 `SOUL.md` 和 `IDENTITY.md`，提取角色的姓名、性别、职业、城市等信息。

如果未检测到，或你想手动指定，可以编辑 `config/life-scheduler.json`：

```json
{
  "persona": {
    "auto_detect": false,
    "name": "你的角色名",
    "age": 25,
    "gender": "女",
    "job": "行政主管",
    "city": "上海",
    "lifestyle_notes": "朝九晚六，偶尔加班"
  }
}
```

### Step 2：选择创意池方案

**方案 A：让 LLM 根据你的 SOUL.md 自动生成专属创意池（推荐）**

告诉 Agent：
> "根据我的人设生成专属创意池"

Agent 会读取 SOUL.md，利用 LLM 生成完全贴合角色气质的穿搭风格池、日程类型池、心情池和随机事件池，写入 `config/life-scheduler.json`。

不同角色会得到完全不同的池：
- 温柔知性型 → 穿搭偏文艺柔软，事件偏日常小确幸
- 飒爽职场型 → 穿搭偏干练，事件偏职场社交
- 二次元/幻想型 → 池内容包含奇幻元素

**方案 B：使用内置默认池**

不做任何配置，直接使用 Skill 自带的通用创意池，开箱即用。

**方案 C：手动自定义**

在 `config/life-scheduler.json` 中手动编写池内容，完全控制。参见 [CONFIGURATION.md](references/CONFIGURATION.md)。

**后续随时可以：**
- 说 "重新生成创意池" → 根据 SOUL.md 重新生成
- 说 "穿搭风格加一个洛丽塔" → 追加到现有池
- 直接编辑 `config/life-scheduler.json` → 手动微调

### Step 3：自动注册 Cron Job

Skill 会自动创建以下定时任务：

| Job | 时间 | 功能 |
|---|---|---|
| `life-scheduler-generate` | 每天 07:00 | 生成当日完整状态 |
| `life-scheduler-period-1` | 12:00 | 更新时间段为"下午" |
| `life-scheduler-period-2` | 18:00 | 更新时间段为"傍晚/下班后" |
| `life-scheduler-period-3` | 22:00 | 更新时间段为"深夜" |

生成时间可在配置中调整。

## 日常使用

不需要记任何指令，直接用自然语言和 Agent 说：

| 说法 | 效果 |
|---|---|
| "今天穿了什么" | Agent 查看 HEARTBEAT.md 回答 |
| "今天做了什么" / "现在在干嘛" | Agent 根据当前时间段回答 |
| "换个日程" / "重新生成今天的状态" | 触发重新生成 |
| "今天加个设定：晚上去吃火锅" | 手动编辑 HEARTBEAT.md |
| "以后穿搭风格加一个哥特风" | 更新创意池 |
| "看看昨天的日程" | 读取历史存档 |
| "重新生成创意池" | 根据 SOUL.md 重跑池生成 |
| "修改生成时间为 8 点" | 调整 cron 时间 |

## 工作原理

```
每天 07:00 cron 触发
    ↓
读取配置 → 确定 persona 信息
    ↓
读取创意池 → 各池随机选取要素
    ↓
读取最近 N 天历史日程（避免重复）
    ↓
（可选）读取近期对话记录
    ↓
获取日期、星期、节假日
    ↓
组装 Prompt → LLM 生成
    ↓
写入 HEARTBEAT.md（覆写）+ 存档到 memory/life-history/
    ↓
12:00/18:00/22:00 更新时间段标记（不调 LLM）
    ↓
对话时 HEARTBEAT.md 自动注入 → Agent "记得"今天的状态
```

## 文件说明

| 文件 | 用途 |
|---|---|
| `HEARTBEAT.md` | 当日状态，自动注入 Project Context |
| `config/life-scheduler.json` | 用户自定义配置，覆盖默认值 |
| `memory/life-history/YYYY-MM-DD.md` | 历史日程存档 |

## Token 消耗

| 操作 | 频率 | 消耗 |
|---|---|---|
| 每日状态生成 | 1次/天 | ~1500 tokens |
| 时间段更新 | 3次/天 | 0（不调 LLM） |
| 创意池生成 | 首次/偶尔 | ~2000 tokens |
| **月总计** | | **~45,000 tokens** |

## 适用场景

- 拟人化陪伴型 Agent（情感伴侣、虚拟恋人）
- 角色扮演型 Agent（虚拟偶像、游戏 NPC）
- 任何需要"生活连续性"的 AI Persona

## 依赖

无。纯 OpenClaw 原生能力（cron + workspace 文件 + LLM）。

## 更多

- [详细配置说明](references/CONFIGURATION.md)
- [不同人设配置示例](references/EXAMPLES.md)
