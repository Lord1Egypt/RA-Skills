# Keep 扫码登录鉴权

本文是 Keep Record Skill 的登录执行手册。目标是让 OpenClaw / Hermes 等 exec 运行器用最少步骤完成扫码登录，并在自动等待没有触发时仍能顺畅续接。

## 核心流程

登录链路固定为 3 个动作，不要改成 Agent 自己拼 HTTP 或手写 sleep 轮询：

```bash
# 1. 获取二维码
node {baseDir}/scripts/mcp-call.js get_qrcode '{"authType":"openclaw"}'

# 2. 等待或检查扫码结果
node {baseDir}/scripts/login-wait.js <qrcodeId>

# 3. 持久化 token
node {baseDir}/scripts/persist_auth.js --token='<jwt>' --username='<name>'
```

- `mcp-call.js` stdout 始终是单行 envelope：`{ "ok": true, "data": {...} }` 或 `{ "ok": false, "error": {...} }`。
- `login-wait.js` 是**一次性 background exec**：内部已自循环 `check_login`（默认 2s 间隔、90s 总窗口），完成 / 失败 / 超时由运行器的 `notifyOnExit` 自动唤醒 Agent。**展示二维码后必须同一回合立即执行**这条命令；不要自己 `sleep + check_login`，也不要先问用户「是否已扫码」再调用——这是默认路径，不是兜底。
- `persist_auth.js` 写入 `~/.keepai/.env`，后续工具自动读取凭证。

## 登录状态机

Agent 只需要按下面状态推进。每一步都必须让用户看到二维码或明确下一步。

| 状态 | 触发条件 | Agent 行为 |
|---|---|---|
| `READY` | 调用需登录工具前，或收到 `AUTH_REQUIRED` / `TOKEN_EXPIRED` | 检查本地凭证；无有效 token 则进入 `QR_REQUESTED` |
| `QR_REQUESTED` | 需要登录 | 调用 `get_qrcode`，保存 `qrcodeId`，读取 `qrcodeUrl` / `redirectUrl` / `qrcodeAscii` |
| `QR_SHOWN` | 已拿到二维码 | 展示二维码图片 + 登录跳转链接，附「正在等待扫码…」提示，**同一回合**立即进入 `WAITING`（不要先问用户、不要 `sleep`） |
| `WAITING` | `QR_SHOWN` 之后**强制执行**（这是默认路径，不是「运行器支持时」的可选项） | 一次性 background exec `login-wait.js <qrcodeId>`，由 `notifyOnExit` 唤醒后读取 envelope：`status=authorized` → `AUTHORIZED`；`QRCODE_EXPIRED` → `RETRY_QR`；`LOGIN_TIMEOUT` → `MANUAL_CONFIRM` |
| `MANUAL_CONFIRM` | **仅当** `WAITING` 返回 `LOGIN_TIMEOUT`，或用户主动回复「已完成扫码 / 扫好了 / 我扫了 / 已确认」 | 用保留的 `qrcodeId` 执行 `login-wait.js <qrcodeId> --timeout=15000` 做最终确认 |
| `AUTHORIZED` | `login-wait` 返回 `ok: true` 且 `status: "authorized"` | 执行 `persist_auth.js --token='<jwt>' --username='<name>'` |
| `RETRY_QR` | 二维码过期或用户要求重试 | 重新执行 `get_qrcode`，展示新二维码 |

> 底线 1：展示二维码和启动 `login-wait.js` 是**同一回合**的两个动作，不允许出现已经启动了 login-wait.js,但是还没有给用户展示扫码链接和登陆链接的情况。
> 底线 2：`MANUAL_CONFIRM` 是 `LOGIN_TIMEOUT` 之后的真兜底，不是默认路径。

## 二维码展示规则 （**图片优先，ASCII 兜底**）

`get_qrcode` 关键字段：

| 字段 | 用法 |
|---|---|
| `qrcodeId` | 登录会话 ID，必须保存到本轮登录上下文 |
| `qrcodeUrl` | 二维码图片 URL，必须展示为图片并附纯文本链接 |
| `qrcodeAscii` | 终端 / TUI 兜底；由 `mcp-cli` 自动从 `qrcodeTextUrl` 注水 |
| `qrcodeTextUrl` | 只给脚本拉取 ASCII 使用，不要展示给用户 |
| `redirectUrl` | 登录跳转 URL，必须作为“图片不可用时”的可点击登录入口 |

