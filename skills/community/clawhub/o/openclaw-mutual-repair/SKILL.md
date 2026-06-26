# 🤖 OpenClaw 双机互修助手

> **让两只 OpenClaw 互相守护，实现 7×24 小时稳定运行**

---

## 📦 安装

```bash
clawhub install openclaw-mutual-repair
```

---

## 🚀 快速开始

### 1. 配置双机环境

在两台机器上分别配置：

**机器 A (192.168.1.100):**
```json
{
  "localHost": "0.0.0.0",
  "localPort": 9528,
  "remoteHost": "192.168.1.101",
  "remotePort": 9528,
  "heartbeatInterval": 300000
}
```

**机器 B (192.168.1.101):**
```json
{
  "localHost": "0.0.0.0",
  "localPort": 9528,
  "remoteHost": "192.168.1.100",
  "remotePort": 9528,
  "heartbeatInterval": 300000
}
```

### 2. 启动互修服务

在飞书或 OpenClaw 中输入：
```
启动互修
```

### 3. 使用示例

```
用户：健康检查
用户：诊断
用户：启动互修
用户：停止互修
```

---

## 📋 核心功能

### 1. 心跳监控 💓
- 双机定期发送心跳（默认 5 分钟）
- 自动检测对端是否在线
- 心跳超时自动告警

### 2. 健康检查 🏥
- 内存使用率监控
- CPU 使用率监控
- PM2 进程状态检查
- 系统运行时间统计

### 3. 故障诊断 🔍
- 自动识别内存泄漏风险
- 检测进程异常重启
- 网络连通性诊断

### 4. 自动修复 🛠️
- 远程重启 OpenClaw 进程
- 发送修复建议
- 故障转移（规划中）

---

## ⚙️ 配置项

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| localHost | string | 0.0.0.0 | 本机监听地址 |
| localPort | number | 9528 | 本机监听端口 |
| remoteHost | string | - | 对端主机地址（必填） |
| remotePort | number | 9528 | 对端监听端口 |
| heartbeatInterval | number | 300000 | 心跳间隔（毫秒） |
| heartbeatTimeout | number | 30000 | 心跳超时（毫秒） |
| memoryThreshold | number | 85 | 内存告警阈值（%） |
| cpuThreshold | number | 80 | CPU 告警阈值（%） |

---

## 🔐 安全说明

1. **网络隔离**：建议在内部网络使用，不要暴露到公网
2. **防火墙配置**：仅允许对端 IP 访问心跳端口
3. **SSH 密钥**：远程修复功能需要配置 SSH 免密登录（可选）

---

## 📊 监控指标

| 指标 | 正常值 | 告警阈值 |
|------|--------|----------|
| 内存使用率 | < 70% | > 85% |
| CPU 使用率 | < 50% | > 80% |
| WebSocket 连接数 | > 10 | < 5 |
| 断连频率 | < 2 次/小时 | > 5 次/小时 |
| 进程重启次数 | 0 | > 5 |

---

## 🐛 故障排查

### 问题 1：心跳发送失败
```
[Heartbeat] Failed to send: connect ECONNREFUSED
```
**解决：** 检查对端 OpenClaw 是否运行，防火墙是否开放端口

### 问题 2：端口被占用
```
Error: listen EADDRINUSE: address already in use
```
**解决：** 修改 `localPort` 配置，或停止占用端口的进程

### 问题 3：PM2 检测失败
```
PM2 未检测到 OpenClaw 进程
```
**解决：** 使用 PM2 启动 OpenClaw：`pm2 start app.js --name openclaw`

---

## 📚 相关文件

- `src/index.ts` - 核心实现
- `skill.json` - Skill 配置
- `package.json` - 依赖管理
- `tsconfig.json` - TypeScript 配置

---

## 📝 更新日志

### v1.0.0 (2026-03-27)
- ✨ 初始版本发布
- 🎯 实现双机心跳协议
- 🏥 健康检查功能
- 🔍 故障诊断功能
- 🛠️ 远程修复功能（PM2/systemd）

---

**作者：** OpenClaw Skill Master  
**许可：** MIT  
**反馈：** https://github.com/rfdiosuao/openclaw-skills/issues
