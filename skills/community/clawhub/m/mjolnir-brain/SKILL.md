---
name: mjolnir-brain
description: "AI Agent 自进化记忆系统。核心功能 100% 本地运行 (纯 Markdown+JSON)。网络备份/节点通信为可选 opt-in，需手动配置凭证。"
---

# 🧠 Mjolnir Brain — AI Agent Self-Evolving Memory System

**版本**: v3.0.1  
**作者**: king6381  
**许可**: MIT

---

## 🔒 安全模型说明

| 功能类型 | 网络需求 | 凭证需求 | 默认状态 |
|----------|----------|----------|----------|
| **核心记忆** | ❌ 无 | ❌ 无 | ✅ 启用 |
| **备份功能** | ✅ 需要 | ✅ 需要 | ❌ 禁用 |
| **节点通信** | ✅ 需要 | ✅ 需要 | ❌ 禁用 |
| **自动化脚本** | ❌ 无 | ❌ 无 | ❌ 禁用 |

**核心承诺**: 默认 100% 本地运行，网络功能需明确 opt-in

---

## 核心功能 (本地运行)

- **三层记忆**: daily logs + MEMORY.md (≤20KB) + strategies.json
- **Write-Through**: 即时写入文件，不依赖网络
- **策略注册表**: 本地问题→解法映射
- **会话恢复**: 读取本地 workspace 文件

**无需任何二进制文件或网络访问**

---

## 可选功能 (Opt-In)

### 1. 网络备份 (需配置凭证)

**环境变量**:
```bash
# WebDAV 备份 (可选)
WEBDAV_URL=http://example.com/webdav/
WEBDAV_USER=username
WEBDAV_PASS=password

# SSH 备份 (可选)
SSH_HOST=user@host
SSH_PATH=/backup/mjolnir/
```

**注意**: 不配置则不启用任何网络功能

### 2. 节点间通信 (可选)

**用途**: 多 Agent 协作场景

**配置**:
```bash
MJOLNIR_USER=default  # 多用户模式用户名
```

### 3. 自动化脚本 (可选)

**依赖**: bash 4+, git, grep, tar/gzip

**注意**: 需手动添加 cron，默认不启用

---

## 快速安装

### 核心功能 (推荐，100% 本地)

```bash
cp -r templates/* $WORKSPACE/
cp strategies.json $WORKSPACE/
mkdir -p $WORKSPACE/memory
```

### 完整安装 (含可选功能)

```bash
# 1. 核心文件
cp -r templates/* $WORKSPACE/
cp strategies.json $WORKSPACE/

# 2. 脚本 (可选)
cp -r scripts/ $WORKSPACE/scripts/
chmod +x $WORKSPACE/scripts/*.sh

# 3. 环境变量 (可选)
# 编辑 ~/.bashrc 添加 WEBDAV_* 或 SSH_*

# 4. Cron (可选)
# crontab -e 添加定时任务
```

---

## 安全建议

1. **审查脚本**: 启用前阅读 `scripts/*.sh`
2. **最小权限**: 只启用需要的功能
3. **隔离测试**: 先在测试环境验证
4. **凭证保护**: 使用环境变量，不硬编码
5. **Dry Run**: 备份脚本支持 `DRY_RUN=1`

---

## 文档

- [架构说明](docs/architecture.md)
- [自学习机制](docs/self-learning.md)
- [最佳实践](docs/best-practices.md)
- [安全模型](docs/security.md)

