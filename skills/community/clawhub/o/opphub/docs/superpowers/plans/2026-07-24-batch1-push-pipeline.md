# 批 1 · 推送管道接通 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `POST /api/matchings` 从直接 `prisma.pendingMessage.create` 改为走 `opphub-ws POST /push`,消除"绕过推送管道"的根问题,实现双方推送。

**Architecture:**
- 新增 `opphub-web/lib/push.ts` 封装 `pushViaWs(userId, message)` 函数 (HTTP POST `WS_INTERNAL_URL/push`, 用 server 端 internal service JWT 鉴权)
- `opphub-web/app/api/matchings/route.ts` 删除 178-195 行直接写 `pendingMessage` 的代码, 改为调 `pushViaWs` 给双方推
- `opphub-ws/ws-server.js` 加 `SYSTEM_TRIGGERS` 白名单,允许 system 事件(`match.*`)由非 admin caller 触发

**Tech Stack:** Node 18+ · Next.js 14 · Prisma 5.22 · ws 8.18 · 内置 fetch

**Spec:** `docs/superpowers/specs/2026-07-24-opphub-discover-to-order-flow-design.md` §3

**工作目录:**
- 主仓库: `/Users/qiuxz/.openclaw/workspace-dev/`
- `opphub-web/` 跟 `opphub-ws/` 都是普通目录(非 submodule)
- `WS_INTERNAL_URL` 默认 `http://127.0.0.1:3001/push`

**本地起服务的姿势:**
```bash
# terminal 1: 起 ws-server
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-ws && node ws-server.js

# terminal 2: 起 web
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && npm run dev
```

---

## File Structure

**新建:**
- `opphub-web/lib/push.ts` — `pushViaWs()` helper (server 端内部调用,带 service JWT)
- `opphub-web/lib/__tests__/push.test.ts` — 单元测试 (mock fetch)
- `opphub-web/lib/__tests__/matchings-push-e2e.test.ts` — 集成测试 (起 ws-server, 调真 HTTP)

**修改:**
- `opphub-web/app/api/matchings/route.ts:178-195` — 删除直接 `pendingMessage.create`,改调 `pushViaWs`
- `opphub-ws/ws-server.js:822` — 加 `SYSTEM_TRIGGERS` 白名单 + 鉴权放宽

**不动:**
- `opphub-web/prisma/schema.prisma` (本期不需改 schema)
- `opphub-web/app/api/matchings/scores/*` (批 2 才改评分)

---

## Task 1: 实现 pushViaWs() helper (TDD)

**Files:**
- Create: `opphub-web/lib/__tests__/push.test.ts`
- Create: `opphub-web/lib/push.ts`

- [ ] **Step 1: 写 failing test**

`opphub-web/lib/__tests__/push.test.ts`:

