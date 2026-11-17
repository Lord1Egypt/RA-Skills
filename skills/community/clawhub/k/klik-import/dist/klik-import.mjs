#!/usr/bin/env node

// src/cli.ts
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline/promises";
import dns from "node:dns/promises";
import { fileURLToPath } from "node:url";

// src/schema.ts
var MAX_ITEMS = 5e3;
var MAX_BYTES = 10 * 1024 * 1024;
function validatePayload(payload) {
  if (!payload || typeof payload !== "object") {
    throw new Error("payload must be an object");
  }
  const p = payload;
  if (!p.schema_version)
    throw new Error("missing schema_version");
  if (p.schema_version !== "1.0")
    throw new Error(`unsupported schema_version: ${p.schema_version}`);
  if (!p.client || typeof p.client !== "object")
    throw new Error("missing client");
  if (!p.redaction || typeof p.redaction !== "object")
    throw new Error("missing redaction");
  if (!Array.isArray(p.collectors))
    throw new Error("collectors must be an array");
  let totalItems = 0;
  for (const c of p.collectors) {
    if (!c || typeof c !== "object")
      throw new Error("each collector must be an object");
    const col = c;
    if (!col.name || typeof col.name !== "string")
      throw new Error("collector missing name");
    if (!Array.isArray(col.items))
      throw new Error(`collector ${col.name} missing items array`);
    totalItems += col.items.length;
  }
  if (totalItems > MAX_ITEMS) {
    throw new Error(`total items ${totalItems} exceeds limit ${MAX_ITEMS}`);
  }
  const bytes = Buffer.byteLength(JSON.stringify(p), "utf8");
  if (bytes > MAX_BYTES) {
    throw new Error(`payload ${bytes} bytes exceeds 10 MB limit`);
  }
}

// src/redactor.ts
var RULES = [
  {
    kind: "api_key_generic",
    pattern: /\b(sk-[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z_-]{20,}|ghp_[A-Za-z0-9]{20,}|xox[bp]-[A-Za-z0-9-]{10,})/g
  },
  {
    kind: "bearer_header",
    pattern: /Bearer\s+[A-Za-z0-9._~+/\-]{20,}/g
  },
  {
    kind: "jwt",
    pattern: /eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/g
  },
  {
    kind: "private_key_pem",
    pattern: /-----BEGIN (?:RSA |EC |OPENSSH |)?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC |OPENSSH |)?PRIVATE KEY-----/g
  },
  {
    kind: "long_hex_secret",
    pattern: /\b[a-f0-9]{40,}\b/g
  }
];
var EMAIL_RULE = {
  kind: "email",
  pattern: /[\w.+-]+@[\w-]+\.[\w.-]+/g
};
function redactContent(content, opts) {
  let result = content;
  let count = 0;
  const rules = opts.redactEmail ? [...RULES, EMAIL_RULE] : RULES;
  for (const { kind, pattern } of rules) {
    const freshPattern = new RegExp(pattern.source, pattern.flags);
    result = result.replace(freshPattern, (_match) => {
      count++;
      return `<REDACTED:${kind}>`;
    });
  }
  return { result, count };
}

// src/uploader.ts
import https from "node:https";
import http from "node:http";
import zlib from "node:zlib";
var KLIK_BASE_URL = process.env.KLIK_BASE_URL ?? "https://hiklik.ai";
var KLIK_AUTH_URL = process.env.KLIK_AUTH_URL ?? KLIK_BASE_URL;
var KLIK_MEMORY_URL = process.env.KLIK_MEMORY_URL ?? KLIK_BASE_URL;
function request(method, url, body, headers) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const transport = parsed.protocol === "https:" ? https : http;
    const req = transport.request(
      {
        method,
        hostname: parsed.hostname,
        port: parsed.port || void 0,
        path: parsed.pathname + parsed.search,
        headers
      },
      (res) => {
        let data = "";
        res.on("data", (chunk) => data += chunk.toString());
        res.on("end", () => resolve({ status: res.statusCode ?? 0, body: data }));
      }
    );
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}
async function verifyCode(code, opts = {}) {
  const base = opts.baseUrl ?? KLIK_AUTH_URL;
  const body = JSON.stringify({ code });
  const { status, body: respBody } = await request(
    "POST",
    `${base}/api/v1/auth/import-code/verify`,
    body,
    { "Content-Type": "application/json", "Content-Length": String(Buffer.byteLength(body)) }
  );
  const json = JSON.parse(respBody);
  if (status !== 200) {
    throw new Error(json.error ?? `HTTP ${status}`);
  }
  return json;
}
async function uploadPayload(payload, importToken, opts = {}) {
  const base = opts.baseUrl ?? KLIK_MEMORY_URL;
  const raw = Buffer.from(JSON.stringify(payload), "utf8");
  const shouldGzip = raw.byteLength > 256 * 1024;
  const body = shouldGzip ? zlib.gzipSync(raw) : raw;
  const headers = {
    "X-Import-Token": importToken,
    "Content-Type": "application/json",
    "Content-Length": String(body.byteLength)
  };
  if (shouldGzip)
    headers["Content-Encoding"] = "gzip";
  const { status, body: respBody } = await request(
    "POST",
    `${base}/api/v1/memory/import/upload`,
    body,
    headers
  );
  const json = JSON.parse(respBody);
  if (status !== 200) {
    throw new Error(json.error ?? JSON.stringify(json));
  }
  return json;
}

