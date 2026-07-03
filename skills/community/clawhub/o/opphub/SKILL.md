---
name: opphub
description: 偶合 OppHub OPC 客户端 · 撮合 + 能力交换 · OPC 注册 / 通道绑定 / 商机 / 撮合匹配
version: 1.0.16
author: opphub-dev
license: MIT-0
homepage: https://api.opphub.ruiplus.cn
metadata:
  emoji: 🤝
  audience: 公开 OPC（人人可装）
  categories: [business, productivity, productivity-automation]
  topics: [opc, one-person-company, matchmaking, capability-exchange, ai-startup, solopreneur]
  openclaw:
    skillKey: opphub
    requires:
      bins: []
      env: []
      config: []
    os: [macos, linux]
---

# 偶合 OppHub · 公开 OPC Skill

> 撮合 + 能力交换 · 公开 OPC · 5 通道独立通知 · 邮箱 / 手机号注册。

## 这是什么

**偶合 OppHub** 是一个面向 OPC（一人公司 / AI 创业者）的撮合 + 能力交换平台，本 skill 是接入偶合平台的 OPC 客户端封装。

撮合引擎 + 能力交换市场 + 5 通道 IM 通知推送。

## 安装

```bash
clawhub install opphub
```

## Quick Start

> **命令前缀说明**：本 skill 装好后，`opphub` 命令会在 PATH 里。
> - 如果你的环境能直接调 `opphub`，**用简写** `opphub status`
> - 如果你的环境只能调 `clawhub`（某些受控设备），**用完整命令** `clawhub opphub status`
> - 两种调用方式走同一个脚本，参数完全一样

```bash
opphub status        # 看当前账号绑定状态
opphub check-update  # 检查 skill 自身更新
opphub update        # 拉取最新版本
opphub version       # 看当前 skill 版本
```

`opphub status` 是 first run 入口。已绑定就告诉用户偶合能干什么，未绑定就引导走 `opphub register`。

## 注册

`opphub register` 启动 6 步交互式引导（3-6 可选跳过）：

1. **邮箱/手机号注册** —— `POST /api/auth/code/send` 发验证码 → `POST /api/auth/register` 建账号
   - **首次可选设密码**：注册完成会问"是否设置登录密码"（8-32 位）
   - 设了 → 后续 `opphub login` 可用密码或验证码
   - 不设 → 只能用验证码登录（后续 `opphub passwd` 可补设）
2. **IM 通道绑定**（至少 1 个）—— 当前可用: email / feishu
3. **手机号 KYC**（可选 +10 信用分）
4. **1 句话开店** —— `POST /api/profile/parse` 调 BGE-M3 抽取 7 维度（mock）
5. **完善公司卡片 + 能力卡片**
6. **完成引导** —— state.status=READY

**前置**：

- `OPPHUB_HOME` 自动解析（1.0.13 起支持多环境）：
  - 显式 `OPPHUB_HOME` → 1
  - `XDG_STATE_HOME/opphub` → 2（XDG）
  - `OPPHUB_DATA_DIR` → 3（容器/K8s 专用）
  - `~/.opphub` → 4（默认）
  - `/tmp/opphub-$UID` → 5（无 HOME 兜底）
- 调试：`export OPPHUB_DEBUG=1` 看实际解析路径
- state 存 `$OPPHUB_HOME/state.json`（权限 0600），不是 `agent.json`

## 两种登录方式

### 验证码登录（主路径，推荐）

```bash
opphub login
# → 邮箱/手机号
# → 选「1) 验证码登录」
# → 6 位码 → JWT(30 天)
```

场景：日常、临时、新设备。

### 密码登录（兜底）

```bash
opphub login
# → 邮箱/手机号
# → 选「2) 密码登录」
# → 8-32 位密码 → JWT(30 天)
```

场景：验证码收不到、自动化脚本、海外手机号。

## Session 管理（jti 黑名单）

`opphubToken` 是 JWT（30 天过期），含 `jti`（JWT ID）存 Redis。

- `opphub logout` 注销当前 jti，后续请求报「已注销」
- 新设备登录顶掉旧设备的 `active_jti`（防多端刷）
- `state.json` 同时存 `opphubToken` + `jti`，方便 logout

## 核心命令

> 所有 `opphub <cmd>` 命令都同时支持完整写法 `clawhub opphub <cmd>`（受 clawhub 管控的设备）。两者调用同一个脚本。

```bash
# 账号
opphub register      # OPC 注册 + 引导
opphub login         # 登录
opphub logout        # 登出
opphub passwd        # 改密码

# 通道管理（5 通道独立：feishu / dingtalk / wecom / sms / email）
opphub channel list    # 列已绑通道
opphub channel add     # 添加通道
opphub channel remove  # 删通道

# 业务（撮合 + 能力交换）
opphub profile         # 个人 / 公司 / 能力 profile
opphub opportunities   # 需求池 / 商机
opphub suppliers       # 推荐供应商 / 能力方
opphub matches         # 撮合引擎（需求 ↔ 能力）

# IM 推送
opphub notify          # 看推送历史 / 配置

# 状态
opphub status          # 当前状态
```

## 5 通道 IM 通知

5 个 IM 通知通道（feishu / dingtalk / wecom / sms / email）**可选**绑定，独立增删，互不影响。通道是**通知手段**，不是身份手段 —— 卸了 IM 客户端账号还在。

## 错误码

| 错误码 | 处理 |
|--------|------|
| `missing_agent_token` | 跑 `status`，引导重新注册 |
| `invalid_agent_token` / `expired_agent_token` | 同上 |
| `quota_exceeded` | 告诉用户今日配额用完 |
| `invalid_code` / `expired_code` | 重新走注册流程 |
| `rate_limited` | 提示等待再试 |

## 安全报告

如发现 skill 存在安全问题，请通过 GitHub Security Advisories 私下提：

- https://github.com/mtty123456/opphub/security/advisories/new

## 反馈

- ⭐ ClawHub star：https://clawhub.ai/mtty123456/skills/opphub
- 🐛 Issue：https://github.com/mtty123456/opphub/issues
- 💬 偶合官方渠道

## 许可证

MIT-0。任何人都可商用，无需署名。
