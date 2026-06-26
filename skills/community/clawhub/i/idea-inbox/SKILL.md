---
name: idea-inbox
description: 收集“idea:/灵感：”消息到飞书多维表格（默认自动创建新表），用大模型生成AI归纳/类别/标签（支持自动新增标签），并按配置的每日时间（默认10:02，今日新增=0不发）推送当日汇总。
---

# 灵感妙计（Idea Inbox）

把你在飞书私聊里随手发来的想法收集成结构化的灵感池，并自动分类，方便后续筛选与推进。

## Triggers

- 以 `idea:` 开头的消息
- 以 `灵感：` 开头的消息

> 仅在飞书私聊生效。

## Use Cases

- 你随手发一个想法：我自动入库并分类
- 你持续积累一周：我每天 10:02 给你发当日新增汇总（若当日 0 新增则不发）

## Data Store

- 默认：首次运行（第一次发 `idea:`/`灵感：`）自动创建一个新的飞书多维表格（Bitable）App：`灵感妙计`。
- 创建完成后，会把 `app_token/table_id/字段id` 等写入本地配置文件：
  - `~/.openclaw/idea-inbox/config.json`

字段（默认）：内容 / AI归纳 / 类别 / 标签 / 状态 / 来源 / 创建时间

## Configuration

`~/.openclaw/idea-inbox/config.json`（自动生成，可手改）示例：

```json
{
  "prefixes": ["idea:", "灵感："],
  "daily_time": "10:02",
  "bitable": {
    "app_token": "...",
    "table_id": "...",
    "fields": {
      "content": "内容",
      "ai_summary": "AI归纳",
      "category": "类别",
      "tags": "标签",
      "status": "状态",
      "source": "来源",
      "created_time": "创建时间"
    }
  },
  "model": {
    "mode": "codex_files_first",
    "fallback": null
  },
  "tags": {
    "auto_add": true,
    "max_tags": 5
  },
  "status": {
    "options": ["待处理", "已处理", "无法处理"],
    "default": "待处理"
  }
}
```

- `daily_time`：仅需配置每日时间；`send_if_zero` 固定为 false（0 新增不发）。
- 模型：默认优先读取 `~/.codex/auth.json` + `~/.codex/config.toml`（不读 env）。
  - 若用户没有 codex 文件，可在 `model.fallback` 填 `baseUrl/apiKey/apiType/model`。

## Inputs

- Required:
  - `text`: 原始消息文本（包含前缀）
  - `chat_type`: 需为 direct/p2p（私聊）

## Outputs

- 成功：写入一条记录到 Bitable，并返回 record_id
- 失败：返回错误原因（网络/权限/字段缺失/模型调用失败等）

## Workflow

1. 校验触发条件（私聊 + 前缀匹配）
2. 抽取原文内容（去掉前缀）
3. 调用大模型生成严格 JSON：{category,tags,summary}
4. 标签自动新增：若 tags 不在 Bitable 选项中，先追加选项
5. 写入 Bitable：内容/AI归纳/类别/标签/状态=收集箱/来源=飞书私聊
6. 每日 10:02 汇总：统计当日新增，>0 才推送

## Limitations

- 本技能不处理群聊消息
- 标签自动新增会带来标签膨胀；可后续加“标签黑名单/合并”规则
- 模型输出需严格 JSON；会做枚举校验与截断
