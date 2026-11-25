import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("../scripts/decode.js", import.meta.url));
const run = (args, input) =>
  new Promise((resolve) => {
    const p = execFile(process.execPath, [SCRIPT, ...args], (err, stdout) =>
      resolve({ code: err?.code ?? 0, stdout }),
    );
    if (input != null) { p.stdin.write(input); p.stdin.end(); }
  });

const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
const tok = b64({ alg: "HS256", typ: "JWT" }) + "." +
  b64({ sub: "u1", password: "hunter2-secret-value", exp: Math.floor(Date.now() / 1000) + 3600 }) + ".sig";

test("decodes a valid token and masks secrets", async () => {
  const { code, stdout } = await run([tok]);
  assert.equal(code, 0);
  const r = JSON.parse(stdout);
  assert.equal(r.valid, true);
  assert.equal(r.expStatus, "ok");
  assert.match(r.claims.password, /^fp: hunt…/);
  assert.equal(stdout.includes("hunter2-secret-value"), false);
});

test("expired token exits 1", async () => {
  const t = b64({ alg: "HS256" }) + "." + b64({ exp: 1000 }) + ".s";
  const { code, stdout } = await run([t]);
  assert.equal(code, 1);
  assert.equal(JSON.parse(stdout).expStatus, "expired");
});

test("malformed token reports invalid", async () => {
  const { code, stdout } = await run(["not-a-jwt"]);
  assert.equal(code, 1);
  assert.equal(JSON.parse(stdout).valid, false);
});

test("stdin input works", async () => {
  const { code, stdout } = await run(["-"], tok);
  assert.equal(code, 0);
  assert.equal(JSON.parse(stdout).valid, true);
});

test("kid header produces upgrade hint", async () => {
  const t = b64({ alg: "RS256", kid: "key-1" }) + "." + b64({ sub: "u" }) + ".s";
  const { stdout } = await run([t]);
  const r = JSON.parse(stdout);
  assert.equal(r.upgrade.skill, "jwt-inspector");
  assert.ok(r.upgrade.reasons.length > 0);
});

test("plain RS256 token has no upgrade field", async () => {
  const t = b64({ alg: "RS256", typ: "JWT" }) + "." + b64({ sub: "u" }) + ".sig";
  const { stdout } = await run([t]);
  assert.equal(JSON.parse(stdout).upgrade, undefined);
});
