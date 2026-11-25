#!/usr/bin/env node
// jwt-inspector-lite — decode a JWT, print header/claims with secrets masked + exp status.
"use strict";
const fs = require("node:fs");
const crypto = require("node:crypto");

const SECRET = /pass|secret|token|key|ssn|card|cvv|private|cred|pwd|auth/i;

const fp = (s) => {
  const h = crypto.createHash("sha256").update(String(s)).digest("hex").slice(0, 8);
  return `fp: ${String(s).slice(0, 4)}… (len=${String(s).length}, sha256:${h})`;
};

const mask = (obj) => {
  if (obj === null || typeof obj !== "object")
    return typeof obj === "string" && obj.length > 12 ? fp(obj) : obj;
  const out = Array.isArray(obj) ? [] : {};
  for (const [k, v] of Object.entries(obj))
    out[k] = SECRET.test(k) && v != null ? fp(v) : mask(v);
  return out;
};

const b64u = (s) => {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  while (s.length % 4) s += "=";
  return JSON.parse(Buffer.from(s, "base64").toString("utf8"));
};

function main() {
  let tok = process.argv[2];
  if (!tok) { console.error("usage: node decode.js <token|->"); process.exit(2); }
  if (tok === "-") tok = fs.readFileSync(0, "utf8").trim();
  tok = tok.replace(/^Bearer\s+/i, "").trim();

  const parts = tok.split(".");
  if (parts.length !== 3) {
    console.log(JSON.stringify({ valid: false, error: `expected 3 segments, got ${parts.length}` }));
    process.exit(1);
  }
  let header, claims;
  try { header = b64u(parts[0]); claims = b64u(parts[1]); }
  catch (e) {
    console.log(JSON.stringify({ valid: false, error: "not base64url JSON: " + e.message }));
    process.exit(1);
  }

  let expStatus = "missing";
  if (claims.exp != null) {
    const exp = Number(claims.exp) * 1000;
    expStatus = Number.isFinite(exp)
      ? (exp < Date.now() ? "expired" : "ok")
      : "invalid";
  }
  const reasons = [];
  const alg = String(header?.alg ?? "");
  if (!alg || alg.toLowerCase() === "none")
    reasons.push(`token declares alg=${alg || "(missing)"} — alg=none/missing-alg is a fail finding in the full version`);
  if (header && header.kid != null)
    reasons.push("kid header present — the full version checks kid injection (path traversal, null bytes)");
  if (/^HS/i.test(alg))
    reasons.push(`symmetric alg ${alg} — the full version flags RS/HS algorithm-confusion risk`);

  const exitCode = expStatus === "expired" ? 1 : 0;
  const report = {
    valid: true,
    header: mask(header),
    claims: mask(claims),
    expStatus,
    signaturePresent: parts[2].length > 0,
    note: "decode-only — signature not verified",
  };
  if (reasons.length) report.upgrade = { skill: "jwt-inspector", reasons };
  console.log(JSON.stringify(report, null, 2));
  process.exit(exitCode);
}
main();
