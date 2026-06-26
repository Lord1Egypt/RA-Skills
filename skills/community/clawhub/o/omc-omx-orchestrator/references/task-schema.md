# task.json Schema 详细说明

## 完整字段定义

```json
{
  "id": "2026-04-27-120000-fix-auth",           // 任务 ID（时间戳 + slug）
  "engine": "omc",                             // 引擎类型：omc|omx|autopilot
  "status": "running",                         // pending → running → completed/failed
  "command": "cd /abs/path && cat .../spec.md | claude -p - --tools \"default\"",
  "description": "修复认证模块（一句话摘要）",      // 任务描述
  "cwd": "/absolute/path/to/project",          // 工作目录（必须绝对路径）
  "pid": 12345,                                // 进程 PID
  "started_at": "2026-04-27T12:00:00+08:00",  // 启动时间（ISO 格式）
  "completed_at": null,                        // 完成时间
  "exit_code": null,                           // 退出码
  "result_file": "result.txt",                 // 结果文件名
  "notify": "telegram:<your_user_id>",             // 通知目标
  "detached": false,                           // 是否分离（重启后恢复时标记）
  "failure_reason": null,                      // 失败原因
  "preflight_ok": true,                        // 预检是否通过
  "sandbox_args": "--skip-git-repo-check"      // OMX 沙箱参数
}
```

## 字段说明

### 核心字段
- **id**: 格式 `YYYY-MM-DD-HHMMSS-{slug}`，唯一标识任务
- **engine**: 执行引擎，支持 `omc`（Claude Code）、`omx`（Codex CLI）、`autopilot`（循环模式）
- **status**: 状态流转 `pending` → `running` → `completed|failed`

### 路径和命令
- **cwd**: **必须**是已验证存在的绝对路径，禁止使用 `~` 简写
- **command**: 完整的执行命令，包含所有参数和重定向
- **sandbox_args**: OMX 特定参数，如 `--skip-git-repo-check`

### 进程管理
- **pid**: 后台进程的 PID，用于状态检查和清理
- **detached**: 重启后发现进程仍在运行时标记为 true

### 时间戳
- **started_at**: 任务开始时间，ISO 8601 格式，东八区时间
- **completed_at**: 任务完成时间，完成时写入

### 错误处理
- **exit_code**: 来自 exit_code 文件，0=成功，非0=失败
- **failure_reason**: 失败原因描述，如进程被杀、工具不可用等
- **preflight_ok**: Step 0 预检结果，false 时不应创建任务

### 通知
- **notify**: 完成通知目标，格式如 `telegram:user_id` 或 `qqbot:channel_id`
- **result_file**: 结果文件名，默认 "result.txt"

## autopilot 扩展字段

autopilot 模式时额外包含：

```json
{
  "mode": "autopilot",
  "pbv_round": 0,
  "pbv_status": "planning",
  "pbv_max_rounds": 5,
  "pbv_history": [
    {"round": 1, "plan": "plan-001.md", "result": "verify_failed", "error_summary": "..."}
  ]
}
```

- **mode**: 标识为 autopilot 循环模式
- **pbv_round**: 当前轮次（0-5）
- **pbv_status**: 循环内状态 `planning|plan_done|building|build_done|verifying|verify_passed|verify_failed`
- **pbv_history**: 每轮的执行结果历史