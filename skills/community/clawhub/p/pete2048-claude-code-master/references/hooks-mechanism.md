# Claude Code Hooks 机制详解

## 一、核心思想：Dispatch 模式

### 1.1 传统方式（高 Token 消耗）

```
OpenClaw ──> 每隔几秒查询 ──> Claude Code 状态
    ↑                                    │
    └────────────────────────────────────┘
              重复轮询 = Token 爆炸 💥
```

**问题：**
- 每 5-10 秒轮询一次
- 长任务可能运行 30+ 分钟
- Token 消耗 = 轮询次数 × 每次消耗
- 成本不可控

### 1.2 Hooks 方式（零轮询）

```
OpenClaw ──> 下达任务 ──> Claude Code 独立运行
                             │
                             ▼
                          完成后触发 Hook
                             │
                             ▼
                      自动通知 OpenClaw
```

**优势：**
- 发射后不管（Fire and Forget）
- 任务完成后自动通知
- 零轮询，零额外消耗
- 支持长时间任务

## 二、技术实现

### 2.1 双通道设计

| 通道 | 作用 | 为什么需要 |
|------|------|-----------|
| latest.json | 数据通道（存结果） | 持久化，不依赖服务在线 |
| wake event | 信号通道（通知到达） | 实时响应，秒级通知 |

**容错设计：**
- 即使 wake event 失败，latest.json 依然存在
- AGI 最迟在下次 heartbeat 时也能发现
- 数据不丢失，只是延迟

### 2.2 latest.json 格式

**文件位置：** `/tmp/claude-code-hooks/latest.json`

```json
{
  "session_id": "abc123def456",
  "timestamp": "2026-02-09T14:54:27+00:00",
  "cwd": "/home/ubuntu/projects/hn-scraper",
  "event": "SessionEnd",
  "output": "Claude Code 的完整输出内容...",
  "status": "done",
  "metadata": {
    "duration_seconds": 342,
    "files_modified": 5,
    "tests_passed": 12,
    "tests_failed": 0
  }
}
```

### 2.3 Wake Event 调用

**API Endpoint：**
```bash
POST http://127.0.0.1:18789/api/cron/wake
Authorization: Bearer $TOKEN
Content-Type: application/json

{
  "text": "Claude Code 任务完成，读取 latest.json",
  "mode": "now"
}
```

**mode 参数：**
- `"now"` - 立刻唤醒，不等下次 heartbeat
- `"next-heartbeat"` - 等下次 heartbeat 周期再处理（延迟但省资源）

## 三、Hook 脚本实现

### 3.1 Stop Hook

**触发时机：** 用户主动停止 Claude Code（Ctrl+C）

**文件位置：** `~/.claude/hooks/stop-hook.sh`

```bash
#!/bin/bash

# Claude Code Stop Hook
# 在用户停止任务时触发

SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
CWD="${CLAUDE_CWD:-$(pwd)}"
OUTPUT="${CLAUDE_OUTPUT:-}"
LATEST_FILE="/tmp/claude-code-hooks/latest.json"

# 创建目录
mkdir -p "$(dirname "$LATEST_FILE")"

# 写入 latest.json
cat > "$LATEST_FILE" <<EOF
{
  "session_id": "$SESSION_ID",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")",
  "cwd": "$CWD",
  "event": "Stop",
  "output": $(echo "$OUTPUT" | jq -Rs .),
  "status": "stopped"
}
EOF

# 发送 wake event（失败也不影响）
curl -X POST "http://127.0.0.1:18789/api/cron/wake" \
  -H "Authorization: Bearer ${OPENCLAW_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Claude Code 任务已停止，读取 latest.json\", \"mode\": \"now\"}" \
  || true

echo "✅ Stop hook executed"
```

### 3.2 SessionEnd Hook

**触发时机：** Claude Code 自然完成或结束

**文件位置：** `~/.claude/hooks/session-end-hook.sh`

