---
name: lark-mention
description: 飞书 @ 提及专属技能。支持在群聊中向指定成员发送带真实 @ 提及的消息，解决飞书无法通过纯文本标签艾特成员的问题。触发场景：群里艾特成员、艾特全员、发送带 @ 的通知公告。
---
# lark-mention — 飞书 @ 提及技能

## 核心能力

将自然语言转换为飞书标准 @ 提及消息，自动生成 mentions 字段并发送。

## API 配置

```
LARK_BRIDGE_URL = http://localhost:18780/proactive
```

## 使用方式

### 方式一：通过 curl 调用

```bash
curl -X POST http://localhost:18780/proactive \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "<群ID>",
    "text": "<at user_id=\"<open_id>\">成员名</at> 消息内容",
    "atOpenIds": ["<open_id>"]
  }'
```

### 方式二：通过 Node.js 模块调用

```javascript
import { sendMention } from './scripts/lark-mention.mjs';

await sendMention({
  chatId: '<群ID>',
  text: '请查收~',
  members: [
    { open_id: '<open_id>', name: '张三' },
    { open_id: '<open_id>', name: '李四' }
  ]
});
```

## 技术原理

### 飞书 @ 提及的正确格式

飞书消息 API 的 `content` 必须是 JSON 字符串，包含 `text` 和 `mentions` 字段：

```json
{
  "text": "<at user_id=\"<open_id>\">成员名</at> 消息内容",
  "mentions": [
    {
      "key": "<open_id>",
      "id": { "open_id": "<open_id>", "id_type": "open_id" },
      "name": "成员名"
    }
  ]
}
```

**关键点：**
- `text` 中用 `<at user_id="<open_id>">display_name</at>` 占位
- `mentions` 数组的 `key` 必须和 `<at user_id="...">` 里的值完全一致
- `msg_type` 必须是 `"text"`，`interactive` 卡片类型不支持 `mentions`

### 常见错误

| 错误写法 | 原因 |
|---|---|
| `<at id="<open_id>">` | 飞书不支持 `id` 属性，必须用 `user_id` |
| `mentions` 的 `key` 和 text 不匹配 | 导致渲染失败 |
| `msg_type` 写成 `interactive` | 卡片消息不支持 `mentions` 字段 |
| 纯文本写在 `<at>` 外部 | 飞书不渲染任何 `<at>` 标签 |

## 依赖

- `lark-openclaw-bridge` 服务必须运行在 `http://localhost:18780`
- 目标群聊需已添加飞书机器人
- 使用者需提供：群ID、成员 open_id（从飞书后台获取）
