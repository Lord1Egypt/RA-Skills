---
name: github-memory-sync
description: 将 OpenClaw 的完整工作空间配置（SOUL.md, IDENTITY.md, USER.md, MEMORY.md, TOOLS.md, memory/*等）同步到 GitHub 进行备份和版本控制，支持跨服务器迁移。Use when user mentions GitHub backup, sync memory, migrate server, 备份配置，同步到 GitHub, or wants to backup/restore OpenClaw workspace.
---

# GitHub Memory Sync 技能

📝 将 OpenClaw 的 **完整工作空间配置** 同步到 GitHub 仓库进行备份和版本控制，支持跨服务器迁移。

## 同步范围

### 核心记忆文件（必须同步）

| 文件 | 路径 | 说明 | 敏感度 |
|------|------|------|--------|
| **SOUL.md** | `/` | AI 人格定义 | 🔒 高 |
| **IDENTITY.md** | `/` | AI 身份定义（名字、emoji 等） | 🔒 高 |
| **USER.md** | `/` | 用户信息 | 🔒 高 |
| **MEMORY.md** | `/` | 长期记忆 | 🔒 高 |
| **TOOLS.md** | `/` | 工具配置（SSH、摄像头等） | 🔒 高 |
| **HEARTBEAT.md** | `/` | 心跳任务配置 | 🟡 中 |
| **memory/*.md** | `memory/` | 日常记忆文件 | 🔒 高 |

### 可选配置文件

| 文件 | 路径 | 说明 | 建议 |
|------|------|------|------|
| **AGENTS.md** | `/` | 工作空间指南 | ✅ 推荐 |
| **BOOTSTRAP.md** | `/` | 初始化脚本（如有） | ⚪ 可选 |
| **skills/** | `skills/` | 自定义技能 | ✅ 推荐 |
| **avatars/** | `avatars/` | 头像图片 | ⚪ 可选 |

### 排除文件（不同步）

- `.git/` - Git 元数据
- `node_modules/` - 依赖包
- `*.log` - 日志文件
- `*.tmp`, `*.bak` - 临时文件
- `sessions/` - 会话数据（可能很大）

## 功能特性

1. **📤 完整备份** - 将所有记忆和配置文件推送到 GitHub
2. **📥 一键恢复** - 从 GitHub 拉取配置到新服务器
3. **📊 查看状态** - 检查本地和远程的差异
4. **📋 列出文件** - 显示所有同步的文件
5. **🔧 初始化仓库** - 首次设置 GitHub 仓库连接
6. **🔄 增量同步** - 只同步变化的文件
7. **📦 迁移模式** - 支持完整工作空间迁移到新服务器

## 配置要求

### 必需配置

**GitHub Token:**
- 需要一个 Personal Access Token
- 权限要求：`repo`（仓库读写权限）
- 生成地址：https://github.com/settings/tokens/new

**GitHub 仓库:**
- 格式：`username/repository-name`
- 示例：`myusername/openclaw-memory-backup`
- 建议设为 **Private**（私有仓库），因为 memory 可能包含敏感信息

### 配置方式

#### 方案 A：使用环境变量（推荐用于测试）

```bash
export GITHUBTOKEN="ghp_xxxxxxxxxxxxxxxxx"
export GITHUB_REPO="yourusername/your-repo"
```

#### 方案 B：配置文件（推荐用于生产）

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "github-memory-sync": {
        "enabled": true,
        "apiKey": "ghp_xxxxxxxxxxxxxxxxx",
        "env": {
          "GITHUBTOKEN": "ghp_xxxxxxxxxxxxxxxxx",
          "GITHUB_REPO": "username/memory-backup",
          "GITHUB_BRANCH": "main",
          "WORKSPACE_DIR": "/root/.openclaw/workspace"
        }
      }
    }
  }
}
```

## 使用示例

### 首次初始化

```
用户："初始化 GitHub memory 仓库"
AI: [获取 Token 和仓库信息后执行初始化]
```

### 推送更新（备份）

```
用户："同步到 GitHub" / "备份配置"
AI: [执行推送操作，同步所有记忆和配置文件]
```

### 拉取更新（恢复）

```
用户："从 GitHub 拉取配置" / "恢复备份"
AI: [执行拉取操作，恢复所有文件]
```

### 查看状态

```
用户："检查同步状态"
AI: [显示本地和远程的差异]
```

### 🚀 服务器迁移（完整流程）

**在原服务器上：**
```
用户："备份所有配置到 GitHub"
AI: [执行完整推送，包括 SOUL.md, IDENTITY.md, USER.md, MEMORY.md, TOOLS.md, memory/* 等]
```

**在新服务器上：**
```
用户："从 GitHub 恢复配置"
AI: [执行以下步骤]
1. 克隆 GitHub 仓库到临时目录
2. 复制所有记忆和配置文件到 workspace
3. 保留新服务器的通道配置（不覆盖 openclaw.json 中的通道凭证）
4. 验证文件完整性
```

### 部分恢复

```
用户："只恢复 MEMORY.md"
AI: [仅拉取指定文件]

用户："恢复 memory 目录"
AI: [仅拉取 memory/*.md 文件]
```

## 安全提醒

⚠️ **重要安全注意事项：**

1. **Token 保护**
   - ❌ 不要把 Token 发送到任何公开渠道
   - ❌ 不要在代码中硬编码 Token
   - ✅ 使用环境变量或配置文件
   - ✅ 定期轮换 Token

2. **仓库隐私**
   - 🔒 建议将 GitHub 仓库设为 **Private**（私有）
   - 👁 memory 可能包含敏感信息
   - 📝 审查 memory 内容再上传

3. **权限最小化**
   - 只给 Token 必要的权限（`repo`）
   - 避免使用具有广泛权限的 Token
   - 设置 Token 过期时间（不要永不过期）

## 激活技能

当用户提到以下关键词时激活此技能：
- "GitHub memory"
- "同步 memory"
- "备份 memory"
- "GitHub 备份"
- "memory 同步"
- "github-memory-sync"

## 配置流程

### 1. 获取配置信息
- 向用户询问 GitHub Token
- 向用户询问 GitHub 仓库地址（或帮其创建）

### 2. 保存配置
- 将 Token 和仓库信息保存到配置文件或环境变量
- 提醒用户注意安全事项

### 3. 执行操作
- 根据用户请求执行 init/push/pull/status/migrate 操作
- 显示操作结果

### 4. 验证同步
- 推送后验证远程仓库文件完整性
- 拉取后验证本地文件完整性

## 注意事项

- 首次使用必须先执行 `init` 初始化
- 推送前建议先拉取，避免冲突
- 定期检查 Token 是否过期
- 建议启用 GitHub 的两因素认证
- **通道凭证不同步** - openclaw.json 中的 tokens/secrets 不应上传到 GitHub
- **迁移模式** - 使用 `migrate` 命令可安全恢复到新服务器

## 相关文件

- `scripts/sync_to_github.py` - 同步脚本
- `references/migration-guide.md` - 完整服务器迁移指南
- `references/backup-policy.md` - 备份策略和安全建议

## 快速参考

### 常用命令

```bash
# 初始化（首次使用）
python scripts/sync_to_github.py init

# 备份
python scripts/sync_to_github.py push

# 恢复
python scripts/sync_to_github.py pull

# 查看状态
python scripts/sync_to_github.py status

# 迁移到新服务器
BACKUP_DIR=/tmp/openclaw-restore python scripts/sync_to_github.py migrate
```

### 对话触发词

- "备份到 GitHub"
- "同步配置"
- "恢复备份"
- "迁移到新服务器"
- "检查同步状态"
- "github-memory-sync"
