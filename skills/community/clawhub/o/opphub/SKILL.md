---
name: opphub
version: 5.0.0
description: 偶合 OppHub - 把偶合账号接入 OpenClaw，录入公司、查商机、收推送。
author: mtty-ai
homepage: https://github.com/mtty-ai/opphub-skill
entry: bin/opphub
defaultLocale: zh-CN
requires:
  bins:
    - node>=18
    - openclaw
    - jq
    - curl
    - security
    - openssl
    - xdg-open
  env: []
  platform:
    darwin: full
    linux: full
    windows: none
metadata:
  api: https://api.opphub.ruiplus.cn
  deviceFlow:
    authorize: https://api.opphub.ruiplus.cn/api/oauth/device/code
    token: https://api.opphub.ruiplus.cn/api/oauth/device/token
    userinfo: https://api.opphub.ruiplus.cn/api/oauth/userinfo
  refreshToken:
    endpoint: https://api.opphub.ruiplus.cn/api/oauth/token
  client_id: opphub-plugin
  scope: profile ws:read ws:write
---

# 偶合 OppHub

把偶合账号接入 OpenClaw，录入公司、查商机、收推送。

支持 3 种触发方式：
- IM 群聊 / 私聊 @bot（飞书 / 微信 / 钉钉 / Telegram 等）
- OpenClaw 后台直接调用
- cron 定时任务

具体 IM 取决于 OpenClaw runtime 已装的 channel plugin。

---

## 一句话介绍

录入公司、查商机、收推送，3 件事 bot 都替你跑。

---

## 安装

```bash
openclaw skills install @mtty-ai/opphub
openclaw plugins install clawhub:@mtty-ai/opphub
```

两条都要装：

- `opphub` skill：在 IM 里跟 bot 对话
- `opphub` plugin：装好后 bot 收得到推送，登录态写 macOS Keychain

装完自动重启 gateway。

依赖 runtime 自动校验，不缺。

---

## 五步上手

### 1. 注册偶合账号

去 <https://api.opphub.ruiplus.cn/register>，邮箱/手机号 + 6 位验证码。

### 2. 验证 plugin 装好

```bash
opphub plugin-check --json
```

返 `installed: true` 就 OK。没装好跑 `openclaw plugins install clawhub:@mtty-ai/opphub` 重装。

### 3. @bot 说"偶合登录"

bot 走 OAuth device flow：
- bot 私聊发你激活链接（不会在群里贴验证码）
- 你打开链接点同意
- 登录态自动写 Keychain，下次不用再登

### 4. @bot 说"偶合配置"

bot 列出你本机已装的 IM 通道（飞书/微信/钉钉/Telegram 等），你选一个作**默认推送通道**。后续商机推送、cron 提醒都走这个通道。

跳过这步也行——bot 会用 server 端上次选的通道；不放心就先跑一次确认。

### 5. @bot 说"偶合录入 [公司名]"

bot 自动 6 步跑完，只问你一次"是否入库"：

- 联网查工商 / 业务 / 招聘 / 项目
- 推断行业（MCN / SaaS / 律所 / 制造）
- 拆能力卡片 + 上下游
- 给你 1 张清单确认
- 批量入库（幂等，重复跑不冲突）
- 跑上下游匹配，列结果

> 第 4 步拆出能力后, bot **不直接入库**, 先给一张确认清单 (含 4 种 entryType: 我能提供/我想找/我的依赖/同行关系).
> 用户回复:
> - 「确认」 → bot 调 `knowledge-submit --confirm` 入库
> - 「删 <type.dimension>」 → bot 去掉某条重发清单
> - 「重抽」 → 回到阶段 1 重新联网查
> - 「改 <字段>」 → 改解析字段后重发清单

---

## 常用命令

| 触发方式 | bot 做的 |
|---|---|
| 偶合登录 | OAuth 登录 |
| 偶合状态 | 看登录态 + 推送通道 + 知识库 |
| 偶合配置 | 选默认推送通道 |
| 偶合录入 [公司] | 录入公司能力画像 |
| 偶合录入关联公司 + 合同 xls | 解析合同拆上下游 |

**触发方式**：群里 @bot、私聊 bot、OpenClaw 后台调用、cron 定时都可以。

---

## 常见问题

**没收到推送？**
确认 plugin 装好：`opphub plugin-check --json`。没装就跑 `openclaw plugins install clawhub:@mtty-ai/opphub`。

**token 过期了？**
@bot 说"偶合登录"重新走一遍。

**浏览器没弹？**
复制 bot 私聊里的链接手动打开。

**录入撞同行业了？**
bot 会弹卡片让你选行业。

**录入冲突了？**
bot 会列新旧版本让你选保留哪个。

---

## 卸载

```bash
openclaw plugins uninstall clawhub:@mtty-ai/opphub
openclaw skills uninstall @mtty-ai/opphub
```

Keychain 里的登录态要手动清：macOS Keychain 搜 `opphub:default` 删除。

---

## 反馈

issue: https://github.com/mtty-ai/opphub-skill/issues