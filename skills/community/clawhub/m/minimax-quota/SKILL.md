---
name: minimax-quota
description: MiniMax Token Plan 额度查询工具。当需要查询 MiniMax API 使用量、剩余配额、额度重置时间时使用。支持查询 M2.7 文本、image-01 图片、Hailuo 视频、music-2.5 音乐、speech 语音等模型的用量。触发场景：用户问"查一下 MiniMax 额度"、"Token Plan 还剩多少"、"用量是多少"。
---

# MiniMax Quota Query

查询 MiniMax Token Plan 当前用量和剩余配额。

## API 信息

**Endpoint**: `https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains`

**认证**: Bearer Token (Token Plan API Key)

## 重要：字段含义

⚠️ **关键发现**: `current_interval_usage_count` 字段表示的是**剩余配额**，不是已用量！

```
已用量 = current_interval_total_count - current_interval_usage_count
剩余配额 = current_interval_usage_count
```

## 使用方法

### 直接 curl 查询

```bash
curl -s --location 'https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains' \
  --header 'Authorization: Bearer <API_KEY>' \
  --header 'Content-Type: application/json'
```

### 使用脚本查询

```bash
uv run python3 scripts/query.py <API_KEY>
```

或设置环境变量后直接运行：

```bash
export MINIMAX_API_KEY="your_api_key"
uv run python3 scripts/query.py
```

## 输出示例

```
==================================================
 MiniMax Token Plan 用量查询
==================================================

【MiniMax-M2.7】
 5小时窗口：已用 1103 / 4500（24%）剩余 3397 次
 本周：已用 0 / 0（0%）剩余 0 次
 窗口：03-22 20:00 ~ 00:00
 重置：约 399 小时后

【image-01】
 5小时窗口：已用 1 / 120（0%）剩余 119 次
 本周：已用 1 / 840（0%）剩余 839 次
```

## 模型额度参考

| 模型 | 每日/窗口配额 | 重置周期 |
|------|--------------|----------|
| M2.7 文本 | 4500次/5小时 | 滚动重置 |
| image-01 图片 | 120张/日 | 每日重置 |
| Hailuo-2.3 视频 | 2个/日 | 每日重置 |
| music-2.5 音乐 | 4首/日 | 每日重置 |
| TTS HD 语音 | 11000字符/日 | 每日重置 |
