import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("../scripts/harmap.js", import.meta.url));
const run = (args) =>
  new Promise((resolve) => {
    execFile(process.execPath, [SCRIPT, ...args], (err, stdout) =>
      resolve({ code: err?.code ?? 0, stdout }),
    );
  });

const har = {
  log: {
    entries: [
      { request: { method: "GET", url: "https://api.x.com/users/123" }, response: { status: 200, content: { mimeType: "application/json" } } },
      { request: { method: "GET", url: "https://api.x.com/users/456" }, response: { status: 200, content: { mimeType: "application/json" } } },
      { request: { method: "POST", url: "https://api.x.com/login" }, response: { status: 401, content: { mimeType: "application/json" } } },
      { request: { method: "GET", url: "https://cdn.x.com/logo.png" }, response: { status: 200, content: { mimeType: "image/png" } } },
    ],
  },
};

test("groups endpoints with normalized paths", async () => {
  const f = path.join(await fs.mkdtemp(path.join(os.tmpdir(), "har-")), "cap.har");
  await fs.writeFile(f, JSON.stringify(har));
  const { code, stdout } = await run([f]);
  assert.equal(code, 0);
  const r = JSON.parse(stdout);
  assert.equal(r.staticSkipped, 1);
  assert.equal(r.endpoints.length, 2);
  assert.equal(r.endpoints[0].path, "/users/:id");
  assert.equal(r.endpoints[0].count, 2);
});

test("missing arg exits 2", async () => {
  const { code } = await run([]);
  assert.equal(code, 2);
});

test("non-GET/query/auth evidence produces upgrade hint", async () => {
  const har2 = {
    log: {
      entries: [
        {
          request: {
            method: "POST",
            url: "https://api.x.com/login?next=/",
            postData: { text: "{}" },
            headers: [{ name: "authorization", value: "x" }],
          },
          response: { status: 200, content: { mimeType: "application/json" } },
        },
      ],
    },
  };
  const f = path.join(await fs.mkdtemp(path.join(os.tmpdir(), "har-up-")), "cap.har");
  await fs.writeFile(f, JSON.stringify(har2));
  const { stdout } = await run([f]);
  const r = JSON.parse(stdout);
  assert.equal(r.upgrade.skill, "har-to-api-map");
  assert.ok(r.upgrade.reasons.length >= 3);
});

test("plain GET inventory has no upgrade field", async () => {
  const har3 = {
    log: {
      entries: [
        {
          request: { method: "GET", url: "https://api.x.com/items" },
          response: { status: 200, content: { mimeType: "application/json" } },
        },
      ],
    },
  };
  const f = path.join(await fs.mkdtemp(path.join(os.tmpdir(), "har-cl-")), "cap.har");
  await fs.writeFile(f, JSON.stringify(har3));
  const { stdout } = await run([f]);
  assert.equal(JSON.parse(stdout).upgrade, undefined);
});
