# GitHub Memory Sync - 定时备份配置

## 🕐 添加定时任务

### 方案 1：使用提供的 cron 脚本（推荐）

```bash
# 1. 编辑 crontab
crontab -e

# 2. 添加以下行（每天凌晨 2:30 自动备份）
30 2 * * * /root/.openclaw/workspace/skills/github-memory-sync/cron-backup.sh

# 3. 保存退出
```

### 方案 2：直接配置 cron

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天凌晨 2:30）
30 2 * * * cd /root/.openclaw/workspace/skills/github-memory-sync && \
  export GITHUBTOKEN="github_pat_xxx" && \
  export GITHUB_REPO="username/repo" && \
  export WORKSPACE_DIR="/root/.openclaw/workspace" && \
  bash sync.sh push >> /var/log/openclaw-memory-sync.log 2>&1
```

## ⏰ 推荐备份时间

| 时间 | Cron 表达式 | 说明 |
|------|-----------|------|
| 每天凌晨 2:30 | `30 2 * * *` | ✅ 推荐（用户休息时间） |
| 每天凌晨 3:00 | `0 3 * * *` | ✅ 备选 |
| 每 6 小时 | `0 */6 * * *` | 高频备份 |
| 每周一 9:00 | `0 9 * * 1` | 每周备份 |

## 📋 环境变量配置

在 `/etc/environment` 或 `~/.bashrc` 中添加：

```bash
# GitHub Memory Sync 配置
export GITHUBTOKEN="github_pat_xxxxxxxxxxxxxxxxx"
export GITHUB_REPO="username/openclaw-memory"
export GITHUB_BRANCH="main"
export WORKSPACE_DIR="/root/.openclaw/workspace"
export SYNC_MODE="full"
```

## 🔔 日志查看

```bash
# 查看最新日志
tail -f /var/log/openclaw-memory-sync.log

# 查看最近 10 次备份
tail -n 100 /var/log/openclaw-memory-sync.log

# 搜索失败记录
grep "❌" /var/log/openclaw-memory-sync.log
```

## 📧 邮件通知（可选）

如果需要备份失败时发送邮件通知：

```bash
# 安装邮件工具
apt-get install -y mailutils

# 修改 cron-backup.sh，在失败时发送邮件
if [ $EXIT_CODE -ne 0 ]; then
    echo "备份失败，请检查日志：$LOG_FILE" | mail -s "OpenClaw Memory Sync 失败" your@email.com
fi
```

## 🔄 手动测试

```bash
# 测试 cron 脚本
bash /root/.openclaw/workspace/skills/github-memory-sync/cron-backup.sh

# 查看日志
tail /var/log/openclaw-memory-sync.log
```

## ⚠️ 注意事项

1. **Token 安全** - 确保 cron 环境变量中的 Token 安全
2. **日志轮转** - 定期清理日志文件，避免占用过多空间
3. **网络检查** - 确保服务器能访问 GitHub
4. **失败重试** - 可配置失败后自动重试机制

## 🎯 完整配置示例

```bash
# 1. 设置环境变量
echo 'export GITHUBTOKEN="github_pat_xxx"' >> ~/.bashrc
echo 'export GITHUB_REPO="davinwang/openclaw-memory"' >> ~/.bashrc
source ~/.bashrc

# 2. 添加定时任务
(crontab -l 2>/dev/null; echo "30 2 * * * /root/.openclaw/workspace/skills/github-memory-sync/cron-backup.sh") | crontab -

# 3. 验证
crontab -l

# 4. 手动测试
bash /root/.openclaw/workspace/skills/github-memory-sync/cron-backup.sh
```

---

**版本**: 1.1.0  
**作者**: OpenClaw Workspace  
**许可**: MIT
