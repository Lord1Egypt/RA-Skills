# OpenClaw Restore - 常见问题

## 📋 目录

- [基础问题](#基础问题)
- [恢复流程](#恢复流程)
- [灾难恢复](#灾难恢复)
- [故障排查](#故障排查)
- [安全问题](#安全问题)

---

## 🔰 基础问题

### Q1: 什么时候需要恢复备份？

**A**: 常见场景：
- 🔴 **系统崩溃**：macOS重装、硬盘损坏
- 🟠 **误操作**：删除了重要配置/数据
- 🟡 **迁移设备**：换新电脑
- 🟢 **测试环境**：搭建开发/测试环境
- 🔵 **版本回退**：OpenClaw升级失败

---

### Q2: 恢复会覆盖当前数据吗？

**A**: **会**，但有保护措施：

**自动备份**：
恢复前会自动备份当前数据到：
```
~/.openclaw.backup.YYYYMMDD_HHMMSS
```

**确认后才恢复**：
脚本会提示：
```
确认恢复？[y/N]
```

---

### Q3: 恢复需要多久？

**A**: 取决于备份大小：

| 备份大小 | 解密时间 | 解压时间 | 总计 |
|---------|---------|---------|------|
| 500 MB | ~10s | ~15s | ~30s |
| 1 GB | ~20s | ~30s | ~1min |
| 2 GB | ~40s | ~1min | ~2min |

**因素**：
- CPU性能
- 磁盘速度（SSD vs HDD）
- 是否加密

---

### Q4: 可以部分恢复吗？

**A**: 可以！

**方式1：手动解压**
```bash
# 解压到临时目录
tar -xzf backup.tar.gz -C /tmp/restore

# 只复制需要的文件
cp /tmp/restore/.openclaw/config.yaml ~/.openclaw/
cp /tmp/restore/.openclaw/workspace/MEMORY.md ~/.openclaw/workspace/
```

**方式2：选择性恢复**（自定义脚本）
```bash
#!/bin/bash
# 仅恢复配置文件
tar -xzf backup.tar.gz -C /tmp/restore .openclaw/config.yaml
cp /tmp/restore/.openclaw/config.yaml ~/.openclaw/
```

---

### Q5: 恢复后需要重新配置吗？

**A**: **大部分不需要**，但有例外：

**无需重新配置**：
- ✅ API Key
- ✅ 记忆文件（MEMORY.md）
- ✅ Skills
- ✅ 大部分配置

**可能需要重新配置**：
- ❓ **WeChat** - 可能需要重新扫码
- ❓ **部分渠道** - 登录状态可能过期
- ❓ **网络代理** - 如果IP变化

---

## 🔄 恢复流程

### Q6: 恢复流程是什么？

**A**: 自动执行以下步骤：

```
1. 验证备份 → 检查SHA256校验和
2. 解密（如需要） → AES-256解密
3. 停止OpenClaw → 停止网关服务
4. 备份当前数据 → 保存到 ~/.openclaw.backup.XXX
5. 恢复数据 → 解压并覆盖
6. 修复检查 → openclaw doctor
7. 重启网关 → 启动OpenClaw
```

---

### Q7: 如何恢复最新备份？

**A**:
```bash
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_latest.sh
```

**会自动**：
- 查找最新备份（优先加密）
- 显示文件信息
- 询问确认
- 执行恢复

---

### Q8: 如何恢复指定备份？

**A**:

**普通备份**：
```bash
bash scripts/restore.sh ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-46-27.tar.gz
```

**加密备份**：
```bash
bash scripts/restore_encrypted.sh ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-40-13.tar.gz.enc
```

---

### Q9: 恢复后如何验证？

**A**:

**检查清单**：
```bash
# 1. 网关状态
openclaw status

# 2. 配置验证
openclaw doctor

# 3. 记忆文件
cat ~/.openclaw/workspace/MEMORY.md

# 4. API配置
openclaw config get

# 5. 测试对话
openclaw chat "你好，测试一下"
```

---

### Q10: 恢复失败怎么办？

**A**:

**回滚**：
```bash
# 恢复会自动备份当前数据
# 如果恢复失败，可以恢复旧数据
mv ~/.openclaw.backup.20260313_204600 ~/.openclaw
openclaw gateway restart
```

**诊断**：
```bash
# 查看错误日志
tail -f ~/.openclaw/logs/gateway.log

# 运行诊断
openclaw doctor
```

---

## 🆘 灾难恢复

### Q11: macOS重装后如何恢复？

**A**: 完整流程：

#### 第1步：安装基础环境
```bash
# 1. 安装Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装Node.js
brew install node

# 3. 安装OpenClaw
npm install -g openclaw
```

#### 第2步：恢复备份
```bash
# 从云盘/移动硬盘拷贝备份
cp /Volumes/External/openclaw_backup_*.tar.gz.enc ~/Desktop/

# 安装恢复Skill
cd ~/.openclaw/skills
git clone https://github.com/halaoluan/openclaw-restore.git

# 恢复
bash openclaw-restore/scripts/restore_encrypted.sh ~/Desktop/openclaw_backup_*.tar.gz.enc
```

#### 第3步：验证
```bash
openclaw doctor
openclaw gateway restart
openclaw status
```

---

### Q12: 硬盘损坏了怎么办？

**A**:

**如果有云盘备份**：
1. 从云盘下载备份
2. 按 Q11 流程恢复

**如果只有本地备份**：
- ❌ 无法恢复（硬盘已损坏）
- 💡 **教训**：必须有异地备份（3-2-1原则）

---

### Q13: 忘记密码怎么办？

**A**: **无法恢复**加密备份。

**补救措施**：
1. 尝试所有可能的密码
2. 检查密码管理器
3. 如果有未加密备份，使用那个
4. 重新配置OpenClaw（最后手段）

---

### Q14: 备份文件损坏怎么办？

**A**:

**诊断**：
```bash
# 验证校验和
shasum -c backup.tar.gz.enc.sha256
```

**如果失败**：
1. 尝试更早的备份
2. 如果在云盘，重新下载
3. 如果多个备份都损坏，检查硬盘健康

**预防**：
- 保留多个版本备份
- 定期验证备份完整性
- 使用RAID/云盘

---

### Q15: 换新电脑如何迁移？

**A**:

**方式1：备份+恢复**（推荐）
```bash
# 旧电脑
bash ~/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh
# 复制到新电脑

# 新电脑
# 1. 安装OpenClaw
npm install -g openclaw

# 2. 恢复备份
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_encrypted.sh backup.tar.gz.enc
```

**方式2：直接复制**（局域网）
```bash
# 新电脑
rsync -avz --progress old-mac:~/.openclaw/ ~/.openclaw/
openclaw gateway restart
```

---

## 🐛 故障排查

### Q16: 恢复后网关无法启动？

**A**:

**诊断**：
```bash
openclaw status
openclaw doctor
tail -f ~/.openclaw/logs/gateway.log
```

**常见原因**：
1. **端口冲突**
   ```bash
   lsof -i :18790
   kill -9 <PID>
   ```

2. **配置文件损坏**
   ```bash
   mv ~/.openclaw/config.yaml ~/.openclaw/config.yaml.broken
   openclaw gateway start
   ```

3. **权限问题**
   ```bash
   chmod -R 755 ~/.openclaw
   chmod 600 ~/.openclaw/config.yaml
   ```

---

### Q17: 提示"bad decrypt"怎么办？

**A**:

**原因**：密码错误或文件损坏

**解决**：
1. **确认密码正确**
   - 检查大小写
   - 检查空格
   - 尝试从密码管理器复制

2. **验证文件完整性**
   ```bash
   shasum -c backup.tar.gz.enc.sha256
   ```

3. **尝试其他备份**
   ```bash
   ls -lt ~/Desktop/OpenClaw_Backups/
   ```

---

### Q18: 恢复后渠道无法登录？

**A**:

**Telegram**：
通常自动恢复，无需重新配置

**WeChat**：
```bash
# 可能需要重新扫码
openclaw wechat login
```

**其他渠道**：
检查 `~/.openclaw/config.yaml`，确认配置正确

---

### Q19: 恢复后Skills缺失？

**A**:

**诊断**：
```bash
ls -la ~/.openclaw/skills/
openclaw skills list
```

**可能原因**：
1. 备份时Skills未包含
2. 恢复路径错误

**解决**：
```bash
# 重新安装Skills
openclaw skills install <skill-name>
```

---

### Q20: 恢复后记忆丢失？

**A**:

**检查**：
```bash
cat ~/.openclaw/workspace/MEMORY.md
ls -la ~/.openclaw/workspace/memory/
```

**如果确实丢失**：
1. 尝试更早的备份
2. 检查 `~/.openclaw.backup.XXX`
3. 如果有云同步，检查版本历史

---

## 🔒 安全问题

### Q21: 恢复是否安全？

**A**: 是的，有多重保护：

1. **自动备份当前数据**
2. **SHA256完整性验证**
3. **需要手动确认**
4. **可回滚**

**风险**：
- ⚠️ 旧备份可能包含过期API Key
- ⚠️ 渠道登录状态可能失效

---

### Q22: 旧备份可以恢复到新版OpenClaw吗？

**A**: **通常可以**，但：

**向前兼容**（旧→新）：
- ✅ 配置格式通常兼容
- ⚠️ 可能需要运行 `openclaw doctor`

**向后不兼容**（新→旧）：
- ❌ 新版配置可能无法用于旧版
- ⚠️ 不推荐

**最佳实践**：
升级前先备份，升级后再备份

---

### Q23: 恢复会泄露数据吗？

**A**: 不会，前提是：

1. **使用加密备份**
2. **密码足够强**
3. **未共享备份文件**

**如果备份泄露**：
1. 立即更换所有API Key
2. 更换Telegram Bot Token
3. 重新登录所有渠道

---

## 📞 获取帮助

还有问题？

- 📖 [完整文档](https://github.com/halaoluan/openclaw-restore)
- 📖 [备份工具](https://github.com/halaoluan/openclaw-backup)
- 💬 [Discord社区](https://discord.com/invite/clawd)
- 🐛 [提交Issue](https://github.com/halaoluan/openclaw-restore/issues)

---

**Made with ❤️ by OpenClaw Community**
