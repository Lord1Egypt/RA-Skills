# NodeCoda MCP Workflow Build Contract

The public service exposes one asynchronous outcome: build a specific NodeCoda Source revision for an explicit Build Target.

## Build

Call `build_dify_workflow` with all fields present:

```json
{
  "source": "@language nodecoda/1\n@mode workflow\nfunction main(string query) -> string { return query; }\n",
  "source_filename": "demo.ncoda",
  "language_identity": "nodecoda/1",
  "target_profile": "dify-1.16-graphon-0.6",
  "idempotency_key": "demo-build-1"
}
```

> **Transport requirement (live gateway, verified 2026-08-14):** the gateway
> requires the `Idempotency-Key` HTTP header to **echo** the body
> `idempotency_key` — sending it in only one place is rejected with
> `400 WORKFLOW_BUILD_REQUEST_INVALID`. The MCP servers in this repo
> (`mcp-stdio-server.mjs`, `mcp-http-server.mjs`) already forward both, so MCP
> callers need to do nothing extra; **direct REST callers must set both** (see
> `references/public-service.md` for the curl form).

A successful admission returns `QUEUED`, a `build_id`, the selected identity fields, and `poll_after_ms`. An unavailable admission returns `availability=UNAVAILABLE`, a `failure_kind`, and sometimes `retry_after_seconds`; it does not return a usable Build identity.

### Guest admission statuses (try.nodecoda.com, no key)

> **Transport (verified 2026-08-15):** with no `NODECODA_KEY` the skill talks to
> **`https://try.nodecoda.com/mcp`** over Streamable-HTTP JSON-RPC (sessionful:
> initialize issues a `Mcp-Session-Id` header, responses are SSE `data:` frames,
> tool results are double-encoded JSON in `result.content[0].text`). try's `/v1`
> REST surface — like www's — strictly rejects the placeholder key with
> `401 INVALID_API_KEY`; guest admission exists ONLY on `/mcp`. The try gateway
> returns lowercase poll statuses (`succeeded`) and inlines the artifact in
> `artifact.content`; the client normalizes poll statuses to the documented
> uppercase contract below (admission statuses `queued`/`throttled`/`exhausted`
> stay lowercase).

On the free-try instance the admission answer is a **structured JSON status**
(HTTP 200, inside `data`) — not a hard error, unless the global budget is
exhausted (then HTTP 429 `GUEST_QUOTA_EXHAUSTED`):

| status | fields | meaning / handling |
|---|---|---|
| `queued` | `build_id`, `poll_after_ms`, `quota { mode, success, success_used, diagnostic, resets_in_seconds, register_hint }` | admitted; poll per `poll_after_ms` (server paces it to 2000 ms when ≥80% of the daily cap is used). `quota.success_used` is the low-key "used N times" counter; never render remaining/countdown/scarcity copy. |
| `throttled` | `reason` (`device_rate` / `ip_quota`), `retry_after_ms`, `quota` | transient rate tier; no `build_id`. Client sleeps `retry_after_ms` and replays the **same** submission (same idempotency key — a throttled admission created no build), bounded ≤3. The MCP servers in this repo do this automatically and annotate the final still-throttled payload with `_client_retries` (client-side field, never sent by the gateway). |
| `exhausted` | `code=GUEST_QUOTA_EXHAUSTED`, `message`, `quota`, `register_hint` | device daily quota soft stop (**NOT an error**, do not retry). Render `message` (server-authored gentle copy) + used count; append registration copy only when `register_hint: true`. |

`exhausted` is passed through untouched — it is a product state, not a failure.

> Live gateway note (verified 2026-08-12): the public gateway wraps every
> response as `{ "code": 0, "message": "...", "data": { ... } }`. The MCP
> servers in this repo (`mcp-stdio-server.mjs`, `mcp-http-server.mjs`) unwrap
> `data` before returning tool results, so the shapes below are what the agent
> actually receives. Error responses without a `data` key pass through as-is.

The same idempotency key is valid only for an exact replay. Any Source, filename, language identity, or target profile change requires a new key.

> **Header 要求（实证 2026-08-14）**：公网网关要求幂等 key **同时**出现在 body 的 `idempotency_key` 字段和 `Idempotency-Key` 请求头中；只放 body 直连 REST 会返回 `400 WORKFLOW_BUILD_REQUEST_INVALID`。MCP server 已自动双份转发，REST 直连必须自己带 header。

