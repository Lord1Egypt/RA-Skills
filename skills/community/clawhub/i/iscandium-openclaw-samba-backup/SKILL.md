---
name: iscandium-openclaw-samba-backup
description: 将 OpenClaw 数据备份到远程 Samba 服务器。当用户提到「备份 openclaw」「设置自动备份」时触发。
---

# OpenClaw Samba 备份

## 触发条件

| 关键词 | 动作 |
|--------|------|
| 「备份 openclaw」「backup openclaw」 | 执行完整备份流程 |
| 「自动备份」「定时备份」 | 设置定时任务 |

## 执行模式

| 选项 | 说明 |
|------|------|
| ✅ 自动执行 | 触发后直接执行备份，无需逐步确认 |

## 配置

配置文件：`config/default.json`（参数说明见 `config/params_schema.json`）

首次使用前，复制配置模板：

```bash
cp config/default.json.example config/default.json
```

| 参数 | 说明 |
|------|------|
| `target_server_ip` | Samba 服务器 IP |
| `target_share_name` | 共享文件夹名称 |
| `target_share_username` | Samba 用户名 |
| `target_share_password` | Samba 密码 |
| `source_admin_username` | 本服务器管理员用户名 |
| `source_admin_password` | 管理员密码（sudo 用） |
| `max_backups` | 保留备份数量（默认 7） |
| `source_dir` | 备份源路径（默认 ~/.openclaw） |
| `target_folder` | 目标文件夹名（默认 hostname） |
| `mount.vers` | SMB 版本（默认 2.0） |
| `mount.mount_point` | 挂载点（默认 /mnt/iscandium-openclaw-samba-backup） |

## 工作流（1 步）

| Step | 职责 | 执行者 | 文档 | 输入 | 输出 |
|------|------|--------|------|------|------|
| 01 | 执行备份 | 脚本 | `scripts/backup.sh` | config/default.json | Samba 共享目录 |

## 备份位置

```
//{target_server_ip}/{target_share_name}/{target_folder}/{timestamp}/
```

## 运行备份

```bash
bash ~/.openclaw/workspace/skills/iscandium-openclaw-samba-backup/scripts/backup.sh
```

## 设置定时备份

首次配置后，使用 OpenClaw 内置 cron：

```bash
openclaw cron add \
    --name "OpenClaw Samba 备份" \
    --cron "0 3 * * *" \
    --tz "<your-timezone>" \
    --message "运行备份：bash ~/.openclaw/workspace/skills/iscandium-openclaw-samba-backup/scripts/backup.sh" \
    --session isolated \
    --agent <your-agent> \
    --timeout-seconds 600 \
    --no-deliver
```

## 依赖

- `cifs-utils`（Samba 客户端）

```bash
sudo apt install cifs-utils
```

## 目录结构

```
iscandium-openclaw-samba-backup/
├── SKILL.md
├── config/
│   ├── default.json           # 私有配置（不发布）
│   ├── default.json.example  # 配置模板
│   └── params_schema.json    # 参数 schema
└── scripts/
    └── backup.sh             # 备份脚本
```
