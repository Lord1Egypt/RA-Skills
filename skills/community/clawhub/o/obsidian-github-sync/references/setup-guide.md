# Obsidian GitHub Sync - 配置指南

## 快速开始

### 1. 环境变量配置

在使用同步脚本之前，需要设置以下环境变量：

```bash
# 必需
export OBSIDIAN_VAULT_DIR="/path/to/your/obsidian-vault"
export GITHUB_REMOTE_URL="git@github.com:username/repo.git"

# 可选
export GIT_USER_NAME="Your Name"
export GIT_USER_EMAIL="your@email.com"
export SYNC_LOG_FILE="/tmp/obsidian-sync.log"
export CONFLICT_FLAG_FILE="/tmp/obsidian-sync-conflict.flag"
```

### 2. SSH 密钥设置

确保本地 SSH 密钥已添加到 GitHub：

```bash
ssh-keygen -t ed25519 -C "your@email.com"
cat ~/.ssh/id_ed25519.pub
# 将公钥添加到 GitHub Settings -> SSH and GPG keys
```

### 3. 手动测试同步

```bash
# 进入 skill scripts 目录
cd /path/to/obsidian-github-sync/scripts

# 运行同步
./obsidian-sync.sh

# 检查冲突
./check-conflict.sh
```

## 自动同步设置

### 使用 Cron (Linux/Mac)

```bash
# 编辑 crontab
crontab -e

# 每天凌晨3点同步
0 3 * * * /path/to/obsidian-github-sync/scripts/obsidian-sync.sh

# 每天早上9点检查冲突
0 9 * * * /path/to/obsidian-github-sync/scripts/check-conflict.sh
```

### 使用 OpenClaw Cron

```bash
openclaw cron add --name "obsidian-sync" \
  --cron "0 3 * * *" \
  --command "/path/to/obsidian-github-sync/scripts/obsidian-sync.sh"

openclaw cron add --name "obsidian-check" \
  --cron "0 9 * * *" \
  --command "/path/to/obsidian-github-sync/scripts/check-conflict.sh"
```

## 冲突处理

当同步遇到冲突时：

1. 冲突标记文件会被创建（默认 `/tmp/obsidian-sync-conflict.flag`）
2. 手动进入 vault 目录解决冲突
3. 解决后重新运行同步脚本

```bash
cd $OBSIDIAN_VAULT_DIR
git status
# 解决冲突文件
git add -A
git rebase --continue
git push
```

## 多设备同步注意事项

1. **确保 Obsidian 关闭**后再运行同步，避免文件被占用
2. 在另一台设备上先 pull 再打开 Obsidian
3. 如果 Obsidian Sync 插件也启用，注意可能的冲突

## 故障排查

### 检查日志

```bash
tail -f /tmp/obsidian-sync.log
```

### 验证 Git 配置

```bash
cd $OBSIDIAN_VAULT_DIR
git remote -v
git status
```

### SSH 连接测试

```bash
ssh -T git@github.com
```