### Guest wire protocol — complete runnable example (try /mcp, no key)

> 这是 guest 路径的**完整可复现配方**（会话式 JSON-RPC over Streamable HTTP）。
> 本仓库已把它脚本化：`npx -y @nodecoda/skill build <file.ncoda> --trace` 打印的就是下面
> 这段交换的实时日志（`initialize` → `notifications/initialized` → `tools/call` →
> SSE `data:` 帧 → 双重解码 → 轮询）。下面的脚本只依赖 Node 18+ 内建 `fetch`，
> 可直接复制运行；无需 API key。**注意本段是 try guest；www 生产端（key 路径、
> 无状态）见 `references/public-service.md`「传输约定（Streamable HTTP，www 生产端）」**。

```js
// guest-build-recipe.mjs — run with: node guest-build-recipe.mjs <source.ncoda>
// Node 18+ (global fetch). No key, no MCP client, no repo dependency.
import { readFile } from 'node:fs/promises';

const URL   = process.env.NODECODA_MCP_JSONRPC_URL || 'https://try.nodecoda.com/mcp';
const DEVICE = process.env.NODECODA_DEVICE_ID || 'custom-device-0001'; // stable per install
const TARGET = 'dify-1.16-graphon-0.6';

function headers(sessionId) {
  return {
    'Content-Type': 'application/json',
    // Guest placeholder key: try's /mcp admits it as a guest build; its /v1
    // REST surface (and www's) strictly rejects it with 401 INVALID_API_KEY.
    Authorization: 'Bearer sk-try-placeholder',
    'X-NodeCoda-Device-Id': DEVICE,
    'X-NodeCoda-Client': 'guest-recipe/0.1',
    ...(sessionId ? { 'Mcp-Session-Id': sessionId } : {}), // MUST echo on later requests
  };
}

// POST a JSON-RPC message; return parsed messages from SSE `data:` frames
// (tolerates plain application/json responses too).
async function post(body, sessionId) {
  const res = await fetch(URL, { method: 'POST', headers: headers(sessionId), body: JSON.stringify(body) });
  const raw = await res.text();
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${raw.slice(0, 300)}`);
  const msgs = raw.split('\n')
    .filter((l) => l.startsWith('data: ') && l !== 'data: [DONE]')
    .map((l) => JSON.parse(l.slice(6)));
  if (msgs.length === 0) { try { msgs.push(JSON.parse(raw)); } catch { /* keep-alive */ } }
  return msgs;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const unwrap = (payload) => (payload && typeof payload === 'object' && payload.data !== undefined ? payload.data : payload);
const terminal = new Set(['SUCCEEDED', 'FAILED', 'CANCELLED']);

async function main() {
  const file = process.argv[2];
  if (!file) throw new Error('usage: node guest-build-recipe.mjs <source.ncoda>');
  const source = await readFile(file, 'utf8');

  // 1) initialize — capture the Mcp-Session-Id RESPONSE header
  const initRes = await fetch(URL, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'initialize',
      params: { protocolVersion: '2025-03-26', capabilities: {}, clientInfo: { name: 'guest-recipe', version: '0.1' } } }),
  });
  if (!initRes.ok) throw new Error(`initialize HTTP ${initRes.status}`);
  const sessionId = initRes.headers.get('mcp-session-id');
  if (!sessionId) throw new Error('no Mcp-Session-Id returned — guest admission only on /mcp');
  console.log('session:', sessionId);

  // 2) notifications/initialized (fire-and-forget; server expects it)
  await post({ jsonrpc: '2.0', method: 'notifications/initialized', params: {} }, sessionId);

  // 3) tools/call build_dify_workflow — response is SSE data: frames
  const idemKey = `${file.replace(/\.ncoda$/, '')}-${Date.now()}`;
  const [admissionMsg] = await post({ jsonrpc: '2.0', id: 2, method: 'tools/call', params: {
    name: 'build_dify_workflow',
    arguments: { source, source_filename: file.split('/').pop(), language_identity: 'nodecoda/1',
      target_profile: TARGET, idempotency_key: idemKey },
  } }, sessionId);
  if (admissionMsg.error) throw new Error(`gateway error: ${JSON.stringify(admissionMsg.error)}`);
  // 4) tool result is DOUBLE-ENCODED: result.content[0].text holds the payload string
  const admission = unwrap(JSON.parse(admissionMsg.result.content[0].text));
  console.log('admission:', JSON.stringify(admission));
  if (admission.status === 'throttled' || admission.status === 'exhausted') return; // see statuses table above

  // 5) poll until terminal — try returns LOWERCASE statuses (queued/building/succeeded);
  //    normalize to the documented uppercase contract. Artifact is inline on success.
  const pollInterval = Math.max(Number(admission.poll_after_ms) || 1000, 500);
  for (;;) {
    await sleep(pollInterval);
    const [msg] = await post({ jsonrpc: '2.0', id: 3, method: 'tools/call', params: {
      name: 'get_workflow_build', arguments: { build_id: admission.build_id },
    } }, sessionId);
    const rec = unwrap(JSON.parse(msg.result.content[0].text));
    const status = (rec.status ?? '').toUpperCase();
    console.log('poll:', status);
    if (terminal.has(status)) {
      if (status === 'SUCCEEDED') console.log('artifact:', rec.artifact?.content ?? '(inline content present)');
      process.exit(status === 'SUCCEEDED' ? 0 : 2);
    }
  }
}

