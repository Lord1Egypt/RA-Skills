---
name: kimi-quota-monitor
description: Kimi (Kimi Chat) membership quota monitoring and daily reporting. Use when the user needs to (1) check current Kimi usage percentage, (2) set up or configure automated Kimi quota daily push to WeChat via openclaw, (3) calculate quota period cycles and KimiClaw sandbox deduction logic, or (4) troubleshoot Kimi quota fetching failures. Triggers on phrases like "Kimi额度", "quota日报", "会员额度", "额度监控".
---

# Kimi Quota Monitor

抓取 Kimi 会员额度百分比，计算周期抵扣逻辑，推送到微信。

## ⚠️ 使用前配置（必须）

本 skill 需要你填入自己的认证信息才能运行。打开 `scripts/fetch_quota.py`，修改**用户配置区**（文件顶部）：

### 1. Cookies 文件

将 Kimi 登录 cookies 导出为 JSON 文件，放在脚本同级目录（或指定绝对路径）。

**格式**（Playwright cookies 数组）：
```json
[
  {"name": "a1", "value": "xxx", "domain": ".kimi.com", "path": "/"},
  {"name": "web_session", "value": "xxx", "domain": ".kimi.com", "path": "/"}
]
```

**导出方式**：在已登录 Kimi 的浏览器中，打开开发者工具 → Application → Cookies → 复制 `.kimi.com` 域下的所有 cookies，粘贴为 JSON 数组保存到 `kimi_cookies.json`。

### 2. 微信推送目标 ID

获取你的 openclaw-weixin 用户 ID：
```bash
openclaw message list-accounts --channel openclaw-weixin
```

将 `TARGET_ID` 替换为你的 ID，格式为 `xxx@im.wechat`。

### 3. localStorage 认证数据

在已登录 Kimi 的浏览器中，打开开发者工具 → Application → Local Storage → `https://www.kimi.com`，复制以下键值：

- `access_token`
- `refresh_token`
- `msh_user_id`
- `msh_user_subscription_data`

填入 `LS_DATA` 字典中。

> ⚠️ 这些是敏感认证信息，请勿泄露给他人。

## Quick Start

### 手动抓取额度

配置完成后，在 skill 目录执行：
```bash
python3 scripts/fetch_quota.py
```

脚本会自动：
1. 启动 Playwright headless Chrome
2. 加载 cookies 和 localStorage 登录
3. 访问 `kimi.com/membership/subscription`
4. 提取额度百分比
5. 计算周期和抵扣
6. 推送到微信

### 配置定时任务

添加到 crontab：
```
8 7 * * * /usr/bin/python3 /path/to/kimi-quota-monitor/scripts/fetch_quota.py >> /path/to/logs/kimi_quota.log 2>&1
```

## Dependencies

- `playwright` Python package (`pip install playwright`)
- System Chrome browser (`google-chrome` or `chromium`)
- `openclaw` CLI with `openclaw-weixin` channel configured
- `kimi_cookies.json` — Kimi login cookies (用户自行配置)

## How Quota Calculation Works

- **Reset date**: 22nd of each month
- **Cycle length**: total days of current month (28/29/30/31)
- **Daily baseline**: `100% / month_days`
- **KimiClaw sandbox est.**: 0.6% per day
- **Deduction logic**: KimiClaw estimate subtracts from diff until diff reaches 0

See [references/quota_rules.md](references/quota_rules.md) for full calculation details, CSS selectors, and message template.

## Resources

### scripts/
- `fetch_quota.py` — Main script: fetch quota, calculate, push to WeChat
  - **Top section marked "用户配置区" must be filled before use**

### references/
- `quota_rules.md` — Calculation rules, page URLs, selectors, message format

## Files

| File | Purpose |
|------|---------|
| `scripts/fetch_quota.py` | Core automation script (requires user config) |
| `references/quota_rules.md` | Calculation rules and reference |
| `kimi_cookies.json` | Kimi login cookies (user-provided, not included) |
