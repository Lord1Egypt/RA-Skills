# OpenClaw生产环境设置指南

基于B站视频《简单易用的openclaw的聊天界面》的学习总结

## 🎯 生产环境部署目标

将OpenClaw部署为稳定可靠的生产环境服务，实现：
- ✅ 7x24小时稳定运行
- ✅ 开机自动启动
- ✅ 资源监控和告警
- ✅ 数据备份和恢复
- ✅ 性能优化和安全加固

## 📋 系统架构

### 生产环境架构
```
┌─────────────────────────────────────────┐
│          用户访问层                      │
│  • Web浏览器 (localhost:18789)          │
│  • 微信/Telegram等聊天平台              │
│  • API客户端                            │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          OpenClaw网关层                  │
│  • Gateway服务 (端口: 18789)            │
│  • 认证和授权                           │
│  • 请求路由和负载均衡                   │
│  • 会话管理                            │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          核心服务层                      │
│  • AI模型服务 (本地/云端)               │
│  • 技能执行引擎                         │
│  • 记忆存储系统                         │
│  • 文件处理服务                         │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          数据存储层                      │
│  • 配置存储 (~/.openclaw/config.yaml)   │
│  • 会话历史 (~/.openclaw/sessions/)     │
│  • 记忆数据库 (~/.openclaw/memory.db)   │
│  • 日志文件 (~/.openclaw/logs/)         │
└─────────────────────────────────────────┘
```

## 🚀 部署流程

### 步骤1: 环境准备
```bash
# 运行环境检查
node scripts/step1-environment.js

# 确保满足:
# • Node.js 22.x 或更高
# • 4GB以上内存
# • 2GB以上存储空间
# • 稳定的网络连接
```

### 步骤2: 一键部署
```bash
# 运行一键部署脚本
node scripts/deploy.js

# 或分步部署
node scripts/step2-install.js      # 安装OpenClaw
node scripts/step3-configure.js    # 生产环境配置
node scripts/step4-service.js      # 注册系统服务
```

### 步骤3: 服务验证
```bash
# 检查服务状态
openclaw gateway status

# 访问Web界面
openclaw dashboard
# 或浏览器访问: http://localhost:18789

# 测试聊天功能
curl -X POST http://localhost:18789/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，测试生产环境"}'
```

## ⚙️ 生产环境配置

### 核心配置项
```yaml
# ~/.openclaw/config.yaml 生产环境配置

environment: production

gateway:
  mode: local
  port: 18789
  host: 0.0.0.0  # 允许局域网访问
  auth:
    enabled: true
    token: "your-secure-production-token"
  
logging:
  level: info
  file: ~/.openclaw/logs/production.log
  maxSize: 100MB
  maxFiles: 10
  format: json  # 生产环境使用JSON格式便于解析

monitoring:
  enabled: true
  port: 18790    # 监控端口
  metrics: true  # 启用指标收集
  healthCheck: true

performance:
  maxMemory: 1GB
  maxConcurrent: 10
  timeout: 30000  # 30秒超时
  cache:
    enabled: true
    ttl: 300      # 5分钟缓存

security:
  rateLimit:
    enabled: true
    windowMs: 60000  # 1分钟窗口
    max: 100         # 最大请求数
  cors:
    enabled: true
    origin: ["http://localhost:18789", "https://your-domain.com"]
```

### 系统服务配置

#### Windows服务配置
```xml
<!-- openclaw-service.xml -->
<service>
  <id>OpenClawGateway</id>
  <name>OpenClaw Gateway</name>
  <description>OpenClaw AI Assistant Gateway Service - Production Environment</description>
  <executable>C:\Program Files\nodejs\node.exe</executable>
  <argument>C:\Program Files\nodejs\node_modules\openclaw\bin\openclaw gateway run</argument>
  <logmode>rotate</logmode>
  <stoptimeout>30sec</stoptimeout>
  <startmode>Automatic</startmode>
  <interactive>false</interactive>
</service>
```

#### Linux systemd服务
```ini
# /etc/systemd/system/openclaw.service
[Unit]
Description=OpenClaw AI Assistant Gateway
After=network.target
Wants=network.target

[Service]
Type=simple
User=openclaw
Group=openclaw
WorkingDirectory=/opt/openclaw
ExecStart=/usr/bin/node /usr/local/bin/openclaw gateway run
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=openclaw
Environment=NODE_ENV=production

# 资源限制
LimitNOFILE=65536
LimitNPROC=4096
LimitCORE=infinity

[Install]
WantedBy=multi-user.target
```

