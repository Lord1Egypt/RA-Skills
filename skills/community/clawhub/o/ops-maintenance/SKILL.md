---
name: ops-maintenance
version: 3.1.0
description: 运维助手 v3.1 - 支持本地、远程、多服务器集群监控、安全审计、智能日志分析、配置变更追踪、告警通知、定时巡检、Docker容器健康巡检、SSL证书监控
userInvocable: true
argumentHint: <health|security|logs|config|report|perf|ports|process|disk|cluster|alert|patrol|docker-health|ssl|add-server|remove-server|upload|download|list|audit> [args]
allowedTools:
 - Bash
 - Read
---

# 运维助手 (ops-maintenance) v3.1

专业的运维助手，支持单服务器和多服务器集群监控、安全审计、智能日志分析、配置变更追踪、告警通知、定时巡检、Docker容器健康巡检、SSL证书监控。

## v3.1 新功能

### Docker 容器健康巡检
- **全面巡检**: 自动检查所有容器的健康状况
- **重启检测**: 检测容器重启次数超限，识别启动即崩溃的僵尸容器
- **OOM Kill检测**: 识别因内存不足被Kill的容器
- **健康检查失败**: 检测Docker HEALTHCHECK失败
- **资源超限**: CPU/内存使用率超阈值告警(70%/75%警告, 90%/90%严重)
- **镜像过期**: 检测超过90天未更新的镜像
- **单容器检查**: 支持指定容器名深度检查

### SSL 证书监控
- **批量域名检查**: 支持同时检查多个域名的SSL证书
- **过期告警**: 默认30天前告警，7天前严重告警
- **证书详情**: 显示颁发者、有效期、SAN域名、协议版本
- **链路检查**: 检测SAN不匹配、不安全协议(TLSv1.0/1.1)
- **配置文件支持**: 从 ~/.config/ops-maintenance/ssl-domains.json 加载域名
- **备用方案**: openssl命令作为Node.js TLS的备用检测方式

### 安全审计系统
- **自动安全扫描**: SSH配置、防火墙状态、文件权限、Docker安全、内核参数
- **风险分级**: high/medium/low 三级风险分类
- **修复建议**: 每项发现自动生成修复建议
- **合规检查**: 对照安全基线自动评估

### 智能日志分析
- **趋势统计**: 按时间段统计错误量，生成时间线
- **模式识别**: 相似日志自动聚合，提取通用模式
- **异常检测**: 4种异常检测(错误突增/新模式/超时聚类/连续爆发)
- **多源关联**: 多个日志源的关联分析
- **自动发现**: 自动发现常见日志路径

### 配置变更追踪
- **基线快照**: 为关键配置文件建立SHA256基线
- **变更检测**: 自动检测配置文件变更
- **差异对比**: 变更详情展示(行级diff)
- **变更历史**: 保留完整变更历史记录
- **预设追踪**: 默认追踪nginx/SSH/sysctl/fstab/hosts/DNS/crontab

### 运维报告生成
- **综合报告**: 一键汇总健康/安全/日志/配置四维报告
- **多格式输出**: Markdown / JSON / 纯文本
- **模块可选**: 可选择性跳过某些模块
- **状态总览**: 一目了然的OK/WARN/CRIT状态汇总

### 告警通知系统
- **多渠道通知**: 飞书机器人 / 企业微信 / 邮件 / Webhook / 控制台
- **8种默认告警规则**: 磁盘(80%/90%)、内存(85%/95%)、负载(5/10)、CPU(80%)、服务宕机
- **告警去重**: 同一规则+服务器不重复触发
- **告警静默**: 指定时间内屏蔽重复告警
- **自动恢复检测**: 阈值恢复后自动标记 resolved 并发送恢复通知
- **告警升级**: 按阈值从高到低，优先触发最高级别
- **持久化存储**: 告警记录保存在 ~/.config/ops-maintenance/alerts.json

### 定时巡检调度
- **自动巡检**: 按配置间隔自动执行 health/disk/memory/load/cpu/service 检查
- **2种默认任务**: 基础健康巡检(5分钟)、服务状态巡检(1分钟)
- **巡检报告**: 自动生成 Markdown 格式报告，保存在 ~/.config/ops-maintenance/reports/
- **手动触发**: 随时手动执行单个或全部巡检任务
- **告警联动**: 巡检结果自动评估告警规则并触发通知

## CLI 命令 (v3.1)

```
ops health              # 系统健康检查
ops security            # 安全审计
ops security --fix      # 安全审计+修复建议
ops logs                # 智能日志分析
ops logs --trends       # 只看趋势
ops logs --anomalies    # 只看异常
ops config list         # 查看追踪文件
ops config check        # 检查配置变更
ops config baseline     # 建立配置基线
ops config history      # 查看变更历史
ops report              # 生成综合运维报告
ops report -f json      # JSON格式报告
ops audit               # 查看审计日志
ops docker-health       # Docker容器健康巡检(全部)
ops docker-health -c nginx  # 检查指定容器
ops docker-health --images  # 只检查镜像更新
ops docker-health --json    # JSON格式输出
ops ssl example.com     # 检查域名SSL证书
ops ssl a.com b.com c.com   # 批量检查
ops ssl example.com --detail  # 证书详情
ops ssl example.com --port 8443  # 指定端口
ops ssl example.com --warn-days 14  # 14天内告警
```

## 告警命令

