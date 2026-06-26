# Validation Guide - Node Connection Doctor

本指南帮助您验证技能是否满足您的需求。

---

## ✅ 快速测试 (5 分钟)

### 1. 诊断模式测试
```bash
# 正常情况 (网关运行，已配对)
openclaw skill run node-connection-doctor --input '{"mode": "diagnose", "verbose": true}'
```

**预期输出**:
- ✅ Gateway status: OK
- ✅ Node config: Valid
- ✅ Network: Connected
- 📊 总评分: Healthy (90-100)

### 2. 修复模式测试 (谨慎使用)
```bash
# 先 dry-run 检查
openclaw skill run node-connection-doctor --input '{"mode": "fix", "dry_run": true}'
```

**预期**: 显示将要执行的操作，不实际修改

**实际修复** (确认后):
```bash
openclaw skill run node-connection-doctor --input '{"mode": "fix", "auto_confirm": false}'
```

---

## 📊 验证清单

| 功能 | 测试场景 | 预期结果 | 状态 |
|------|----------|----------|------|
| 网关状态检测 | `gateway status` 正常运行 | ✅ OK | ☐ |
| 网关状态检测 | `gateway status` 停止 | ❌ 错误详情 | ☐ |
| 配置读取 | 配置文件存在 | ✅ 解析成功 | ☐ |
| 配置读取 | 配置文件缺失 | ❌ 明确错误 | ☐ |
| 修复流程 | 用户取消 | ❌ Cancelled | ☐ |
| 修复流程 | 用户确认 | ✅ 逐步执行 | ☐ |
| 报告生成 | 诊断完成 | ✅ HTML 文件 | ☐ |

---

## 🎯 真实场景演练

### 场景 A: QR 扫描失败
**症状**: "Pairing required" 错误

**验证步骤**:
1. 运行诊断: `openclaw skill run node-connection-doctor --mode diagnose`
2. 检查输出: 应该指出 bootstrap token 缺失或无效
3. 运行修复: `openclaw skill run node-connection-doctor --mode fix`
4. 重新配对: 使用新的 QR code/token

**预期**: 问题解决，设备成功配对

---

### 场景 B: 手动连接失败 (unauthorized)
**症状**: "Invalid token" 错误

**验证步骤**:
1. 诊断确认 token 问题
2. 修复 → 生成新 token
3. 手动输入新 token 连接

**预期**: 新 token 有效，连接成功

---

### 场景 C: 网络/VPN 问题
**症状**: Ping 失败，连接超时

**验证步骤**:
1. 诊断应该检测到网络不通
2. 建议检查 Tailscale/VPN
3. 修复不会修改网络配置 (用户需手动处理)

**预期**: 正确识别网络层问题，不尝试自动修复

---

## 🐛 已知限制

1. **不支持**: 修改用户防火墙规则 (需手动)
2. **不支持**: 自动安装 Tailscale (需预装)
3. **依赖**: `openclaw` CLI 必须在 PATH 中
4. **权限**: 修复需要管理员/root (部分步骤)

---

## 📝 测试报告模板

完成测试后，记录以下信息:

```
Date: ____________________
OpenClaw version: ________
Node OS: _________________

测试项:
☐ 诊断模式 (正常)
☐ 诊断模式 (错误)
☐ 修复 dry-run
☐ 修复实际 (谨慎)
☐ 场景 A (QR失败)
☐ 场景 B (token无效)
☐ 场景 C (网络问题)

发现的问题:
1. __________________
2. __________________
3. __________________

建议改进:
1. __________________
2. __________________
```

---

**支持**: 提交 issue 到 GitHub repository with test report attached.
