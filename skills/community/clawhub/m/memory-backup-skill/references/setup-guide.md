# 备份体系搭建工作流

## 前提条件

- 一个 Git 远程仓库（推荐 Gitee / GitHub / GitLab 私有仓库）
- 生成一对 SSH 密钥专用于记忆备份

## Step 1：创建并初始化仓库

```bash
# 1. 在 Git 平台创建私有仓库，例如：
#    仓库名：openclaw-memory
#    私有仓库URL：git@gitee.com:yourname/openclaw-memory.git

# 2. 在服务器生成专用 SSH 密钥
ssh-keygen -t ed25519 -C "openclaw-memory-backup" -f ~/.ssh/openclaw_memory_key

# 3. 将公钥 ~/.ssh/openclaw_memory_key.pub 添加到 Git 平台的 SSH Keys
cat ~/.ssh/openclaw_memory_key.pub
# 复制输出，添加到 Gitee/GitHub/GitLab 的 SSH Keys 设置页

# 4. 验证 SSH 连接
ssh -i ~/.ssh/openclaw_memory_key git@gitee.com -T
# 期望输出：Welcome to Gitee [yourname]!
```

## Step 2：克隆仓库到工作目录

```bash
cd /root/.openclaw
git clone git@gitee.com:yourname/openclaw-memory.git workspace
# 或如果 workspace 已存在，直接初始化：
cd /root/.openclaw/workspace
git remote add origin git@gitee.com:yourname/openclaw-memory.git
```

## Step 3：建立基础记忆文件

至少建立以下最小结构：

```
workspace/
├── MEMORY.md          # 长期记忆入口（空文件即可，之后慢慢填）
├── SOUL.md            # AI 人格（可从系统模板或空白开始）
├── USER.md            # 用户基本信息
├── TOOLS.md           # 工具配置占位
└── memory/
    └── YYYY-MM-DD.md  # 当天日记
```

## Step 4：创建备份脚本

```bash
mkdir -p workspace/scripts
# 将 memory-backup.sh 放入 workspace/scripts/
chmod +x workspace/scripts/memory-backup.sh
```

配置脚本中的三个 TODO：
1. `GIT_REMOTE`：你的仓库地址
2. `MEMORY_BACKUP_KEY`：你的 SSH 私钥路径
3. `WORKDIR`：工作目录（默认 `/root/.openclaw/workspace`）

## Step 5：首次手动备份

```bash
cd /root/.openclaw/workspace
bash scripts/memory-backup.sh
```

期望输出：`[memory-backup] 备份已推送：memory-backup: 2026-04-29 xx:xx:xx +0800`

## Step 6：配置定时自动备份（可选）

```bash
# 编辑 crontab
crontab -e

# 每天早上 9 点自动备份
0 9 * * * cd /root/.openclaw/workspace && bash scripts/memory-backup.sh >> /root/.openclaw/logs/backup.log 2>&1
```

## Step 7：新机器/重装后恢复

```bash
# 1. 克隆仓库
git clone git@your-gitrepo:yourname/openclaw-memory.git /root/.openclaw/workspace

# 2. 安装 OpenClaw（如果未安装）
# 参考 OpenClaw 官方安装文档

# 3. 配置 SSH 密钥（同 Step 1）
# 将备份仓库的 SSH 公钥添加到 Git 平台

# 4. 验证
cd /root/.openclaw/workspace && bash scripts/memory-backup.sh

# 5. 重启 OpenClaw
openclaw restart
```

## 验证检查清单

- [ ] SSH 密钥对已生成并添加到 Git 平台
- [ ] `git clone` 成功
- [ ] `bash scripts/memory-backup.sh` 成功推送
- [ ] Git 平台上能看到第一次提交记录
- [ ] 定时任务（如配置）确认生效

## 常见问题

**Q: 推送时提示 `Permission denied (publickey)`**
→ SSH 密钥路径错误或未添加到 Git 平台，检查 `MEMORY_BACKUP_KEY` 路径是否正确。

**Q: 提示 `No memory changes to backup`**
→ 正常，说明没有新增内容需要提交，无需处理。

**Q: 敏感信息可以推送到仓库吗？**
→ 不可以。API 密钥、密码等不要写入记忆文件。写入 `TOOLS.md` 时只记录"某服务的 key 在 X 位置，是否需要轮换"。
