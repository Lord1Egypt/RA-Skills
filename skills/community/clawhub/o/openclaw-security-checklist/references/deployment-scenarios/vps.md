# VPS 部署检查清单

**适用场景**: 在云服务器（阿里云/腾讯云/AWS/华为云等）上部署 OpenClaw

## 云服务商选择

### 国内服务商（推荐，数据不出境）

| 服务商 | 优势 | 注意事项 |
|--------|------|----------|
| 阿里云 | 生态完善，文档丰富 | 实名认证 required |
| 腾讯云 | 游戏/社交场景优化 | 实名认证 required |
| 华为云 | 政企客户多 | 部分区域需审批 |

### 国际服务商

| 服务商 | 优势 | 注意事项 |
|--------|------|----------|
| AWS | 全球覆盖，服务丰富 | 数据出境需评估 |
| GCP | AI/ML 工具强 | 数据出境需评估 |
| DigitalOcean | 简单易用，价格便宜 | 无国内节点 |

## 安全检查项

### 1. 账户安全

- [ ] **启用多因素认证（MFA）**
  ```
  阿里云：访问控制 RAM → 用户 → MFA 设备
  腾讯云：访问管理 → 用户列表 → MFA
  AWS: IAM → Users → Security credentials → MFA
  ```

- [ ] **使用 RAM/IAM 用户**（非主账户）
  ```bash
  # 创建 RAM 用户并授权
  # 主账户仅用于账单和管理，日常使用 RAM 用户
  ```

- [ ] **API 访问密钥轮换**
  ```bash
  # 每 90 天轮换一次 AccessKey
  # 旧密钥禁用后观察 24-48 小时再删除
  ```

### 2. 网络安全

- [ ] **安全组配置**（最小开放原则）
  ```
  入站规则：
  - 22/tcp (SSH): 仅允许特定 IP
  - 7001/tcp (Gateway): 按需开放，建议限制 IP
  - 7002/tcp (Node): 不开放（仅内网通信）
  
  出站规则：
  - 允许所有（或限制到特定 API 端点）
  ```

- [ ] **修改 SSH 端口**（非 22）
  ```bash
  # 编辑 /etc/ssh/sshd_config
  Port 22345  # 改为非标准端口
  
  # 重启 SSH
  sudo systemctl restart sshd
  
  # 更新安全组规则
  ```

- [ ] **禁用 root 登录**
  ```bash
  # /etc/ssh/sshd_config
  PermitRootLogin no
  PasswordAuthentication no
  PubkeyAuthentication yes
  ```

- [ ] **配置 SSH 密钥认证**
  ```bash
  # 生成密钥
  ssh-keygen -t ed25519 -C "openclaw@yourdomain"
  
  # 上传到服务器
  ssh-copy-id -p 22345 user@your-vps-ip
  
  # 测试登录后再禁用密码
  ```

### 3. 系统加固

- [ ] **安装并配置防火墙**
  ```bash
  # Ubuntu/Debian
  sudo apt install ufw
  sudo ufw default deny incoming
  sudo ufw default allow outgoing
  sudo ufw allow from YOUR_IP to any port 22345
  sudo ufw allow from YOUR_IP to any port 7001
  sudo ufw enable
  
  # CentOS/RHEL
  sudo yum install firewalld
  sudo systemctl enable firewalld
  sudo systemctl start firewalld
  ```

- [ ] **安装 fail2ban**（防暴力破解）
  ```bash
  # 安装
  sudo apt install fail2ban  # Ubuntu/Debian
  sudo yum install fail2ban  # CentOS/RHEL
  
  # 配置 SSH 保护
  sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
  sudo systemctl enable fail2ban
  sudo systemctl start fail2ban
  ```

- [ ] **配置自动更新**
  ```bash
  # Ubuntu/Debian
  sudo apt install unattended-upgrades
  sudo dpkg-reconfigure --priority=low unattended-upgrades
  
  # CentOS/RHEL
  sudo yum install yum-cron
  sudo systemctl enable yum-cron
  sudo systemctl start yum-cron
  ```

- [ ] **禁用不必要的服务**
  ```bash
  # 查看运行的服务
  systemctl list-units --type=service --state=running
  
  # 禁用不需要的服务（示例）
  sudo systemctl disable cups  # 打印机服务
  sudo systemctl disable bluetooth  # 蓝牙
  ```

### 4. 数据安全

- [ ] **配置云盘加密**
  ```
  阿里云：云盘 → 加密选项
  腾讯云：云硬盘 → 加密
  AWS: EBS → Encryption
  ```

- [ ] **定期快照备份**
  ```
  阿里云：云盘 → 自动快照策略（建议每天）
  腾讯云：云硬盘 → 快照 → 自动快照
  AWS: EC2 → Create Image（定期 AMI）
  ```

- [ ] **配置对象存储备份**（可选）
  ```bash
  # 使用 ossutil 备份到 OSS
  ossutil cp -r ~/.openclaw oss://your-bucket/backup/
  
  # 配置生命周期规则，自动删除旧备份
  ```

