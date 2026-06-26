# Auth Guard（所有业务命令前必须执行）

## 触发条件

- **主动登录**：用户说"登录 Meegle"、"连接飞书项目"、"login meegle"等。
- **被动拦截**：用户请求任何 Meegle 业务操作（查询待办、查工作项、创建任务等），优先执行 Auth Guard。
- **URL 触发**：用户发送了飞书项目/Meegle URL。处理流程：
  1. 先调 `npx @lark-project/meegle@latest url decode` 拿到结构化字段（`url_kind`、`host`、`simple_name`、`work_item_id` 等）。**禁止**自己从 URL 截取路径段作参数。字段含义与 kind 分支见 [url-kinds.md](./url-kinds.md)。
  2. 保存 `$host` = response.host、`$url_kind`、`$simple_name`、`$work_item_id`。
  3. 执行 Auth Guard（下面的 STEP 1 起）。
  4. 登录成功后按 `$url_kind` 分支：
     - `workitem_detail` → `npx @lark-project/meegle@latest project search` 得权威 `$project_key`，再 `npx @lark-project/meegle@latest workitem get` 查询详情
     - `workitem_homepage` / `view_*` / `unknown` 等非详情页 → 按 url-kinds.md 的指引拒绝或追问
     - 其他 kind → 参考 url-kinds.md 对应处理方式

按以下 STEP 顺序执行。每个 STEP 结尾的 GOTO 指明下一步，严格遵循跳转。

---

### STEP 1 — 检查登录状态

```bash
npx @lark-project/meegle@latest auth status --format json
```

返回值示例：
- 已登录：`{ "authenticated": true, "host": "meegle.com", "source": "token_store", "expires_in_minutes": 42 }`
- 未登录且有 host：`{ "authenticated": false, "host": "meegle.com", "source": null, "expires_in_minutes": null }`
- 未登录且无 host：`{ "authenticated": false, "host": null, "source": null, "expires_in_minutes": null }`

解析返回值，保存变量：
- `$authenticated` = response.authenticated
- `$host` = response.host

**URL 触发时的 host 覆盖**：如果用户发送了飞书项目/Meegle URL 触发本流程，且 `$host` 为 null，则使用上一步 `url decode` 返回的 `host` 字段作为 `$host`。

**跳转：**
- IF `$authenticated == true` → GOTO STEP DONE
- IF `$host != null` → GOTO STEP 2
- IF `$host == null` → GOTO STEP HOST

---

### STEP HOST — 选择站点

ASK user（等待用户回复）：

> 你要连接哪个站点？
> 1) 飞书项目 (project.feishu.cn)
> 2) Meegle (meegle.com)
> 3) 自定义域名（请直接输入域名）

SAVE `$host` from user reply → GOTO STEP 2

---

### STEP 2 — 初始化 Device Code

```bash
npx @lark-project/meegle@latest auth login --device-code --phase init --host $host --format json
```

SAVE from response：
- `$verification_uri_complete` = response.verification_uri_complete
- `$user_code` = response.user_code
- `$device_code` = response.device_code
- `$client_id` = response.client_id
- `$interval` = response.interval
- `$expires_in` = response.expires_in
- `$max_attempts` = floor($expires_in / $interval)

**发送验证链接给用户：**

SEND to user: `请在浏览器中打开以下链接完成授权：\n$verification_uri_complete\n验证码：$user_code（$expires_in 秒内有效）`

> ⚠️ 发送后立即 GOTO STEP 3。**禁止**在此停下等用户回复"我授权好了"。你必须主动轮询。

→ GOTO STEP 3

---

### STEP 3 — 轮询授权结果（循环）

> ⚠️ 使用 STEP 2 保存的 `$device_code` 和 `$client_id`。**禁止**重新执行 STEP 2（否则会生成新的验证码，用户之前打开的链接作废）。

```bash
sleep $interval && npx @lark-project/meegle@latest auth login --device-code --phase poll --once \
  --device-code-value $device_code --client-id $client_id --format json
```

PARSE response → `$status` = response.status

**跳转：**
- IF `$status == "ok"` → GOTO STEP OK
- IF `$status == "authorization_pending"` → GOTO STEP 3（重复本步骤，继续轮询）
- IF `$status == "slow_down"` → `$interval = $interval + 5`，GOTO STEP 3
- IF `$status == "expired_token"` → SEND "授权已超时，请重新发起登录"，STOP
- IF attempts > `$max_attempts` → SEND "轮询超时，请重试"，STOP

---

### STEP OK — 通知登录成功

SEND to user: "登录成功！"

> ⚠️ 此消息**必须单独发送**，不要与后续业务查询结果合并到同一条回复中。用户需要第一时间看到授权状态变化。

→ GOTO STEP DONE

---

### STEP DONE — 执行业务命令

Auth 已通过，执行用户请求的操作。

## 错误处理

- 如果 bash 返回 `command not found` 或 npx 不可用，提示用户安装 Node.js 18+。
- 如果 `--phase init` 返回错误（站点不支持 Device Code），提示用户在终端中执行 `npx @lark-project/meegle@latest auth login`。
- 如果 `--phase poll` 超时，提示用户重试登录流程。
