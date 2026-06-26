---
name: openclaw-backup
version: 1.0.0
description: 一键备份 OpenClaw 工作区，支持必选/可选内容，生成 ZIP 压缩包（含 SHA256 校验）
author: 木木
---

# OpenClaw Backup 🔒

一键备份 OpenClaw 工作区的重要文件，支持自定义选择备份内容。

## 触发条件

当用户提到以下关键词时激活此技能：
- "备份 OpenClaw"
- "备份工作区"
- "backup openclaw"
- "导出配置"
- "打包技能"

## 备份内容

### 🟢 必选（默认包含，不可取消）

| 文件/目录 | 说明 |
|-----------|------|
| `MEMORY.md` | 长期记忆 |
| `memory/` | 每日记忆日志 |
| `skills/` | 已安装技能 |
| `SOUL.md` | 身份定义 |
| `IDENTITY.md` | 角色配置 |
| `USER.md` | 用户信息 |
| `AGENTS.md` | Agent 配置 |
| `TOOLS.md` | 工具配置 |
| `HEARTBEAT.md` | 心跳任务 |

### 🟡 可选（用户选择）

| 文件/目录 | 说明 |
|-----------|------|
| `docs/` | 文档目录 |
| `logs/` | 日志文件 |
| `tasks/` | 任务文件 |
| `knowledge/` | 知识库 |
| `.openclaw/config.json` | 配置文件 |

## 使用方法

### 交互式备份（默认，可选择内容）

```bash
python3 ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.py
```

### 快速备份（仅必选内容）

```bash
python3 ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.py --required-only
```

### 指定输出路径

```bash
python3 ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.py --output ~/Desktop/openclaw-backup
```

## 输出

- 生成时间戳命名的压缩包：`openclaw-backup-YYYYMMDD-HHMMSS.zip`
- 包含备份清单：`BACKUP_MANIFEST.txt`
- 可选：生成校验和文件

## 恢复备份

```bash
python3 ~/.openclaw/workspace/skills/openclaw-backup/scripts/restore.py <backup.zip>
```

## 安全提示

- ⚠️ **备份文件未加密** - ZIP 包使用标准压缩，不包含加密
- 备份文件可能包含敏感信息（API Keys、记忆等）
- 建议手动加密存储（如用 7z 加密或存放在安全位置）
- 不要将备份文件上传到公开仓库
- 恢复时会验证路径安全，防止 ZipSlip 攻击

---

**木木提示**：定期备份，数据安全 🌲