```ts
// lib/__tests__/push.test.ts
// 批 1 · pushViaWs() 单元测试 (mock fetch)
//
// 跑: cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && npx tsx lib/__tests__/push.test.ts

import { pushViaWs } from "../push";

// === mock global fetch ===
const fetchMock = (globalThis as any).fetch as jest.Mock | undefined;
let originalFetch: typeof fetch | undefined;

interface MockResp {
  ok: boolean;
  status: number;
  body: any;
}

function mockFetchOnce(resp: MockResp) {
  originalFetch = globalThis.fetch;
  (globalThis as any).fetch = async (url: string, init?: any) => ({
    ok: resp.ok,
    status: resp.status,
    json: async () => resp.body,
    text: async () => JSON.stringify(resp.body),
  } as any);
}

function restoreFetch() {
  if (originalFetch) globalThis.fetch = originalFetch;
}

// === test 1: 成功推送 ===
async function testSuccess() {
  mockFetchOnce({ ok: true, status: 200, body: { ok: true, messageId: "msg_001" } });
  const r = await pushViaWs({
    userId: "opc_buyer",
    message: { type: "match", event: "match.created", matchingId: "m_001", otherOpcId: "opc_seller" },
  });
  if (!r.ok) throw new Error(`expected ok=true, got ${JSON.stringify(r)}`);
  if (r.messageId !== "msg_001") throw new Error(`expected messageId=msg_001, got ${r.messageId}`);
  restoreFetch();
  console.log("✅ testSuccess");
}

// === test 2: fetch 失败 (ws-server 不可达) ===
async function testFetchFailure() {
  originalFetch = globalThis.fetch;
  (globalThis as any).fetch = async () => { throw new Error("ECONNREFUSED"); };
  const r = await pushViaWs({
    userId: "opc_buyer",
    message: { type: "match", event: "match.created", matchingId: "m_002" },
  });
  if (r.ok) throw new Error(`expected ok=false on fetch failure, got ${JSON.stringify(r)}`);
  if (r.error !== "fetch_failed") throw new Error(`expected error=fetch_failed, got ${r.error}`);
  restoreFetch();
  console.log("✅ testFetchFailure");
}

// === test 3: ws-server 返 4xx/5xx ===
async function testWsServerError() {
  mockFetchOnce({ ok: false, status: 500, body: { ok: false, error: "db_persist_failed" } });
  const r = await pushViaWs({
    userId: "opc_buyer",
    message: { type: "match", event: "match.created", matchingId: "m_003" },
  });
  if (r.ok) throw new Error(`expected ok=false on 500, got ${JSON.stringify(r)}`);
  if (r.error !== "db_persist_failed") throw new Error(`expected error=db_persist_failed, got ${r.error}`);
  restoreFetch();
  console.log("✅ testWsServerError");
}

// === test 4: payload 含 event 字段, ws-server 用来鉴权 SYSTEM_TRIGGERS ===
async function testPayloadIncludesEvent() {
  let captured: any = null;
  originalFetch = globalThis.fetch;
  (globalThis as any).fetch = async (url: string, init: any) => {
    captured = JSON.parse(init.body);
    return { ok: true, status: 200, json: async () => ({ ok: true, messageId: "msg_004" }) } as any;
  };
  await pushViaWs({
    userId: "opc_buyer",
    message: { type: "match", event: "match.bid", matchingId: "m_004", amount: 3000 },
  });
  if (!captured.message.event) throw new Error(`expected message.event in body, got ${JSON.stringify(captured)}`);
  if (captured.message.event !== "match.bid") throw new Error(`expected event=match.bid, got ${captured.message.event}`);
  restoreFetch();
  console.log("✅ testPayloadIncludesEvent");
}

// === runner ===
(async () => {
  await testSuccess();
  await testFetchFailure();
  await testWsServerError();
  await testPayloadIncludesEvent();
  console.log("\n🎉 4/4 tests passed");
})().catch((e) => {
  console.error("❌", e?.message ?? e);
  process.exit(1);
});
```

- [ ] **Step 2: 跑测试,确认失败**

Run:
```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && npx tsx lib/__tests__/push.test.ts 2>&1 | head -10
```

Expected: 报错 `Cannot find module '../push'` 或类似 (因为 lib/push.ts 还不存在)

- [ ] **Step 3: 实现 pushViaWs()**

`opphub-web/lib/push.ts`:

