# 认证命令 (auth)

> 🔐 = 需要先登录

## 命令列表

| 命令 | 说明 | 需要登录 |
|------|------|---------|
| `kugou-cli auth login` | 获取二维码（`qrcode` 内部字符串 + `qrcode_img_url` 远程图片 URL + `qrcode_img_path` 本地 PNG 路径） | 否 |
| `kugou-cli auth status` | 检查登录状态（**单次查询，不内部轮询**，agent 需外层循环 2-3s 间隔） | 否 |
| `kugou-cli auth set-secret <secret>` | 直接导入已持有的 base64 secret 登录（跳过扫码） | 否 |
| `kugou-cli auth logout` | 登出 | 否 |

---

## 1. 扫码登录

登录流程极简：

```bash
# Step 1: 获取二维码，同时得到远程 URL 和本地 PNG 路径
kugou-cli auth login

# Step 2: 循环调用 status（**单次查询不内部轮询**，agent 自己外层循环）
# 每次间隔 2-3 秒，看到 logged_in=true / status=success 即完成
kugou-cli auth status
```

**auth login 输出示例**:
```json
{"qrcode": "xxx", "qrcode_img_path": "C:\\Temp\\kugou-qrcode.png", "qrcode_img_url": "https://static.kugou.com/.../qrcode.png"}
```

字段说明：
- `qrcode`：二维码字符串标识，**Agent 不要使用** —— 仅供 CLI 内部持久化，以便后续 status 调上游 check 接口
- `qrcode_img_path`：CLI 生成的本地二维码 PNG 文件绝对路径。当前客户端支持读取或附加本地图片时使用它，例如 Codex 等本地文件能力较强的客户端
- `qrcode_img_url`：酷狗上游返回的远程二维码图片 URL。当前客户端支持 Markdown 外链图片时使用它，例如 WorkBuddy 等客户端
- `qrcode_img_path` 和 `qrcode_img_url` 是两种并行的图片展示方式，Agent 根据当前客户端能力自行选择一种，不要同时展示两张二维码

---

## 2. AI 引导流程

### 2.1 决策点：先问 secret，再选路径

在调用任何 auth 命令之前，**先询问用户**：

> "你手上是否已有可用的 base64 secret 字符串？（从其他设备/工具导出的）"

- **用户明确说"有"** → 直接走 §3 `set-secret`，跳过 §1 扫码
- **用户说"没有"或不确定** → 走 §2.2 扫码流程
- **当前环境无法发送图片**（纯文本 agent、SSH 远端、容器）→ 强制走 §3 `set-secret`，不要走扫码

> **默认行为**：除非用户明确说"我有 secret"，否则优先走扫码。

### 2.2 扫码流程

1. 调用 `auth login`，读取返回的 `qrcode_img_path` 和 `qrcode_img_url`
2. **根据当前客户端能力选择一种方式展示二维码图片**：
   - 客户端支持读取或附加本地文件（如 Codex 等）→ 优先使用 `qrcode_img_path`，通过客户端的本地图片读取/附件能力展示。不要只把路径作为普通文本发给用户
   - 客户端支持 Markdown 外链图片（如 WorkBuddy 等）→ 使用 `qrcode_img_url`，在消息中输出 `![酷狗登录二维码](<qrcode_img_url>)`
   - Agent 可以自行选择最适合当前环境的方式，不要同时展示两张二维码
   - **避免**只输出“请打开 xxx URL”或“图片路径是 xxx”这种纯文字提示，用户应直接看到二维码图片
   - 选择的方式展示失败时，切换到另一种方式：远程图片加载失败则尝试本地文件，本地文件无法读取则尝试远程 Markdown 图片
   - 如果当前客户端既不能读取本地文件，也不能渲染远程 Markdown 图片 → 放弃扫码，切换到 §3 `set-secret` 路径
3. **阶段 A — 主动轮询（覆盖秒扫）**：图片展示后，**主动**外层循环调用 `auth status`，每次间隔 2-3 秒，**最多 5 次**（与 `failed` 重试合并计数）：
   - 看到 `logged_in: true` → 完成，继续执行用户请求
   - 看到 `status: success` → 完成，继续执行用户请求
   - 看到 `status: scanned` → 等几秒再调一次 status
   - 看到 `status: failed` → **不要换新图**，隔 1-2 秒后用同一个本地 qrcode 再调一次 status（计入 5 次轮询预算）
   - 看到 `status: expired` → **不再继续轮询**，主动告诉用户"二维码已失效，正在重新获取"，调 `auth login` 拿新图，回到步骤 1
   - 5 次都是 `waiting` / `failed` → 进入阶段 B
4. **阶段 B — 等待用户反馈（关键）**：5 次主动轮询后仍未登录，**停下来**，不再调任何 auth 命令。主动告诉用户：
   > "请用酷狗 APP 扫码登录，扫完后告诉我已扫码"
   然后**等用户主动回复**。**不要**自己继续轮询。
