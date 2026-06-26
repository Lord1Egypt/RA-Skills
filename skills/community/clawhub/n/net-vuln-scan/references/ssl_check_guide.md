# SSL/TLS 证书检测指南

## ssl_check.py

### 功能说明
检测 HTTPS 服务的 SSL/TLS 证书问题。

### 使用方法

```bash
# 检测单个域名
python scripts/ssl_check.py example.com

# 检测多个域名
python scripts/ssl_check.py example.com google.com

# 详细输出
python scripts/ssl_check.py example.com --verbose
```

### 输出示例

```
=== SSL 证书检测结果 ===
域名: example.com
检测时间: 2026-03-18 14:30

证书信息:
- 颁发者: Let's Encrypt
- 有效期: 2026-01-01 至 2026-04-01
- 剩余天数: 45 天
- 证书链: 完整

协议支持:
✅ TLS 1.2 - 支持
✅ TLS 1.3 - 支持
❌ SSLv3 - 不支持 (安全)
❌ TLS 1.0 - 不支持 (安全)
❌ TLS 1.1 - 不支持 (安全)

加密套件:
✅ 安全套件优先

安全头:
✅ HSTS 已启用
✅ Content-Security-Policy 已设置
❌ X-Frame-Options 未设置

风险评估:
🟡 中危: 证书将在 45 天后过期
🟡 中危: 缺少 X-Frame-Options 头

建议:
1. 证书到期前续期
2. 添加 X-Frame-Options: DENY 头
3. 启用 Certificate Transparency
```

## 常见 SSL 问题

### 1. 证书过期

**问题**: 证书已过期或即将过期
**风险**: 用户访问时显示警告，信任度下降
**修复**: 续期证书，配置自动续期

### 2. 自签名证书

**问题**: 使用自签名证书
**风险**: 中间人攻击风险
**修复**: 使用 Let's Encrypt、CA 签发证书

### 3. 弱协议

**问题**: 启用 SSLv3、TLS 1.0、1.1
**风险**: POODLE、BEAST 攻击
**修复**: 禁用弱协议，仅启用 TLS 1.2+

### 4. 弱加密套件

**问题**: 支持 3DES、RC4 等弱加密
**风险**: 加密可被破解
**修复**: 仅启用 AEAD 加密套件

### 5. 缺失安全头

**问题**: 缺少 HSTS、X-Frame-Options 等
**风险**: 点击劫持、跨站脚本
**修复**: 配置安全响应头

## 检测项目清单

| 检测项 | 严重程度 | 建议 |
|--------|----------|------|
| 证书过期 | 🔴 高 | 立即续期 |
| 证书链不完整 | 🔴 高 | 修复证书链 |
| 启用 SSLv3 | 🔴 高 | 禁用 |
| 启用 TLS 1.0/1.1 | 🟡 中 | 禁用 |
| 弱加密套件 | 🔴 高 | 禁用 |
| 未启用 HSTS | 🟡 中 | 启用 |
| 缺失 CSP | 🟢 低 | 添加 |
| 缺失 X-Frame-Options | 🟢 低 | 添加 |
