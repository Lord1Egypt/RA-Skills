# 安装指南

## 快速安装

### 方法1: 使用clawhub安装 (推荐)
```bash
clawhub install openclaw-security-configurator
```

### 方法2: 手动安装
```bash
# 克隆仓库
git clone https://github.com/openclaw-skills/security-configurator.git
cd security-configurator

# 安装依赖
chmod +x scripts/*.sh

# 初始化配置
./scripts/token-monitor.sh config
```

## 系统要求

### 最低要求
- **操作系统**: Linux (Ubuntu 20.04+, CentOS 7+, Debian 10+)
- **OpenClaw版本**: 2026.3.0 或更高
- **内存**: 512MB RAM
- **存储**: 100MB 可用空间
- **权限**: root或sudo权限 (部分功能需要)

### 推荐配置
- **操作系统**: Ubuntu 22.04 LTS
- **OpenClaw版本**: 最新稳定版
- **内存**: 2GB RAM
- **存储**: 1GB 可用空间
- **监控频率**: 每5分钟检查一次

## 详细安装步骤

### 步骤1: 下载技能包
```bash
# 创建技能目录
mkdir -p ~/.openclaw/skills/
cd ~/.openclaw/skills/

# 下载最新版本
wget https://github.com/openclaw-skills/security-configurator/releases/download/v1.0.0/openclaw-security-configurator-v1.0.0.tar.gz
tar -xzf openclaw-security-configurator-v1.0.0.tar.gz
cd openclaw-security-configurator
```

### 步骤2: 设置执行权限
```bash
chmod +x scripts/*.sh
```

### 步骤3: 配置监控
```bash
# 创建配置目录
mkdir -p ~/.openclaw/security/

# 编辑配置文件 (可选)
./scripts/token-monitor.sh config
```

### 步骤4: 测试安装
```bash
# 运行安全检查
./scripts/security-check.sh

# 测试Token监控
./scripts/token-monitor.sh check
```

### 步骤5: 启动监控服务
```bash
# 启动后台监控
./scripts/token-monitor.sh start

# 检查服务状态
./scripts/token-monitor.sh status
```

## 配置说明

### 主要配置文件
- `~/.openclaw/security/token-monitor.conf` - Token监控配置
- `~/.openclaw/security/openclaw-token-monitor.log` - 监控日志
- `~/.openclaw/security/openclaw-token-daily-*.log` - 每日统计

### 配置示例
```bash
# Token监控配置示例
ALERT_THRESHOLD=10000      # 单次请求超过10000 tokens告警
DAILY_LIMIT=100000         # 每日限额100000 tokens
CHECK_INTERVAL=300         # 每5分钟检查一次
ALERT_METHOD="log"         # 告警方式: log/email/webhook
```

## 系统集成

### 与OpenClaw集成
```bash
# 添加安全检查到OpenClaw启动脚本
echo "./scripts/security-check.sh" >> ~/.openclaw/startup-scripts.sh
```

### 系统服务配置 (可选)
```bash
# 创建systemd服务文件
sudo tee /etc/systemd/system/openclaw-security-monitor.service << EOF
[Unit]
Description=OpenClaw Security Monitor
After=openclaw.service
Requires=openclaw.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/scripts/token-monitor.sh start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启用并启动服务
sudo systemctl daemon-reload
sudo systemctl enable openclaw-security-monitor
sudo systemctl start openclaw-security-monitor
```

## 升级指南

### 自动升级 (如果支持)
```bash
clawhub update openclaw-security-configurator
```

### 手动升级
```bash
# 停止当前服务
./scripts/token-monitor.sh stop

# 备份配置
cp -r ~/.openclaw/security ~/.openclaw/security-backup-$(date +%Y%m%d)

# 下载新版本
wget https://github.com/openclaw-skills/security-configurator/releases/download/v1.1.0/openclaw-security-configurator-v1.1.0.tar.gz
tar -xzf openclaw-security-configurator-v1.1.0.tar.gz --strip-components=1

# 恢复配置
cp ~/.openclaw/security-backup-$(date +%Y%m%d)/token-monitor.conf ~/.openclaw/security/

# 重启服务
./scripts/token-monitor.sh start
```

## 卸载指南

### 完全卸载
```bash
# 停止监控服务
./scripts/token-monitor.sh stop

# 删除技能目录
cd ~/.openclaw/skills/
rm -rf openclaw-security-configurator/

# 删除配置文件 (可选)
# rm -rf ~/.openclaw/security/

# 删除系统服务 (如果已安装)
sudo systemctl stop openclaw-security-monitor
sudo systemctl disable openclaw-security-monitor
sudo rm /etc/systemd/system/openclaw-security-monitor.service
sudo systemctl daemon-reload
```

### 保留配置卸载
```bash
# 仅删除程序文件，保留配置和日志
./scripts/token-monitor.sh stop
cd ~/.openclaw/skills/
mv openclaw-security-configurator/config-backup/
# 配置和日志保留在 ~/.openclaw/security/
```

## 故障排除

### 常见问题

#### 1. 权限不足
```
错误: Permission denied
解决: chmod +x scripts/*.sh
```

#### 2. 配置文件不存在
```
错误: No such file or directory
解决: ./scripts/token-monitor.sh config
```

#### 3. OpenClaw未运行
```
警告: OpenClaw服务未运行
解决: 启动OpenClaw服务
```

#### 4. 日志文件过大
```
问题: 日志文件占用过多空间
解决: 设置日志轮转或定期清理
```

### 获取帮助
- **文档**: 查看README.md获取详细说明
- **社区**: 加入Discord社区获取支持
- **问题**: 在GitHub提交issue
- **邮件**: security-support@openclaw-skills.com

## 安全注意事项

### 权限管理
- 不要以root身份运行监控脚本
- 定期检查配置文件权限
- 使用最小权限原则

### 数据保护
- 配置文件可能包含敏感信息
- 定期备份配置和日志
- 加密存储敏感数据

### 监控建议
- 定期查看监控日志
- 设置合理的告警阈值
- 及时响应安全告警

---

**安装完成!** 现在您可以开始使用OpenClaw Security Configurator来保护您的OpenClaw部署了。