5. **阶段 C — 验证登录**：用户回复"已扫码"后，调一次 `auth status` 验证：
   - `logged_in: true` → 完成，继续执行用户请求
   - `status: scanned` → 用户在手机上还没点确认，等几秒再调一次
   - `status: failed` → **不要换新图**，隔 1-2 秒后用同一个本地 qrcode 再调一次 status（最多重试 2-3 次）
   - `status: expired` → 上游明确说过期（CLI 已清理本地），重新 `auth login` 拿新图，回到步骤 1
   - `logged_in: false`（无 status 字段）→ qrcode 已被清理（通常是上一步 `expired` 后状态），提示用户"二维码可能已过期，正在重新获取"并回到步骤 1
6. **若用户在阶段 B 回复"没看到图片" / "图片打不开"** → 先切换到另一种二维码展示方式；两种方式都失败后，再切换到 §3 `set-secret` 路径
7. **若用户在阶段 B 回复"已扫码"**但阶段 C 验证发现没登录成功（`scanned` / `failed`），按阶段 C 各项处理，不要替用户做"再扫一次"之类的猜测

### 2.3 状态表

| 返回 | 含义 | Agent 应做 |
|------|------|-----------|
| `{"logged_in": true, "nickname": "...", "login_time": "..."}` | 已登录（**已有 token 持久化**，通常是之前登录过） | 继续执行用户请求 |
| `{"logged_in": true, "status": "success", "nickname": "..."}` | 扫码刚完成登录（**本轮 status 检查中完成 token 持久化**） | 继续执行用户请求 |
| `{"logged_in": false, "status": "waiting", "qrcode": "..."}` | 二维码待扫码 | **阶段 A**：2-3s 后重试 status，最多 5 次；5 次后**进入阶段 B**，停下来等用户主动反馈 |
| `{"logged_in": false, "status": "scanned", "nickname": "...", "qrcode": "..."}` | 已扫码待确认 | 等几秒再调一次 status（用户还没在手机上点确认） |
| `{"logged_in": false, "status": "expired", "message": "..."}` | 二维码被上游明确判定为过期（**CLI 会自动清理本地 qrcode**） | **不再重试**：调 `auth login` 拿新图（覆盖本地 qrcode），回到 §2.2 步骤 1 |
| `{"logged_in": false, "status": "failed", "message": "..."}` | 上游返回了 CLI 不识别的 status 码（**CLI 不会清理本地 qrcode**，本地缓存仍可用） | **重试** 1-2 秒后再调一次 status（用同一个本地 qrcode）；阶段 A 中计入 5 次预算，阶段 C 中最多 2-3 次。**不要调 `auth login` 换新图** |
| `{"logged_in": false}` | 无登录态（未登录过 / 登录过期被清理 / qrcode 刚被 expired 清理掉） | 走完整登录流程（§2.1 决策点） |

> **判定"已登录"**：`logged_in: true` 即算成功，**不管有没有 `status: success` 字段**——两种 JSON shape 都合法。
>
> 区分"无登录态"和"等待扫码"的关键：前者**没有** `status` 字段，后者有。
>
> **轮询逻辑（两阶段）**：
> - 阶段 A：图片刚展示，主动循环 status 最多 5 次（2-3s 间隔）→ 覆盖秒扫场景
> - 阶段 B：5 次仍 `waiting` → 主动告诉用户"请扫码登录，扫完后告诉我已扫码"，**不再调 status**，等用户**主动回复**

### 2.3.1 边界提醒：`expired` 会清掉 qrcode 并需换新图，`failed` 不清且应重试

**关键事实**：

- `status: expired` 时 CLI 会自动清理本地 qrcode 文件（**不是清理登录态**）。这是上游**明确**判定二维码失效（协议层不可恢复）→ **必须换新图**。
- `status: failed` 时 CLI **不会**清理本地 qrcode 文件。这是上游返回了 CLI 不识别的 status 码（短暂异常 / 未知协议值 / 上游 gateway 抖动）。本地 qrcode 字符串**没失效** → **不应换新图，应重试同一 qrcode**。

**两种返回在阶段 A / 阶段 C 的处理**：

| 见到位置 | 状态值 | 原因可能性 | Agent 应做 |
|---------|--------|-----------|-----------|
| 阶段 A 主动轮询中 | `expired` | 上游明确说过期 | **不再继续轮询**，主动告诉用户"二维码已失效，正在重新获取"，调 `auth login` 拿新图，回到 §2.2 步骤 1 |
| 阶段 A 主动轮询中 | `failed` | 上游短暂异常 / 未知 status 码 | **不换新图**，隔 1-2 秒后用同一个本地 qrcode 再调一次 status（计入阶段 A 的 5 次主动轮询预算） |
| 阶段 C 用户说"已扫码"后验证 | `expired` | 登录过程中上游判定过期 | 重新 `auth login` 拿新图 |
| 阶段 C 用户说"已扫码"后验证 | `failed` | 登录过程中上游返回非预期 | **不换新图**，隔 1-2 秒后用同一个本地 qrcode 再调一次 status，最多重试 2-3 次；仍 `failed` 再按上游持续异常处理（建议告诉用户稍后重试或切 `set-secret`） |
| 阶段 A 之后阶段 B 之前 | `expired` / `failed` | （不应发生） | 视为阶段 A 见到对应状态值处理 |

