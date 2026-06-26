---
name: multi-bot-dedup
version: 1.0.0
description: 多飞书机器人去重回复规则。当同一用户通过多个机器人渠道同时发送相同消息时，AI 只回复一次，避免重复打扰。适用于配置了多路飞书机器人接入的 OpenClaw 场景。
---

# multi-bot-dedup — 多飞书机器人去重回复

## 使用场景

用户配置了多个飞书机器人（如兵部/吏部/礼部/钦天监/御书房/太医院等），同一条消息会同时触发多个机器人渠道，导致 AI 重复回复。本 skill 提供去重规则，确保每条消息只回复一次。

## 去重规则

收到消息时，**先检查以下条件，全部满足才跳过（NO_REPLY），否则正常回复**：

1. **发送者匹配**：`dedup_state.json` 中存在该 `sender_id` 的记录
2. **时间窗口**：上次回复时间距现在 < 30秒
3. **内容相同**：消息内容前50字的 hash 与上次相同

三条全满足 → **NO_REPLY（跳过）**
否则 → **正常回复，并更新 dedup_state.json**

## 状态文件

位置：`skills/multi-bot-dedup/dedup_state.json`

```json
{
  "ou_6a0ac66dd49d41eef5e5b85c68dafb9f": {
    "last_reply_time": 1742130000000,
    "last_message_hash": "abc123"
  }
}
```

## 操作步骤

**Step 1** — 读取 `dedup_state.json`（不存在则跳过检查，正常回复）

**Step 2** — 计算 `sender_id + 消息内容前50字` 的简单 hash

**Step 3** — 对比：
- `now - last_reply_time < 30000ms` 且 `hash == last_message_hash` → **NO_REPLY**
- 否则继续正常处理

**Step 4** — 回复后立即更新 `dedup_state.json`

## 例外（必须回复，不去重）

- 消息内容与上次不同（新话题）
- 距上次回复超过 30 秒
- 用户明确说"再说一遍"等重复指令

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 时间窗口 | 30秒 | 覆盖多路同时触发延迟（通常 < 5秒） |
| hash 长度 | 消息前50字 | 防止相同内容被误判为不同消息 |

## 注意

本 skill 是**行为规范**，不是可执行代码。AI 在每次处理飞书消息时主动遵守上述规则。
