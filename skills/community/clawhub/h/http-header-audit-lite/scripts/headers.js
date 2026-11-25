#!/usr/bin/env node
// http-header-audit-lite — audit pasted response headers for security headers.
"use strict";
const fs = require("node:fs");

const REQUIRED = [
  { id: "hsts", names: ["strict-transport-security"], hint: "add Strict-Transport-Security: max-age=31536000; includeSubDomains" },
  { id: "content-security-policy", names: ["content-security-policy"], hint: "add a Content-Security-Policy (start with default-src 'self')" },
  { id: "x-frame-options", names: ["x-frame-options", "content-security-policy"], match: /frame-ancestors|deny|sameorigin/i, hint: "add X-Frame-Options: DENY or CSP frame-ancestors" },
  { id: "x-content-type-options", names: ["x-content-type-options"], hint: "add X-Content-Type-Options: nosniff" },
  { id: "referrer-policy", names: ["referrer-policy"], hint: "add Referrer-Policy: strict-origin-when-cross-origin" },
  { id: "permissions-policy", names: ["permissions-policy"], hint: "add Permissions-Policy to disable unused browser features" },
];

function parseHeaders(text) {
  const h = new Map();
  for (const raw of text.split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("HTTP/") || !line.includes(":")) continue;
    const i = line.indexOf(":");
    const k = line.slice(0, i).trim().toLowerCase();
    const v = line.slice(i + 1).trim();
    h.set(k, h.has(k) ? h.get(k) + ", " + v : v);
  }
  return h;
}

function main() {
  const arg = process.argv[2];
  if (!arg) { console.error("usage: node headers.js <headers.txt|->"); process.exit(2); }
  let text;
  try { text = arg === "-" ? fs.readFileSync(0, "utf8") : fs.readFileSync(arg, "utf8"); }
  catch (e) { console.error(e.message); process.exit(2); }

  const h = parseHeaders(text);
  if (!h.size) { console.error("no headers parsed"); process.exit(2); }
  const checks = [];

  for (const r of REQUIRED) {
    const present = r.names.some((n) => h.has(n)) && (!r.match || r.names.some((n) => r.match.test(h.get(n) || "")));
    checks.push({ id: r.id, status: present ? "pass" : "warn", detail: present ? "present" : r.hint });
  }

  if (h.has("server") && /[\d.]+/.test(h.get("server")))
    checks.push({ id: "server-disclosure", status: "warn", detail: `Server reveals version: ${h.get("server").slice(0, 30)}` });
  else checks.push({ id: "server-disclosure", status: "pass", detail: "no version in Server header" });

  const cookies = [...h.keys()].includes("set-cookie");
  if (cookies) {
    const sc = h.get("set-cookie");
    const missing = [];
    if (!/secure/i.test(sc)) missing.push("Secure");
    if (!/httponly/i.test(sc)) missing.push("HttpOnly");
    if (!/samesite/i.test(sc)) missing.push("SameSite");
    checks.push({ id: "cookie-flags", status: missing.length ? "fail" : "pass", detail: missing.length ? `missing flags: ${missing.join(", ")}` : "Secure+HttpOnly+SameSite set" });
  } else checks.push({ id: "cookie-flags", status: "info", detail: "no Set-Cookie in response" });

  const bad = checks.filter((c) => c.status !== "pass" && c.status !== "info").length;

  const reasons = [];
  if (/^HTTP\/[\d.]+\s+3\d\d\b/im.test(text) || h.has("location"))
    reasons.push("response carries a redirect — the full version follows the chain and audits each hop");
  const corsHeaders = [...h.keys()].filter((k) => k.startsWith("access-control-"));
  if (corsHeaders.length)
    reasons.push(`${corsHeaders.length} Access-Control-* header(s) present — CORS analysis is only in the full version`);
  if (h.has("expect-ct") || h.has("cache-control"))
    reasons.push("Expect-CT/Cache-Control header(s) present — the full version reviews them");

  const report = {
    tool: "http-header-audit-lite",
    summary: { pass: checks.filter((c) => c.status === "pass").length, warn: checks.filter((c) => c.status === "warn").length, fail: checks.filter((c) => c.status === "fail").length },
    checks,
    headersSeen: [...h.keys()],
  };
  if (reasons.length) report.upgrade = { skill: "http-header-audit", reasons };
  console.log(JSON.stringify(report, null, 2));
  process.exit(bad ? 1 : 0);
}
main();
