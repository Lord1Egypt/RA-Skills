---
name: openclaw-migration-pro
description: |
  OpenClaw 环境迁移工具专业版。识别 Skills 与其维护数据的关联关系，
  完整迁移到另一个 OpenClaw 环境。
  打包 → 运输 → 归位，像搬家一样简单。
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
---

# OpenClaw Migration Pro

## 一句话定位

> 像搬家一样迁移 OpenClaw 环境。

## 核心概念

### 你的东西 vs 房东的东西

**你的东西**（需要迁移）：
- Memory（你的数据资产）
- Skills（你创建/修改的）
- Cron Jobs（你配置的任务）
- 工作区配置（SOUL.md, USER.md, AGENTS.md 等）
- OpenClaw 配置（openclaw.json）

**房东的东西**（不需要迁移）：
- OpenClaw 系统本身（新环境重新安装）
- API Keys（应该重新配置）
- Channel 配置（每台机器独立）

### 关联关系

每个 Skill 可能维护特定的数据目录：

| Skill | 维护的目录 |
|-------|-----------|
| just-note | memory/just-note/ |
| finance-analyst | memory/finance-*/ |
| daily-report | memory/daily-report/ |

迁移时需要保持这种关联关系。

## 快速开始

### 步骤 1: 分析（可选）

```bash
# 分析当前环境
openclaw-migration-pro analyze ~/migration/

# 输出：
# 🔍 分析 OpenClaw 环境...
# 📦 Skills: ClawHub 安装 50 个，工作区本地 3 个
# 📝 Memory: 1090 个文件，50MB
# ⏰ Cron Jobs: 1 个
```

### 步骤 2: 打包（源电脑）

```bash
# 打包所有数据（默认 ZIP 格式 + 自动发送）
openclaw-migration-pro pack --output ~/openclaw-pack.zip

# 输出：
# 📦 开始打包 OpenClaw...
# 📦 打包 Skills... ✅ 工作区 3 个，ClawHub 50 个
# 📦 打包 Memory... ✅ 1090 个文件
# 📦 打包配置... ✅ 已打包
# 📦 打包 Cron... ✅ 1 个
# 🗜️  正在压缩为 zip 格式...
# ✅ 打包完成：~/openclaw-pack.zip
# 📤 正在发送文件到当前频道...
# 备份大小：61MB
```

**打包选项：**
- `--compress zip`（默认）：Mac/Windows 兼容格式
- `--compress tar.gz`：Linux 推荐格式
- `--no-send`：禁用自动发送
- `--versioned`：带时间戳的版本化打包

### 步骤 3: 运输（用户手动）

```bash
# 复制到 U 盘/网盘/网络
cp -r ~/openclaw-pack/ /mnt/usb-drive/
# 或
rsync -av ~/openclaw-pack/ user@new-pc:~/
```

### 步骤 4: 归位（目标电脑）

```bash
# 1. 安装 OpenClaw（如果未安装）
curl -fsSL https://openclaw.ai/install.sh | bash

# 2. 归位
openclaw-migration-pro unpack --input ~/openclaw-pack/

# 输出：
# 🏠 开始归位 OpenClaw...
# 📦 恢复 Skills... ✅ 工作区 3 个，ClawHub 50 个
# 📦 恢复 Memory... ✅ 1090 个文件
# 📦 恢复配置... ✅ 已恢复
# 📦 恢复 Cron... ✅ 1 个
# ✅ 归位完成！
# 请重启 OpenClaw Gateway:
#   openclaw gateway restart
```

## 命令参考

### analyze - 分析环境

分析当前 OpenClaw 环境，生成 MANIFEST.json。

```bash
openclaw-migration-pro analyze [output-dir]

# 示例
openclaw-migration-pro analyze ~/migration/
```

**输出**:
- Skills 数量（ClawHub vs 工作区）
- Memory 文件数和大小
- Cron Jobs 数量
- MANIFEST.json

---

### pack - 打包

根据分析结果打包所有数据。

```bash
openclaw-migration-pro pack --output <dir>

# 示例
openclaw-migration-pro pack --output ~/openclaw-pack/
```