**OpenClaw Web 等聊天 / 富文本 UI 默认优先展示 `data.qrcodeUrl` 图片，不要默认先贴 ASCII 二维码。**
1. **二维码图片**：`data.qrcodeUrl`，以 Markdown 图片 + 可点击链接形式给出，作为默认主展示
2. **ASCII 二维码**：`data.qrcodeAscii`，仅在终端 / 等宽字体场景主展示，或作为补充兜底
OpenClaw Web / 聊天 UI 展示模板：

````markdown
请使用 Keep App 扫描下方二维码完成登录：

![Keep 扫码登录](<qrcodeUrl>)

纯文本二维码图片链接：
<qrcodeUrl>

如果二维码图片无法加载，也可以点击登录跳转链接：
<redirectUrl>

扫码完成登陆后，如果我没有自动继续，请回复「已完成扫码」，我会继续检查登录状态。
````

终端 / TUI 可以追加 `qrcodeAscii`：

```text
<qrcodeAscii 原样输出>
```

禁止：

- 只贴 ASCII，不展示 `qrcodeUrl` 图片。
- 只给 `redirectUrl`，不展示 `qrcodeUrl` 二维码图片链接。
- 只给 `qrcodeUrl`，不展示 `redirectUrl` 登录跳转链接。
- 只说“请登录”，但没有给二维码图片、二维码图片链接和登录跳转链接。
- 把 `qrcodeTextUrl` 当成人看的链接。
- 把 `redirectUrl` 当成二维码图片。

## 等待与续接

优先路径：展示二维码后直接启动等待。

```bash
node {baseDir}/scripts/login-wait.js <qrcodeId>
```

返回处理：

| 返回 | 行为 |
|---|---|
| `ok: true` 且 `data.status == "authorized"` | 进入持久化 |
| `error.code == "QRCODE_EXPIRED"` | 告知二维码过期，重新获取二维码 |
| `error.code == "LOGIN_TIMEOUT"` | 询问是否继续等待或重新给二维码 |
| 其他错误 | 展示 `error.message`，按错误含义决定重试或终止 |

- 未自动等待的兜底路径：用户回复「已完成扫码」「扫码完成」「我扫了」等表达后，用上一轮保存的 `qrcodeId` 检查状态。

```bash
node {baseDir}/scripts/login-wait.js <qrcodeId> --timeout=15000
```

- 已授权：进入持久化。
- 未检测到授权：提示用户确认 Keep App 内已确认登录，可继续等待或重新获取二维码。
- 二维码过期：重新获取二维码，不要让用户继续扫旧码。

## 持久化与安全

登录成功后只执行本地持久化脚本，不要再用脚本调用 MCP：

```bash
node {baseDir}/scripts/persist_auth.js --token='<jwt>' --username='<name>'
```

- `<jwt>` 来自 `login-wait` 返回的 `data.token`。
- `<name>` 来自 `data.user.username`，没有则可省略。
- 不要把 token 通过 `export keep_auth_token=...` 写进 shell 命令。
- 不要向用户展示、复述或总结 token 值。

凭证会写入 `~/.keepai/.env`：

```text
keep_auth_token=eyJhbGciOi...
keep_auth_token_expired=1713312000
keep_username=Seancaixp
```

后续 `mcp-call.js` 会自动读取凭证并注入 `Authorization` header。

## 相关脚本

| 文件 | 职责 |
|---|---|
| `scripts/mcp-call.js` | MCP 工具调用代理，获取二维码和调用业务工具 |
| `scripts/login-wait.js` | 扫码状态等待器，内部封装 `check_login` |
| `scripts/persist_auth.js` | 写入或清理 `~/.keepai/.env` |

退出登录见 [revoke-auth.md](revoke-auth.md)：先 `revoke_auth`，再 `persist_auth.js --clear`；如果工具列表没有 `revoke_auth`，只清理本地凭证。