```bash
#!/bin/bash

# Claude Code SessionEnd Hook
# 在任务完成时触发

SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
TIMESTAMP="${CLAUDE_TIMESTAMP:-$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")}"
CWD="${CLAUDE_CWD:-$(pwd)}"
OUTPUT="${CLAUDE_OUTPUT:-}"
STATUS="${CLAUDE_STATUS:-done}"
LATEST_FILE="/tmp/claude-code-hooks/latest.json"

# 创建目录
mkdir -p "$(dirname "$LATEST_FILE")"

# 解析元数据
DURATION=$(echo "$OUTPUT" | grep -oP 'Duration: \K[0-9]+' || echo "0")
FILES_MODIFIED=$(git diff --name-only HEAD 2>/dev/null | wc -l || echo "0")

# 写入 latest.json
cat > "$LATEST_FILE" <<EOF
{
  "session_id": "$SESSION_ID",
  "timestamp": "$TIMESTAMP",
  "cwd": "$CWD",
  "event": "SessionEnd",
  "output": $(echo "$OUTPUT" | jq -Rs .),
  "status": "$STATUS",
  "metadata": {
    "duration_seconds": $DURATION,
    "files_modified": $FILES_MODIFIED,
    "tests_passed": $(echo "$OUTPUT" | grep -c "✓" || echo "0"),
    "tests_failed": $(echo "$OUTPUT" | grep -c "✗" || echo "0")
  }
}
EOF

# 发送 wake event
curl -X POST "http://127.0.0.1:18789/api/cron/wake" \
  -H "Authorization: Bearer ${OPENCLAW_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Claude Code 任务完成，session: $SESSION_ID\", \"mode\": \"now\"}" \
  || true

echo "✅ SessionEnd hook executed"
```

### 3.3 通用 Hook 模板

```bash
#!/bin/bash
# Claude Code Hook Template

set -euo pipefail

# 环境变量（由 Claude Code 提供）
# CLAUDE_SESSION_ID - 会话 ID
# CLAUDE_TIMESTAMP - 时间戳
# CLAUDE_CWD - 工作目录
# CLAUDE_OUTPUT - 完整输出
# CLAUDE_STATUS - 状态 (done/error/stopped)
# CLAUDE_EVENT - 事件类型

# 配置
LATEST_FILE="/tmp/claude-code-hooks/latest.json"
WAKE_API="http://127.0.0.1:18789/api/cron/wake"
TOKEN="${OPENCLAW_TOKEN:-}"

# 函数：写入 latest.json
write_latest() {
  mkdir -p "$(dirname "$LATEST_FILE")"
  cat > "$LATEST_FILE" <<EOF
{
  "session_id": "${CLAUDE_SESSION_ID:-unknown}",
  "timestamp": "${CLAUDE_TIMESTAMP:-$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")}",
  "cwd": "${CLAUDE_CWD:-$(pwd)}",
  "event": "${CLAUDE_EVENT:-unknown}",
  "output": $(echo "${CLAUDE_OUTPUT:-}" | jq -Rs .),
  "status": "${CLAUDE_STATUS:-unknown}"
}
EOF
}

# 函数：发送 wake event
send_wake() {
  local text="$1"
  local mode="${2:-now}"

  if [[ -n "$TOKEN" ]]; then
    curl -s -X POST "$WAKE_API" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"text\": \"$text\", \"mode\": \"$mode\"}" \
      || true
  fi
}

# 主逻辑
main() {
  # 1. 持久化结果
  write_latest

  # 2. 发送通知
  send_wake "Claude Code ${CLAUDE_EVENT:-event}: ${CLAUDE_STATUS:-status}"

  # 3. 日志
  echo "✅ Hook executed: ${CLAUDE_EVENT:-unknown}"
}

main "$@"
```

## 四、配置步骤

### 4.1 创建 Hook 目录

```bash
mkdir -p ~/.claude/hooks
chmod +x ~/.claude/hooks
```

### 4.2 安装 Hook 脚本

```bash
# 下载或创建 hook 脚本
cat > ~/.claude/hooks/stop-hook.sh << 'EOF'
#!/bin/bash
# ... (粘贴上面的脚本)
EOF

cat > ~/.claude/hooks/session-end-hook.sh << 'EOF'
#!/bin/bash
# ... (粘贴上面的脚本)
EOF

# 添加执行权限
chmod +x ~/.claude/hooks/*.sh
```

### 4.3 配置环境变量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export OPENCLAW_TOKEN="your-token-here"
export CLAUDE_HOOKS_ENABLED="true"
```

### 4.4 Claude Code 配置

**文件位置：** `~/.claude/config.json`

```json
{
  "hooks": {
    "enabled": true,
    "stop": "~/.claude/hooks/stop-hook.sh",
    "sessionEnd": "~/.claude/hooks/session-end-hook.sh"
  }
}
```

## 五、使用示例

### 5.1 单任务 Dispatch

```python
# OpenClaw 发送任务
response = sessions_spawn(
    task="构建一个 Python 命令行计算器，支持加减乘除",
    runtime="acp",
    agentId="claude-code",
    mode="run"
)

# 不等待，继续处理其他事情
# Claude Code 完成后会自动触发 Hook
# 读取 latest.json 获取结果
```

### 5.2 多 Agent 并行（Agent Teams）

```bash
# 一次性 dispatch 多个任务
claude-code --dispatch "构建 Markdown 转 HTML 工具"
claude-code --dispatch "构建 REST API"
claude-code --dispatch "构建落沙模拟游戏"