// src/cli.ts
var [, , subcommand, ...args] = process.argv;
function parseArgs(args2) {
  const out = {};
  for (let i = 0; i < args2.length; i++) {
    if (args2[i].startsWith("--")) {
      out[args2[i].slice(2)] = args2[i + 1] ?? "true";
      i++;
    }
  }
  return out;
}
function readPayload(inputPath) {
  const content = fs.readFileSync(inputPath, "utf8");
  return JSON.parse(content);
}
function applyRedactionToPayload(payload, redactEmail) {
  let totalRedacted = 0;
  const redacted = structuredClone(payload);
  for (const collector of redacted.collectors) {
    for (const item of collector.items) {
      if (item.content) {
        const { result, count } = redactContent(item.content, { redactEmail });
        item.content = result;
        totalRedacted += count;
      }
      if (item.prompt) {
        const { result, count } = redactContent(item.prompt, { redactEmail });
        item.prompt = result;
        totalRedacted += count;
      }
    }
  }
  redacted.redaction.redacted_count = totalRedacted;
  redacted.redaction.email_redacted = redactEmail;
  return { payload: redacted, totalRedacted };
}
function printSummary(payload) {
  console.log("\n=== Import Summary ===");
  for (const c of payload.collectors) {
    console.log(`  ${c.name}: ${c.items.length} items from ${c.source_root}`);
  }
  const totalItems = payload.collectors.reduce((s, c) => s + c.items.length, 0);
  const bytes = Buffer.byteLength(JSON.stringify(payload), "utf8");
  console.log(`  Total: ${totalItems} items, ${(bytes / 1024).toFixed(1)} KB`);
  if (payload.redaction.redacted_count > 0) {
    console.log(`  Redacted: ${payload.redaction.redacted_count} secret(s) replaced`);
  }
  console.log("");
}
async function cmdSubmit(flags) {
  if (!flags.input) {
    console.error("--input required");
    process.exit(1);
  }
  if (!flags.code) {
    console.error("--code required");
    process.exit(1);
  }
  const raw = readPayload(flags.input);
  const nonInteractive = flags.yes === "true";
  let redactEmail = false;
  if (!nonInteractive) {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const answer = await rl.question("Redact email addresses? [y/N]: ");
    rl.close();
    redactEmail = answer.trim().toLowerCase() === "y";
  }
  const { payload } = applyRedactionToPayload(raw, redactEmail);
  try {
    validatePayload(payload);
  } catch (e) {
    console.error("Validation failed:", e.message);
    process.exit(1);
  }
  printSummary(payload);
  if (!nonInteractive) {
    const rl2 = readline.createInterface({ input: process.stdin, output: process.stdout });
    const confirm = await rl2.question("Upload to Klik? [y/N]: ");
    rl2.close();
    if (confirm.trim().toLowerCase() !== "y") {
      console.log("Upload cancelled.");
      process.exit(0);
    }
  }
  console.log("Verifying import code...");
  const { import_token, user_id } = await verifyCode(flags.code);
  console.log(`Authenticated as user ${user_id}`);
  console.log("Uploading...");
  const result = await uploadPayload(payload, import_token);
  console.log(`
Import complete. ID: ${result.import_id}`);
  for (const a of result.accepted) {
    console.log(`  ${a.collector}: ${a.item_count} items`);
  }
}
async function cmdValidate(flags) {
  if (!flags.input) {
    console.error("--input required");
    process.exit(1);
  }
  const raw = readPayload(flags.input);
  try {
    validatePayload(raw);
    console.log("Payload is valid");
  } catch (e) {
    console.error("Validation failed:", e.message);
    process.exit(1);
  }
}
async function cmdRedact(flags) {
  if (!flags.input) {
    console.error("--input required");
    process.exit(1);
  }
  const raw = readPayload(flags.input);
  const { payload, totalRedacted } = applyRedactionToPayload(raw, flags["redact-email"] === "true");
  const out = flags.output ?? "/dev/stdout";
  fs.writeFileSync(out, JSON.stringify(payload, null, 2), "utf8");
  console.error(`Redacted ${totalRedacted} secret(s)`);
}
async function cmdDoctor() {
  const nodeVer = parseInt(process.versions.node.split(".")[0]);
  console.log(`Node version: ${process.versions.node} ${nodeVer >= 18 ? "ok" : "FAIL (need >= 18)"}`);
  try {
    await dns.lookup("hiklik.ai");
    console.log("DNS hiklik.ai: ok");
  } catch {
    console.log("DNS hiklik.ai: FAIL (no network or wrong domain)");
  }
  const skillMd = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "SKILL.md");
  console.log(`SKILL.md present: ${fs.existsSync(skillMd) ? "ok" : "missing"}`);
}
(async () => {
  const flags = parseArgs(args);
  switch (subcommand) {
    case "submit":
      await cmdSubmit(flags);
      break;
    case "validate":
      await cmdValidate(flags);
      break;
    case "redact":
      await cmdRedact(flags);
      break;
    case "doctor":
      await cmdDoctor();
      break;
    default:
      console.log("Usage: node klik-import.mjs <submit|validate|redact|doctor> [options]");
      process.exit(1);
  }
})().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
