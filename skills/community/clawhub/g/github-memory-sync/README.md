# 📦 GitHub Memory Sync

将 OpenClaw 完整工作空间配置同步到 GitHub 进行备份和版本控制。

## ✅ 功能特性

- ✅ **完整备份** - 同步所有配置文件（SOUL.md, IDENTITY.md, USER.md, MEMORY.md, TOOLS.md 等）
- ✅ **记忆文件** - 同步 memory/*.md 日常记忆
- ✅ **技能备份** - 同步 skills/ 自定义技能
- ✅ **一键恢复** - 从 GitHub 拉取配置到新服务器
- ✅ **状态检查** - 查看本地和远程的差异
- ✅ **定时备份** - 支持 cron 自动备份
- ✅ **增量同步** - 只同步变化的文件

## 🚀 快速开始

### 1. 配置环境变量

```bash
export GITHUBTOKEN="github_pat_xxx"
export GITHUB_REPO="username/openclaw-memory"
export WORKSPACE_DIR="/root/.openclaw/workspace"
```

### 2. 同步到 GitHub

```bash
cd /root/.openclaw/workspace/skills/github-memory-sync
bash sync.sh push
```

### 3. 从 GitHub 恢复

```bash
bash sync.sh pull
```

## 📋 同步文件列表

### 核心文件
- ✅ SOUL.md - AI 人格定义
- ✅ IDENTITY.md - AI 身份定义
- ✅ USER.md - 用户信息
- ✅ MEMORY.md - 长期记忆
- ✅ TOOLS.md - 工具配置
- ✅ HEARTBEAT.md - 心跳任务
- ✅ AGENTS.md - 工作指南
- ✅ memory/*.md - 日常记忆文件

### 可选文件
- ✅ skills/ - 自定义技能
- ✅ avatars/ - 头像图片
- ✅ BOOTSTRAP.md - 初始化脚本

## ⏰ 定时备份

### 添加自动备份任务

```bash
# 每天凌晨 2:30 自动备份
(crontab -l 2>/dev/null; echo "30 2 * * * /root/.openclaw/workspace/skills/github-memory-sync/cron-backup.sh") | crontab -
```

### 查看备份日志

```bash
tail -f /var/log/openclaw-memory-sync.log
```

## 📖 完整文档

- [SKILL.md](./SKILL.md) - 技能详细说明
- [CRON.md](./CRON.md) - 定时任务配置指南

## 🔒 安全提醒

- ⚠️ 使用 Private 仓库
- ⚠️ 保护 GitHub Token
- ⚠️ 定期轮换 Token
- ⚠️ 不要同步敏感凭证

---

**版本**: 1.1.0  
**作者**: OpenClaw Workspace  
**许可**: MIT  
**GitHub**: https://github.com/davinwang/openclaw-memory
