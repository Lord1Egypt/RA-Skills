---
name: ops-maintenance
description: 运维助手 v3.3.10 - 本地/远程/集群监控 (健康检查、日志分析、性能监控、批量操作、密码过期检查、告警通知、定时巡检、Docker健康、SSL证书、安全审计、网络诊断)
userInvocable: true
argumentHint: <health|logs|perf|ports|process|disk|password|network|report|audit|docker|ssl|security|cluster> [args]
allowedTools:
  - Bash
  - Read
---

# 运维助手 (ops-maintenance) v3.3.10

专业的运维助手，支持单服务器和多服务器集群监控。

## v3.3.8 新功能

### 网络诊断
```
/ops-maintenance network               # 网络诊断（ping/dns/port）
/ops-maintenance network <host>        # 指定主机检测
```

### 运维报告
```
/ops-maintenance report                # 集群状态摘要报告
```

### 操作审计
```
/ops-maintenance audit                 # 查看审计日志统计
```

### Docker 健康巡检
```
/ops-maintenance docker                # Docker容器健康检查
```

### SSL 证书监控
```
/ops-maintenance ssl                   # SSL证书检查
```

### 安全审计
```
/ops-maintenance security              # 安全配置审计
```

### 远程密码检查
```
/ops-maintenance user@host password    # 远程服务器密码过期检查
```

## 功能命令

### 健康检查
```
/ops-maintenance health              # 本地
/ops-maintenance user@host health    # 远程 SSH
```

### 日志分析  
```
/ops-maintenance logs [关键词]       # 本地
/ops-maintenance user@host logs error  # 远程
```

### 性能监控 (本地)
```
/ops-maintenance perf
```

### 端口检查
```
/ops-maintenance ports [端口]        # 本地
/ops-maintenance user@host ports 80  # 远程
```

### 进程检查
```
/ops-maintenance process [名称]      # 本地
/ops-maintenance user@host process nginx  # 远程
```

### 磁盘使用
```
/ops-maintenance disk                # 本地
/ops-maintenance user@host disk      # 远程
```

### 密码过期检查
```
/ops-maintenance password            # 检查所有配置服务器的密码过期状态
```

## 远程服务器配置

### 方式 1: SSH Config (推荐)
在 `~/.ssh/config` 中配置:
```
Host myserver
    HostName 192.168.1.100
    User root
    Port 22
    IdentityFile ~/.ssh/id_rsa
```

### 方式 2: 直接指定
```
user@192.168.1.100 health
root@server.com:2222 disk
```

## 支持的远程操作
- health: 系统负载、内存、磁盘、服务状态
- logs: 远程日志搜索
- ports: 端口占用检查
- process: 进程查找
- disk: 磁盘使用分析
- password: 远程密码过期检查（v3.3.8新增）

## 输出格式

返回 Markdown 格式结果，包含:
- 标题 (emoji + 操作名 + 服务器)
- 代码块中的命令输出
- 关键发现和建议

### 密码过期检查输出示例

```
### 🔐 密码过期检查 (本地)

| 用户 | 上次修改 | 过期日期 | 最大天数 | 状态 |
|------|----------|----------|----------|------|
| root | 2024-01-15 | 2024-07-15 | 180 | ✅ 有效 |
| admin | 2024-02-01 | never | 90 | ⚠️ 永不过期 |
| user1 | 2023-11-01 | 2024-01-01 | 60 | ❌ 已过期 |
```

## 多服务器集群管理

### 查看集群状态
```
/ops-maintenance cluster              # 查看所有服务器状态
/ops-maintenance cluster @production  # 按标签筛选
```

### 批量添加服务器
```
# 直接添加多个 IP
/ops-maintenance batch-add 192.168.1.100 192.168.1.101 192.168.1.102

# 带端口
/ops-maintenance batch-add 192.168.1.100:2222 192.168.1.101:22

# 带用户
/ops-maintenance batch-add root@192.168.1.100 admin@192.168.1.101

# 完整格式
/ops-maintenance batch-add user@host:port user2@host2:port

# CSV 格式 (多行)
/ops-maintenance import-servers <<EOF
192.168.1.100,22,root,web-1,production;web
192.168.1.101,22,admin,db-1,production;database
EOF

# JSON 格式
/ops-maintenance import-servers [{"host":"192.168.1.100","name":"web-1","tags":["prod"]}]
```

### 添加服务器
```
/ops-maintenance add-server 192.168.1.100 --name web1 --tags production,web
```

### 移除服务器
```
/ops-maintenance remove-server 192.168.1.100
```

### 批量执行命令
```
/ops-maintenance exec "df -h" @production   # 在 production 组执行
/ops-maintenance exec "uptime" all          # 在所有服务器执行
```

### 服务器配置文件
- 位置: `~/.config/ops-maintenance/servers.json`
- 支持字段: host, port, user, keyFile, name, tags
- **密码加密**: v3.3.8+ 自动加密存储，密钥文件位于 `~/.config/ops-maintenance/.key`

### 示例配置
```json
[
  {
    "host": "192.168.1.100",
    "user": "root",
    "name": "web-1",
    "tags": ["production", "web"]
  },
  {
    "host": "192.168.1.101",
    "user": "admin",
    "name": "db-1",
    "tags": ["production", "database"]
  }
]
```

## 告警通知 (v3.3+)

