---
name: ikuai-report
description: "从 iKuai 路由器的 ikuai-cli JSON 数据生成可视化 HTML 流量报表（5 标签页、Chart.js 动画图表）。触发词：生成/创建/构建 iKuai HTML 报表、爱快流量报表、ikuai report、ikuai-traffic-report"
---

# iKuai 流量报表

生成可视化 HTML 流量报表，纯静态、无外部依赖，直接用浏览器打开。

**输出路径**: `/tmp/ikuai-report.html`

## 快速使用

```bash
python3 {{SKILL_DIR}}/scripts/generate_report.py
open /tmp/ikuai-report.html
```

## 首次使用：配置 ikuai-cli Auth

每个用户的路由器 IP/Token 不同，**启动脚本会自动检测**，若未配置会报错并提示：

```bash
# 1. 设置路由器地址
ikuai-cli auth set-url http://<路由器IP>
# 例如: ikuai-cli auth set-url http://10.10.10.253

# 2. 设置认证 Token（在路由器 Web UI → 系统状态 → API Token 获取）
ikuai-cli auth set-token <你的token>

# 3. 验证配置
ikuai-cli auth status
```

> **提示**：脚本会自动搜索 PATH 中的 `ikuai-cli`，找不到时回退到 `~/.local/bin/ikuai-cli`，无需硬编码路径。

## 报表结构（5 标签页）

| 标签 | 内容 |
|------|------|
| 总览 | 系统状态 + 资源 + 流量 + 网口 + 图表 |
| 网络配置 | WAN/LAN/DNS/NAT/端口转发/VLAN |
| 流量分析 | 协议柱图 + 应用 Top20 + 设备 Top20 |
| 安全状态 | ACL/L7/MAC + VPN + 在线设备 |
| 系统日志 | 关键事件日志 |

## 数据收集命令

```bash
ikuai-cli monitor system --format json
ikuai-cli monitor traffic-summary --format json
ikuai-cli monitor app-traffic-summary --format json
ikuai-cli monitor protocols --format json
ikuai-cli monitor clients-online --format json
ikuai-cli monitor interfaces-physical --format json
ikuai-cli network wan --format json
ikuai-cli network lan list --format json
ikuai-cli network dns get --format json
ikuai-cli security acl list --format json
ikuai-cli qos ip list --format json
ikuai-cli network dnat list --format json
ikuai-cli log system list --format json --human-time
```

## 关键 API 字段（实际返回值，与文档常有不符）

| 命令 | 字段 | 说明 |
|------|------|------|
| `monitor system` | `sysinfo.stream.total_down/up` | 今日总流量（Bytes） |
| | `sysinfo.online_user.count` | 在线用户数 |
| `monitor traffic-summary` | `terminal[].ip_addr / mac / sum_total_down / sum_total` | 设备流量 |
| | `terminal_total_flow` | 所有设备总流量 |
| `monitor app-traffic-summary` | `proto3_day[].appname` | 应用名（⚠️ 不是 `app_name`） |
| | `proto3_day[].total_down/up/total` | 流量（⚠️ 不是 `total_byte`） |
| `monitor protocols` | `data[].proto_name / total` | 协议分布 |
| `monitor clients-online` | `data[].ip_addr / client_vendor / client_type` | 在线设备 |
| `network wan` | `data[].dhcp_ip_addr / internet` | WAN 状态 |
| `network lan list` | `data[].ip_mask / dhcp_server / vlan` | LAN 配置 |
| `network dnat list` | `data[].wan_port / lan_addr / lan_port` | 端口转发规则 |

## 故障排查

**"ikuai-cli 未完成认证配置"**

```bash
ikuai-cli auth status        # 查看当前配置状态
ikuai-cli auth set-url <IP>  # 设置路由器地址
ikuai-cli auth set-token <token>  # 设置 Token
```

**API 返回空数据（`{"data":[]}`）**

- 路由器不可达 — `ping <路由器IP>`
- Token 过期 — 重新获取并 `ikuai-cli auth set-token <新token>`

**图表无数据或 Tab 切换失效**

- 用 `node --check /tmp/ikuai-report.html` 验证 JS 语法
- 确认 `ikuai-cli monitor app-traffic-summary` 有返回数据

## 依赖

- `ikuai-cli` v1.0+（自动检测 PATH）
- Python 3.6+
- 报表：纯静态 HTML + Chart.js（CDN）
