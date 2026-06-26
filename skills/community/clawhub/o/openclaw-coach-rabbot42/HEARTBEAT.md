# HEARTBEAT.md

# OpenClaw 教练心跳检查

## 检查时间
- 早上 7:21 - 发送每日技巧
- 晚上 21:05 - 发送技巧选择

## 检查逻辑
1. 读取当前时间
2. 如果是 07:21 ±5min - 执行 send-daily-tip.sh
3. 如果是 21:05 ±5min - 执行 pick-daily-tip.sh