### 告警规则管理
```
/ops-maintenance alert rules     # 查看告警规则
/ops-maintenance alert list      # 查看活跃告警
/ops-maintenance alert stats     # 查看告警统计
/ops-maintenance alert silence <ruleId> <server> [分钟]  # 静默告警
/ops-maintenance alert cleanup [天数]  # 清理旧告警
```

### 通知渠道配置
```
/ops-maintenance alert notify email '{"smtpHost":"smtp.qq.com","smtpPort":465,"smtpUser":"xxx","smtpPass":"授权码","from":"xxx","to":["收件人"]}'
/ops-maintenance alert notify feishu '{"webhook":"https://...", "secret":"..."}'
/ops-maintenance alert notify webhook '{"url":"https://..."}'
```

## 定时巡检 (v3.3+)

### 巡检任务管理
```
/ops-maintenance patrol list     # 查看巡检任务
/ops-maintenance patrol run      # 执行巡检
/ops-maintenance patrol start    # 启动定时巡检
/ops-maintenance patrol stop     # 停止定时巡检
```

## i18n 国际化 (v3.3.8新增)

```bash
# 设置语言
export LANG=en_US.UTF-8  # 英文
export LANG=zh_CN.UTF-8  # 中文（默认）
```

## 测试

### 运行测试
```bash
# 运行所有测试
npm test

# 运行核心功能测试（快速）
npm test -- test/core.test.ts

# 运行特定测试
npm test -- --testNamePattern="健康检查"
```

### 测试覆盖
- ✅ 平台检测与命令执行
- ✅ 本地健康检查
- ✅ 日志分析
- ✅ 性能监控
- ✅ 进程检查
- ✅ 密码过期检查
- ✅ 服务器配置管理
- ✅ 告警管理
- ✅ 巡检调度
- ✅ SSL监控
- ✅ 邮件通知
- ✅ 安全审计
- ✅ Docker健康
- ✅ 密码加密
- ✅ i18n 国际化
- ✅ 配置变更追踪
- ✅ 审计报告生成
- ✅ 网络诊断

## 故障排除

### SSH连接问题
1. **连接超时**: 检查网络连接和防火墙设置
2. **认证失败**: 确认SSH密钥配置正确
3. **主机密钥验证**: 首次连接需要手动确认主机密钥

### 命令执行缓慢
1. **网络延迟**: 远程命令受网络影响
2. **系统负载**: 高负载时响应变慢
3. **超时设置**: 可在代码中调整超时时间

### 权限问题
1. **文件访问**: 某些系统文件需要root权限
2. **命令执行**: 部分命令需要sudo权限
3. **日志读取**: 确保有日志文件读取权限

## 性能优化

### 缓存策略
- 内存缓存: 30秒TTL，减少重复计算
- 文件缓存: 持久化存储，跨会话复用
- 连接池: SSH连接复用，减少握手开销

### 批量操作
- 使用集群命令而非单台操作
- 合并相关命令减少网络往返
- 合理设置超时时间

### 监控建议
- 定期检查服务器健康状态
- 关注密码过期时间
- 监控磁盘使用趋势
- 设置关键服务端口监控

## 架构说明

### Clean Architecture
```
src-new/
├── core/              # 核心业务逻辑
│   ├── usecases/     # 用例实现
│   └── domain/       # 领域模型
├── infrastructure/    # 基础设施
│   ├── ssh/          # SSH客户端
│   ├── cache/        # 缓存实现
│   └── monitoring/   # 监控策略
├── presentation/      # 表现层
│   └── cli/          # CLI接口
└── config/           # 配置管理
```

### 设计模式
- **依赖注入**: 使用容器管理依赖
- **策略模式**: 可插拔的监控策略
- **适配器模式**: 兼容旧版API
- **工厂模式**: 创建SSH连接

### 数据流
```
用户命令 → CLI解析 → UseCase → Infrastructure → 外部系统
                ↓
            缓存层
```

## 开发指南

### 添加新功能
1. 在`core/usecases/`创建新的UseCase
2. 在`infrastructure/`实现必要的适配器
3. 在`presentation/cli/`添加CLI命令
4. 更新`container.ts`注册依赖
5. 添加测试用例

### 代码规范
- 使用TypeScript类型注解
- 遵循Clean Architecture原则
- 保持向后兼容性
- 添加适当的错误处理
- 编写单元测试

### 调试技巧
```bash
# 启用详细日志
DEBUG=* npm start

# 测试单个功能
node run.js health

# 检查配置
cat ~/.config/ops-maintenance/servers.json
```

## 限制与注意事项

### 平台支持
- ✅ Linux: 完整支持
- ✅ macOS: 基本支持（部分功能受限）
- ⚠️ Windows: 有限支持（通过WSL）

### 网络要求
- SSH连接需要稳定的网络
- 防火墙需要开放SSH端口
- 建议使用SSH密钥认证

### 安全建议
- 不要在代码中硬编码密码
- 使用SSH密钥而非密码认证
- 定期更新SSH密钥
- 限制服务器访问权限
- 加密敏感配置信息（v3.3.8+自动加密）

## 贡献指南

### 报告问题
提供详细的错误信息：
- 操作系统版本
- Node.js版本
- 复现步骤
- 错误日志

### 提交代码
1. Fork项目
2. 创建功能分支
3. 编写测试
4. 提交Pull Request

### 文档改进
- 修正错误和不准确之处
- 添加使用示例
- 翻译文档
