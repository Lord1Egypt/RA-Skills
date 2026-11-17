# 通道回推规则

## 默认规则

- 当前通道触发：结果回当前通道。
- 其他通道手动触发：结果回触发来源通道。
- 定时任务触发：结果推送到默认通道。
- 指定 `--reply-channel` 时，优先回指定通道。

## 当前实现

`scripts/channel_notify.py` 默认：

- 打印 Markdown 到 stdout。
- 保存一份到 `.temp/last_notification.md`。

接入所在平台具体通道时，在 `send_notification()` 中添加对应发送实现。
