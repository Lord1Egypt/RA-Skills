# Skill 猎手周报 · 格式规范 & Cron 配置

## 消息卡片格式铁律

### 换行规则
- 消息卡片只认 `\n\n`（双换行）才能分段/换行
- 单个 `\n` 只渲染为空格，不会分行！
- 项目之间用盲文空格 `⠀`（U+2800）单独占一行强制分隔

### 周报结构

```
🎯 **Skill 猎手周报 · YYYY.MM.DD**（自动）

🆕 本周新发现 N 个 | 共推荐 M 个 | 数据源：GitHub + ClawHub + SkillHub

🏆 **本周精选**

🥇 [名称](链接) ⭐stars

　　描述（≤80字，中文优先）

　　🐙GitHub · 语言 · 🆕本周新建

⠀

🥈 [名称](链接) ⭐stars

　　描述

　　🦀ClawHub

⠀

...（精选共8个）

────────────────────

📌 **备选区**

1. [名称](链接) ⭐stars

　　描述

　　🐙GitHub · 语言 · 🆕本周新建

⠀

...（备选若干）

🔒 安装任何外部 Skill 前，先说「帮我审查 [skill名]」🛡️
```

### 格式硬约束

| 约束 | 说明 |
|------|------|
| 名称即超链接 | `[名称](url)` 格式，不需要单独🔗行 |
| 描述≤80字 | 超出截断加 `...`，优先用中文 |
| 每条3个段落 | ①标题+星数 ②描述 ③来源标签，用 `\n\n` 分隔 |
| 项目间分隔 | 用 `⠀`（盲文空格U+2800）单独占一行 |
| 来源标签 | 🐙GitHub 或 🦀ClawHub，必须标注来源 |
| 精选/备选分隔 | 用 `────────────────────`（20个─） |
| 标题含(自动) | Cron推送标题必须含「(自动)」 |

### 三维严选机制

**严选依据：**
- 热度 50%：stars 对数归一化
- 相关性 30%：关键词命中密度（agent-skill/mcp/agent-framework/skill/automation）
- 新鲜度 20%：本周新建=20，本月=10，更早=2

**强制混排：**
- 严选8位：≥2个 ClawHub + ≥4个 GitHub，剩余按三维依据竞争
- 备选区：不限比例，按三维依据排序

**去重：**
- ClawHub 按 slug 去重
- GitHub 同 owner ≤2 个

**描述补全：**
- ClawHub 无描述时用 `get_insight()` 补推荐理由
- 同一规则轮换不同文案，避免千篇一律

## Cron 配置

- 计划：`0 18 * * 0`（每周日 18:00）
- 时区：Asia/Shanghai
- payload：agentTurn，运行 trending.py 并推送结果
- delivery：announce 到微信/飞书
- 标题必须含「(自动)」

## 生成命令

```bash
# 生成本周周报
python3 ./scripts/trending.py --period weekly

# 生成日报
python3 ./scripts/trending.py --period daily
```