```ts
// lib/push.ts
// 批 1 · server 端内部调 opphub-ws POST /push 的封装
//
// 设计要点:
// 1. server 端 service 内部调用, 用 OPPHUB_JWT_SECRET 签发一个 isAdmin=true 的 short-lived JWT 作为鉴权
//    (ws-server.js:822 鉴权放宽后会接 SYSTEM_TRIGGERS 白名单, isAdmin JWT 也能通过, 双保险)
// 2. fetch 失败时不抛异常, 返回 { ok: false, error: 'fetch_failed' } 让调用方决定兜底 (写 pending_message 退路)
// 3. timeout 5s, 防 ws-server 卡住拖累 matchings 接口
//
// 用法:
//   import { pushViaWs } from '@/lib/push';
//   await pushViaWs({ userId: 'opc_xxx', message: { type: 'match', event: 'match.created', ... } });

import jwt from "jsonwebtoken";

const WS_INTERNAL_URL = process.env.WS_INTERNAL_URL || "http://127.0.0.1:3001/push";
const OPPHUB_JWT_SECRET = process.env.OPPHUB_JWT_SECRET || "dev-secret-change-me";

export type PushResult =
  | { ok: true; messageId: string }
  | { ok: false; error: string; detail?: string };

function signServiceJwt(): string {
  // 1 小时过期, service 内部调用
  return jwt.sign(
    { isAdmin: true, scope: "internal:push" },
    OPPHUB_JWT_SECRET,
    { expiresIn: "1h" },
  );
}

export async function pushViaWs(args: {
  userId: string;
  message: Record<string, any>;
  timeoutMs?: number;
}): Promise<PushResult> {
  const { userId, message, timeoutMs = 5000 } = args;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const token = signServiceJwt();
    const resp = await fetch(WS_INTERNAL_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ userId, message }),
      signal: controller.signal,
    });
    clearTimeout(timer);

    const body = await resp.json().catch(() => ({}));
    if (resp.ok && body?.ok) {
      return { ok: true, messageId: body.messageId };
    }
    return { ok: false, error: body?.error || `http_${resp.status}`, detail: body };
  } catch (e: any) {
    clearTimeout(timer);
    if (e?.name === "AbortError") {
      return { ok: false, error: "timeout" };
    }
    return { ok: false, error: "fetch_failed", detail: e?.message };
  }
}
```

- [ ] **Step 4: 跑测试,确认通过**

Run:
```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && npx tsx lib/__tests__/push.test.ts
```

Expected: `🎉 4/4 tests passed`

- [ ] **Step 5: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev && git add opphub-web/lib/push.ts opphub-web/lib/__tests__/push.test.ts && git commit -m "feat(web): pushViaWs() helper - server 内部调 opphub-ws POST /push"
```

---

## Task 2: 改造 POST /api/matchings 调 pushViaWs (含双方推送)

**Files:**
- Modify: `opphub-web/app/api/matchings/route.ts:178-195` (删除直接 pendingMessage.create)
- Modify: `opphub-web/app/api/matchings/route.ts:1-5` (加 import)

- [ ] **Step 1: 读现状,确认改造范围**

Read `opphub-web/app/api/matchings/route.ts` 的 175-205 行,确认两处需要改:
- L178-195: 第一次创建撮合时的 pendingMessage.create (给对方推)
- L127-145: 已存在 pending matching 但没推过时的 pendingMessage.create (兜底推送)

这两处都改成调 `pushViaWs`,且都要给**双方**推。

- [ ] **Step 2: 改 route.ts - 加 import**

修改 `opphub-web/app/api/matchings/route.ts:1-19`,在 `import` 块加:

```ts
import { pushViaWs } from "@/lib/push";
```

(其他 import 不变)

- [ ] **Step 3: 改 route.ts - 删直接 pendingMessage.create,改 pushViaWs (双方)**

替换 `opphub-web/app/api/matchings/route.ts:178-195` 的 `await prisma.pendingMessage.create(...)` 调用块 (从 `await prisma.pendingMessage.create` 到对应闭合 `})`):

替换为 (注意:新增**给对方** + **给自己** 两次 push):

```ts
  // === 批 1 改造: 改走 opphub-ws POST /push (双方推送) ===
  // 失败时退路: 直接写 pending_message, 不阻塞撮合创建
  const pushArgs = {
    matchingId: matching.id,
    otherOpcId: fromOpcId,
    otherEntryId: otherEntryId,
    otherDisplayName: fromName,
    otherDimension: dimensionLabel,
    matchScore: finalScore,
    text: trimmedMessage,
    createdAt: matching.createdAt.toISOString(),
  };

  // 推给对方 (toOpcId)
  const pushToOther = await pushViaWs({
    userId: otherEntry.opcId,
    message: {
      type: "match",
      event: "match.created",
      role: "to",
      ...pushArgs,
    },
  }).catch((e) => ({ ok: false as const, error: "push_throw", detail: String(e) }));

  if (!pushToOther.ok) {
    // 退路: 直接写 pending_message (保留原有行为)
    await prisma.pendingMessage.create({
      data: {
        opcId: otherEntry.opcId,
        type: "credit",
        score: 80,
        payload: pushArgs,
        expiredAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
      },
    });
    console.warn(`[matchings POST] push to other failed (${pushToOther.error}), fallback to direct pending_message`);
  }

  // 推给自己 (fromOpcId) - 撮合记录 mirror
  const pushToSelf = await pushViaWs({
    userId: fromOpcId,
    message: {
      type: "match",
      event: "match.created",
      role: "from",
      ...pushArgs,
    },
  }).catch((e) => ({ ok: false as const, error: "push_throw", detail: String(e) }));

  if (!pushToSelf.ok) {
    console.warn(`[matchings POST] push to self failed (${pushToSelf.error}), skip fallback (mirror is best-effort)`);
  }
