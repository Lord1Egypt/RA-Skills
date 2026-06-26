# FAQ - Node Connection Doctor

## ❓ 常见问题

### 1. 技能收费吗？为什么？
**答**: 收费是为了持续维护和更新。提供:
- 单次诊断: $5 (一次性)
- 完整修复: $15 (含30天技术支持)

免费 alternative: 手动查阅文档，但可能花费 30-60 分钟。

---

### 2. 修复会丢失我的数据吗？
**答**: 不会。技能只修改配置 (bootstrap token, gateway 绑定)，不触碰:
- 已安装的技能
- 用户数据
- API 密钥
- 历史记录

**建议**: 修复前手动备份 `config/` 目录。

---

### 3. 支持哪些操作系统？
**答**: 所有 OpenClaw 支持的平台:
- Windows 10/11 (推荐)
- Ubuntu 20.04+, Debian 10+
- macOS 12+

需要: Node.js 18+, OpenClaw CLI v2026.3.23+

---

### 4. 为什么诊断说"网络不通"？
**答**: 可能原因:
1. OpenClaw 网关未运行 → `openclaw gateway start`
2. VPN/Tailscale 未连接 → 检查 VPN 状态
3. 防火墙阻止 → 允许 `gateway.openclaw.ai` 端口
4. DNS 问题 → 尝试 `nslookup gateway.openclaw.ai`

技能无法自动修复网络层问题，需要人工干预。

---

### 5. 修复后还是无法连接？
**答**: 常见原因:
1. **配对码过期**: 新 token 生成后 10 分钟内有效，尽快配对
2. **设备已配对**: 需要先在设备上"忘记网络"，重新扫描
3. **网关 token 无效**: 检查 `openclaw config get gateway.auth.token` 是否设置

运行诊断获取具体错误信息。

---

### 6. 可以批量修复多个节点吗？
**答**: 当前版本为单节点设计。批量需求请购买企业版 ($99/月) 或联系定制开发。

---

### 7. 为什么需要管理员权限？
**答**: 部分修复步骤需要:
- 重启系统服务 (`openclaw gateway restart`)
- 修改系统配置文件
- 清除系统级缓存

请以 Administrator/root 运行。

---

### 8. 技能会收集我的数据吗？
**答**: 不会。所有诊断数据仅本地存储:
- 不收集 API 密钥
- 不发送配置到外部服务器
- 不记录诊断历史（除非用户主动保存）

隐私承诺: 100% 离线运行。

---

### 9. 退款政策？
**答**: 14 天内，如果技能未能解决您的问题，全额退款。需提供:
- 诊断日志 (`openclaw skill run node-connection-doctor --log-level debug`)
- 错误截图
- 已尝试的解决步骤

---

### 10. 如何获得更新？
**答**: ClawHub 自动推送更新。或者在 GitHub:
```bash
git clone https://github.com/yourusername/node-connection-doctor
cd node-connection-doctor
npm install
```

---

**仍有问题？** 联系:
- GitHub Issues: https://github.com/yourusername/node-connection-doctor/issues
- Email: support@yourdomain.com
- Discord: @yourusername#1234
