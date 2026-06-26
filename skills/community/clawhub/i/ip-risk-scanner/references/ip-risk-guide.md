# IP 风险监测参考文档

## Claude Code IP 审查机制分析

### 已知的 IP 风险因素

根据 2026 年 3 月 Claude 封号潮的分析，以下 IP 类型容易被封：

#### 高风险 IP（避免使用）

| IP 类型 | 风险等级 | 原因 |
|--------|---------|------|
| Tor 出口节点 | ❌ 极高 | 匿名网络，立即触发风控 |
| 免费公共代理 | ❌ 极高 | 大量滥用历史 |
| 数据中心 IP（高频使用）| ❌ 高 | 被标记为非人类流量 |
| 有 Abuse 记录的 IP | ❌ 高 | 历史不良记录 |
| Catixs Ltd 部分 IP | ⚠️ 高 | 所有者声誉问题 |

#### 中等风险 IP（需谨慎）

| IP 类型 | 风险等级 | 建议 |
|--------|---------|------|
| AWS/Azure/GCP | ⚠️ 中 | 控制频率，避免多账号 |
| DigitalOcean/Vultr | ⚠️ 中 |  same as above |
| 小型主机商 VPS | ⚠️ 中 | 定期监测声誉 |
| Back Waves | ⚠️ 中低 | 声誉良好但仍是 IDC |

#### 低风险 IP（推荐使用）

| IP 类型 | 风险等级 | 说明 |
|--------|---------|------|
| 移动网络 (4G/5G) | ✅ 最低 | CGNAT 共享，Anthropic 最宽容 |
| 住宅宽带 | ✅ 低 | 真实家庭用户 |
| 大型 ISP(Comcast/Verizon) | ✅ 低 | 知名运营商 |
| Cogent 等骨干网 | ✅ 低 | 声誉良好 |

---

## Scamalytics 欺诈评分标准

### 评分范围

| 分数 | 等级 | 含义 |
|------|------|------|
| 0-20 | 极低风险 | 几乎可以确定是合法流量 |
| 21-40 | 低风险 | 可能是合法流量 |
| 41-60 | 中等风险 | 需要进一步验证 |
| 61-80 | 高风险 | 很可能是欺诈流量 |
| 81-100 | 极高风险 | 几乎可以确定是欺诈 |

### 评估维度

1. **IP 类型** (权重 25%)
   - 住宅/移动 > 数据中心 > 代理 > Tor

2. **地理位置** (权重 15%)
   - 与用户声明位置是否一致
   - 是否来自高风险国家

3. **运营商声誉** (权重 20%)
   - 历史流量质量
   - Abuse 记录数量

4. **代理/VPN 检测** (权重 20%)
   - 是否使用匿名服务

5. **使用模式** (权重 20%)
   - 流量异常检测
   - 行为分析

---

## BrowserLeaks 检测项目

### 1. WebRTC 泄漏检测

**检测原理**: WebRTC 可通过 STUN 服务器获取真实 IP

**测试方法**:
```
访问 https://browserleaks.com/webrtc
查看是否显示真实 IP
```

**修复建议**:
- 禁用 WebRTC
- 使用 WebRTC Leak Prevent 扩展
- 使用支持 WebRTC 隔离的 VPN

### 2. DNS 泄漏检测

**检测原理**: DNS 请求可能绕过 VPN/代理

**测试方法**:
```
访问 https://browserleaks.com/dns
查看 DNS 服务器是否属于预期 ISP
```

**修复建议**:
- 使用 DNS over HTTPS (DoH)
- 使用 VPN 提供商的 DNS
- 手动配置 DNS

### 3. Canvas 指纹检测

**检测原理**: Canvas 渲染结果可用于设备识别

**测试方法**:
```
访问 https://browserleaks.com/canvas
查看 Canvas 指纹唯一性
```

**修复建议**:
- 使用 Canvas 指纹保护扩展
- 使用 Tor Browser
- 禁用 JavaScript (不推荐)

### 4. 字体指纹检测

**检测原理**: 安装字体组合可用于设备识别

**修复方法**:
```
访问 https://browserleaks.com/fonts
```

---

## 快速查询 API

### 免费 IP 查询 API

| API | 地址 | 限制 |
|-----|------|------|
| ip-api.com | http://ip-api.com/json/{IP} | 45 次/分钟 |
| ipapi.co | https://ipapi.co/{IP}/json/ | 1000 次/月 |
| ipwhois.app | http://ipwhois.app/json/{IP} | 无限制 |

### 付费 API（更准确）

| API | 价格 | 特点 |
|-----|------|------|
| Scamalytics | 联系询价 | 欺诈评分最准确 |
| IPinfo | $99/月起 | 数据全面 |
| MaxMind | $24/月起 | 地理位置准确 |

---

## Claude Code 使用建议

### 安全使用指南

1. **首选 IP 类型**
   - ✅ 移动网络 (4G/5G)
   - ✅ 住宅宽带
   - ⚠️ 知名云服务商（控制频率）

2. **避免的行为**
   - ❌ 高频请求（>100 次/小时）
   - ❌ 多账号同 IP
   - ❌ 使用公共代理

3. **建议的频率限制**
   ```
   住宅/移动 IP: < 200 请求/5 小时
   数据中心 IP: < 50 请求/5 小时
   ```

4. **定期检查**
   - 每月检查一次 IP 声誉
   - 关注 Scamalytics 评分变化
   - 检查是否有 Abuse 记录

---

## 常见问题解答

### Q: 我的 IP 风险评分高怎么办？

**A:** 
1. 联系 ISP 申请更换 IP
2. 重启路由器（动态 IP 有效）
3. 使用移动网络（手机热点）
4. 避免使用公共代理

### Q: 数据中心 IP 一定被封吗？

**A:** 不一定，但需要注意：
- 控制请求频率
- 不要同时使用多账号
- 定期检查 IP 声誉

### Q: 如何知道我的 IP 是否被列入黑名单？

**A:** 检查以下网站：
- Spamhaus: https://www.spamhaus.org/query/ip/
- AbuseIPDB: https://www.abuseipdb.com/check/
- VirusTotal: https://www.virustotal.com/gui/ip-address/

### Q: Claude Code 会立即封禁数据中心 IP 吗？

**A:** 不会立即封禁，但：
- 高频使用会被标记
- 多账号操作风险极高
- 有 Abuse 记录的会优先处理

---

## 参考资料

- [Scamalytics 官方网站](https://scamalytics.com)
- [BrowserLeaks 官方网站](https://browserleaks.com)
- [IP Fraud Score 工作原理](https://youverify.co/blog/ip-fraud-score)
- [Claude 封号原因解析](https://www.augmunt.com/blog/claude-account-ban-solutions-deep-dive-2026/)
