# OpenClaw 关键文件备份技能

## 元信息

- **名称**: openclaw-backup
- **版本**: 1.1.0
- **描述**: OpenClaw 关键文件备份技能，支持全量备份和分类备份，保护您的核心配置和自定义技能
- **作者**: FrankMei (neverland_83@163.com)
- **运行时**: node18
- **主入口**: scripts/backup.js

## 功能说明

在 LLM 大模型的加持下，OpenClaw 功能很强大，但同时也很"傻"——它经常"自杀"（把 `openclaw.json` 等关键配置文件改坏，导致系统异常），也经常"自残"（把上一秒还能正常工作的 skill 搞得乱七八糟）。如果你也经常遇到这样的困扰，那就应该经常备份那些关键文件！这个 skill 就是帮你做这件事的。

备份 OpenClaw 运行所需的关键配置文件和用户数据，包括：

- **系统配置**: openclaw.json, .env, exec-approvals.json
- **核心文件**: AGENTS.md, SOUL.md, USER.md, IDENTITY.md, TOOLS.md, HEARTBEAT.md, MEMORY.md
- **技能目录**: skills/ 下所有自定义技能
- **其他数据**: cron/ 定时任务, devices/ 设备配置, memory/ 记忆数据

## 触发关键词

- 备份
- backup
- openclaw backup

## 使用方式

### 基本用法

```bash
# 通过 OpenClaw Agent 调用
node scripts/backup.js [options]

# 或让 agent 执行备份操作
```

### 命令行参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--full` | `-f` | 执行全量备份（默认） |
| `--system` | `-s` | 只备份系统配置 |
| `--workspace` | `-w` | 只备份核心文件 |
| `--skills` | `-k` | 只备份技能目录 |
| `--memory` | `-m` | 只备份记忆数据 |
| `--cron` | `-c` | 只备份定时任务配置 |
| `--devices` | `-d` | 只备份设备配置 |
| `--output <path>` | `-o` | 指定输出目录 |
| `--dry-run` | | 预览模式，显示将备份的文件但不实际执行 |
| `--retain <days>` | | 保留最近 N 天的备份，自动删除更早的备份 |
| `--clean` | | 清理模式：只删除旧备份，不执行新备份 |
| `--json` | `-j` | 以 JSON 格式输出结果 |

### 使用示例

#### 命令行调用

```bash
# 全量备份
node scripts/backup.js

# 只备份技能目录
node scripts/backup.js --skills

# 组合备份
node scripts/backup.js --system --workspace

# 自定义输出位置
node scripts/backup.js --output /path/to/backup

# 预览模式
node scripts/backup.js --dry-run

# JSON 输出（供程序解析）
node scripts/backup.js --json

# 备份并只保留最近14天的备份
node scripts/backup.js --full --retain 14

# 只清理旧备份（不执行新备份）
node scripts/backup.js --clean --retain 14

# 预览将删除的旧备份
node scripts/backup.js --clean --retain 14 --dry-run
```

#### 自然语言调用

你也可以直接对 OpenClaw 说以下话，让它帮你执行备份：

```
帮我备份一下 OpenClaw
备份 OpenClaw 所有配置
只备份我的技能目录
预览一下要备份哪些文件
```

OpenClaw 会识别你的意图并调用本技能完成备份操作。

#### Cron 定时任务

你可以在 OpenClaw 中设置定时任务，实现每天自动备份 + 自动清理：

```bash
# 每天凌晨2点备份，保留最近14天
0 2 * * * node ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.js --full --retain 14
```

通过 OpenClaw 的 cron 功能添加此任务后，系统会自动在每天凌晨执行备份，并只保留最近14天的备份文件。

## 输出文件

备份完成后会生成以下文件：

| 文件类型 | 文件名格式 | 说明 |
|----------|------------|------|
| 备份包 | `openclaw-backup-{type}-{YYYYMMDD}-{HHMMSS}.tar.gz` | 压缩备份文件 |
| 清单文件 | `openclaw-backup-{type}-{YYYYMMDD}-{HHMMSS}.json` | 备份清单（JSON格式） |
| 恢复指南 | `RECOVERY_GUIDE.md` | 手动恢复操作指南 |

默认输出目录: `~/backups/openclaw/`

## 重要说明

### 安全性

- **不自动恢复**: 本技能只提供备份功能，恢复需要根据生成的 `RECOVERY_GUIDE.md` 手动操作
- **敏感文件保护**: `.env` 文件会在清单中标记为敏感
- **权限保持**: 备份文件权限设为仅当前用户可读

### 文件处理

- 不存在的文件会被跳过，在清单中标记为 "skipped"
- 备份过程中不会修改原始文件
- 临时文件会在备份完成后自动清理

## 依赖

- Node.js >= 18.0.0
- fs-extra (文件操作)
- tar (压缩)
- commander (命令行解析)
- dayjs (日期处理)

## 安装

```bash
cd ~/.openclaw/workspace/skills/openclaw-backup
npm install  # 安装必要的依赖包（根据你的环境自动安装缺失的依赖）
```

## 注意事项

1. 备份前确保有足够的磁盘空间
2. 建议定期备份（可通过 cron 设置）
3. 重要修改后建议立即备份
4. 备份文件包含敏感信息，请妥善保管
5. 恢复时请仔细阅读恢复指导书

## 相关文档

- [备份文件清单](references/FILE_LIST.md)
- [恢复指导模板](references/RECOVERY_GUIDE_TEMPLATE.md)
- [配置示例](config/config.example.json) - **配置文件功能即将推出**