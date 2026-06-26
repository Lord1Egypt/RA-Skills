---
name: kimi-quota
version: 1.0.1
description: 查询 Kimi API 用量、订阅额度和账户信息。当用户询问"Kimi 额度"、"API 用量"、"剩余次数"、"订阅状态"或需要查看 Kimi Code 使用情况时使用。支持加密保存登录态，首次配置后自动查询。
---

# Kimi Quota

查询 Kimi Code/API 用量、订阅套餐和功能额度。

## 快速使用

```bash
# 首次使用 - 保存 Cookie
python3 scripts/check_quota.py --cookie "kimi-auth=xxx" --save

# 之后使用 - 自动读取保存的 Cookie
python3 scripts/check_quota.py

# 查看 JSON 格式
python3 scripts/check_quota.py --json

# 清除保存的登录态
python3 scripts/check_quota.py --clear
```

## 获取 Cookie

1. 登录 https://www.kimi.com
2. F12 → Application → Cookies → `kimi-auth`
3. 复制值（格式：`eyJhbGciOiJIUzUxMiIs...`）

## 安全说明

Cookie 使用 Fernet 加密存储，密钥派生自机器标识。也可设置环境变量：

```bash
export KIMI_QUOTA_KEY="your-secret-key"
```

存储位置：`~/.config/kimi-quota/cookie.enc`

## 查询内容

- **API 用量**: 本周使用百分比、剩余次数、重置时间
- **频限明细**: 5分钟窗口限额、重置时间
- **订阅信息**: 套餐、价格、周期、续费时间
- **功能额度**: 深度研究、Agent、PPT 剩余次数

## 依赖

```bash
pip install requests cryptography
```
