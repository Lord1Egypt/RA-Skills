---
name: internal-admin-playwright
description: Python + Playwright 内部后台自动化技能，支持 VPN(L2TP/IPsec) 可配置接入、严格域名白名单、中文指令路由（例如进入评论管理到视频评论、进入文章管理到文章列表）与固定流程执行。用于受控访问内网后台、禁止外网访问并按预设命令执行菜单操作。
---

# Internal Admin Playwright

## 执行流程

1. 加载 `references/vpn_config.yaml`（可选自动 VPN）。
2. 加载 `references/whitelist.yaml`（白名单和域名解析覆盖）。
3. 执行 `scripts/run.py --command "<中文指令>"`。

## 命令示例

```bash
python3 scripts/run.py --command "进入文章管理->文章列表"
python3 scripts/run.py --command "进入评论管理->视频评论"
```

## 配置点

- VPN：`references/vpn_config.yaml`
- 访问边界白名单：`references/whitelist.yaml`
- 指令路由：`references/menu_map.yaml`

## 环境变量

- `STAFF_USERNAME` / `STAFF_PASSWORD`
- `GOOGLE_OTP`（或页面“标识码/动态码”）
- `LOGIN_URL`（默认 mogusp 登录页）
- `AUTO_VPN=1`（执行前自动 `vpn up`，结束自动 `vpn down`）
- `HEADLESS=1|0`
- `FORCE_IPV4=1|0`

## VPN 手动命令

```bash
python3 scripts/vpn_l2tp.py up
python3 scripts/vpn_l2tp.py status
python3 scripts/vpn_l2tp.py down
```

## 约束

- 未在白名单的域名请求会被直接阻断。
- 未定义命令不会执行（必须先配置 `menu_map.yaml`）。
- 凭据仅通过环境变量或 `vpn_config.yaml` 维护，不要硬编码到脚本。
