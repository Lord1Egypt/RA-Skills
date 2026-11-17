---
name: hawkeye-lead-skill
description: |
  鹰眼线索池（merchant_lead）运营技能，封装线索池 10 个 Hawkeye 后台 HTTP 接口，
  支持查看私海/公海线索列表与统计、查看线索详情、认领/分配线索、更新跟进状态/备注/采纳优先级。
  触发词：线索池、私海线索、公海线索、认领线索、分配线索、跟进状态、线索备注、采纳优先级、鹰眼线索、merchant_lead。
  当前仅部署在测试泳道（线索项目尚未合并到 master），正式环境域名待项目上线后启用。
---

# 鹰眼线索池 Agent Skill

通过本目录下的零依赖本地 CLI（`bin/cli.js`，仅用 Node 内置 `fetch`）调用鹰眼后台的线索管理接口。10 个接口一一对应 10 个独立子命令，**每个子命令都自带 `--schema`（JSON Schema）和 `--help`（人类可读说明），字段/取值范围现查即可**，不需要预读本文档。这份文档只写 CLI 自省拿不到的东西：认证怎么配、怎么发现命令、写操作的安全规则。

## 环境准备

无需 `npm install`，Node >= 18 即可直接运行：

```bash
node <本 skill 目录>/bin/cli.js <子命令> ...
```

以下示例统一用 `hawkeye-lead-cli` 代指这行命令。

## 认证设置

**根因已经跟接口负责人确认**：这 10 个 `merchant_lead` 接口在 edith 网关层挂载了一个专门的 SSO 插件，必须装这个插件，网关才能把用户的登录信息解析出来、透传给后端 RPC 服务（RPC 层自己不做任何鉴权，完全信任网关注入的身份）。像 `butterfly/data/require`、`opportunity/search_opportunity_shop` 这类零 cookie 也能访问的接口，就是因为网关上**没有**挂这个插件，压根不检查登录态，跟"稳不稳定"没关系。

**目前实测确认**：codewiz/seal/OpenClaw 这类 agent 环境自带的免登录 ambient token（`~/.token/sso_token.json` 里的 `common-internal-access-token-<tier>`）在这个插件面前不生效，必须用真实浏览器登录该域名后拿到的、专门针对这个域名签发的 cookie 值。这个 ambient token 在上线到正式域名后是否会被这个插件认可，**还没有实测确认**，不能想当然认为上线后就自动免登录了。

测试阶段如果遇到鉴权失败，需要开发/测试人员手动执行一次：

```bash
hawkeye-lead-cli auth set-token <token>
```

`<token>` 是从浏览器登录鹰眼测试泳道后，DevTools → Application → Cookies 里 `access-token-<当前域名>` 这一行的值。这一步只在测试阶段、由懂技术的人做一次。

**查看当前认证状态**：`hawkeye-lead-cli auth status`（显示 token 来源，只展示脱敏后的值）。

## 怎么用

```bash
hawkeye-lead-cli commands                    # 1. 看有哪些子命令（path/method/mutating/verified/summary）
hawkeye-lead-cli <子命令> --help             # 2. 看这个命令怎么传参、有什么业务警示（人类可读）
hawkeye-lead-cli <子命令> --schema           # 2'. 同上，机器可读版（标准 JSON Schema，响应含嵌套 $defs）
hawkeye-lead-cli <子命令> [--flag value ...] # 3. 调用：flag 由 schema 的 snake_case 字段名转 kebab-case
```

- 数组字段用可重复 flag：`list-private-leads --industries 美妆 --industries 3C`
- 布尔字段传了 flag 本身就是 true（如 `--plain-phone`），不传视为 false/默认值
- 必填字段缺失、或值不在 `enum` 范围内，CLI 会在本地直接报错（退出码 1），不会真的发请求
- `--dry-run`：只打印会发出的 method/url/body（token 脱敏），不真正发请求
- `--confirm`：调用 5 个"写"命令（`claim-lead`/`assign-lead`/`update-follow-status`/`update-remark`/`update-accept-level`）必须加，否则拒绝执行

## 高风险操作确认规则

5 个写命令会真实修改线索状态，且没有对应的"撤销"接口（尤其 `claim-lead`）。**在加 `--confirm` 真正执行之前，必须把要发送的请求体内容原样展示给用户，拿到明确同意后才能执行**——不加 `--confirm` 直接调用时，CLI 的报错信息里已经带上了拼好的请求体，方便先给用户看。这条规则不因为"当前只是测试泳道"而放松：实测确认测试泳道里是真实业务数据（公海线索 2 万+ 条），应按等同于生产数据的谨慎程度对待。

## 退出码

| 退出码 | 含义 | agent 应对方式 |
| --- | --- | --- |
| 0 | 成功 | 正常处理返回的 JSON |
| 1 | 用法错误（子命令/flag 不对、必填参数缺失、枚举值不合法、写命令缺 `--confirm`） | 修正参数后重试，不需要找用户 |
| 2 | 鉴权失效（未设置 token 或 token 已过期） | 把报错原文转达给用户，引导走"认证设置"里的流程重新获取，不要自动重试 |
| 3 | 上游业务错误（非鉴权类的 4xx/5xx 或业务报错） | 把报错内容转达给用户，判断是参数问题还是业务本身拒绝 |
| 4 | 网络错误（DNS/连接失败/超时） | 测试泳道域名是他人分支的临时环境，可能会变化或下线，提示用户确认域名是否还有效 |

已实测过的鉴权失效响应样本：`HTTP 401 {"code":-100,"success":false,"msg":"无登录信息","data":{}}`。

## 环境切换

当前只有一套环境（`hawkeye-luren33.devops.sl.beta.xiaohongshu.com`，配置在 `lib/config.js`）。如果测试泳道域名变了，或者线索项目已经合并上线切到正式域名，可以用环境变量覆盖，不用改代码：

```bash
HAWKEYE_LEAD_DOMAIN=hawkeye.devops.xiaohongshu.com hawkeye-lead-cli list-private-leads --page-num 1
```

切到正式域名后，`lib/config.js` 里的 `AMBIENT_SSO_TIER` 会自动判定成 `prod`，届时"认证设置"里的自带登录态兜底大概率就会自动生效。如果鉴权失效但确认 token 本身没过期，可以用 `HAWKEYE_LEAD_COOKIE_NAME` 环境变量覆盖 cookie 名。
