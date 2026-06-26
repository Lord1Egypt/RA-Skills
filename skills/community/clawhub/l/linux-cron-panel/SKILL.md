---
name: linux-cron-panel
description: Linux 定时任务 Web 管理面板 - 通过 API 管理 Linux crontab，支持自动安装、任务创建、编辑、删除、立即执行和日志查看。当用户需要管理 Linux 定时任务、crontab、计划任务时使用本 skill。
---

# SKILL.md - Linux Cron Panel

配合 [Linux Cron Panel](https://github.com/wdmywm3/linux-cron-panel) 项目使用，通过 API 管理 Linux crontab，后端自动处理回调上报。

## 前置检查与自动安装

使用本 skill 前，必须先确保 Linux Cron Panel 服务可用。

### 检查与启动流程

**步骤 1：检查服务是否运行**
```bash
curl -sS http://127.0.0.1:5002/api/version
```
如果返回 JSON 版本信息，说明服务正常，直接使用。如果连接失败，继续下一步。

**步骤 2：检查并安装**
```bash
if [ -d "$HOME/.openclaw/linux-cron-panel" ]; then
  # 已安装，启动服务
  cd "$HOME/.openclaw/linux-cron-panel"
  bash start.sh
else
  # 未安装，执行安装
  git clone https://github.com/wdmywm3/linux-cron-panel.git "$HOME/.openclaw/linux-cron-panel"
  
  # 配置 systemd 服务
  mkdir -p "$HOME/.config/systemd/user"
  cat > "$HOME/.config/systemd/user/linux-cron-panel.service" << 'SERVICE_EOF'
[Unit]
Description=Linux Cron Panel API Service
After=network.target

[Service]
Type=forking
WorkingDirectory=%h/.openclaw/linux-cron-panel
ExecStart=bash start.sh
Restart=always
RestartSec=10
TimeoutStopSec=30

[Install]
WantedBy=default.target
SERVICE_EOF

  # 启动服务
  systemctl --user daemon-reload
  systemctl --user enable --now linux-cron-panel
fi
```

**步骤 3：验证**
```bash
curl -sS http://127.0.0.1:5002/api/version
```

## 服务信息

- **Base URL:** http://127.0.0.1:5002
- **数据格式:** JSON
- **任务主键:** id (格式: task_xxxxxxxx)

## 脚本管理

创建任务需要执行脚本时，**优先使用 `~/.openclaw/scripts/` 作为脚本存储路径**。

### 创建脚本目录

```bash
mkdir -p "$HOME/.openclaw/scripts"
```

### 创建并写入脚本示例

```bash
SCRIPT_DIR="$HOME/.openclaw/scripts"
mkdir -p "$SCRIPT_DIR"

# 创建脚本
cat > "$SCRIPT_DIR/my-task.sh" << 'EOF'
#!/bin/bash
echo "Task started at $(date)"
# 你的任务逻辑
echo "Task finished"
EOF

# 添加执行权限
chmod +x "$SCRIPT_DIR/my-task.sh"
```

### 创建任务时使用脚本路径

```bash
curl -sS -X POST http://127.0.0.1:5002/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "我的定时任务",
    "cron_expr": "*/10 * * * *",
    "command": "'"$SCRIPT_DIR"'/my-task.sh",
    "enabled": true
  }' | jq
```

## 日志输出规范

脚本如需自行写入日志文件，建议遵循以下格式以便后续查看和维护。

### 推荐格式

```
[YYYY-MM-DD HH:MM:SS] [LEVEL] 消息内容
```

| 字段 | 说明 | 示例 |
|------|------|------|
| 时间戳 | 日期时间 | `[2026-04-03 21:30:00]` |
| 级别 | INFO/WARN/ERROR | `[INFO]` |
| 消息 | 具体内容 | `备份完成，共 15MB` |

### 脚本示例

```bash
#!/bin/bash
LOG_FILE="$HOME/.openclaw/linux-cron-panel/logs/my-task.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$1] $2" >> "$LOG_FILE"
}

log "INFO" "任务开始"
# ... 任务逻辑 ...
log "INFO" "任务完成"
```

### 查看日志

```bash
# panel 任务执行日志（stdout/stderr）
curl -sS http://127.0.0.1:5002/api/tasks/{id}/log

# 脚本自行写入的日志
tail -f ~/.openclaw/linux-cron-panel/logs/my-task.log
```

## 核心 API

### 1. 查询版本号
```bash
curl -sS http://127.0.0.1:5002/api/version
```

### 2. 查询任务列表
```bash
curl -sS http://127.0.0.1:5002/api/tasks | jq
```

### 3. 查询任务详情
```bash
curl -sS http://127.0.0.1:5002/api/tasks/{id} | jq
```

### 4. 创建任务
```bash
curl -sS -X POST http://127.0.0.1:5002/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "任务名称",
    "cron_expr": "*/10 * * * *",
    "command": "/path/to/script.sh",
    "log_file": "/tmp/task.log",
    "enabled": true
  }' | jq
```
说明：后端会自动包装 command，添加回调上报逻辑，无需手动处理。

### 5. 编辑任务
```bash
curl -sS -X PUT http://127.0.0.1:5002/api/tasks/{id} \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "新名称",
    "cron_expr": "0 */6 * * *",
    "command": "新命令",
    "enabled": true
  }' | jq
```

### 6. 删除任务
```bash
curl -sS -X DELETE http://127.0.0.1:5002/api/tasks/{id} | jq
```

### 7. 立即运行任务
```bash
curl -sS -X POST http://127.0.0.1:5002/api/tasks/{id}/run | jq
```

### 8. 启用/禁用切换
```bash
curl -sS -X POST http://127.0.0.1:5002/api/tasks/{id}/toggle | jq
```

### 9. 读取任务日志
```bash
curl -sS http://127.0.0.1:5002/api/tasks/{id}/log
```

### 10. 状态汇总
```bash
curl -sS http://127.0.0.1:5002/api/status | jq
```

## 任务对象结构

```json
{
  "id": "task_d9ea3ed9ef4443c3",
  "name": "任务名称",
  "cron_expr": "*/10 * * * *",
  "command": "/path/to/script.sh",
  "log_file": "/tmp/task.log",
  "enabled": true,
  "last_run": "2026-04-03 13:00:00",
  "last_status": "success",
  "last_exit_code": 0,
  "history": [...]
}
```

## Cron 表达式格式

标准 Linux crontab 格式：

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── 星期 (0-7, 0和7都是周日)
│ │ │ └───── 月份 (1-12)
│ │ └─────── 日期 (1-31)
│ └───────── 小时 (0-23)
└─────────── 分钟 (0-59)
```

常用示例：
- `*/5 * * * *` - 每5分钟
- `0 * * * *` - 每小时
- `0 0 * * *` - 每天零点
- `0 9 * * 1-5` - 工作日9点

## 调用流程

1. **前置检查:** GET /api/version 验证服务运行
2. **创建脚本目录:** `mkdir -p ~/.openclaw/scripts`
3. **创建脚本:** 写入脚本并添加执行权限
4. **创建任务:** POST /api/tasks → 使用脚本路径作为 command
5. **验证:** GET /api/tasks/{id} 确认任务状态
6. **编辑/删除:** 使用对应 API 操作

## 项目地址

- Repository: https://github.com/wdmywm3/linux-cron-panel
