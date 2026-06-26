---
name: jiuwu-message
description: 调用久吾消息网关HTTP接口给企业内部联系人发送消息。适用于：(1) 需要向企业内部同事发送通知或提醒时，(2) 需要批量发送内部消息时。当用户要求发送内部通知、提醒同事、向企业员工发消息、或调用消息网关时触发。
---

# 久吾消息网关

调用久吾消息网关发送企业内部消息。

## 环境配置

网关地址从环境变量 `JIUWU_MESSAGE_GATEWAY_URL` 读取，默认为 `http://192.168.1.213:5000`。可在 `~/.openclaw/workspace/.env` 或 `~/.openclaw/.env` 中配置。

## 脚本调用（优先使用）

**始终使用 `scripts/send_message.py`，不要直接 HTTP 请求。**

### 命令行调用

```bash
python scripts/send_message.py -c "工号" -t "消息内容" [-tt "标题"]
```

示例：
```bash
python scripts/send_message.py -c "1112" -t "您的报销单已审批通过" -tt "报销提醒"
```

### 批量发送

多个工号用英文逗号分隔：
```bash
python scripts/send_message.py -c "1112,1113,1114" -t "会议通知：今天下午2点开会" -tt "会议提醒"
```

### Python 代码调用

```python
import sys
sys.path.insert(0, 'skills/jiuwu-message/scripts')
from send_message import send_message

result = send_message(
    code="1112,1113",
    text="消息内容",
    title="可选标题"
)
```

## 参数说明

| 参数 | 缩写 | 必填 | 说明 |
|-----|-----|-----|------|
| `--code` | `-c` | 是 | 接收人工号，多个用英文逗号分隔 |
| `--text` | `-t` | 是 | 消息内容 |
| `--title` | `-tt` | 否 | 消息标题 |

## 响应格式

```json
{
  "success": true,
  "data": true,
  "message": "请求成功"
}
```

失败时 `success` 为 `false`，`message` 包含错误信息。