> **判定要点**：
> - 不要因为"看到 expired/failed → 看到 logged_in: false"就误判"用户没登录"。expired/failed 都是 qrcode 状态，不是登录态。
> - `expired` 后下次 `auth status` 会拿到 `{"logged_in": false}`（无 status 字段，本地已被清）。
> - `failed` 后下次 `auth status` **可能仍返回 failed**（上游持续异常），也可能恢复 `waiting`（上游恢复后用同一个 qrcode 仍可扫码登录）。**不要假设 `failed` 后本地一定被清**。
> - 关键决策：`expired` 是**协议层不可恢复** → 换新图；`failed` 是**传输层/未知码** → 重试同一 qrcode。

### 备选路径：用户已持有 secret

当用户**已经持有**一个有效的 base64 secret 字符串时（例如从其他设备、其他工具导出的），可以直接用 `auth set-secret` 跳过整个扫码流程，**不需**调用 `auth login` / `auth status`：

```bash
kugou-cli auth set-secret "<base64-secret>"
```

调用成功后 secret 会被持久化（路径见 §3），所有 music 命令立即可用，效果与扫码登录一致。

---


## 3. 直接设置 secret

**适用场景**：
- 用户在其他设备/工具上已登录酷狗，导出或复制了一份 base64 secret
- 测试、调试、自动化场景下需要直接注入 secret
- 任何不便于扫码的终端环境（如 SSH 远端、容器、CI）
- 当前 agent 工具集无法渲染 `qrcode_img_url` 远程图片，或无法读取 `qrcode_img_path` 本地图片（不联网、不支持 Markdown 渲染或不支持本地图片附件，见 §2.2）

**命令**:

```bash
kugou-cli auth set-secret "{secret}"
```

**shell 引号注意事项**：
- secret 字符串含 `+`、`/`、`=` 等 base64 字符是**正常的**，**不会**被 shell 误解析
- 但 `+` 在 bash 中是通配符、`=` 在 cmd.exe 中会触发变量赋值，**务必用引号包起来**
- 推荐使用双引号 `"..."`（除非 secret 中含 `$`，那就用单引号 `'...'`）

**输出示例**:
```json
{"status": "ok", "message": "secret saved"}
```

**失败示例**（secret 为空）:
```
secret cannot be empty
```

**与扫码登录的等价性**：
- secret 落到本地登录态文件，**跨平台位置**：
  - Linux/macOS：`~/.config/kugou-cli/auth.json`
  - Windows：`%AppData%\kugou-cli\auth.json`（通常为 `C:\Users\<user>\AppData\Roaming\kugou-cli\auth.json`）
  - 若用户询问"登录态存在哪"，按平台给对应路径，**不要**直接说 `~/.config/...` 在 Windows 下不准确
- 后续 `auth status` 输出 `{"logged_in": true}`
- 所有 `music` 子命令立即可用，无需任何额外步骤
- nickname 字段为空（因为导入途径不带昵称），不影响功能

**登录态过期处理**：
- 当任意 `music` 命令遇到登录态过期时，CLI 会**自动清理**本地登录态，并在 stderr 输出 `账号登录过期，请重新登录`，以非 0 exit code 退出
- Agent 收到该错误后应**直接引导用户重新登录**（`auth login` 走扫码，或 `auth set-secret` 导入新 secret），无需手动清理本地文件
- 之后调用 `auth status` 会得到 `{"logged_in": false}`（**无 status 字段**，对应 §2.3 状态表最后一行）

---

## 4. 登出 (logout)

**命令**：

```bash
kugou-cli auth logout
```

**行为**：
1. **未登录时**：幂等直接返回 `{"status": "logged out"}`
2. **已登录时**：CLI 会先与服务端同步登出，**确认成功后才**清理本地登录态。任何一步失败都会在 stderr 报错并保留本地登录态，以便用户重试
3. 成功输出：`{"status": "logged out"}`

**失败场景**：
- 网络/服务端异常 → stderr 报错，**不清理**本地，提示用户稍后重试
- 此时再次执行 `auth status` 仍会显示 `logged_in: true`，本地登录态被保留

**AI 引导建议**：
- 用户说"登出 / 退出登录 / 注销"时直接执行 `auth logout`
- 看到 `{"status": "logged out"}` 后，告诉用户已成功登出，可继续 `auth login` 重新登录
- 看到错误时：
  1. **自动重试 1 次**（网络抖动常见）
  2. 仍失败 → 告知用户"登出失败，本地登录态保留，可能是网络问题"，**询问**用户："是否要稍后重试？"
  3. **不要**擅自清理本地文件或调任何 music 命令
