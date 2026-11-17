# 失败模式与处理

> Build 不总是 SUCCEEDED。Build 返回的 `status` + `failure_kind` + `diagnostics` 共同决定下一步动作。

## 状态机

```text
QUEUED ──▶ BUILDING ──▶ SUCCEEDED (终态)
                │      └▶ FAILED   (终态,带 failure_kind)
                │      └▶ CANCELLED(终态,带 cancel_reason)
                └─────▶ CANCELLING ──▶ CANCELLED
```

`availability=UNAVAILABLE` 是**信号态**,不是终态,带 `retry_after_seconds` 时按有界重试处理。

## failure_kind 处理表

| `failure_kind` | 含义 | 动作 | 迭代循环是否触发 |
|----------------|------|------|------------------|
| `SOURCE_INVALID` | Source 静态分析失败,带结构化 `diagnostics` | 修 Source,**新幂等 key**,**新一次** Build | 是 |
| `ARTIFACT_INVALID` | 目标产物不通过 Dify schema 校验 | 留 Build ID 报告主仓库,**不改 Source** | 否 |
| `REPAIR_EXHAUSTED` | 系统侧判断修复预算耗尽(诊断循环超过阈值) | 重新审视设计,看 `iteration-loop.md` 停止信号 | 否,需人工 |
| `TARGET_INCOMPATIBLE` | 当前 target 无法保留 Source 语义 | **改设计或换 target**,**不改 Source** | 否 |
| `POLICY` | 管理策略禁止(配额/付费/合规) | 报告用户,引导管理后台;**不改 Source** | 否 |
| `TARGET_UNAVAILABLE` | 目标 Dify 不可用 | 等待 `retry_after_seconds` 重试;**不改 Source** | 否 |
| `TIMEOUT` | 编译超时 | 重试 1 次;**不改 Source**;改 Source 只在第 2 次仍超时 | 视情况 |
| `SERVICE` | NodeCoda MCP / Workspace 内部错误 | 等 + 重试;**不改 Source** | 否 |

`DATA_INTEGRITY`(隐含在 artifact 缺失/不一致场景):**绝不能补值或猜测默认 target**,直接停止。

## 认证 / 配置失败(工具调用 401)

MCP 工具存在但调用直接返回 `401 NO_KEY` 时,**不是凭据/配置缺失问题,而是环境传播问题**:

| 错误 | 含义 | 排查与动作 |
|------|------|-----------|
| `401 NO_KEY` | MCP server 在请求时读 `process.env.NODECODA_KEY` 为空 | ① 在你**实际启动 Codex 的那个 shell** 里 `echo $NODECODA_KEY`——GUI/其他终端启动的 Codex 不继承别的 shell profile;② 在 `config.toml` 的 `[mcp_servers.nodecoda]` 加 `env = { NODECODA_KEY = "${NODECODA_KEY}" }` 显式传入 stdio 子进程;③ 重启 agent 会话后重试 |
| `401 UNAUTHORIZED` | key 存在但无效/被拒(如本地栈拒远程 key) | 核对 key 属于当前后端;本地 dev stack 只认本地数据库里的 sk- key(见 `.codex/config.example.toml` Alternative 3) |
| `401 UNAUTHORIZED`,响应里带字面量 `Bearer ${NODECODA_KEY}` | Codex 版本未做 `env` 值展开,把 `${...}` 当字面量发出去 | 升级 Codex;或直接在 `env` 块/客户端配置里写实际 key 值;或改用 `bearer_token_env_var = "NODECODA_KEY"`(HTTP 传输) |

**不绕过**:key 缺失时报告安装/环境指引,不要猜测凭据、不把 key 写进 Source / prompt / artifact / 报告。

## 各 kind 的诊断模板

### SOURCE_INVALID

```json
{
  "status": "FAILED",
  "failure_kind": "SOURCE_INVALID",
  "diagnostics": [
    { "code": "TYPE_MISMATCH", "severity": "error", "message": "expected string, got int", "location": { "line": 12, "column": 9 } }
  ]
}
```

**正确反应**:进 `iteration-loop.md` 的修复循环,只改 `location` 指向的位置,新幂等 key。

### TARGET_INCOMPATIBLE

```json
{
  "status": "FAILED",
  "failure_kind": "TARGET_INCOMPATIBLE",
  "diagnostics": [
    { "code": "CAPABILITY_BLOCKED", "severity": "error", "message": "feature X is not supported by target dify-1.16-graphon-0.6", "location": { "line": 8, "column": 1 } }
  ]
}
```

