# 偶合 OppHub · OpenClaw Skill

> 公开 OPC（一人公司 / AI 创业者）的撮合 + 能力交换统一入口。
> **账号独立、5 个 IM 通知通道可选绑定** —— 注册用邮箱 / 手机号。

[![ClawHub](https://img.shields.io/badge/ClawHub-opphub-blue)](https://clawhub.ai/mtty123456/skills/opphub)
![Version](https://img.shields.io/badge/version-1.0.10-blue)
![License](https://img.shields.io/badge/license-MIT--0-green)

## 这是什么

**偶合 OppHub** 是一个面向 OPC 的撮合 + 能力交换平台，本 skill 是接入偶合平台的 OPC 客户端封装。

撮合引擎 + 能力交换市场 + 5 通道 IM 通知推送。

## 30 秒决定装不装

| 问 | 答 |
|----|----|
| 这是什么？| 偶合平台的 OPC 客户端封装 |
| 谁维护？| ClawHub owner `mtty123456` |
| 安全吗？| ClawHub 自动安全扫描 + VirusTotal 通过 |
| 能商用吗？| 可以。MIT-0，无需署名 |
| 我的数据去哪？| 仅去偶合后端。本 skill **不上传任何本地文件、不读 IM 通讯录** |
| 源码在哪？| https://github.com/mtty123456/opphub |

## 它能做什么

- **OPC 能力库**：个人 / 公司 / 能力 profile 上传与查询
- **需求池**：商机发布与订阅
- **撮合引擎**：需求 ↔ 能力 的双向匹配
- **IM 推送**：5 通道独立绑定（feishu / dingtalk / wecom / sms / email）
- **简单后台**：注册 / 登录 / 通道管理 / profile / 商机

## 安装

### 方式 1：ClawHub 商店

```bash
clawhub install opphub
```

## 命令速查

```bash
# 账号
opphub register      # OPC 注册 + 引导
opphub login / logout / passwd

# 通道（5 通道独立）
opphub channel list / add / remove

# 业务
opphub profile
opphub opportunities
opphub suppliers
opphub matches

# 推送
opphub notify

# 元
opphub status / version / check-update / update
```

## 安全披露

发现问题请用 GitHub Security Advisories 私下提：

- https://github.com/mtty123456/opphub/security/advisories/new

## 反馈

- ⭐ ClawHub star：https://clawhub.ai/mtty123456/skills/opphub
- 🐛 Issue：https://github.com/mtty123456/opphub/issues
- 💬 偶合官方渠道

## 许可证

MIT-0。可商用，无需署名。