### 5. 监控告警

- [ ] **启用云监控**
  ```
  阿里云：云监控 → 主机监控 → 安装插件
  腾讯云：云监控 → 可观测性 → 安装监控 agent
  AWS: CloudWatch → Install unified CloudWatch agent
  ```

- [ ] **配置告警规则**
  ```
  关键指标：
  - CPU 使用率 > 80% 持续 5 分钟
  - 内存使用率 > 85% 持续 5 分钟
  - 磁盘使用率 > 80%
  - 网络流量异常
  - SSH 登录失败次数 > 5 次/分钟
  ```

- [ ] **配置告警通知**
  ```
  通知方式：
  - 短信（推荐）
  - 邮件
  - 钉钉/企业微信 webhook
  - 电话（严重告警）
  ```

### 6. 日志审计

- [ ] **配置日志留存**（≥6 个月）
  ```bash
  # 配置 logrotate
  sudo vim /etc/logrotate.d/openclaw
  
  # 内容：
  ~/.openclaw/logs/*.log {
      daily
      rotate 180
      compress
      delaycompress
      missingok
      notifempty
  }
  ```

- [ ] **启用操作审计**
  ```
  阿里云：操作审计 ActionTrail → 创建跟踪
  腾讯云：操作审计 CloudAudit → 开启审计
  AWS: CloudTrail → Create trail
  ```

- [ ] **集中日志收集**（可选）
  ```bash
  # 使用 ELK Stack 或云日志服务
  # 阿里云：日志服务 SLS
  # 腾讯云：日志服务 CLS
  ```

### 7. 合规检查

- [ ] **服务器位置确认**
  ```bash
  # 确认服务器在国内（如服务中国用户）
  curl -s ipinfo.io/country
  # 应显示：CN
  ```

- [ ] **ICP 备案**（如提供公开 Web 服务）
  ```
  通过云服务商备案系统提交
  所需材料：营业执照/身份证、网站信息等
  时间：约 20 个工作日
  ```

- [ ] **等保测评**（企业用户，可选）
  ```
  二级等保：年费约 3-5 万
  三级等保：年费约 8-15 万
  ```

## 快速检查脚本

```bash
#!/bin/bash
# VPS 安全检查脚本

echo "🔍 VPS OpenClaw 安全检查"
echo "========================="

# SSH 配置
if grep -q "PermitRootLogin no" /etc/ssh/sshd_config; then
    echo "✓ 禁止 root 登录"
else
    echo "✗ 未禁止 root 登录"
fi

if grep -q "PasswordAuthentication no" /etc/ssh/sshd_config; then
    echo "✓ 禁用密码认证"
else
    echo "⚠ 密码认证未禁用"
fi

# 防火墙
if systemctl is-active --quiet ufw || systemctl is-active --quiet firewalld; then
    echo "✓ 防火墙已启用"
else
    echo "✗ 防火墙未启用"
fi

# fail2ban
if systemctl is-active --quiet fail2ban; then
    echo "✓ fail2ban 已启用"
else
    echo "⚠ fail2ban 未启用"
fi

# 磁盘使用率
USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [[ $USAGE -lt 80 ]]; then
    echo "✓ 磁盘使用率正常 ($USAGE%)"
else
    echo "⚠ 磁盘使用率过高 ($USAGE%)"
fi

echo "========================="
echo "检查完成"
```

## 成本优化

| 优化项 | 节省比例 | 实施难度 |
|--------|----------|----------|
| 使用抢占式实例 | 50-70% | 中 |
| 预留实例券（1-3 年） | 30-50% | 低 |
| 自动伸缩（按需扩缩容） | 20-40% | 中 |
| 对象存储替代云盘 | 40-60% | 低 |
| CDN 加速静态资源 | 30-50% | 中 |

## 常见问题

### Q: 选择什么配置的 VPS？

**A**: 根据用户量选择：
- 个人使用：2 核 4GB，50GB 云盘（约 100-200 元/月）
- 小团队（10 人内）：4 核 8GB，100GB 云盘（约 300-500 元/月）
- 企业部署：8 核 16GB+，负载均衡+ 自动伸缩（1000 元+/月）

### Q: 需要备案吗？

**A**: 
- 仅内部使用：**不需要**
- 提供公开 Web 服务：**需要**
- 仅 API 访问：建议咨询当地通信管理局

### Q: 如何选择地域？

**A**: 
- 用户主要在华东：上海/杭州
- 用户主要在华南：深圳/广州
- 用户主要在华北：北京/青岛
- 全国分布：选择多个地域 + 负载均衡

## 资源链接

- 阿里云安全最佳实践：https://help.aliyun.com/product/28617.html
- 腾讯云安全基线：https://cloud.tencent.com/document/product/213
- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/

## 更新记录

- 2026-03-15: 初始版本