# 所有任务并行运行
# 每个 agent 完成后都会触发 Hook
# OpenClaw 主进程不被阻塞
```

### 5.3 OpenClaw 处理 Wake Event

```python
# OpenClaw 收到 wake event
@app.route('/api/cron/wake', methods=['POST'])
def handle_wake():
    data = request.json
    text = data.get('text', '')

    if 'Claude Code 任务完成' in text:
        # 读取 latest.json
        with open('/tmp/claude-code-hooks/latest.json') as f:
            result = json.load(f)

        # 处理结果
        session_id = result['session_id']
        output = result['output']
        status = result['status']

        # 发送通知到用户
        send_message(
            channel="telegram",
            to="user",
            message=f"✅ 任务完成\n\n{output[:500]}..."
        )

    return {'status': 'ok'}
```

## 六、高级用法

### 6.1 条件触发 Hook

```bash
#!/bin/bash
# 只在测试全部通过时才通知

if echo "$CLAUDE_OUTPUT" | grep -q "All tests passed"; then
  curl -X POST "$WAKE_API" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"text": "✅ 所有测试通过", "mode": "now"}'
else
  echo "⚠️ 测试失败，不发送通知"
fi
```

### 6.2 结果分类处理

```bash
#!/bin/bash
# 根据状态分类处理

case "$CLAUDE_STATUS" in
  "done")
    emoji="✅"
    priority="normal"
    ;;
  "error")
    emoji="❌"
    priority="high"
    ;;
  "stopped")
    emoji="⏸️"
    priority="low"
    ;;
esac

curl -X POST "$WAKE_API" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"text\": \"$emoji Claude Code: $CLAUDE_STATUS\", \"mode\": \"now\", \"priority\": \"$priority\"}"
```

### 6.3 多项目隔离

```bash
#!/bin/bash
# 为不同项目创建独立的 latest.json

PROJECT_NAME=$(basename "$CLAUDE_CWD")
LATEST_FILE="/tmp/claude-code-hooks/${PROJECT_NAME}/latest.json"

mkdir -p "$(dirname "$LATEST_FILE")"

cat > "$LATEST_FILE" <<EOF
{
  "project": "$PROJECT_NAME",
  "session_id": "$CLAUDE_SESSION_ID",
  ...
}
EOF
```

## 七、故障排查

### 7.1 Hook 不触发

**检查清单：**
- [ ] 脚本有执行权限 (`chmod +x`)
- [ ] 文件路径正确
- [ ] config.json 配置正确
- [ ] 环境变量已设置
- [ ] Claude Code 版本支持 Hooks

**调试方法：**
```bash
# 手动测试 hook
CLAUDE_SESSION_ID="test" \
CLAUDE_OUTPUT="test output" \
CLAUDE_STATUS="done" \
CLAUDE_EVENT="SessionEnd" \
~/.claude/hooks/session-end-hook.sh
```

### 7.2 Wake Event 失败

**可能原因：**
1. Token 无效或过期
2. API endpoint 不可达
3. 网络问题

**解决方案：**
```bash
# 使用 || true 忽略失败
curl ... || true

# 或记录错误到日志
curl ... 2>> /tmp/hook-errors.log || true
```

### 7.3 latest.json 未生成

**检查：**
```bash
# 检查目录权限
ls -la /tmp/claude-code-hooks/

# 手动创建
mkdir -p /tmp/claude-code-hooks
chmod 777 /tmp/claude-code-hooks
```

## 八、最佳实践

### 8.1 幂等性设计

Hook 脚本应该是幂等的，多次执行不会产生副作用：
```bash
# 使用临时文件 + 原子操作
TMP_FILE=$(mktemp)
cat > "$TMP_FILE" <<EOF
...
EOF
mv "$TMP_FILE" "$LATEST_FILE"
```

### 8.2 超时保护

```bash
# 为 curl 设置超时
curl --max-time 5 -X POST "$WAKE_API" ... || true
```

### 8.3 日志记录

```bash
# 记录所有 hook 执行
LOG_FILE="/var/log/claude-code-hooks.log"
echo "$(date): Hook executed - $CLAUDE_EVENT" >> "$LOG_FILE"
```

### 8.4 错误隔离

```bash
# 即使 hook 失败，也不影响 Claude Code
set +e  # 允许命令失败
... hook 逻辑 ...
# 不检查退出码
```

---

**参考项目：** [claude-code-hooks](https://github.com/win4r/claude-code-hooks)
