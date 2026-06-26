# OpenCode 自动回调脚本

## 问题
OpenClaw 调用 `opencode run` 执行任务后，需要手动调用回调脚本通知 OpenClaw。如果忘记调用，OpenClaw 就不知道任务完成，无法继续工作。

## 解决方案
使用自动回调脚本，让 OpenCode 任务完成后自动通知 OpenClaw。

## 脚本说明

### 1. opencode-auto-callback.sh（推荐）
简化版脚本，直接调用 `opencode run` 并自动回调。

**用法：**
```bash
./opencode-auto-callback.sh <session_key> <task_description> <opencode_args...>
```

**示例：**
```bash
# 简单任务
./opencode-auto-callback.sh "agent:main:qqbot:direct:xxx" "修复bug" "修复登录问题"

# 指定模型
./opencode-auto-callback.sh "agent:main:qqbot:direct:xxx" "添加功能" -m opencode/mimo-v2-pro-free "添加用户认证"

# 继续会话
./opencode-auto-callback.sh "agent:main:qqbot:direct:xxx" "继续任务" -c "继续刚才的工作"
```

### 2. opencode-run-with-callback.sh
包装器脚本，可以包装任意 opencode 命令。

**用法：**
```bash
./opencode-run-with-callback.sh <session_key> <task_description> <opencode_command> [timeout]
```

**示例：**
```bash
./opencode-run-with-callback.sh "agent:main:qqbot:direct:xxx" "修复bug" "opencode run '修复登录问题'" 3600
```

## 工作流程

1. OpenClaw 调用自动回调脚本
2. 脚本发送"任务开始"通知
3. 脚本执行 `opencode run`（使用 JSON 格式输出）
4. 任务完成后，脚本解析结果并发送"任务完成/失败"通知
5. OpenClaw 收到通知，继续处理其他任务

## 获取 Session Key

Session Key 格式：`agent:main:qqbot:direct:xxx`

可以从 sessions.json 文件获取：
```bash
cat ~/.openclaw/agents/main/sessions/sessions.json | jq 'keys'
```

## 结果文件

任务结果保存在 `~/.openclaw/task-results/` 目录：
- `task-<timestamp>.txt` - 结果文本
- `task-<timestamp>.log` - 执行日志
- `task-<timestamp>.jsonl` - JSON 输出（用于解析）

## 注意事项

- 脚本会自动处理超时（默认 1 小时）
- 任务开始和完成都会发送通知
- 结果摘要会自动提取（最多 2000 字符）
- 如果任务失败，会包含退出码信息