```
/ops-maintenance alert rules          # 查看告警规则
/ops-maintenance alert list           # 查看活跃告警
/ops-maintenance alert stats          # 查看告警统计
/ops-maintenance alert silence <ruleId> <server> [分钟]  # 静默告警
/ops-maintenance alert cleanup [天数] # 清理旧告警
/ops-maintenance alert notify <channel> <config>  # 配置通知渠道
/ops-maintenance alert add <rule>     # 添加告警规则
/ops-maintenance alert remove <ruleId> # 删除告警规则
/ops-maintenance alert toggle <ruleId> <on|off>  # 启用/禁用规则
```

## 巡检命令

```
/ops-maintenance patrol start         # 启动定时巡检
/ops-maintenance patrol stop          # 停止定时巡检
/ops-maintenance patrol run [jobId]   # 手动执行巡检
/ops-maintenance patrol jobs          # 查看巡检任务
/ops-maintenance patrol reports       # 查看巡检报告
/ops-maintenance patrol add <job>     # 添加巡检任务
/ops-maintenance patrol remove <jobId> # 删除巡检任务
/ops-maintenance patrol toggle <jobId> <on|off>  # 启用/禁用任务
```

## 网络诊断命令

```
/ops-maintenance net ping <host> [count]     # Ping测试
/ops-maintenance net dns <host> [server]     # DNS查询
/ops-maintenance net trace <host> [maxHops]  # 路由追踪
/ops-maintenance net mtr <host> [count]      # MTR测试
/ops-maintenance net port <host> <port>      # 端口连通测试
/ops-maintenance net check <host> [ports]    # 综合连通性测试
```

## 服务管理命令 (Docker + systemd)

```
/ops-maintenance docker ps [all]             # 容器列表
/ops-maintenance docker stats [container]    # 容器资源使用
/ops-maintenance docker inspect <name|id>    # 容器详情
/ops-maintenance docker logs <name|id> [lines] # 容器日志
/ops-maintenance docker images               # 镜像列表
/ops-maintenance svc status <name>           # 服务状态(systemd)
/ops-maintenance svc status <n1> <n2> ...    # 批量服务状态
/ops-maintenance svc logs <name> [lines]     # 服务日志(journalctl)
```

## 基础功能命令

### 健康检查
```
/ops-maintenance health                     # 本地
/ops-maintenance user@host health           # 远程 SSH
```

### 日志分析
```
/ops-maintenance logs [关键词]              # 本地
/ops-maintenance user@host logs error       # 远程
```

### 性能监控 (本地)
```
/ops-maintenance perf
```

### 端口检查
```
/ops-maintenance ports [端口]               # 本地
/ops-maintenance user@host ports 80         # 远程
```

### 进程检查
```
/ops-maintenance process [名称]             # 本地
/ops-maintenance user@host process nginx    # 远程
```

### 磁盘使用
```
/ops-maintenance disk                       # 本地
/ops-maintenance user@host disk             # 远程
```

### 文件传输
```
/ops-maintenance upload <local> <remote>    # 上传文件
/ops-maintenance download <remote> <local>  # 下载文件
/ops-maintenance list <remote>              # 列出远程目录
```

### 审计日志
```
/ops-maintenance audit                      # 查看审计统计
```

## 远程服务器配置

### 方式 1: 配置文件 (推荐)
在 `~/.config/ops-maintenance/servers.json` 中配置:
```json
[
  {
    "host": "192.168.1.100",
    "user": "root",
    "port": 22,
    "keyFile": "~/.ssh/id_rsa",
    "name": "web-1",
    "tags": ["production", "web"]
  }
]
```

### 方式 2: 直接指定
```
user@192.168.1.100 health
root@server.com:2222 disk
```

## 多服务器集群管理

### 查看集群状态
```
/ops-maintenance cluster                    # 查看所有服务器状态
/ops-maintenance cluster @production        # 按标签筛选
```

### 批量添加服务器
```
/ops-maintenance batch-add 192.168.1.100 192.168.1.101
/ops-maintenance batch-add root@192.168.1.100 admin@192.168.1.101
/ops-maintenance import-servers <<EOF
192.168.1.100,22,root,web-1,production;web
192.168.1.101,22,admin,db-1,production;database
EOF
```

### 批量执行命令
```
/ops-maintenance exec "df -h" @production   # 在 production 组执行
/ops-maintenance exec "uptime" all          # 在所有服务器执行
```

## 安全性说明

### v2.1 安全改进
- **移除默认root用户**：必须显式指定SSH用户
- **密码加密存储**：使用AES-256-GCM加密
- **命令白名单验证**：只允许执行安全的只读命令
- **增强安全检查**：检测管道、重定向、命令替换等绕过方式

### 命令白名单
允许: uptime, free, df, ps, tail, grep, journalctl, netstat, ss, lsof, systemctl status, docker ps, ls, du, find
禁止: rm, mv, cp, chmod, shutdown, reboot, useradd, passwd, apt, yum, npm, systemctl start/stop

### 认证方式
1. 密钥认证（推荐）: `"keyFile": "~/.ssh/id_rsa"`
2. 密码认证（加密存储）: 密码自动使用AES-256-GCM加密
3. 默认密钥: 自动使用 ~/.ssh/id_rsa

## 审计日志

- 位置: ~/.config/ops-maintenance/logs/audit.log
- 记录: 时间戳、操作类型、目标服务器、执行命令、状态、时长、错误信息

## 性能优化

- 连接池: 最大10连接，5分钟超时，自动清理
- 并发控制: 批量操作默认5并发
- 重试机制: 3次重试，指数退避

## 技术栈

- Node.js + TypeScript
- ssh2: SSH客户端库
- ssh2-sftp-client: SFTP文件传输
- commander: CLI命令框架
- 审计日志: JSON格式，支持查询和统计

## 开发说明

```bash
cd /Users/a1234/.openclaw/workspace/skills/ops-maintenance
npm install
npm run dev
npm test
npm run build
```