#### macOS launchd服务
```xml
<!-- ~/Library/LaunchAgents/com.openclaw.gateway.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.gateway</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/node</string>
        <string>/usr/local/bin/openclaw</string>
        <string>gateway</string>
        <string>run</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/var/log/openclaw.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/openclaw-error.log</string>
</dict>
</plist>
```

## 📊 监控和维护

### 健康检查
```bash
# 手动健康检查
curl http://localhost:18789/health

# 或使用监控脚本
node monitoring/check-health.js

# 预期响应:
# {
#   "status": "healthy",
#   "timestamp": "2026-04-18T09:38:00Z",
#   "version": "2026.4.15-beta.2",
#   "uptime": "2d 5h 30m",
#   "memory": {
#     "used": "450MB",
#     "total": "1GB",
#     "percentage": 45
#   }
# }
```

### 性能监控
```bash
# 实时监控
node monitoring/monitor-service.js

# 收集指标
node monitoring/collect-metrics.js

# 监控指标包括:
# • CPU使用率
# • 内存使用
# • 请求响应时间
# • 错误率
# • 并发连接数
# • 队列长度
```

### 日志管理
```bash
# 查看实时日志
openclaw logs --follow

# 查看错误日志
openclaw logs --level error

# 日志轮转配置
# 自动清理旧日志，保留最近10个100MB文件
```

### 备份和恢复
```bash
# 定期备份配置
node backup/backup-config.js

# 备份数据
node backup/backup-data.js

# 恢复备份
node backup/restore-backup.js --backup-file backup-2026-04-18.tar.gz

# 备份策略建议:
# • 每日增量备份
# • 每周全量备份
# • 保留最近30天备份
# • 异地备份重要数据
```

## 🔧 故障排除

### 常见问题及解决方案

#### Q1: 服务无法启动
**症状**: `openclaw gateway status` 显示未运行
**解决**:
```bash
# 检查端口占用
netstat -ano | findstr :18789  # Windows
lsof -i :18789                 # Linux/macOS

# 检查配置文件语法
openclaw config validate

# 查看启动日志
openclaw logs --level error --limit 20

# 手动前台启动调试
openclaw gateway run --verbose
```

#### Q2: 开机自启失效
**症状**: 重启后服务未自动启动
**解决**:
```bash
# Windows: 检查服务状态
sc query OpenClawGateway

# Linux: 检查systemd服务
systemctl status openclaw.service
systemctl enable openclaw.service  # 重新启用

# 检查启动依赖
# 确保网络服务在OpenClaw之前启动
```

#### Q3: 性能下降
**症状**: 响应变慢，内存使用高
**解决**:
```bash
# 检查资源使用
node monitoring/collect-metrics.js

# 优化配置
openclaw config set performance.maxMemory 2GB
openclaw config set performance.maxConcurrent 5

# 清理缓存和临时文件
openclaw cache clear

# 重启服务释放内存
openclaw gateway restart
```

#### Q4: 网络访问问题
**症状**: 无法从其他设备访问
**解决**:
```bash
# 检查绑定地址
openclaw config get gateway.host
# 应该为 0.0.0.0 或特定IP

# 检查防火墙
# Windows: 允许端口18789通过防火墙
# Linux: sudo ufw allow 18789/tcp

# 检查网络配置
ping [目标IP]
telnet [目标IP] 18789
```

#### Q5: 认证失败
**症状**: 无法登录Web界面
**解决**:
```bash
# 重置Token
openclaw config set gateway.auth.token "new-secure-token"
openclaw gateway restart

# 或禁用认证（仅测试环境）
openclaw config set gateway.auth.enabled false
openclaw gateway restart
```

### 紧急恢复流程

#### 场景1: 服务完全崩溃
```bash
# 1. 停止服务
openclaw gateway stop

# 2. 恢复最近备份
node backup/restore-backup.js --latest

# 3. 启动服务
openclaw gateway start

# 4. 验证恢复
openclaw gateway status
curl http://localhost:18789/health
```

#### 场景2: 数据损坏
```bash
# 1. 停止服务
openclaw gateway stop

# 2. 备份当前状态（用于分析）
cp -r ~/.openclaw ~/.openclaw-broken-$(date +%Y%m%d)

# 3. 恢复数据
node backup/restore-backup.js --backup-file backup-2026-04-17.tar.gz

# 4. 启动服务
openclaw gateway start
```

#### 场景3: 配置错误
```bash
# 1. 恢复默认配置
cp ~/.openclaw/config.yaml ~/.openclaw/config.yaml.bak
openclaw config reset

# 2. 重新配置
openclaw onboard --production

# 3. 应用生产环境配置
cp configs/openclaw-prod.yaml ~/.openclaw/config.yaml

# 4. 重启服务
openclaw gateway restart
```

