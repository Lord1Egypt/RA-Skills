# IP Intelligence Fusion

[English](README.md) | [简体中文](README.zh-CN.md)

[![版本](https://img.shields.io/badge/version-2.0.0-0969da)](scripts/ip_intelligence.py)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab)](https://www.python.org/)
[![许可证](https://img.shields.io/badge/license-MIT-2da44e)](LICENSE)

这是一个面向单个公网 IPv4 或 IPv6 的多源 IP 情报工具。它将注册信息、路由、地理区域、网络
类型和信誉证据规范化，生成本地 JSON、Markdown 或自包含 HTML 报告。

本项目是调查辅助工具，不是自动放行/封禁、身份识别、位置证明或平台审核工具。MIT 许可证不构成
法律意见，也不保证在中国或其他法域、服务商条款和组织制度下自动合规。发布或使用前请阅读
[COMPLIANCE.md](COMPLIANCE.md)。

## 适用范围

支持的场景仅包括：

- 核查操作者自有的服务器、网络资产和公网 IP；
- 核验服务商或注册机构已经公开的信息；
- 已获授权的安全运维和异常请求排查；
- 在获得授权的前提下验收代理或网络供应商交付的资源。

v2.0 公开接口严格接受一个公网 IP，不接受客户登录日志、账号日志、Cookie、设备标识、设备指纹
或批量 IP 数据集。

以下用途被项目文档和运行政策明确禁止：

- 未授权调查或画像个人、客户、员工或账号；
- 批量收集个人 IP，或把 IP 与身份、账号、客户或员工记录关联；
- 伪造地理位置、账号养号、批量注册或规避平台审核；
- 绕过 CAPTCHA、登录限制、访问控制或服务商限制；
- 端口扫描、漏洞利用、攻击或代理转发。

IP 在与个人、账号、客户、员工或登录记录关联后可能属于个人信息。使用者应在运行前自行确认
授权、必要的告知和处理依据、留存期限，以及服务商合同和数据出境要求。

## 安全默认值

- 默认模式是 `local-only`：只校验输入 IP、读取本地证据并生成报告，不产生网络请求。
- 远程查询必须显式使用 `--external`。交互终端始终显示确认提示；非交互运行还必须提供
  `--confirm-external`。
- 确认提示会显示目标 IP、选中的服务商、允许的域名和可能的跨境传输。该确认只用于操作审计，
  不等于法律授权证明。
- 默认 profile 是 `fast`，需要完整来源时必须显式选择 `comprehensive`。
- 所有请求只能访问审核过的 HTTPS 域名；重定向、用户信息、非标准端口和带凭据查询参数都会被拒绝。
- 报告不保留上游原始响应、联系人、邮箱和个性化 hostname。支持的 API 凭据只通过请求头发送。

## 环境要求

- Python 3.9 或更高版本
- 只使用 Python 标准库
- 只有在明确使用 `--external` 时才需要网络权限

## 快速开始

校验一个 IP 并输出本地 JSON 报告。该命令不会联系任何服务商：

```bash
python scripts/ip_intelligence.py 8.8.8.8 --format json
```

在 `reports/` 生成本地 JSON 和离线 HTML：

```bash
python scripts/ip_intelligence.py 8.8.8.8
```

导入仓库中的合成公开页测试夹具。证据文件只在本地读取，CLI 不会替你抓取页面：

```bash
python scripts/ip_intelligence.py 8.8.8.8 \
  --evidence tests/fixtures/public-page-evidence-8.8.8.8.json \
  --format markdown
```

在阅读确认提示后启用外部查询：

```bash
python scripts/ip_intelligence.py 8.8.8.8 --external --profile fast
```

在计划任务或管道中运行时：

```bash
python scripts/ip_intelligence.py 8.8.8.8 \
  --external --confirm-external --profile fast --format json
```

查询本机当前公网 IP 同样必须同时使用两个选项，确认前不会访问 IP 发现服务：

```bash
python scripts/ip_intelligence.py --self --external --confirm-external --format json
```

可用 `--providers` 或 `--exclude` 缩小范围。只有在确有必要且已评估额外传输时才使用
`--profile comprehensive`。v2.0 已移除 `--include-raw`，该参数会被识别为不支持的选项。

## 服务商和传输边界

下表是 v2.0 CLI 唯一允许的请求域名。每次请求使用 HTTPS，最终响应地址也必须继续位于允许域名内。

| 服务商 | 允许域名 | v2.0 采集方式 |
|---|---|---|
| GeoJS | `get.geojs.io` | 免密钥 API |
| RDAP | `rdap.org`、`rdap-bootstrap.arin.net` | 注册信息 API |
| RIPEstat | `stat.ripe.net` | 路由 API |
| ipapi.is | `api.ipapi.is` | 免密钥 API |
| proxycheck.io | `proxycheck.io` | 免密钥 API |
| Ping0.cc | `ping0.cc`、`www.ping0.cc`、`ip.ping0.cc` | 实验性公开页面适配器 |
| IPinfo | `api.ipinfo.io` | 请求头令牌 API；公开页证据需本地导入 |
| AbuseIPDB | `api.abuseipdb.com` | 请求头 API 密钥 |
| IPQualityScore | `ipqualityscore.com`、`www.ipqualityscore.com` | 仅允许公开页证据 |
| Scamalytics | `scamalytics.com`、`www.scamalytics.com` | 仅允许公开页证据 |
| ipdata | `ipdata.co`、`www.ipdata.co` | 仅允许公开页证据 |
| `--self` 地址发现 | `api64.ipify.org` | 仅在确认后访问 |

旧 IP-API 明文 HTTP 适配器已经删除。IPQualityScore、Scamalytics 和 ipdata 的 API 适配器也已禁用，
因为旧集成需要把凭据放在 URL 路径、查询参数或任意自定义端点中。公开页证据必须来自官方页面、
精确匹配目标 IP，并且只包含允许字段。不得登录、提交表单、处理 CAPTCHA 或绕过访问控制获取证据。

## 凭据

CLI 不会索要凭据。只有操作者已经独立配置且确认条款的服务商才会使用以下变量：

| 服务商 | 环境变量 | 传输方式 |
|---|---|---|
| IPinfo | `IPINFO_TOKEN` | `Authorization: Bearer ...` 请求头 |
| AbuseIPDB | `ABUSEIPDB_API_KEY` | `Key` 请求头 |

不得把密钥放入命令参数、证据文件、URL、报告、日志或 Issue 附件。服务商的处理地点、留存期限、
跨境传输和服务条款必须由使用者逐项核查。

## 报告和数据处理

报告包含完整目标 IP，可能包含地理区域、组织/ISP、分配或路由前缀以及网络风险标签。报告元数据
会包含：

```json
{
  "policy": {
    "network_mode": "local-only",
    "confirmation_mode": null,
    "sent_fields": [],
    "policy_version": "2.0"
  },
  "data_policy": {
    "accepted_input": "single public IP",
    "personal_data_mode": "not intended for customer or account logs",
    "raw_payloads": false,
    "contact_data": false
  }
}
```

外部模式会记录 `external-confirmed` 以及实际开始请求的服务商域名。应设置合适的文件权限，不要把
报告提交到公开 Issue、演示站点或公共日志系统，并按组织留存期限及时删除。

## 从 1.4.x 迁移

v2.0 是一次破坏性版本升级：

- 默认命令不再联网；
- 远程访问必须使用 `--external` 并明确确认；
- 默认 profile 改为 `fast`，`comprehensive` 改为显式选项；
- 原始响应输出和 `--include-raw` 被移除；
- IP-API 明文适配器被移除；
- 旧的凭据放入 URL 的适配器被禁用；
- 报告 schema 和 CLI 版本更新为 `2.0` 和 `2.0.0`；
- 旧 ZIP 和打包目录不属于正式发布物。

## 开发与发布检查

```bash
py -3 -m unittest discover -s tests -v
py -3 -m py_compile scripts/ip_intelligence.py tests/test_ip_intelligence.py
py -3 scripts/release_audit.py
```

发布包只应包含经过审计的源码、文档、测试和许可证。不要提交压缩包、缓存、生成报告、真实查询
结果、原始响应或密钥。

## 许可证

本项目使用 [MIT License](LICENSE)。许可证不构成法律意见或合规保证。
