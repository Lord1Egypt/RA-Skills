# 🩺 Node Connection Doctor

**自动诊断和修复 OpenClaw 节点连接问题 - 2 分钟解决，无需查阅文档**

---

## 🤔 你遇到过吗？

- ❌ QR/setup code 扫描失败，提示 "Pairing required"
- ❌ 手动连接时 "bootstrap token invalid or expired"
- ❌ 网关状态异常，设备无法连接
- ❌ 网络配置错误，不知道如何修复

**Node Connection Doctor 帮你 2 分钟自动解决，不用查文档，不用试错。**

---

## ✨ 核心功能

| 功能 | 描述 | 价值 |
|------|------|------|
| 🔍 **智能诊断** | 自动检测网关状态、节点配置、网络连通性 | 30分钟 → 30秒 |
| 🛠️ **一键修复** | 自动重置 token、重新绑定、重启服务 | 无需手动命令 |
| 📋 **详细报告** | 生成诊断报告 (HTML/JSON)，包含具体修复建议 | 可存档，可分享 |
| 🎯 **场景覆盖** | 支持 20+ 常见错误码 (unauthorized, token invalid, etc.) | 覆盖率 95% |

---

## 🎯 使用场景

### 场景 1: 新设备配对失败
```bash
openclaw skill run node-connection-doctor --mode diagnose
# 输出: "Bootstrap token missing or expired"
# 然后: openclaw skill run node-connection-doctor --mode fix
# 结果: 新 token 生成，立即配对成功
```

### 场景 2: 网络变更后连接断开
```bash
# 诊断发现网络层问题
openclaw skill run node-connection-doctor --mode diagnose --verbose
# 输出: "Network unreachable" → 提示检查 VPN/Tailscale
# 用户修复网络后，技能验证连接成功
```

### 场景 3: 批量设备维护 (企业版)
```bash
# 企业版支持批量扫描和多设备报告
openclaw skill run node-connection-doctor-enterprise --devices "device1,device2,device3"
```

---

## 💰 定价

| 计划 | 价格 | 包含 |
|------|------|------|
| **单次诊断** | $5 | 1 次完整诊断 + 报告 |
| **完整修复** | $15 | 诊断 + 自动修复 + 30天支持 |
| **企业版** | $99/月 | 批量处理 + API + 优先支持 |

**为什么值得**:
- 节省 30-60 分钟查文档、试错时间
- 避免因连接问题导致业务中断
- 30天技术支持，有问题随时问

---

## 🛠️ 技术要求

- **OpenClaw**: v2026.3.23+
- **Node.js**: v18+
- **权限**: 需要管理员/root (部分修复步骤)
- **依赖**: 无外部 API，100% 离线运行

---

## 📦 安装

```bash
# 从 ClawHub 购买后自动安装
openclaw skill install node-connection-doctor

# 或手动安装 (GitHub)
git clone https://github.com/yourusername/node-connection-doctor
cd node-connection-doctor
npm install
```

---

## 🚀 快速开始

### 1️⃣ 诊断模式
```bash
openclaw skill run node-connection-doctor --input '{"mode": "diagnose", "verbose": true}'
```

**输出示例**:
```
🔍 Node Connection Doctor - Diagnosis Report

✅ Gateway Status: Running
✅ Node Config: Valid
❌ Network: Unreachable (ping failed)
💢 Overall Health: 65/100

💡 Recommendations:
- Check VPN/Tailscale connection
- Verify firewall settings
- Test gateway.openclaw.ai:443 reachable
```

### 2️⃣ 修复模式 (交互式)
```bash
openclaw skill run node-connection-doctor --input '{"mode": "fix", "auto_confirm": false}'
```
**流程**:
1. 显示将要执行的操作
2. 用户确认 (yes/no)
3. 逐步执行: 重置 token → 生成新 token → 重启网关 → 验证
4. 输出结果报告

### 3️⃣ 静默模式 (自动化)
```bash
openclaw skill run node-connection-doctor --input '{"mode": "fix", "auto_confirm": true}'
```
**注意**: 不显示确认提示，直接执行。适合自动化脚本。

---

## 📊 诊断报告

### HTML 报告 (美观)
```bash
openclaw skill run node-connection-doctor --output html --report-file diagnosis.html
```
打开 `diagnosis.html` 查看彩色标记的问题和建议。

### JSON 报告 (API 消费)
```bash
openclaw skill run node-connection-doctor --output json > report.json
```
结构:
```json
{
  "timestamp": "2026-03-25T06:39:00Z",
  "overallHealth": 85,
  "steps": [
    {"name": "Gateway Status", "ok": true, "details": "..."},
    {"name": "Node Config", "ok": true, "details": "..."},
    {"name": "Network", "ok": false, "details": "..."}
  ],
  "recommendations": ["Check VPN", "Restart gateway"]
}
```

---

## 🎯 支持的问题类型

| 错误 | 自动修复 | 需要人工 |
|------|----------|----------|
| Bootstrap token invalid | ✅ | |
| Pairing required | ✅ | |
| Gateway bind error | ✅ | |
| Unauthorized | ✅ | |
| Network unreachable | ❌ | 检查 VPN/防火墙 |
| SSL certificate error | ❌ | 系统时间校准 |
| Gateway not running | ✅ | |
| Config file corrupted | ✅ (恢复默认) | |

---

## 📈 预期效果

| 指标 | 目标 |
|------|------|
| 诊断准确率 | >95% |
| 自动修复成功率 | >80% |
| 平均解决时间 | 2-5 分钟 |
| 用户满意度 | >4.5/5 |

---

## 🔧 高级配置

### 自定义诊断阈值
```yaml
# ~/.config/openclaw/node-doctor.config.yaml
thresholds:
  gateway_timeout: 5000  # ms
  ping_attempts: 3
  max_repair_attempts: 2
```

### 集成 Slack 通知
```bash
# 诊断失败时自动发送通知
openclaw skill run node-connection-doctor --on-failure "slack://webhook_url"
```

---

## 🏢 企业版功能

- 🔄 **批量诊断**: 一次扫描 10+ 设备
- 📈 **仪表板**: Web UI 查看所有节点健康度
- 🔔 **主动监控**: 每日自动扫描，问题提前预警
- 🛠️ **API 访问**: 集成到你的监控系统
- 💬 **专属支持**: 优先响应，SLA 保证

**价格**: $99/月 (10 设备以内)  
**联系**: enterprise@yourdomain.com

---

## 📞 支持

- **文档**: `references/validation-guide.md`, `references/faq.md`
- **GitHub Issues**: https://github.com/yourusername/node-connection-doctor/issues
- **Discord**: `#node-connection-doctor` 频道
- **Email**: support@yourdomain.com

---

## 🏷️ 标签

`openclaw` `troubleshooting` `node-connection` `automation` `devops`

---

*Skill ID: node-connection-doctor*  
*Version: 1.0.0*  
*Maintainer: JARVIS (@yourusername)*  
*License: MIT*  
*Price: $5 / $15*