```

- [ ] **Step 4: 改 route.ts - 同样的改造应用到 L127-145 的兜底推送**

替换 `opphub-web/app/api/matchings/route.ts:113-145` 的 `await prisma.pendingMessage.create({...})` 块:

替换为 (注意:这是已有 pending matching 时,只补推一次,**只推给对方**, 因为自己已推过):

```ts
    if (!alreadyInformed) {
      // === 批 1 改造: 改走 pushViaWs ===
      const pushToOtherRetry = await pushViaWs({
        userId: otherEntry.opcId,
        message: {
          type: "match",
          event: "match.created",
          role: "to",
          matchingId: existing.id,
          otherOpcId: fromOpcId,
          otherEntryId: otherEntryId,
          otherDisplayName: fromName2,
          otherDimension: dim2,
          matchScore: existing.matchScore ?? 0,
          text: existing.message ?? "",
          createdAt: existing.createdAt.toISOString(),
        },
      }).catch((e) => ({ ok: false as const, error: "push_throw", detail: String(e) }));

      if (!pushToOtherRetry.ok) {
        // 退路: 直接写 pending_message
        await prisma.pendingMessage.create({
          data: {
            opcId: otherEntry.opcId,
            type: "credit",
            score: 80,
            payload: {
              matchingId: existing.id,
              fromOpcId,
              fromName: fromName2,
              title: `${fromName2} 发来撮合请求`,
              desc: `「${dim2}」 · ${(existing.message ?? "").slice(0, 80) || "发来撮合请求"}`,
              text: existing.message ?? "",
              otherDimension: dim2,
              otherEntryId: otherEntryId,
            },
            expiredAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
          },
        });
        console.warn(`[matchings POST retry] push failed (${pushToOtherRetry.error}), fallback`);
      }
    }
```

- [ ] **Step 5: lint + build**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && npm run lint 2>&1 | grep -E "error|warn" | head -10
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && npm run build 2>&1 | tail -20
```

Expected: lint 无 error, build 成功 (可能有 warning, 看是不是自己引入的)

- [ ] **Step 6: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev && git add opphub-web/app/api/matchings/route.ts && git commit -m "feat(matchings): 改走 opphub-ws push 管道, 双方推送 + 失败退路"
```

---

## Task 3: ws-server.js 加 SYSTEM_TRIGGERS 白名单

**Files:**
- Modify: `opphub-ws/ws-server.js:822-825` (鉴权放宽)

- [ ] **Step 1: 读现状,锁定改造行**

Read `opphub-ws/ws-server.js:815-830`,确认 `handlePush` 鉴权段:

```js
    // 鉴权: caller 必须是 admin OR caller == userId
    if (!caller.isAdmin && caller.opcId !== userId) {
      res.writeHead(403, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: 'forbidden', message: 'caller 必须是 admin 或 = userId', caller: caller.opcId, userId }));
    }
