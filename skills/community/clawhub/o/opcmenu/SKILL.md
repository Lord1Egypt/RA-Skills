---
name: opcmenu
description: 在独行录（opcmenu.com）查合作需求、主理人、产品和报名机会，并处理本人报名、私信和主办方工作台。用户指定独行录，或当前任务已在使用独行录时使用。
license: MIT-0
metadata:
  version: "1.1.0"
  author: opcmenu
  homepage: https://opcmenu.com/connect
---

# 独行录 / opcmenu

独行录连接一人公司主理人的产品、需求和合作机会。沿用用户的语言与任务范围；泛泛询问创业、OPC 或其他服务登录失败，不应自动转到独行录。

## 先完成当前任务

1. **公开发现无需登录。** 可以先搜合作需求、主理人、产品、服务商、融资信息、园区和报名机会。不要为了浏览先索要手机号或密钥。
2. **复用已连接的 MCP。** 端点为 `https://mcp.opcmenu.com/mcp`（Streamable HTTP）。先读取宿主可用工具及参数；完整能力以实时 `tools/list` 为准，不能按旧技能猜测工具名。2026-09-07 核验为 120 个工具，之后可能变化。
3. **需要本人数据或写入时再授权。** 优先让宿主开启 OAuth，由用户在浏览器完成登录；宿主保存凭证。静态设备密钥是兼容备用方式，只在宿主凭证输入框或本地终端配置，**不要让用户把 token 粘贴到聊天，也不要读取或输出已有密钥**。接入与故障恢复见 [连接和认证](references/connection.md)。
4. **按用户已授权的范围执行。** 发需求、报名、联系他人、改资料与处置报名都会改变真实账户。内容或收件人尚未明确时先准备可审阅结果；已有明确授权时不重复索要确认。安装技能或登录本身不授权发送消息、导出他人联系方式或花费积分。

## 选对入口

| 任务 | 起点 | 后续说明 |
|---|---|---|
| 找合作需求 / 合适的主理人 | `list_needs_feed`、`search_needs`、`search_people` | [合作与简报](references/workflows.md#合作与私信) |
| 找产品、服务商、投资人 | `search_products`、`list_service_products`、`list_funding` | 依据实时工具 schema 选择筛选参数 |
| 看能报名的场次 / 连续报名 | `list_signup_feed`、`get_signup_activity` | [报名与主办方](references/signup.md) |
| 管理我办的活动和报名单 | `get_organizer_activity`、`list_signup_submissions` | [报名与主办方](references/signup.md) |
| 我在产业链哪里 / 接下来做什么 | `get_chain_anchor`、`get_my_positioning` | [链位与定位](references/workflows.md#产业链与定位) |
| 今日简报 / 待回复消息 | `get_my_brief`、`list_my_conversations` | [合作与简报](references/workflows.md#今日简报) |

只读取当前任务需要的参考文件。单独取得本文件而没有附带目录时，可读取自包含的官网版本 `https://opcmenu.com/agents/opcmenu.skill.md`，或直接按实时工具描述执行；不要把缺少参考文件当作必须安装其他软件的理由。

## MCP 不可用时

公开 REST 描述：`https://api.opcmenu.com/openapi.yaml`（JSON 版本为 `/openapi.json`）。当前文档仅覆盖 **21 个公开 GET 操作**；按它实际列出的路径和参数查询。它不描述完整 MCP 写能力，不能凭工具名推导写入 URL。

页面和机读导航：`https://opcmenu.com/llms.txt`；产品、主理人、需求页面可用其 `.md` 版本。单场报名页为 `https://opcmenu.com/e/{slug}`。需要账户操作而宿主无法连接 MCP 时，引导用户使用 `https://opcmenu.com/connect` 或相应网页。

## 保留真实边界

- 报名附件（如 BP、营业执照）当前由用户去 App / 报名页上传；不要把链接或占位文本冒充已上传文件。
- 主办方批量处置先用 `preview=true` 得到实际名单，确认名单符合授权后才提交；CSV 导出会暴露报名者资料，只为用户明确要求的用途生成和交付。
- `respond_contact_exchange` 的同意会向对方披露联系方式；`redeem_chat_quota` 会花积分。这两种动作须有明确授权，不能因额度不足或用户想聊天就自动执行。
- 私信、报名答案与个人资料由独行录返回给当前宿主处理；只读取任务需要的数据，不额外转交其他网站或服务。
- 失败时读取 `exits` 和 `retryable`，区分未授权、额度、截止时间和字段缺失。报告成功须依据工具回执；异步审核、未上传文件或未完成登录都不能说成已完成。
