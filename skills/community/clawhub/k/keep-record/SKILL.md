---
name: keep-record
description: >
  Assist users in recording personal health data, including diet, weight, body fat, body measurements, exercise, sleep, and menstrual cycle. Activate when the user clearly expresses an intent to record, log, check in, or save health-related information.
  Examples that should trigger include: 
  - "帮我记录今天体重80kg"
  - "记一下我跑了5公里"
  - "把这顿饭记录到Keep"
  - "记一下我昨晚睡了7小时"
priority: normal
trigger:
  intentBased: true
metadata:
  requires:
    mcp: "https://mcp.gotokeep.com/skills-mcp-gateway-page/v1"
  version: "1.5.8"
---

# Keep 健康记录工具

记录饮食、运动、体重、围度、生理期、睡眠等数据到 Keep App。支持文字描述和图片上传。

## 何时必须调用

当用户在**陈述、打卡或记录自己的健康数据**时，优先调用本 Skill，不要先普通聊天，不要反问“要不要帮你记一下”，除非用户表达明显不想记录，或明显是在提问 / 求建议 / 求分析。

即使用户**没有明确说 Keep / 记到 Keep**，只要输入看起来是在**描述刚刚发生的饮食 / 体重 / 身体围度 / 运动 / 睡眠 / 生理期数据**，也应优先调用本 Skill，而不是先当作普通聊天。

**运动记录的额外限制**：记录运动时，用户**必须提供运动相关图片作为佐证**。如果只有「今天跑了 5km」「打了羽毛球」这类纯文本、**没有图片**，仍应按运动记录意图处理并使用本 Skill，但**不要直接调用记录工具落库**，而应先明确提醒用户补充上传运动图片，待用户补图后再继续记录。

**必定适用此 Skill 的场景**：

- 明确提到 Keep 且意图是记录：如「帮我记到 Keep」「记到 Keep App」「Keep 打个卡」「这是 Keep 截图，帮我记一下」
- 未提 Keep，但明显是在记录 / 打卡：如「帮我记一下今天午饭」「登记一下体重」「刚称了 63.2kg」「昨晚睡了 6 小时」
- 体重 / 体脂 / 围度：如「今天体重 80kg」「腰围 76」「体脂率 18」
- 饮食：如「早餐吃了鸡蛋面」「中午吃了潮汕牛肉火锅」「喝了杯奶茶」「加餐一个苹果」
- 运动（必须带图）：如用户提供运动截图、运动照片、Keep 运动页截图，并表达记录意图，如「这是今天跑步截图，帮我记一下」「上传一张羽毛球运动图，记到 Keep」
- 睡眠：如「昨晚睡了 7 小时」「深睡 1.8h」「失眠到 2 点」
- 生理期：如「生理期第 3 天」「痛经」「姨妈来了」
- 附图打卡：消息包含早餐 / 运动 / 体重秤 / Keep App 截图，且语义是在打卡或记录

**不适用此 Skill**：

- 提问或建议咨询：如「减脂期吃什么」「跑步配速多少合适」
- 闲聊：如「今天天气好」「这家火锅店好吃吗」
- 其他业务：如项目 / 报销 / 汇报 / 审批

## USE WHEN
- 用户说要记录饮食、体重、运动、睡眠、生理期
- 用户说要打卡、同步、保存到 Keep
- 用户提供健康数据（体重、体脂、运动截图、饮食照片）
- 用户说“帮我记一下”“记录一下”
- 任何健康数据录入行为

**Triggers**：体重记录, 饮食记录, 运动记录, 围度记录, 生理期记录, 睡眠记录.

## LOAD MODE
lazyLoad: false
preload: true

## Runner

本 Skill 面向 **OpenClaw / Hermes** 运行器，支持两种调用方式：

