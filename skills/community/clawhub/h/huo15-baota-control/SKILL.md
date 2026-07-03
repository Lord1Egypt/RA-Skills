---
name: huo15-baota-control
displayName: 宝塔服务器控制
description: >-
  用宝塔(BT-Panel)HTTP API 操控火一五的服务器——查系统状态/内存/磁盘/负载、管网站
  (停站/启站/重载)、数据库、SSL 证书、计划任务、Docker，以及调用任意宝塔接口。
  当用户说"看下 xx 服务器状态/负载/磁盘""重启/停掉某网站""宝塔面板""续证书"
  "列计划任务""管一下服务器""bt panel"等运维意图时使用。支持多面板。
  凭据在 ~/.huo15/baota.json，脚本 scripts/bt_api.py。
---

# 宝塔面板控制 (huo15-baota-control)

用宝塔 HTTP API 远程操控服务器。脚本 `scripts/bt_api.py`（零依赖，标准库）。

## 配置（凭据，不入库）
`~/.huo15/baota.json`：
```json
{ "panels": [ { "name": "gjb-ssh", "desc": "...", "url": "https://gjbserver.huo15.com", "token": "<明文token>" } ] }
```
- `token` = 宝塔「面板设置→API接口」里的接口密钥（明文）。多台服务器就多个 panel 对象。
- 默认用第一个 panel；`--panel <name>` 指定某台。

## 常用命令
```bash
# 系统总览（CPU/内存/负载/磁盘）
python3 scripts/bt_api.py sysinfo [--panel gjb-ssh]
python3 scripts/bt_api.py disk
python3 scripts/bt_api.py network
# 网站
python3 scripts/bt_api.py sites
python3 scripts/bt_api.py site_stop  --id <ID> --name <域名>
python3 scripts/bt_api.py site_start --id <ID> --name <域名>
# 数据库
python3 scripts/bt_api.py databases
# 任意接口（最万能）—— 端口/动作见 references/endpoints.md
python3 scripts/bt_api.py raw --endpoint "/crontab?action=GetCrontab" --params '{}'
python3 scripts/bt_api.py raw --endpoint "/system?action=GetTaskCount" --params '{}'
```

## 触发后的做法
1. 用户提运维意图 → 选对 panel → 跑只读命令（sysinfo/sites/...）先汇报现状。
2. 涉及**写操作**（停站/删库/改配置/续证书）→ 先确认目标，再用对应命令或 `raw`。
3. 结果是 JSON，挑关键字段用中文转述，别把整坨 JSON 丢给用户。

## 重要前提 / 注意
- 宝塔有反扫描：脚本已带浏览器 UA（必需，否则返回伪装 404）。
- API 必须在面板里「开启」且把调用方 IP 加白名单；经 `gjbserver.huo15.com` 隧道访问时宝塔看到的源 IP 是 `127.0.0.1`（隧道 localIP），所以白名单含 `127.0.0.1` 即可远程调用。
- **token 是唯一防线**（隧道公网可达），务必保密；泄露即轮换（面板→重新生成 Token，或 `scripts/enable_api.py` 重跑）。
- 任意 shell 命令宝塔 API 不直接给（安全限制）→ 需要跑命令走 SSH，不走本 skill。

详见 [references/endpoints.md](references/endpoints.md) 与 [README.md](README.md)（API 鉴权原理 + 如何开启）。
