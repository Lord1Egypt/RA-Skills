# 个人 Mac 部署检查清单

**适用场景**: 在个人 macOS 设备上部署 OpenClaw

## 系统要求

- [ ] macOS 12.0 (Monterey) 或更高版本
- [ ] 至少 8GB RAM（推荐 16GB+）
- [ ] 至少 20GB 可用存储空间
- [ ] Node.js 18+ (`node --version`)

## 安全检查项

### 1. 系统安全

- [ ] **FileVault 磁盘加密已启用**
  ```bash
  # 检查状态
  fdesetup status
  
  # 如未启用，在系统偏好设置 → 安全性与隐私 → FileVault 中启用
  ```

- [ ] **防火墙已启用**
  ```bash
  # 检查状态
  sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
  
  # 启用防火墙
  sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
  ```

- [ ] **自动更新已启用**
  ```bash
  # 检查设置
  defaults read /Library/Preferences/com.apple.SoftwareUpdate
  
  # 在系统偏好设置 → 软件更新 → 自动更新 中启用
  ```

### 2. 用户权限

- [ ] **使用标准用户账户**（非管理员日常使用）
  ```bash
  # 检查当前用户权限
  id
  
  # 如显示 groups=... admin ... 则为管理员账户
  # 建议：创建单独的管理员账户用于系统更改，日常使用标准账户
  ```

- [ ] **sudo 权限限制**
  ```bash
  # 检查 sudoers 配置
  sudo visudo
  
  # 确保仅授权用户有 sudo 权限
  ```

### 3. 网络安全

- [ ] **仅开放必要端口**
  ```bash
  # 检查开放端口
  lsof -i -P | grep LISTEN
  
  # OpenClaw 默认端口：7001 (Gateway), 7002 (Node)
  # 如无需远程访问，可在防火墙中阻止外部连接
  ```

- [ ] **禁用不必要的服务**
  ```bash
  # 检查正在运行的服务
  launchctl list
  
  # 禁用不需要的服务（谨慎操作）
  # 如：AirDrop、Handoff 等
  ```

### 4. 应用安全

- [ ] **Gatekeeper 已启用**（仅允许 App Store 和认证开发者）
  ```bash
  # 检查状态
  spctl --status
  
  # 应显示：assessments enabled
  
  # 启用
  sudo spctl --master-enable
  ```

- [ ] **隐私权限审查**
  ```bash
  # 在系统偏好设置 → 安全性与隐私 → 隐私 中检查：
  # - 文件和文件夹访问
  # - 麦克风访问
  # - 摄像头访问
  # - 屏幕录制权限
  ```

### 5. OpenClaw 配置

- [ ] **配置文件权限**
  ```bash
  # 检查配置文件权限
  ls -la ~/.openclaw/
  
  # 敏感文件权限应为 600
  chmod 600 ~/.openclaw/config.json
  chmod 600 ~/.openclaw/.env
  ```

- [ ] **API 密钥使用环境变量**
  ```bash
  # 检查是否在代码中硬编码
  grep -r "sk-" ~/.openclaw/workspace/
  
  # 正确做法：在 ~/.zshrc 中设置
  # export OPENCLAW_API_KEY="sk-..."
  ```

- [ ] **日志配置**
  ```bash
  # 确保日志目录存在且权限正确
  mkdir -p ~/.openclaw/logs
  chmod 755 ~/.openclaw/logs
  ```

### 6. 备份策略

- [ ] **Time Machine 已配置**
  ```bash
  # 检查 Time Machine 状态
  tmutil status
  
  # 或在系统偏好设置 → Time Machine 中配置
  ```

- [ ] **OpenClaw 配置备份**
  ```bash
  # 定期备份配置
  cp -r ~/.openclaw/config.json ~/Backup/openclaw-config-$(date +%Y%m%d).json
  ```

### 7. 监控和审计

- [ ] **定期检查系统日志**
  ```bash
  # 查看系统日志
  log show --predicate 'eventMessage contains "openclaw"' --last 24h
  
  # 查看 OpenClaw 日志
  tail -f ~/.openclaw/logs/*.log
  ```

- [ ] **监控异常进程**
  ```bash
  # 检查异常进程
  ps aux | grep -E "openclaw|node"
  ```

## 快速检查脚本

```bash
#!/bin/bash
# 个人 Mac 安全检查

echo "🔍 个人 Mac OpenClaw 安全检查"
echo "==============================="

# FileVault
if fdesetup status | grep -q "FileVault is On"; then
    echo "✓ FileVault 已启用"
else
    echo "⚠ FileVault 未启用"
fi

# 防火墙
if sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate | grep -q "enabled"; then
    echo "✓ 防火墙已启用"
else
    echo "⚠ 防火墙未启用"
fi

# Gatekeeper
if spctl --status | grep -q "assessments enabled"; then
    echo "✓ Gatekeeper 已启用"
else
    echo "⚠ Gatekeeper 未启用"
fi

# 配置文件权限
if [[ $(stat -f %A ~/.openclaw/config.json 2>/dev/null) == "600" ]]; then
    echo "✓ 配置文件权限正确"
else
    echo "⚠ 配置文件权限不正确，建议：chmod 600 ~/.openclaw/config.json"
fi

echo "==============================="
echo "检查完成"
```

## 常见问题

### Q: 可以在公司 Mac 上部署吗？

**A**: 需先获得 IT 部门许可，并遵守公司安全政策。特别注意：
- 不得存储公司敏感数据
- 不得将公司数据发送到境外 API
- 遵守公司数据分类和保密要求

### Q: 需要关闭 SIP（系统完整性保护）吗？

**A**: **绝对不要**。SIP 是 macOS 的核心安全机制，关闭会带来严重风险。OpenClaw 不需要 SIP 权限。

### Q: 如何防止家人误操作？

**A**: 
- 使用独立用户账户运行 OpenClaw
- 配置屏幕使用时间限制
- 在家庭共享中设置权限

## 资源链接

- Apple 安全支持：https://support.apple.com/zh-cn/HT201127
- macOS 安全基线：https://support.apple.com/guide/deployment/deploy-macos-security-baseline-dep0f483f0a7/web

## 更新记录

- 2026-03-15: 初始版本
