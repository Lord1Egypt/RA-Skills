/**
 * Insurance Broker Skill V2 — Comprehensive Tests
 *
 * Coverage:
 *  1. Metadata & schema validity
 *  2. Input validation (missing key, bad key, bad endpoint, GET)
 *  3. HTTP response branches (200, 401, 402, 403, 429, 500, non-JSON)
 *  4. Network edge cases (network error, timeout)
 *  5. Config override (custom baseUrl)
 *
 * Run: node test/test-all.js
 */

import assert from "node:assert";
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

let passCount = 0;
let failCount = 0;

// Speed up timeout tests
globalThis.process.env.ZHENINSURE_TIMEOUT_MS = "50";

function pass(msg) {
  process.stdout.write(`  \x1b[32m✓\x1b[0m ${msg}\n`);
  passCount++;
}

function fail(name, err) {
  process.stderr.write(`  \x1b[31m✗\x1b[0m ${name}\n    ${err}\n`);
  failCount++;
}

async function test(name, fn) {
  try {
    await fn();
    pass(name);
  } catch (e) {
    fail(name, e?.message ?? String(e));
  }
}

function assertMatch(actual, expected, msg = "mismatch") {
  const ok = Object.entries(expected).every(([k, v]) => actual[k] === v);
  if (!ok) throw new Error(`${msg}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
}

// ─────────────────────────────────────────
// fetch mock helpers
// ─────────────────────────────────────────

let _originalFetch = null;
let _mockNext = null;
let _mockCallCount = 0;
let _mockLastArgs = null;

function installFetchMock() {
  if (_originalFetch) return;
  _originalFetch = globalThis.fetch;
  globalThis.fetch = async (...args) => {
    _mockCallCount++;
    _mockLastArgs = args;
    const init = args[1];
    const signal = init?.signal;

    return new Promise((resolve, reject) => {
      if (signal?.aborted) {
        const err = new Error("The operation was aborted.");
        err.name = "AbortError";
        return reject(err);
      }

      const onAbort = () => {
        const err = new Error("The operation was aborted.");
        err.name = "AbortError";
        reject(err);
      };

      if (signal) signal.addEventListener("abort", onAbort, { once: true });

      if (_mockNext) {
        _mockNext().then((val) => {
          if (signal) signal.removeEventListener("abort", onAbort);
          resolve(val);
        }).catch((err) => {
          if (signal) signal.removeEventListener("abort", onAbort);
          reject(err);
        });
      } else {
        reject(new Error("fetch called without mock setup"));
      }
    });
  };
}

function uninstallFetchMock() {
  if (_originalFetch) {
    globalThis.fetch = _originalFetch;
    _originalFetch = null;
  }
  _mockNext = null;
  _mockCallCount = 0;
  _mockLastArgs = null;
}

function queueFetchResponse(status, body, contentType = "application/json", delay = 0) {
  _mockNext = () =>
    new Promise((resolve) => {
      const resp = {
        ok: status >= 200 && status < 300,
        status,
        headers: {
          get: (h) => (h.toLowerCase() === "content-type" ? contentType : null),
        },
        json: async () => body,
        text: async () => JSON.stringify(body),
      };
      if (delay) setTimeout(() => resolve(resp), delay);
      else resolve(resp);
    });
}

function queueFetchText(status, text) {
  _mockNext = () =>
    Promise.resolve({
      ok: status >= 200 && status < 300,
      status,
      headers: { get: (h) => (h.toLowerCase() === "content-type" ? "text/html" : null) },
      json: async () => { throw new Error("not json"); },
      text: async () => text,
    });
}

function queueFetchNetworkError(message) {
  _mockNext = () => Promise.reject(new Error(message));
}

function queueFetchTimeout() {
  // Never resolves so that AbortController aborts first.
  _mockNext = () => new Promise(() => {});
}

// ─────────────────────────────────────────
// Suite
// ─────────────────────────────────────────

process.stdout.write("\n=== Insurance Broker Skill V2 Tests ===\n\n");

await test("package.json is valid and has correct structure", () => {
  const raw = readFileSync(join(root, "package.json"), "utf-8");
  const pkg = JSON.parse(raw);
  assert.strictEqual(pkg.name, "insurance-broker");
  assert.strictEqual(pkg.version, "2.0.0");
  assert.strictEqual(pkg.type, "module");
  assert.ok(Array.isArray(pkg.keywords));
  assert.ok(pkg.keywords.some((k) => k.includes("skill") || k.includes("openclaw")));
});

await test("skill.json is valid JSON and defines proxy action", () => {
  const raw = readFileSync(join(root, "skill.json"), "utf-8");
  const s = JSON.parse(raw);
  assert.ok(s.name);
  assert.strictEqual(s.version, "2.0.0");
  assert.ok(Array.isArray(s.actions));
  assert.equal(s.actions.length, 1);
  assert.strictEqual(s.actions[0].name, "proxy");
  assert.strictEqual(s.actions[0].handler, "actions/proxy.js");
  assert.ok(s.requirements);
});

await test("README.md, SKILL.md, LICENSE all exist", () => {
  for (const f of ["README.md", "SKILL.md", "LICENSE"]) {
    assert.ok(existsSync(join(root, f)), `${f} missing`);
  }
});

await test("actions/index.js exports proxy function", async () => {
  const { proxy } = await import(join(root, "actions", "index.js"));
  assert.strictEqual(typeof proxy, "function");
});

await test("proxy handler is default exported function", async () => {
  const mod = await import(join(root, "actions", "proxy.js"));
  assert.strictEqual(typeof mod.proxy, "function");
  assert.strictEqual(typeof mod.default, "function");
});

// ── Validation tests (no network) ──

await test("proxy: missing API key → missing_api_key", async () => {
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  const res = await proxy({ args: { endpoint: "/api/v1/skill/chat/conversations", method: "POST" } });
  assertMatch(res, { success: false, error: "missing_api_key" });
  assert.ok(res.message.includes("未配置"));
  assert.ok(res.action?.url);
});

await test("proxy: invalid API key format → invalid_api_key_format", async () => {
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/conversations", method: "POST" },
    secrets: { ZHENINSURE_API_KEY: "bad-key-123" },
  });
  assertMatch(res, { success: false, error: "invalid_api_key_format" });
});

await test("proxy: forbidden endpoint → forbidden_endpoint", async () => {
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  const res = await proxy({
    args: { endpoint: "/api/v1/admin/delete-everything", method: "POST" },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });
  assertMatch(res, { success: false, error: "forbidden_endpoint" });
  assert.ok(res.message.includes("端点不可用"));
});

await test("proxy: wrong method for endpoint → forbidden_endpoint", async () => {
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/conversations", method: "GET" },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });
  assertMatch(res, { success: false, error: "forbidden_endpoint" });
});

// ── HTTP response branches (mocked fetch) ──

process.stdout.write("\n  (HTTP branches — mocked fetch)\n");

await test("proxy: 200 OK → success with cost", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(200, { conversation_id: "conv_001", title: "保险咨询" });

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/conversations", method: "POST" },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: true, cost: "Free" });
  assert.strictEqual(res.data.conversation_id, "conv_001");
  assert.ok(res.message.includes("成功"));

  // verify request headers
  const [url, init] = _mockLastArgs;
  assert.ok(url.includes("/api/v1/skill/chat/conversations"));
  assert.strictEqual(init.headers.Authorization, "Bearer sk_live_12345678901234567890123456789012");
  assert.ok(init.headers["User-Agent"].includes("ZhenInsure-Skill"));
  assert.ok(init.signal);

  uninstallFetchMock();
});

await test("proxy: 200 with non-JSON body → success with raw_body", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchText(200, "<html>some html</html>");

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/handoff", method: "POST", body: {} },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: true });
  assert.strictEqual(res.data.raw_body, "<html>some html</html>");
  uninstallFetchMock();
});

await test("proxy: 401 Unauthorized → unauthorized + action link", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(401, { detail: "Invalid token" });

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/messages", method: "POST", body: { conversation_id: "c", content: "hi" } },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: false, error: "unauthorized", status: 401 });
  assert.ok(res.message.includes("鉴权失败"));
  assert.ok(res.action?.url);
  uninstallFetchMock();
});

await test("proxy: 402 Payment Required → insufficient_balance + recharge action", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(402, { detail: "余额不足" });

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/messages", method: "POST", body: {} },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: false, error: "insufficient_balance", status: 402 });
  assert.ok(res.message.includes("余额不足"));
  assert.strictEqual(res.action?.type, "recharge");
  uninstallFetchMock();
});

await test("proxy: 403 with balance hint → insufficient_balance", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(403, { detail: "insufficient balance for this call" });

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/messages", method: "POST", body: {} },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: false, error: "insufficient_balance" });
  uninstallFetchMock();
});

await test("proxy: 403 without balance hint → forbidden", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(403, { detail: "Access denied" });

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/conversations", method: "POST" },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: false, error: "forbidden" });
  uninstallFetchMock();
});

await test("proxy: 429 Rate Limit → rate_limited", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(429, { detail: "Too many requests" });

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/messages", method: "POST", body: {} },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: false, error: "rate_limited" });
  assert.ok(res.message.includes("限流"));
  uninstallFetchMock();
});

await test("proxy: 500 Server Error → server_error", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(500, { detail: "Database error" });

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/messages", method: "POST", body: {} },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: false, error: "server_error" });
  assert.ok(res.message.includes("服务端错误"));
  uninstallFetchMock();
});

await test("proxy: 418 I'm a teapot → api_error (fallback)", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(418, { detail: "I'm a teapot" });

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/messages", method: "POST", body: {} },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: false, error: "api_error", status: 418 });
  uninstallFetchMock();
});

// ── Network edge cases ──

process.stdout.write("\n  (Network edge cases)\n");

await test("proxy: network failure → network_error with message", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchNetworkError("getaddrinfo ENOTFOUND www.zhenins.com");

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/messages", method: "POST", body: {} },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: false, error: "network_error" });
  assert.ok(res.message.includes("网络失败"));
  uninstallFetchMock();
});

await test("proxy: timeout → timeout error", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchTimeout();

  const res = await proxy({
    args: { endpoint: "/api/v1/skill/chat/messages", method: "POST", body: {} },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  assertMatch(res, { success: false, error: "timeout" });
  assert.ok(/\d+\s*ms/.test(res.message), `Expected timeout message with ms, got: ${res.message}`);
  uninstallFetchMock();
});

// ── Config override ──

process.stdout.write("\n  (Config & misc)\n");

await test("proxy: config overrides baseUrl", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(200, {});

  await proxy({
    config: { ZHENINSURE_BASE_URL: "https://staging.zhenins.com" },
    args: { endpoint: "/api/v1/skill/chat/conversations", method: "POST" },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  const [url] = _mockLastArgs;
  assert.ok(url.startsWith("https://staging.zhenins.com"));
  uninstallFetchMock();
});

await test("proxy: trailing slashes stripped from baseUrl", async () => {
  installFetchMock();
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(200, {});

  await proxy({
    config: { ZHENINSURE_BASE_URL: "https://api.zhenins.com/" },
    args: { endpoint: "/api/v1/skill/chat/conversations", method: "POST" },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  const [url] = _mockLastArgs;
  assert.strictEqual(url, "https://api.zhenins.com/api/v1/skill/chat/conversations");
  uninstallFetchMock();
});

await test("proxy: env overrides baseUrl via process.env", async () => {
  installFetchMock();
  process.env.ZHENINSURE_BASE_URL = "https://env-base.zhenins.com";
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  queueFetchResponse(200, {});

  await proxy({
    args: { endpoint: "/api/v1/skill/chat/conversations", method: "POST" },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });

  const [url] = _mockLastArgs;
  assert.ok(url.startsWith("https://env-base.zhenins.com"));

  delete process.env.ZHENINSURE_BASE_URL;
  uninstallFetchMock();
});

await test("proxy: missing endpoint → missing_endpoint", async () => {
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  const res = await proxy({
    args: { method: "POST" },
    secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
  });
  assertMatch(res, { success: false, error: "missing_endpoint" });
});

await test("proxy: cost table covered for all allowed endpoints", async () => {
  const { proxy } = await import(join(root, "actions", "proxy.js"));
  installFetchMock();

  const cases = [
    { ep: "/api/v1/skill/chat/conversations", method: "POST", expCost: "Free" },
    { ep: "/api/v1/skill/chat/messages", method: "POST", expCost: "¥0.15" },
    { ep: "/api/v1/skill/chat/handoff", method: "POST", expCost: "Free" },
  ];

  for (const c of cases) {
    queueFetchResponse(200, { ok: true });
    const res = await proxy({
      args: { endpoint: c.ep, method: c.method, body: {} },
      secrets: { ZHENINSURE_API_KEY: "sk_live_12345678901234567890123456789012" },
    });
    assert.strictEqual(res.cost, c.expCost, `Expected cost ${c.expCost} for ${c.ep}`);
  }
  uninstallFetchMock();
});

// ── Summary ──

process.stdout.write(`\n═══ Results ═══\n`);
process.stdout.write(`  Passed: ${passCount}\n`);
process.stdout.write(`  Failed: ${failCount}\n`);
process.stdout.write(`  Total:  ${passCount + failCount}\n\n`);

if (failCount > 0) {
  process.exitCode = 1;
} else {
  process.stdout.write(`🎉 All tests passed.\n\n`);
}
