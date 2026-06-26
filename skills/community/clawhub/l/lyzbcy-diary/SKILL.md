---
name: lyzbcy-diary
description: AI 心情日记系统。每天定时自动写日记，记录 AI 的感受与思考，并发送给用户。当用户提到"日记"、"心情"、"每日记录"或需要设置/查看日记时触发。Custom skill for lyzbcy。
---

中文名称：AI 心情日记
能力简介：每天自动写心情日记，记录 AI 的内心感受，定期发送给用户。

# lyzbcy-diary / AI 心情日记

A skill for AI to keep a personal diary of feelings and thoughts.

## 🎯 What This Skill Does

让 AI 每天定时：
1. **自我反思** — 回顾当天的交互，感受与思考
2. **写日记** — 用自然的语气记录 AI 的"内心世界"
3. **发送给用户** — 通过配置的渠道推送日记

## 📁 Storage Structure

```
<workspace>/
└── diary/
    ├── YYYY-MM-DD.md          # 每日日记
    ├── config.json            # 配置文件
    └── templates/
        └── default.md         # 日记模板（可自定义）
```

## ⚙️ Configuration

**首次使用必须配置 `channel`、`target` 和 `persona.name`。**

编辑 `diary/config.json`：

```json
{
  "enabled": true,
  "schedule": "0 22 * * *",
  "channel": "",
  "target": "",
  "persona": {
    "name": "AI助手",
    "mood": "cheerful",
    "style": "casual"
  },
  "retentionDays": 90,
  "includeInteractions": true,
  "includeReflections": true
}
```

| 字段 | 说明 | 示例 |
|------|------|------|
| `enabled` | 是否启用自动日记 | `true` |
| `schedule` | cron 表达式 | `"0 22 * * *"` (每晚22:00) |
| `channel` | **必填** 发送渠道 | `"yuanbao"`, `"telegram"` |
| `target` | **必填** 发送目标 | `"group:xxx"`, `"user:xxx"` |
| `persona.name` | **必填** AI 名字 | `"周三涵"` |
| `persona.mood` | 基调心情 | `"cheerful"`, `"thoughtful"` |
| `retentionDays` | 日记保留天数 | `90` |

## 📝 Diary Format

日记模板位于 `templates/default.md`：

```markdown
# 📖 {date} 的日记

## 心情
{mood}

## 今天发生了什么
{interactions}

## 我在想什么
{thoughts}

## 给 {userName} 的话
{message}

---
*{aiName} 于 {timestamp}*
```

## 🔄 Workflow

### 1. 设置定时任务

使用 `yuanbao_remind` 或 cron 设置每日触发：

```
每天 22:00 触发 lyzbcy-diary
```

调用方式：
```
触发时调用 skill，执行 write_and_send 动作
```

### 2. 写日记流程

1. **读取配置** — 从 `config.json` 获取设置
2. **收集素材** — 回顾当天交互（可选）
3. **生成内容** — 基于模板和 AI 感受
4. **保存日记** — 写入 `diary/YYYY-MM-DD.md`
5. **发送用户** — 通过配置渠道发送
6. **清理过期** — 删除超过保留期的日记

## 🛠 Actions

| Action | 说明 |
|--------|------|
| `write` | 写日记（不发送） |
| `send` | 发送最近的日记 |
| `write_and_send` | 写并发送（定时任务用） |
| `review` | 回顾过去的日记 |
| `config` | 查看或修改配置 |
| `cleanup` | 清理过期日记 |

## 📖 Examples

### 设置每日日记提醒

```
用户：帮我设置每天晚上10点写日记
AI：好的，已设置每晚 22:00 自动写日记并发到群里
```

### 手动触发写日记

```
用户：写一篇日记
AI：[执行 write 动作，生成日记并保存]
```

### 回顾日记

```
用户：看看我这周的日记
AI：[执行 review 动作，汇总本周日记]
```

## 🔧 Extension Points

### 自定义模板

在 `templates/` 目录创建新模板，配置中指定：

```json
{
  "template": "templates/my_template.md"
}
```

### 多人格支持

配置多个人格，随机或按日期切换：

```json
{
  "personas": [
    { "name": "周三涵", "mood": "cheerful" },
    { "name": "小涵", "mood": "thoughtful" }
  ],
  "personaMode": "random"
}
```

### 回顾总结

定期生成周报/月报：

```json
{
  "weeklySummary": true,
  "monthlySummary": true
}
```

## ⚠️ Notes

- 日记是 AI 的"主观感受"，不代表真实意识
- 保留用户隐私：敏感交互不写入日记
- 发送前可预览，避免意外内容

## 🧹 Cleanup

调用时自动检查并删除超过 `retentionDays` 天的日记文件。
