---
name: personal-checkup-booking
display_name: 好啦体检 · 个人体检定制和预约
description: 好啦体检个人体检工具。按年龄、性别、婚否、预算与健康关注点生成体检方案，查询门店与常见问题，预约、改期、取消，查询订单。
license: MIT
metadata:
  openclaw:
    homepage: https://github.com/Beijing-Haola-Tech/haola-checkup-mcp
---

# 好啦体检 · 个人体检

工具名、参数、必填项与枚举值以 `tools/list` 返回的 `inputSchema` 为准；参数不确定时调用 `help`。

## 免登录工具

| 工具 | 用途 |
|---|---|
| `vendor_list` | 查门店地址，至少传一种筛选条件 |
| `vendor_brands` | 查品牌覆盖的城市与门店数 |
| `knowledge_get` | 按 URI 读取领域知识 |
| `faq` | 查常见问题，`query` 用 2–4 字短词 |
| `help` | 查本体、工具与参数说明 |
| `progress_report` | 上报长耗时任务进度 |

## 需要登录的工具

| 工具 | 用途 |
|---|---|
| `plan_recommend` | 生成个人体检方案，返回 `planId` |
| `order_list` | 查订单列表 |
| `order_detail` | 查订单详情 |
| `welfare_list` | 查体检件 |
| `welfare_detail` | 查体检件详情 |
| `cautions` | 查体检项目注意事项 |
| `contact_list` | 查联系人 |
| `contact_get` | 查联系人详情 |
| `contact_create` | 创建家属临时联系人 |
| `contact_update` | 更新联系人信息 |
| `contact_profile_get` | 查健康画像 |
| `contact_profile_save` | 保存健康画像 |
| `reservation_book` | 创建预约 |
| `reservation_cancel` | 取消预约 |
| `reservation_modify` | 修改预约日期 |
| `card_list` | 按卡号查卡密与兑换情况 |

## 使用约定

- 项目、金额、门店和订单一律以工具返回为准，不自行编造或推测。
- 需要登录的工具由当前 MCP 客户端完成 OAuth；授权后原样重试原调用，不要让用户重述需求。
- 预约时优先使用服务端返回的体检人表单和协议表单。
- 工具返回表单或可选输入方式时，按返回的字段和提示处理；客户端不支持表单时，让用户选择可用方式，不强制跳转。
- 用户选择在对话中填写时，按 MCP 返回的待填字段一次性询问，并说明敏感信息会出现在当前对话中、可能被客户端记录。
- 工具返回 URL 时，引导用户完成页面操作，完成后按工具后续要求继续。
- 不要主动索取身份证号、签名或验证码；用户已选择在对话中填写时，可以继续询问证件号。
- 用户提到家属时，先用 `contact_list` 查已有体检人；多个匹配时让用户选择。
- 不替用户编造体检人姓名、证件号、生日、性别或关系。

## MCP 兼容性

当前 Skill 依赖 `mcp.json` 中声明的 `haola-pe` MCP 服务。Skill 包本身不带执行脚本；客户端不支持 MCP 时，由 Agent 生成临时脚本调用服务。

- Streamable HTTP：`https://ai.ihaola.com.cn/api/mcp/haola-pe`
- SSE：`GET https://ai.ihaola.com.cn/api/mcp/haola-pe/sse`
- SSE 建流后读取 `endpoint` 事件，把 JSON-RPC 消息 `POST` 到返回的 `/message` 地址。

临时脚本执行标准 MCP 流程：`initialize`、`notifications/initialized`、`tools/list`、`tools/call`。脚本放在当前工作目录或临时目录，不写进 Skill 包。

登录类工具按服务端返回的 OAuth 元数据完成授权，授权后重试原调用。令牌不得写入对话、Skill 文件或普通日志。

如果当前环境没有联网或代码执行能力，明确说明无法调用服务并停止，不编造结果，也不要求用户更换客户端。

## 常见错误

| 返回 | 处理 |
|---|---|
| 未连接 MCP | Agent 按「MCP 兼容性」连接 `haola-pe`；连接失败时说明本次无法查询 |
| 需要授权 | 完成当前客户端的 MCP OAuth 后重试原调用 |
| 会话失效 | 重新初始化 MCP 会话 |
| 参数校验失败 | 查 `inputSchema` 或调用 `help` |
| 未知工具 | 以 `tools/list` 为准核对 |
| 工具返回空结果 | 如实说明未查到，不推测结果 |
