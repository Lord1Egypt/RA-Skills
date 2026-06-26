# lark-mention

飞书 @ 提及消息发送技能。

## 功能

在飞书群聊中向指定成员发送带真实 @ 提及的消息，支持：

- 单个成员 @ 提及
- 多个成员同时 @ 提及
- @all 全员
- 自定义消息内容

## 安装

```bash
clawhub install lark-mention
```

## 使用

```bash
# curl 方式
curl -X POST http://localhost:18780/proactive \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "<群ID>",
    "text": "<at user_id=\"<open_id>\">成员名</at> 你好~",
    "atOpenIds": ["<open_id>"]
  }'
```

```javascript
// Node.js 方式
import { sendMention } from 'lark-mention';

await sendMention({
  chatId: '<群ID>',
  text: '请查收~',
  members: [
    { open_id: '<open_id>', name: '张三' },
    { open_id: '<open_id>', name: '李四' }
  ]
});
```

## 前提条件

- `lark-openclaw-bridge` 服务必须运行在 `http://localhost:18780`
- 目标群聊需已添加飞书机器人
- 使用者需提供：群ID、成员 open_id（从飞书后台获取）

## 技术原理

飞书消息 API 的 `content` 必须是 JSON 字符串，包含 `text` 和 `mentions` 字段：

```json
{
  "text": "<at user_id=\"<open_id>\">成员名</at> 你好~",
  "mentions": [
    {
      "key": "<open_id>",
      "id": { "open_id": "<open_id>", "id_type": "open_id" },
      "name": "成员名"
    }
  ]
}
```