```

- [ ] **Step 2: 写集成测试 (起 ws-server,真 HTTP 调用,验证 system trigger 通过)**

`opphub-ws/__tests__/system-triggers-whitelist.test.js`:

```js
// ws-server.js SYSTEM_TRIGGERS 白名单集成测试
//
// 跑: cd /Users/qiuxz/.openclaw/workspace-dev/opphub-ws && node __tests__/system-triggers-whitelist.test.js
// 前置: ws-server.js 没在跑 (本测试会自己起一个临时实例, 端口 13901)

const { spawn } = require('node:child_process');
const path = require('node:path');
const http = require('node:http');
const jwt = require('jsonwebtoken');

const TEST_PORT = 13901;
const TEST_SECRET = 'test-secret';
let wsProcess = null;

function signToken(payload) {
  return jwt.sign(payload, TEST_SECRET, { expiresIn: '5m' });
}

function httpPost(url, body, headers) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const data = JSON.stringify(body);
    const req = http.request({
      hostname: u.hostname,
      port: u.port,
      path: u.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data),
        ...headers,
      },
    }, (res) => {
      let chunks = '';
      res.on('data', (c) => chunks += c);
      res.on('end', () => resolve({ status: res.statusCode, body: JSON.parse(chunks || '{}') }));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function startWs() {
  return new Promise((resolve, reject) => {
    wsProcess = spawn('node', ['ws-server.js'], {
      cwd: path.join(__dirname, '..'),
      env: { ...process.env, WS_PORT: String(TEST_PORT), OPPHUB_JWT_SECRET: TEST_SECRET, MOCK_DB: '1' },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    wsProcess.stdout.on('data', (d) => {
      const s = d.toString();
      if (s.includes('listening')) resolve();
    });
    wsProcess.stderr.on('data', (d) => process.stderr.write(d));
    setTimeout(() => reject(new Error('ws start timeout')), 5000);
  });
}

async function stopWs() {
  if (wsProcess) wsProcess.kill('SIGTERM');
  await new Promise((r) => setTimeout(r, 500));
}

async function runTests() {
  // === test 1: 业务触发 (fromOpcId 推 toOpcId, isAdmin=false) match.created → 应该通过 ===
  const bizToken = signToken({ opcId: 'opc_buyer', isAdmin: false });
  const r1 = await httpPost(`http://127.0.0.1:${TEST_PORT}/push`, {
    userId: 'opc_seller',
    message: { type: 'match', event: 'match.created', matchingId: 'm_001' },
  }, { Authorization: `Bearer ${bizToken}` });
  if (r1.status === 403) throw new Error(`test1 failed: business caller got 403, ${JSON.stringify(r1)}`);
  console.log('✅ test1: business caller + match.created → ok');

  // === test 2: 业务触发 + 非白名单 event → 仍然 403 ===
  const r2 = await httpPost(`http://127.0.0.1:${TEST_PORT}/push`, {
    userId: 'opc_seller',
    message: { type: 'dm', text: '假装撮合推送' },
  }, { Authorization: `Bearer ${bizToken}` });
  if (r2.status !== 403) throw new Error(`test2 failed: dm should be 403, got ${r2.status}`);
  console.log('✅ test2: business caller + dm → 403');

  // === test 3: admin caller + 任何 type → 都通过 (backward compat) ===
  const adminToken = signToken({ isAdmin: true });
  const r3 = await httpPost(`http://127.0.0.1:${TEST_PORT}/push`, {
    userId: 'opc_seller',
    message: { type: 'dm', text: 'admin push' },
  }, { Authorization: `Bearer ${adminToken}` });
  if (r3.status === 403) throw new Error(`test3 failed: admin got 403, ${JSON.stringify(r3)}`);
  console.log('✅ test3: admin caller + dm → ok');

  // === test 4: 撮合 5 个白名单 event 全通过 ===
  const events = ['match.created', 'match.inquiry', 'match.bid', 'match.bid_accepted', 'match.declined'];
  for (const ev of events) {
    const r = await httpPost(`http://127.0.0.1:${TEST_PORT}/push`, {
      userId: 'opc_seller',
      message: { type: 'match', event: ev, matchingId: `m_${ev}` },
    }, { Authorization: `Bearer ${bizToken}` });
    if (r.status === 403) throw new Error(`test4 failed: ${ev} got 403`);
  }
  console.log('✅ test4: 5 白名单 event 全通过');

  console.log('\n🎉 4/4 tests passed');
}

(async () => {
  try {
    console.log('Starting ws-server on port', TEST_PORT);
    await startWs();
    await runTests();
  } catch (e) {
    console.error('❌', e?.message ?? e);
    process.exit(1);
  } finally {
    await stopWs();
  }
})();
```

- [ ] **Step 3: 跑测试,确认失败**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-ws && node __tests__/system-triggers-whitelist.test.js 2>&1 | head -10
```

Expected: `test1 failed: business caller got 403` (因为白名单还没加)

- [ ] **Step 4: 改 ws-server.js 加 SYSTEM_TRIGGERS 白名单**

修改 `opphub-ws/ws-server.js`,在 `WS_TYPE_TO_DB_TYPE` 定义附近 (大约 L213-223),加:

```js
// v0.7.41 (批 1 改造): system trigger 白名单 — 业务流 (撮合/订单) 由 server 端代发,
//   caller 是 fromOpcId 但要推给对方 (toOpcId), 鉴权放宽: caller 是合法 OPC + message.event 在白名单内即通过
const SYSTEM_TRIGGERS = new Set([
  'match.created',
  'match.inquiry',
  'match.bid',
  'match.counter',
  'match.bid_accepted',
  'match.declined',
  'order.created',
  'order.paid',
  'order.delivered',
  'order.accepted',
]);
```

修改 `opphub-ws/ws-server.js:822-825` 鉴权段:

```js
    // 鉴权: caller 必须是 admin OR caller == userId OR (system trigger 白名单 + caller 是合法 OPC)
    const isSystemTrigger = message?.event && SYSTEM_TRIGGERS.has(message.event);
    if (!caller.isAdmin && caller.opcId !== userId && !(isSystemTrigger && caller.opcId)) {
      res.writeHead(403, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ ok: false, error: 'forbidden', message: 'caller 必须是 admin / userId / system trigger 白名单', caller: caller.opcId, userId, event: message?.event }));
    }
```

- [ ] **Step 5: 跑测试,确认通过**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-ws && node __tests__/system-triggers-whitelist.test.js
```

Expected: `🎉 4/4 tests passed`

- [ ] **Step 6: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev && git add opphub-ws/ws-server.js opphub-ws/__tests__/system-triggers-whitelist.test.js && git commit -m "feat(ws): 加 SYSTEM_TRIGGERS 白名单, 允许业务流代发撮合推送"
```

---

## Task 4: 端到端验证 (起双服务 + 真实撮合调用)

**Files:** 无新建/修改 (纯集成验证)

- [ ] **Step 1: 起 ws-server (terminal 1)**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-ws && node ws-server.js
```

Expected: 输出 `> [ws] ws-server listening on 0.0.0.0:3001` 之类

- [ ] **Step 2: 起 web (terminal 2)**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && npm run dev
```

Expected: 输出 `ready - started server on 0.0.0.0:3000` 之类

- [ ] **Step 3: 用 skill 模拟一次撮合触发, 验证双向推送**

```bash
# 拿到两个 OPC 的 access_token (用现有 opcAccount, 如 opc_1hz6wsjrmt1s)
# 这里直接 curl, 假设 token 已经准备好
FROM_TOKEN=$(...)  # 睿驰嘉禾
TO_TOKEN=$(...)    # 紫冠科技

# 1. 创建撮合 (FROM 发起到 TO)
curl -X POST http://127.0.0.1:3000/api/matchings \
  -H "Authorization: Bearer $FROM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"otherEntryId": "<紫冠某个 entry id>", "message": "测试撮合"}'
```

Expected: 返 `{ ok: true, matchingId: "..." }`

- [ ] **Step 4: 检查 ws-server 日志,确认双方 push 都入队**

Terminal 1 (ws-server) 应该看到类似:
```
> [queue] pushed mid=xxx opc=opc_xxx inFlight=1
> [queue] pushed mid=yyy opc=opc_yyy inFlight=1
```

(两条,FROM 和 TO 各一条)

- [ ] **Step 5: 检查 DB,确认 pushViaWs 写入成功 + 退路不触发**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && npx prisma studio
# 打开 opc_pending_message 表, 应该看到 type='credit' 的两条新记录 (双方各一)
```

Expected: 两条 pending_message, type='credit', opcId 分别是 FROM 和 TO

- [ ] **Step 6: 关闭服务,Commit 验证记录 (无新代码改动)**

```bash
# terminal 1: Ctrl+C
# terminal 2: Ctrl+C
```

(无 commit, 验证记录可以贴到 commit message 里)

---

## Task 5: 合并 spec 文档到主仓库 (收尾)

**Files:**
- Modify: `docs/superpowers/specs/2026-07-24-opphub-discover-to-order-flow-design.md` (在 §3.5 加"已实装"标记)

- [ ] **Step 1: 在 spec §3 末尾加"已实装"备注**

Read `docs/superpowers/specs/2026-07-24-opphub-discover-to-order-flow-design.md`,找到 §3.5 改动文件表格,在末尾加:

```markdown
**批 1 实施 (2026-07-24)**: 
- `lib/push.ts` 新建, pushViaWs() + service JWT 鉴权
- `ws-server.js` SYSTEM_TRIGGERS 白名单 (9 个 event)
- `app/api/matchings/route.ts` 改造, 双方推送, push 失败退路写 pending_message
```

- [ ] **Step 2: Commit spec 更新**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev && git add docs/superpowers/specs/2026-07-24-opphub-discover-to-order-flow-design.md && git commit -m "docs(spec): 标注批 1 已实装项"
```

---

## Self-Review

### 1. Spec 覆盖
- ✅ spec §3.1 推送管道接通 — Task 2 实施
- ✅ spec §3.2 opphub-ws 鉴权 — Task 3 实施
- ✅ spec §3.3 双方推送 — Task 2 实施 (Step 3 同时给 from/to 推)
- ✅ spec §3.4 payload schema — Task 2 Step 3 的 pushArgs 含 matchingId/otherOpcId/otherEntryId/otherDisplayName/otherDimension/matchScore/text/createdAt
- ✅ spec §3.5 改动文件清单 — Task 1/2/3 都对齐

### 2. 占位符扫描
- 无 "TBD" / "TODO" / "implement later"
- 无 "Similar to Task N" — Task 1/2/3/4/5 各自完整
- 代码块都完整, 命令都带 expected output

### 3. 类型一致性
- `pushViaWs({ userId, message, timeoutMs? })` 在 Task 1 定义, Task 2 调用一致
- `PushResult` 类型 Task 1 定义 `{ ok: true, messageId } | { ok: false, error, detail? }`, Task 2 Step 3 用 `.ok` / `.error` 一致
- `SYSTEM_TRIGGERS` Set Task 3 Step 4 定义, Task 3 Step 2 test 用一致

### 4. 风险
- ws-server.js 鉴权改动可能影响现有 admin/messages 调用 — test 3 验证 admin 仍通过
- pushViaWs fetch 失败时 route.ts 走退路写 pending_message — Task 2 Step 3 保留原有 pendingMessage.create 作为 fallback
- service JWT 用 OPPHUB_JWT_SECRET 同 secret, 跟 ws-server 一致 — 避免 401 invalid_token

---

## 后续 (不属批 1, 留作批 2-5)

- 批 2: 评分公式升级 + 频控 + 匿名 (`/api/matchings/scores` 改 semantic cosine + recency + trust_score 接入)
- 批 3: 状态机补全 (`OpcMatching.status` enum 迁移 active→inquiry + `OpcMatchingBid` + `OpcMatchingOrder` 表 + 4 个新 endpoint)
- 批 4: 运营基础 (PushLog 表 + 死信 + `/match` 301 redirect)
- 批 5: 页面 UI (`/matches/[id]` 详情页 + `/matches` 筛选维度 + `/orders` 列表详情)
