# OpenClaw Cursor Agent System

这是一个把 `OpenClaw -> tmux -> Cursor CLI` 串起来的三层执行架构，目标是让长时编码任务可以在后台持续运行、可监控、可干预、可回连。

## 目录结构

```text
cursor-agent-system/
├── README.md
├── scripts/
│   ├── common.sh
│   ├── spawn-cursor.sh
│   ├── check-status.sh
│   ├── attach-session.sh
│   ├── send-command.sh
│   └── kill-session.sh
├── templates/
│   └── cursor-task-prompt.md
├── status/
├── tasks/
└── logs/
```

## 环境要求

- `tmux` 3.3+
- `agent` 或 `cursor-agent`
- `python3`
- `bash`

Windows 原生不能直接跑 `tmux`，建议在 WSL 里使用本套脚本。

## 脚本说明

### 1. 启动任务

```bash
./scripts/spawn-cursor.sh \
  feature-auth \
  "实现 JWT 登录接口并补充测试" \
  /path/to/project \
  --priority high \
  --eta 45分钟
```

功能：

- 自动生成唯一会话名：`{project}-{task}-{timestamp}`
- 自动创建任务文件、状态文件、日志文件
- 在指定项目目录下创建 tmux 会话
- 通过真实 TTY 启动 Cursor CLI

### 2. 查看状态

```bash
./scripts/check-status.sh
./scripts/check-status.sh feature-auth
./scripts/check-status.sh myproj-feature-auth-20260318-180000
```

功能：

- 无参数时列出所有已记录任务
- 有参数时输出状态文件、tmux PID 和最近 30 行输出
- 自动回写状态快照

### 3. 实时附加

```bash
./scripts/attach-session.sh myproj-feature-auth-20260318-180000
```

退出方式：`Ctrl+B, D`

### 4. 发送额外指令

```bash
./scripts/send-command.sh myproj-feature-auth-20260318-180000 "/status"
./scripts/send-command.sh myproj-feature-auth-20260318-180000 "/focus 登录 API"
./scripts/send-command.sh myproj-feature-auth-20260318-180000 "把 JWT 签名算法改成 RS256"
```

### 5. 结束会话

```bash
./scripts/kill-session.sh myproj-feature-auth-20260318-180000
./scripts/kill-session.sh myproj-feature-auth-20260318-180000 --force
./scripts/kill-session.sh myproj-feature-auth-20260318-180000 --force --purge --yes
```

默认行为是先发送 `Ctrl+C` 尝试优雅退出；如果仍未结束，再使用 `--force` 强制终止。

## 状态文件约定

每个任务都会在 `status/` 下生成一个同名 JSON 文件，文件名与 tmux 会话名一致。这样 `check-status.sh`、`send-command.sh`、`kill-session.sh` 都可以直接通过会话名或任务别名解析到同一个状态文件。

核心字段包括：

- `taskId`
- `taskName`
- `sessionName`
- `status`
- `projectPath`
- `priority`
- `estimatedDuration`
- `progress.currentStep`
- `progress.completedSteps`
- `output.lastCapture`

## 与原型脚本相比的改进

- 用统一的 `common.sh` 收敛公共逻辑
- 避免依赖 `find + grep + head` 去猜测状态文件
- 支持用任务别名自动解析最近一次会话
- `spawn-cursor.sh` 支持 `--priority`、`--eta`、`--task-file`
- `check-status.sh` 支持批量列出全部任务
- `kill-session.sh` 提供确认、强制终止和清理文件选项

## 推荐工作流

1. 在 WSL/macOS 环境安装 `tmux` 和 Cursor CLI。
2. 进入 `cursor-agent-system/`。
3. 用 `spawn-cursor.sh` 启动后台任务。
4. 用 `check-status.sh` 轮询状态。
5. 需要人工调整时，用 `send-command.sh` 发指令。
6. 需要进入现场时，用 `attach-session.sh` 附加。
7. 任务结束后，用 `kill-session.sh` 做优雅收口。
