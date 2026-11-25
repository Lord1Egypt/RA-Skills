import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("../scripts/headers.js", import.meta.url));
const run = (args, input) =>
  new Promise((resolve) => {
    const p = execFile(process.execPath, [SCRIPT, ...args], (err, stdout) =>
      resolve({ code: err?.code ?? 0, stdout }),
    );
    if (input != null) {
      p.stdin.write(input);
      p.stdin.end();
    }
  });

const GOOD = `HTTP/1.1 200 OK
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=()
Server: nginx
Set-Cookie: s=abc; Secure; HttpOnly; SameSite=Lax
`;

const BAD = `HTTP/1.1 200 OK
Server: Apache/2.4.41 (Ubuntu)
Set-Cookie: s=abc
`;

test("hardened headers pass", async () => {
  const { code, stdout } = await run(["-"], GOOD);
  assert.equal(code, 0);
  const r = JSON.parse(stdout);
  assert.equal(r.summary.fail, 0);
  assert.equal(r.summary.warn, 0);
});

test("bare headers produce warns + cookie fail", async () => {
  const { code, stdout } = await run(["-"], BAD);
  assert.equal(code, 1);
  const r = JSON.parse(stdout);
  assert.ok(r.summary.warn >= 5);
  assert.equal(r.checks.find((c) => c.id === "cookie-flags").status, "fail");
});

test("usage error exits 2", async () => {
  const { code } = await run([]);
  assert.equal(code, 2);
});

test("redirect + CORS headers produce upgrade hint", async () => {
  const { stdout } = await run(
    ["-"],
    "HTTP/1.1 301 Moved\nLocation: https://x.com/\nAccess-Control-Allow-Origin: *\n",
  );
  const r = JSON.parse(stdout);
  assert.equal(r.upgrade.skill, "http-header-audit");
  assert.ok(r.upgrade.reasons.length >= 2);
});

test("plain 200 headers have no upgrade field", async () => {
  const { stdout } = await run(["-"], GOOD);
  assert.equal(JSON.parse(stdout).upgrade, undefined);
});