**方式 1 — exec（推荐）**：所有工具通过以下命令调用，调用约定见 [auth.md · exec 调用约定](references/auth.md#路径-b-调用约定mcp-calljs)：

```
node {baseDir}/scripts/mcp-call.js <tool> '<json>'
```

> **`{baseDir}` 占位符**：由运行器注入 Skill 的安装绝对路径。Agent 在 exec 命令里**保留字面 `{baseDir}`**，不要自己替换。

**方式 2 — 原生 MCP**：若运行器支持 streamable-http，可直接注册 MCP Server：

```json
{
  "mcpServers": {
    "keep-record": {
      "url": "https://mcp.gotokeep.com/skills-mcp-gateway-page/v1",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer ${env:keep_auth_token}"
      }
    }
  }
}
```

- 协议：JSON-RPC 2.0；`url` 只填根地址，**不要**拼接 `tools/call` / 工具名 / REST 子路径
- 运行器从环境变量读取 token 注入 HTTP header，Agent 不直接接触 token 值

 ## 处理流程
 
 1. **确保已登录**：调用任何需登录工具前先检查本地凭证；无效则走 [鉴权流程](references/auth.md)。收到 `AUTH_REQUIRED` / `TOKEN_EXPIRED` 也要重登。
 2. **校验运动是否带图**：如果是运动记录，先检查用户是否提供运动相关图片；没有图片时先提醒用户补充上传运动图片，并等待用户补图后再继续，不要直接调用 `record_tool`。
 3. **处理图片（如有）**：先 `get_upload_url` 拿预签名 URL，再用 `scripts/put-upload.js` 执行 PUT 上传。该脚本会先把源图片复制到固定目录（默认 `~/.keepai/tmp`，可用 `KEEP_UPLOAD_TMP_DIR` 覆盖），再发起上传；2xx 视为成功。详见 [图片上传](references/get-upload-url.md)。
 4. **调用 `record_tool`**：把用户原始描述原样作为 `text` 传入，**不要预分类**，由服务端识别路由；详见 [记录工具](references/record.md)。
 5. **格式化结果**：按下方「结果呈现」给用户。

 具体命令样例统一见下方 **Quick Recipes**。

## 登录顺畅性要求（OpenClaw / Hermes）

执行鉴权流程时按 [auth.md](references/auth.md) 的状态机推进，重点保证二维码可扫、跳转可点、上下文可续接：

1. `get_qrcode` 返回后，保存 `data.qrcodeId`。
2. 每次展示登录引导时必须同时给用户 `data.qrcodeUrl` 和 `data.redirectUrl`：
   - `data.qrcodeUrl`：渲染为 Markdown 图片，并附“二维码图片链接”纯文本。
   - `data.redirectUrl`：附“登录跳转链接”，用于二维码图片无法加载时点击打开。
3. 二维码消息必须包含兜底话术：**“扫码完成后，如果我没有自动继续，请回复「已完成扫码」，我会继续检查登录状态。”**
4. 优先执行 `login-wait.js <qrcodeId>` 自动等待；如果没有自动等待，用户回复「已完成扫码」后仍使用同一个 `qrcodeId` 检查状态。
5. 授权成功后执行 `persist_auth.js --token='<jwt>' --username='<name>'` 落盘，再继续原业务工具。

> 底线：不要让用户进入“被要求登录但没有可扫二维码 / 没有可点击跳转链接 / 没有下一步说明”的状态。二维码图片链接、登录跳转链接、下一步触发语和后续检查动作必须完整。

## 工具清单

由 MCP Server 的 `tools/list` 动态返回；下表是 Agent 首次使用前需要知道的骨架。**入参 / 返回字段 / 错误码以对应 reference 为准**。

| 工具 | 入参骨架 | 需登录 | 详见 |
|---|---|---|---|
| `get_qrcode` | `{ authType }` | 否 | [auth.md](references/auth.md#2-调用-get_qrcode) |
| `check_login` | `{ qrcodeId }` | 否 | 不要直接调；用 `scripts/login-wait.js`，详见 [auth.md](references/auth.md) |
| `revoke_auth` | `{}` | 是 | [revoke-auth.md](references/revoke-auth.md) |
| `get_upload_url` | `{ filename, content_type }` | 是 | [get-upload-url.md](references/get-upload-url.md) |
| `record_tool` | `{ text, image_url? }` | 是 | [record.md](references/record.md) |

## Quick Recipes

**Recipe 1 — 首次登录**：

```bash
node {baseDir}/scripts/mcp-call.js get_qrcode '{"authType":"openclaw"}'
# → OpenClaw Web / 聊天 UI 默认优先展示 data.qrcodeUrl（![](url) + 纯 URL）
#   若当前运行器是终端 / TUI，再补充 data.qrcodeAscii 原样打印到 stderr 作为兜底
#   详见 references/auth.md「展示策略」
node {baseDir}/scripts/login-wait.js <qrcodeId>
node {baseDir}/scripts/persist_auth.js --token='<jwt>' --username='<name>'
```

**Recipe 2 — 纯文本记录**：

```bash
node {baseDir}/scripts/mcp-call.js record_tool '{"text":"今天体重63.2kg"}'
```

**Recipe 3 — 带图记录（运动记录必须使用此方式）**：

```bash
node {baseDir}/scripts/mcp-call.js get_upload_url '{"filename":"run.jpg","content_type":"image/jpeg"}'
node {baseDir}/scripts/put-upload.js --file='<local_image_path>' --upload-url='<upload_url>' --content-type='image/jpeg'
node {baseDir}/scripts/mcp-call.js record_tool '{"text":"今天跑了5km","image_url":"<cdn_url>"}'
```

**Recipe 4 — 退出登录**：

```bash
node {baseDir}/scripts/mcp-call.js revoke_auth '{}'      # tools/list 未返回则跳过本步
node {baseDir}/scripts/persist_auth.js --clear
```

## 结果呈现

记录成功后，向用户展示：

```
✅ [记录类型]记录成功

[具体内容摘要]

记录时间：[时间]
```

## 通用错误码

仅列跨工具的通用错误。**业务错误码（登录类 / 上传类）见对应 reference**：

| 错误码 | 含义 | 应对 |
|---|---|---|
| `AUTH_REQUIRED` | 未登录 / token 非法 | 走 [鉴权流程](references/auth.md) |
| `TOKEN_EXPIRED` | 登录过期 | 走 [鉴权流程](references/auth.md) |
| `RATE_LIMITED` | 请求过频 | 等待 `retry_after` 秒后重试 |
| `UPSTREAM_ERROR` | Keep 服务异常 | 提示稍后重试 |
| `INVALID_ARGS` | `mcp-call.js` 用法错误（退出码 2） | 检查 `<tool_name>` 与 JSON 参数；`--list` 查工具 |

按工具的细分错误码：

- 登录 / 二维码相关：见 [auth.md · 鉴权 / 登录相关错误码](references/auth.md#鉴权--登录相关错误码)
- 图片上传相关：见 [get-upload-url.md · 上传相关错误码](references/get-upload-url.md#上传相关错误码)