**打包内容**:
- `skills/workspace/` - 工作区 Skills（本地创建的）
- `skills/clawhub/` - ClawHub Skills（完整备份）
- `memory/` - 所有 Memory 文件
- `config/` - OpenClaw 配置 + 工作区配置
- `cron/` - Cron Jobs
- `BACKUP_INFO.md` - 备份清单

**排除内容**:
- API Keys（敏感信息）
- Channel 配置（每台机器独立）
- 缓存文件（可自动生成）

---

### unpack - 归位

在新环境恢复数据。

```bash
openclaw-migration-pro unpack --input <dir>

# 示例
openclaw-migration-pro unpack --input ~/openclaw-pack/
```

**归位流程**:
1. 检查 OpenClaw 是否安装
2. 恢复 Skills 到正确位置
3. 恢复 Memory 到正确位置
4. 恢复配置文件
5. 恢复 Cron Jobs
6. 提示重启 Gateway

---

## 打包内容详解

### Skills

| 类型 | 位置 | 说明 |
|------|------|------|
| **工作区 Skills** | `skills/workspace/` | 本地创建/修改的 Skills |
| **ClawHub Skills** | `skills/clawhub/` | 从 ClawHub 安装的 Skills |

**策略**:
- 工作区 Skills：完整打包
- ClawHub Skills：完整打包（可选重新安装）

---

### Memory

| 类型 | 位置 | 说明 |
|------|------|------|
| **日常 Memory** | `memory/YYYY-MM-DD.md` | 日记、笔记 |
| **Skill 维护** | `memory/<skill-name>/` | Skills 维护的数据 |
| **项目文件** | `memory/projects/` | 项目相关 |

**策略**: 完整打包，保持目录结构

---

### 配置

| 文件 | 位置 | 说明 |
|------|------|------|
| **OpenClaw 配置** | `~/.openclaw/openclaw.json` | Gateway 配置 |
| **工作区配置** | `SOUL.md`, `USER.md` 等 | 工作区规则 |
| **Cron Jobs** | `~/.openclaw/cron/` | 定时任务 |

**策略**: 完整打包（不包括 API Keys）

---

## 最佳实践

### 1. 迁移前

- [ ] 停止 OpenClaw Gateway
- [ ] 运行 analyze 检查
- [ ] 确保有足够磁盘空间（至少 100MB）

### 2. 迁移后

- [ ] 检查 Skills 数量
- [ ] 检查 Memory 文件
- [ ] 检查 Cron Jobs
- [ ] 重新配置 API Keys
- [ ] 重新配置 Channel

### 3. 定期备份

```bash
# 每周备份
0 3 * * 0 openclaw-migration-pro pack --output ~/weekly-backup/$(date +\%Y-\%m-\%d)/
```

---

## 故障排除

### 问题 1: 归位后 Skills 不可用

```bash
# 检查工作区 Skills
ls -1 ~/openclaw/workspace/skills/

# 重新安装 ClawHub Skills
npx clawhub install just-note --force
```

### 问题 2: Memory 文件丢失

```bash
# 检查打包内容
ls -1 ~/openclaw-pack/memory/

# 手动恢复
cp -r ~/openclaw-pack/memory/* ~/openclaw/workspace/memory/
```

### 问题 3: Cron Jobs 丢失

```bash
# 检查打包内容
ls -1 ~/openclaw-pack/cron/

# 手动恢复
cp ~/openclaw-pack/cron/*.json ~/.openclaw/cron/
```

---

## 与其他工具对比

| 功能 | openclaw-migration-pro | openclaw-backup | claw-sync |
|------|-----------------|-----------------|-----------|
| **完整打包** | ✅ | ✅ | ❌ |
| **关联关系识别** | ✅ | ❌ | ❌ |
| **选择性打包** | ✅ | ⚠️ | ❌ |
| **配置恢复** | ✅ | ❌ | ❌ |
| **Cron 迁移** | ✅ | ✅ | ❌ |
| **Git 同步** | ❌ | ❌ | ✅ |

---

## 许可证

MIT License

## 贡献

Issues and PRs welcome!

GitHub: https://github.com/your-org/openclaw-migration-pro
