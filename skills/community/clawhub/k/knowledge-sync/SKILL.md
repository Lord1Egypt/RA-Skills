---
name: knowledge-sync
version: 1.0.0
description: Real-time knowledge base synchronization for AI assistants. Supports inotifywait file monitoring, Git auto-push/pull, Nutstore sync, and multi-device consistency. Use for maintaining knowledge continuity across servers and local devices.
---

# Knowledge Sync - 知识库同步机制

> **核心原则**: Text > Brain，文件 > 记忆，同步 > 备份

---

## 🚀 快速开始

### systemd 服务配置

```bash
# 启用实时同步服务
systemctl --user enable sync-realtime.service
systemctl --user start sync-realtime.service
```

### Crontab 配置

```bash
# 每 5 分钟 Git push
*/5 * * * * /path/to/git-auto-push.sh

# 每小时 Git pull
0 * * * * cd /path/to/workspace && git pull origin main --rebase
```

---

## 🔧 核心功能

### 1. 实时同步

- ✅ inotifywait 文件监听
- ✅ 3-10 秒同步延迟
- ✅ 6 个目录监听（articles/memory/projects/docs/scripts/learnings）
- ✅ 自动排除（node_modules/__pycache__/.git）

### 2. Git 备份

- ✅ 每 5 分钟自动 push
- ✅ 每小时自动 pull
- ✅ 冲突检测和解决
- ✅ Gitee 远程备份

### 3. 多端同步

- ✅ 服务器→坚果云→Mac Obsidian
- ✅ 双向同步支持
- ✅ 多端一致性保障

---

## 📁 包含文件

```
knowledge-sync/
├── SKILL.md                  # 主文档
├── README.md                 # 项目说明
├── scripts/
│   ├── sync-realtime.sh      # 实时同步脚本
│   ├── git-auto-push.sh      # Git 自动推送
│   └── git-auto-pull.sh      # Git 自动拉取
└── docs/
    ├── QUICKSTART.md         # 快速上手
    └── sync-guide.md         # 同步指南
```

---

## 📊 同步架构

```
服务器 Workspace → 坚果云实时监听 → 本地同步 → Gitee → Mac Obsidian
         3-10 秒           实时         ≤5 分钟    ≤5 分钟
```

**总延迟**: 5-10 分钟（主要等待 Git 推送周期）

---

## 💡 使用场景

### 1. 实时文件同步

```bash
# 启动实时同步服务
systemctl --user start sync-realtime.service

# 查看状态
systemctl --user status sync-realtime.service
```

### 2. Git 自动备份

```bash
# 手动推送
./git-auto-push.sh

# 或定时执行
*/5 * * * * ./git-auto-push.sh
```

### 3. 多端同步

```bash
# Mac 端拉取
cd ~/Obsidian-MKH/我的知识/OpenClaw
git pull origin main
```

---

## 🔧 配置说明

### 监听目录配置

```bash
WATCH_DIRS=(
    "/path/to/workspace/articles"
    "/path/to/workspace/memory"
    "/path/to/workspace/projects"
    "/path/to/workspace/docs"
    "/path/to/workspace/scripts"
    "/path/to/workspace/learnings"
)
```

### 排除模式

```bash
EXCLUDE_PATTERN="\\.(log|tmp|swp|pyc)$|node_modules|__pycache__|\\.git"
```

---

## 📈 监控指标

| 指标 | 正常值 | 警告值 |
|------|--------|--------|
| 同步延迟 | <10 秒 | >30 秒 |
| Git push 间隔 | 5 分钟 | >10 分钟 |
| Git pull 间隔 | 1 小时 | >2 小时 |
| 冲突次数 | 0 | >1/周 |

---

## 🎓 最佳实践

### 1. 同步频率

- 实时同步：inotifywait 监听（3-10 秒）
- Git push：每 5 分钟
- Git pull：每小时

### 2. 冲突处理

- push 前先 pull
- 大改动分多次 commit
- 人工编辑前先 git pull

### 3. 备份策略

- Git 远程备份（Gitee）
- 坚果云本地备份
- 定期完整备份（每周）

---

## 📝 更新日志

### v1.0.0 (2026-03-15)

- ✅ 初始版本发布
- ✅ 实时同步功能
- ✅ Git 自动备份
- ✅ 多端同步支持

---

**维护者**: 虾球 🦐  
**许可**: MIT  
**状态**: 生产环境运行中
