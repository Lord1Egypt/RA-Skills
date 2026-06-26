#!/bin/bash
# TrackerDaemon flock wrapper - prevents multiple instances
# Must be run as root for /run/track-daemon.lock

LOCK_FILE="/run/track-daemon.lock"
PID_FILE="/root/.openclaw/workspace/skills/message-tracker/.daemon.pid"
SOCKET_FILE="/run/track-daemon.sock"
DAEMON_LOCK="/root/.openclaw/workspace/memory/index/.daemon.lock"

# Clean up residual files first
rm -f "$LOCK_FILE" "$PID_FILE" "$SOCKET_FILE" "$DAEMON_LOCK"

# 打开锁文件并获取文件描述符
exec 200>"$LOCK_FILE"

# 获取锁（阻塞）- 关键：在systemd环境下通过fd继承锁
flock 200

# 写入PID
echo $$ > "$PID_FILE"

# Register cleanup on exit
trap 'rm -f "$LOCK_FILE" "$PID_FILE" "$SOCKET_FILE" "$DAEMON_LOCK"' EXIT

# Keep flock acquired and start daemon
exec python3 /root/.openclaw/workspace/skills/message-tracker/track_v2.py daemon
