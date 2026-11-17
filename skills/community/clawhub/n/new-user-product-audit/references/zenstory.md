# ZenStory 运行须知

本文件是**运行须知，开跑前读**：只包含环境、访问方式、账号与安全边界，不剧透产品怎么用。
产品事实（定位、项目类型、工作区、套餐额度、刻意的产品决定、术语表）在
[zenstory-facts.md](zenstory-facts.md)，**首轮体验结束后才读**。

## 环境

| 环境 | 官网 | 应用 | 说明 |
|---|---|---|---|
| production | `https://zenstory.ai` | `https://app.zenstory.ai` | 真实用户在用；**需要操作者明确授权** |
| staging | — | `https://app-preview.zenstory.ai` | 受 Vercel Deployment Protection 保护 |

`zenstory.ai` 是组织官网（同时介绍开源写作工具），从那里链到应用；应用根地址本身也有一个
未登录首页。到达阶段两条入口都走：先从 `zenstory.ai` 点进应用（看官网对应用的介绍与跳转是否
顺），再单独看应用未登录首页的五秒测试。staging 没有对应官网，只看应用首页，并在报告里注明。

## 访问 staging（Vercel 保护）

直接打开会落到 Vercel 登录/保护页。两种方式，**都不要把令牌打印、写进日志或截图**：

- HTTP 请求（健康检查、看接口响应）：用 `vercel curl` 代替 `curl`。
- 浏览器：用 `vercel env run` 注入短期 OIDC 令牌，作为按源限定的请求头带上：

```bash
# 在 zenstory 仓库的 apps/web 目录执行（已 link 到 web 的 Vercel 项目；没 link 先 `vc link`）
vc env run -- sh -c \
  'test -n "$VERCEL_OIDC_TOKEN" && agent-browser --session "$2" open "$1" \
     --headers "{\"x-vercel-trusted-oidc-idp-token\":\"$VERCEL_OIDC_TOKEN\"}"' \
  sh https://app-preview.zenstory.ai novelist          # 末尾是 persona 短名
```

之后每条命令都带同一个 `--session <persona>` 继续操作（访问头只对该源生效）。请求头名必须是
`x-vercel-trusted-oidc-idp-token`，不要换成 `x-vercel-oidc-token`。令牌过期（又落到保护页）就重新执行上面这条。

## 账号

- production：用一次性邮箱真实注册（见 [disposable-inbox.md](disposable-inbox.md)）。注册页若出现
  邀请码字段，记录它是否可选、说明是否清楚，不要向任何人索要邀请码。
- staging：可用操作者提供的预验证测试账号文件（通常在运行目录之外、权限 0600）；用它时
  报告里把「注册与验证」标为未覆盖。
- 昵称 `audit-<persona>-<YYYYMMDD>`，项目名加 `[audit]` 前缀。

## 安全边界（本产品特有）

- 支付页：**任何情况都不扫码、不付款**；看到支付页即停，记录到这一步为止的体验。
- 免费额度按北京时间自然日计算；一个 persona 用完当天额度就停，不要换号绕过额度来“多测一点”
  （除非操作者要求测多账号场景）。
- 不在「反馈 / 联系我们 / 客服邮箱」里发测试内容。
- 结束时删除测试项目，或保留并在报告附录里列出项目名。
