# 退出登录（`revoke_auth`）

## 工具：`revoke_auth`

主动退出 Keep 登录。**标准退出 = `revoke_auth`（服务端失效 token） + `persist_auth.js --clear`（本地清凭证），两步按顺序执行**。

> Agent 判定逻辑：如果 `tools/list` **未返回** `revoke_auth`，直接走「降级路径」（只做本地 `--clear`）。发布状态参见文末。

## 使用场景

- 用户明确表达退出意图（"退出登录"、"切换账号"、"注销"）
- 用户反馈账号疑似被盗用，需要立即终止 token
- 调试 / 开发场景：强制刷新凭证以排除缓存干扰

## 参数说明

无入参。`revoke_auth` 通过请求已有的 `Authorization: Bearer <jwt>` header 识别当前用户。

## 返回值

| 字段 | 说明 |
|---|---|
| `success` | 固定 `true`；业务错误统一走 `code`（`AUTH_REQUIRED` / `TOKEN_EXPIRED` / `UPSTREAM_ERROR`） |

## 执行流程

### 优先路径（`revoke_auth` 已发布）

1. 调用 `revoke_auth`（无入参）
2. 根据返回：
   - `success=true` → 下一步
   - `code=AUTH_REQUIRED` / `TOKEN_EXPIRED` → 本地已无有效会话，直接下一步
   - `code=UPSTREAM_ERROR` → 提示用户"服务端撤销失败"，再询问是否仅做本地清理（降级路径）
3. 本地清理：

   ```bash
   node {baseDir}/scripts/persist_auth.js --clear
   ```

   stdout：`{ "type": "auth_cleared", "cleared": true|false }`（`false` 表示本地原本就没有凭证文件）
4. 告知用户"已退出登录，下次使用需重新扫码"

### 降级路径（`revoke_auth` 未发布 / 调用失败）

1. 仅执行 `persist_auth.js --clear`
2. 提示用户：服务端 token 仍在自然过期时失效；如需立即下线，可到 Keep App「我 → 设置 → 登录设备管理」手动移除该会话

## `revoke_auth` 与 `--clear` 的职责

| 步骤 | 作用 |
|---|---|
| `revoke_auth`（MCP） | **服务端**失效 token，防止泄露的 JWT 在过期前被滥用 |
| `persist_auth.js --clear`（本地） | **本地**从 `~/.keepai/.env` 中删除 `keep_auth_token` / `keep_auth_token_expired` / `keep_username` 相关行 |

两步缺一都有缺口：

- 只 revoke 不 clear：本地 env 残留旧 token，下次被运行器注入到 `Authorization` 再请求会收到 `TOKEN_EXPIRED`，体验差
- 只 clear 不 revoke：本地不再用，但如果之前该 token 已被外泄，在自然过期前仍可用

## 相关错误码

| 错误码 | 含义 | 应对 |
|---|---|---|
| `AUTH_REQUIRED` | 未携带 token | 视为已退出，直接本地 `--clear` |
| `TOKEN_EXPIRED` | token 已过期 | 同上 |
| `UPSTREAM_ERROR` | Keep 服务异常 | 提示用户，再询问是否仅做本地清理 |

## 运行器适配

详见 [SKILL.md · Runner](../SKILL.md#runner)。

- **exec 方式**：`revoke_auth` 通过 `node {baseDir}/scripts/mcp-call.js revoke_auth '{}'` 调；`--clear` 通过 `exec` 执行
- **原生 MCP 方式**：`revoke_auth` 走 MCP `tools/call`；`--clear` 单独 exec 执行

## 发布状态（维护者信息）

Gateway 侧 `revoke_auth.json` 当前为 `status: "draft"`，待运维确认 `/account/v2/logout` 在 MCP Gateway 侧 `x-device-id` 固定值下能正确失效 token 后置为 `published`。**Agent 不需要感知此字段**，直接用 `tools/list` 的结果判定是否可调即可。