main().catch((e) => { console.error(e.message); process.exit(1); });
```

要点（与 `scripts/mcp-core.mjs` 的 `JsonRpcUpstream` 完全对应）：

1. **会话头**：`initialize` 的响应头 `Mcp-Session-Id` 必须在后续每个请求回显；
2. **SSE 解析**：POST 响应是 `data: <jsonrpc>` 帧（也可能直接 `application/json`，两种都容错）；
3. **双重编码**：工具结果在 `result.content[0].text` 里是**字符串化的 JSON**，先 parse 外层 JSON-RPC 再 parse 内层 payload；
4. **guest 占位 key** `sk-try-placeholder` + 设备头 `X-NodeCoda-Device-Id`（服务端只存 sha256）；
5. **状态归一化**：try 返回小写（`succeeded`），客户端按文档契约转大写；admission 的 `queued/throttled/exhausted` 保持小写；
6. **artifact 内联**：SUCCEEDED 的 poll 响应直接带 `artifact.content`（无需 `/artifact` 端点）。

`npx -y @nodecoda/skill build <file.ncoda> --trace` 内部就是这个流程，并把每一步真实交换打印到 stderr——以后不需要再逆向源码。

## Poll

Call `get_workflow_build`:

```json
{
  "build_id": "build_example"
}
```

Continue polling `QUEUED`, `BUILDING`, or `CANCELLING`. Terminal states are `SUCCEEDED`, `FAILED`, and `CANCELLED`. `availability=UNAVAILABLE` is also a stop condition unless bounded retry guidance is present.

A successful response contains an `artifact` with `media_type`, `sha256`, and `content`. The public gateway's poll response carries only artifact *metadata* (`artifact_sha256`, `artifact_size`, `artifact_media_type`, `artifact_available`) and serves the raw content at `GET /v1/workflow-builds/{build_id}/artifact`; the MCP servers fetch that endpoint best-effort on `SUCCEEDED` and attach it as `artifact.content` so the contract shape holds. Treat Source as the source of truth and the artifact as generated target-specific output.

> **REST 直连拉取 artifact**：直连 REST 时 poll 响应只带 metadata，内容需另行 `GET /v1/workflow-builds/{build_id}/artifact`（MCP server 会在 SUCCEEDED 时 best-effort 拉取并拼成 `artifact.content`，直连时无此便利）。

On `FAILED`, use `failure_kind` and structured `diagnostics`. Repair Source only for deterministic Source diagnostics. Target, policy, timeout, service, or data-integrity failures are not evidence for a Source edit.

## Cancel

Call `cancel_workflow_build` once after the overall polling deadline:

```json
{
  "build_id": "build_example"
}
```

Cancellation may return `CANCELLED`, `CANCELLING`, an already-terminal state, or `availability=UNAVAILABLE`. Continue bounded observation for at most 35 seconds after requesting cancellation.

## Invariants

- Source filename ends in `.ncoda`.
- Source and request identity are both `nodecoda/1`.
- Target profile is explicit and must match the returned Build.
- Public identity is always `build_id`.
- No generic operation selector exists.
- No implementation package, service code, or internal execution state is part of this contract.
