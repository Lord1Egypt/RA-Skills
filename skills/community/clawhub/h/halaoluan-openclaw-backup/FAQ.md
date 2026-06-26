# OpenClaw Backup - 常见问题

## 📋 目录

- [基础问题](#基础问题)
- [使用问题](#使用问题)
- [安全问题](#安全问题)
- [性能问题](#性能问题)
- [故障排查](#故障排查)

---

## 🔰 基础问题

### Q1: 为什么需要备份 OpenClaw？

**A**: OpenClaw 包含重要数据：
- ✅ **配置文件**：API Key、渠道配置
- ✅ **记忆数据**：MEMORY.md、对话历史
- ✅ **Skills**：自定义技能和脚本
- ✅ **渠道登录状态**：Telegram、WeChat等

一旦丢失，需要重新配置所有内容。

---

### Q2: 备份包含哪些数据？

**A**: 完整备份 `~/.openclaw` 目录，包括：
- `config.yaml` - 主配置
- `workspace/` - 工作空间（MEMORY.md、记忆文件）
- `skills/` - 已安装的Skills
- `plugins/` - 插件
- `logs/` - 日志（可选排除）

---

### Q3: 加密备份和普通备份有什么区别？

**A**:

| 特性 | 普通备份 | 加密备份 |
|------|---------|---------|
| **安全性** | ❌ 明文，任何人都能解压 | ✅ AES-256加密 |
| **速度** | ⚡ 快 | 稍慢（需加密） |
| **云盘上传** | ❌ 不推荐 | ✅ 安全 |
| **恢复** | 直接解压 | 需要密码 |

**建议**：云盘备份必须用加密，本地备份可用普通备份。

---

### Q4: 备份文件多大？

**A**: 取决于你的数据量：
- **典型大小**：500 MB - 2 GB
- **影响因素**：
  - 对话历史数量
  - Skills数量
  - 日志文件大小

**优化建议**：
```bash
# 排除日志文件（可减小50%）
find ~/.openclaw -name "*.log" -delete
```

---

### Q5: 多久备份一次？

**A**: 推荐策略：
- 🔵 **每天**：如果频繁使用，重要对话多
- 🟢 **每周**：普通使用（推荐）
- 🟡 **每月**：轻度使用

**关键时机**：
- 修改配置后
- 新增Skill后
- 完成重要对话后
- 系统升级前

---

## 🛠️ 使用问题

### Q6: 如何验证备份是否成功？

**A**:
```bash
# 1. 检查文件存在
ls -lh ~/Desktop/OpenClaw_Backups/

# 2. 验证SHA256
shasum -c openclaw_backup_2026-03-13_20-40-13.tar.gz.enc.sha256

# 3. 测试解压（不影响当前环境）
mkdir /tmp/test_backup
tar -xzf backup.tar.gz -C /tmp/test_backup
ls /tmp/test_backup/.openclaw/
```

---

### Q7: 忘记加密密码怎么办？

**A**: **无法恢复**。AES-256加密无法暴力破解。

**预防措施**：
1. 使用密码管理器（1Password/Bitwarden）
2. 写在纸上，放保险柜
3. 同时创建普通备份（本地保存）

---

### Q8: 如何定时自动备份？

**A**:
```bash
# 运行配置脚本
bash ~/.openclaw/skills/openclaw-backup/scripts/setup_cron.sh

# 选择频率（推荐：每周日21:00）
选择 [1-4]: 2

# 验证
crontab -l
```

---

### Q9: 如何备份到云盘？

**A**:

**iCloud Drive**:
```bash
export OPENCLAW_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/OpenClaw_Backups"
bash scripts/backup_encrypted.sh
```

**Google Drive** (需安装客户端):
```bash
export OPENCLAW_BACKUP_DIR="$HOME/Google Drive/OpenClaw_Backups"
bash scripts/backup_encrypted.sh
```

**Dropbox**:
```bash
export OPENCLAW_BACKUP_DIR="$HOME/Dropbox/OpenClaw_Backups"
bash scripts/backup_encrypted.sh
```

---

### Q10: 如何删除旧备份？

**A**:
```bash
cd ~/Desktop/OpenClaw_Backups

# 方式1：手动删除
rm openclaw_backup_2026-03-01_*.tar.gz*

# 方式2：只保留最近5个
ls -t openclaw_backup_*.tar.gz.enc | tail -n +6 | xargs rm -f
ls -t openclaw_backup_*.tar.gz.enc.sha256 | tail -n +6 | xargs rm -f

# 方式3：删除30天前的备份
find . -name "openclaw_backup_*.tar.gz*" -mtime +30 -delete
```

---

## 🔒 安全问题

### Q11: 备份文件安全吗？

**A**:

**加密备份**：
- ✅ AES-256-CBC加密
- ✅ PBKDF2密钥派生（100,000轮）
- ✅ 随机盐值
- ✅ 符合NIST标准

**未加密备份**：
- ❌ 明文存储
- ⚠️ 包含敏感数据（API Key、Token）
- ❌ 不建议上传云盘

---

### Q12: 可以用弱密码吗？

**A**: **强烈不建议**。

**弱密码示例**（不要用）：
- ❌ `123456`
- ❌ `password`
- ❌ 生日、姓名

**强密码要求**：
- ✅ 至少12位
- ✅ 包含大小写字母、数字、符号
- ✅ 不包含个人信息
- ✅ 使用密码生成器

**推荐**：
```bash
# macOS 生成随机密码
openssl rand -base64 16
```

---

### Q13: 备份可以共享吗？

**A**: **不建议**。备份包含：
- API Key（可能产生费用）
- Telegram Bot Token（可被滥用）
- 个人对话历史

**如果必须共享**：
1. 创建新的OpenClaw实例
2. 移除所有敏感数据
3. 加密后再共享

---

## ⚡ 性能问题

### Q14: 备份太慢怎么办？

**A**:

**诊断**：
```bash
# 检查数据大小
du -sh ~/.openclaw

# 检查磁盘速度
dd if=/dev/zero of=/tmp/test bs=1M count=1000
```

**优化方案**：
1. **使用并行压缩**：
   ```bash
   brew install pigz
   # 修改脚本使用 pigz
   ```

2. **排除大文件**：
   ```bash
   # 排除日志
   rm -rf ~/.openclaw/logs/*.log
   
   # 排除node_modules（如果有）
   rm -rf ~/.openclaw/skills/*/node_modules
   ```

3. **使用SSD作为临时目录**：
   ```bash
   export TMPDIR=/Volumes/SSD/tmp
   ```

---

### Q15: 备份占用太多空间怎么办？

**A**:

**方案1：增量备份**（高级）
```bash
# 使用rsync
rsync -a --link-dest=/path/to/previous ~/.openclaw/ /path/to/current/
```

**方案2：仅备份关键数据**
```bash
# 创建最小备份
mkdir /tmp/minimal
cp ~/.openclaw/config.yaml /tmp/minimal/
cp -r ~/.openclaw/workspace/memory /tmp/minimal/
tar -czf minimal_backup.tar.gz -C /tmp/minimal .
```

**方案3：提高压缩率**
```bash
tar --use-compress-program="gzip -9" ...
```

---

## 🐛 故障排查

### Q16: cron任务不执行怎么办？

**A**:

**诊断**：
```bash
# 1. 检查cron任务
crontab -l

# 2. 查看日志
tail -f /tmp/openclaw_backup.log

# 3. 手动运行脚本
bash ~/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh
```

**常见原因**：
- ❌ 脚本无执行权限
  ```bash
  chmod +x ~/.openclaw/skills/openclaw-backup/scripts/*.sh
  ```

- ❌ 环境变量未设置
  ```bash
  # 在脚本开头添加
  export PATH=/usr/local/bin:/usr/bin:/bin
  ```

- ❌ 密码未设置
  ```bash
  export OPENCLAW_BACKUP_PASSWORD="your_password"
  ```

---

### Q17: 提示"Permission denied"怎么办？

**A**:
```bash
# 检查权限
ls -la ~/.openclaw

# 修复权限
chmod -R 755 ~/.openclaw
chmod 600 ~/.openclaw/config.yaml

# 检查磁盘空间
df -h
```

---

### Q18: 加密备份损坏怎么办？

**A**:

**验证备份**：
```bash
shasum -c backup.tar.gz.enc.sha256
```

**如果校验失败**：
1. 尝试恢复更早的备份
2. 检查磁盘是否有坏道
3. 如果在云盘，重新下载

**预防措施**：
- 保留多个备份（至少3个）
- 定期验证备份完整性
- 使用多个存储位置

---

### Q19: macOS升级后cron失效怎么办？

**A**:

**问题**：macOS Ventura+可能需要授予权限

**解决**：
```bash
# 1. 重新配置cron
bash scripts/setup_cron.sh

# 2. 或改用 launchd
# 创建 ~/Library/LaunchAgents/ai.openclaw.backup.plist
```

---

### Q20: 备份到一半中断了怎么办？

**A**:

**安全性**：中断不会影响原数据（备份到临时目录）

**清理**：
```bash
# 删除未完成的备份
rm -f ~/Desktop/OpenClaw_Backups/openclaw_backup_*.tar.gz.tmp
rm -rf /tmp/openclaw_backup_*
```

**重新备份**：
```bash
bash scripts/backup_encrypted.sh
```

---

## 📞 获取帮助

还有问题？

- 📖 [完整文档](https://github.com/halaoluan/openclaw-backup)
- 📖 [高级指南](ADVANCED.md)
- 💬 [Discord社区](https://discord.com/invite/clawd)
- 🐛 [提交Issue](https://github.com/halaoluan/openclaw-backup/issues)

---

**Made with ❤️ by OpenClaw Community**
