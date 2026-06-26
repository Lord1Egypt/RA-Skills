#!/bin/bash
# TrackerDaemon flock 包装脚本
# 用于手动启动时防止多实例

LOCK_FILE="/run/track-daemon.lock"
PID_FILE="/root/.openclaw/workspace/skills/message-tracker/.daemon.pid"

# 清理残留
rm -f "$LOCK_FILE" "$PID_FILE" /run/track-daemon.sock

# 创建锁
exec 200>"$LOCK_FILE"

# 获取锁（阻塞模式）
flock 200

# 写入 PID
echo $$ > "$PID_FILE"

# 注册退出清理
trap 'rm -f "$LOCK_FILE" "$PID_FILE" /run/track-daemon.sock' EXIT

# 执行实际进程
exec python3 /root/.openclaw/workspace/skills/message-tracker/track_v2.py daemon