**正确反应**:
1. 看 `target-capabilities.md` 找替代写法
2. 没有合适替代 → 改设计
3. 实在绕不开 → 报告用户当前 target 不能满足,问是否要等支持

**禁止**:为了通过 Build 改写 Source 用更弱构造模拟。

### TIMEOUT

```json
{
  "status": "FAILED",
  "failure_kind": "TIMEOUT",
  "diagnostics": []
}
```

**正确反应**:
- Source 通常很大或包含很重操作,先看 Source 大小(64 KiB 上限,接近上限时裁剪)
- 重试 1 次,新幂等 key(因为是不同 Build 调用)
- 仍超时 → 大概率是设计问题(过深的循环、过多并行),回到需求分析

### SERVICE

```json
{
  "status": "FAILED",
  "failure_kind": "SERVICE",
  "diagnostics": []
}
```

**正确反应**:等服务恢复;`availability=UNAVAILABLE` 可能附带 `retry_after_seconds`,按它重试。**不改 Source**。

### POLICY

```json
{
  "status": "FAILED",
  "failure_kind": "POLICY",
  "diagnostics": [
    { "code": "QUOTA_EXHAUSTED", "severity": "error", "message": "monthly build quota exceeded" }
  ]
}
```

**正确反应**:停止,报告用户,引导订阅/付费/管理后台。**严禁**通过删代码"省配额"。

## 客户端/环境层 HTTP 错误（不是 Source 诊断）

`401 NO_KEY`、`400 WORKFLOW_BUILD_REQUEST_INVALID` 等来自网关/客户端的错误**不属于** `failure_kind`，不是 Source 修复信号：

- `401 NO_KEY`：MCP server 未继承 `NODECODA_KEY` → 走「公共部署 · REST 直连回退」（SKILL.md），或在启动 agent 的 shell 导出 key。
- `400 WORKFLOW_BUILD_REQUEST_INVALID`（REST 直连时）：缺 `Idempotency-Key` 请求头 → 补 header（见 gotchas G14）。
- 上述情况下**不要**改 Source、不要伪造构建成功、不要编造 build_id。

## availability=UNAVAILABLE

不是终态,带 `retry_after_seconds` 时:

- admission 最多重试 3 次
- 重试间隔服从 `retry_after_seconds`
- 不带 `retry_after_seconds` → 退避 1s → 2s → 4s
- 仍 UNAVAILABLE → 停止,报告用户

## 跨 Build 的一致性

Build 之间的"诊断集合"应**单调收敛**:

- error count 严格下降
- 新 error 出现(从未见过)→ 视为引入新 bug,**回退**到上一版 Source
- 同一 error 重复 3 次 → 视为结构性不可解决,**改设计**

## 报告结构

见 `iteration-loop.md` 末尾的"报告模板"。失败时额外带:

- 最后一次 Build 的 `failure_kind`
- 是否已尝试过修复
- 修复尝试次数 / 上限
- 建议下一步(具体动作,不是"再试一次")


## `WORKFLOW_BUILD_SERVICE_UNAVAILABLE` (public deployment)

**Symptom** — `POST /v1/workflow-builds` returns `503` with body:

```json
{ "code": 503, "message": "workflow build service is temporarily unavailable", "reason": "WORKFLOW_BUILD_SERVICE_UNAVAILABLE" }
```

**Root cause** — The MCP gateway's OAuth resource server middleware (`auth.RequireBearerToken` in the main NodeCoda repo's MCP server) rejects opaque `sk-...` keys with `401 token missing expiration` because it requires a JWT-style `exp` claim before consulting the custom introspect verifier. The Workspace catches the upstream 401 and maps it to 503.

**This is a known launch blocker for the whole service**: every Workflow Build submitted with an API key hits this path until the main NodeCoda repo fixes the auth wiring.

**Repair** —
- Not a Source issue; do not edit `.ncoda`.
- Fix the main NodeCoda repo: change the MCP server's auth wiring so it calls the introspect verifier directly instead of through `auth.RequireBearerToken`. Rebuild the MCP image, redeploy, retry.
- A working `/health` (`{"status":"ok","checks":{"database":"ok","redis":"ok"}}`) is **not** evidence the Build path is up; the MCP gateway can be live and still reject opaque keys.