## 🚀 性能优化

### 硬件优化建议
- **CPU**: 至少4核心，推荐8核心
- **内存**: 至少8GB，推荐16GB
- **存储**: SSD硬盘，至少50GB可用空间
- **网络**: 千兆以太网，稳定的互联网连接

### 软件优化配置
```yaml
performance:
  # 内存优化
  maxMemory: "2GB"
  gcInterval: 300000  # 5分钟GC
  
  # 并发优化
  maxConcurrent: 20
  queueSize: 100
  
  # 缓存优化
  cache:
    enabled: true
    memory: "512MB"
    ttl: 600  # 10分钟
    
  # 网络优化
  keepAlive: true
  timeout: 30000
  compression: true
```

### 监控告警配置
```yaml
alerts:
  enabled: true
  channels:
    - email
    - slack
    - webhook
  
  rules:
    - metric: "memory.usage"
      condition: ">"
      threshold: 80  # 百分比
      duration: "5m"
      severity: "warning"
      
    - metric: "response.time.p95"
      condition: ">"
      threshold: 5000  # 5秒
      duration: "10m"
      severity: "critical"
      
    - metric: "error.rate"
      condition: ">"
      threshold: 5  # 百分比
      duration: "5m"
      severity: "warning"
```

## 🔒 安全加固

### 访问控制
```yaml
security:
  # IP白名单
  ipWhitelist:
    - 127.0.0.1
    - 192.168.1.0/24
    - 10.0.0.0/8
    
  # API密钥认证
  apiKeys:
    - name: "production-client"
      key: "secure-api-key-123"
      permissions: ["read", "write"]
      
  # 速率限制
  rateLimit:
    enabled: true
    windowMs: 60000
    max: 100
    message: "请求过于频繁，请稍后再试"
```

### 数据安全
```yaml
dataSecurity:
  # 加密存储
  encryption:
    enabled: true
    algorithm: "aes-256-gcm"
    
  # 数据脱敏
  masking:
    enabled: true
    patterns:
      - "password"
      - "token"
      - "api_key"
      - "secret"
      
  # 访问日志
  auditLog:
    enabled: true
    file: "~/.openclaw/logs/audit.log"
    retention: "30d"
```

### 网络安全
```bash
# 使用HTTPS（生产环境必须）
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# 配置OpenClaw使用HTTPS
openclaw config set gateway.ssl.enabled true
openclaw config set gateway.ssl.key /path/to/key.pem
openclaw config set gateway.ssl.cert /path/to/cert.pem
```

## 📈 扩展和升级

### 水平扩展
```bash
# 多实例部署
# 实例1
openclaw gateway run --port 18789 --name instance-1

# 实例2  
openclaw gateway run --port 18790 --name instance-2

# 使用负载均衡器
# Nginx配置示例:
# upstream openclaw_servers {
#   server 127.0.0.1:18789;
#   server 127.0.0.1:18790;
# }
```

### 版本升级
```bash
# 1. 备份当前版本
node backup/backup-full.js

# 2. 停止服务
openclaw gateway stop

# 3. 升级OpenClaw
npm update -g openclaw

# 4. 验证新版本
openclaw --version

# 5. 启动服务
openclaw gateway start

# 6. 监控升级后状态
node monitoring/check-health.js
```

### 容量规划
- **用户数 < 10**: 单实例，4GB内存
- **用户数 10-100**: 单实例，8GB内存，考虑负载均衡
- **用户数 100-1000**: 多实例，16GB内存，数据库分离
- **用户数 > 1000**: 集群部署，专业运维支持

## 🎯 成功指标

### 部署成功标志
1. ✅ 服务稳定运行超过24小时
2. ✅ 开机自动启动正常
3. ✅ 健康检查全部通过
4. ✅ 性能指标在预期范围内
5. ✅ 备份恢复测试成功

### 生产就绪检查清单
- [ ] 环境检查通过
- [ ] 服务注册成功
- [ ] 开机自启配置
- [ ] 监控系统就绪
- [ ] 备份策略实施
- [ ] 安全配置完成
- [ ] 性能测试通过
- [ ] 文档完整可用

## 📚 学习资源

### 视频教程
- B站视频: 《简单易用的openclaw的聊天界面》
- 视频地址: https://www.bilibili.com/video/BV1VkQBBfEcd

### 官方文档
- 生产环境部署: https://docs.openclaw.ai/deployment/production
- 性能优化: https://docs.openclaw.ai/performance
- 安全指南: https://docs.openclaw.ai/security

### 社区支持
- GitHub讨论: https://github