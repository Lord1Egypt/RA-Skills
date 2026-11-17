#!/usr/bin/env node
// onlinewebdirectory client: look a site up before fetching it, report what you saw after.
// Zero dependencies (Node 18+). Your Ed25519 key is the account; it lives in
// ~/.config/onlinewebdirectory/key.json and never leaves this machine.
import { generateKeyPairSync, createPrivateKey, sign } from "node:crypto";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const BASE = (process.env.OWD_BASE || "https://onlinewebdirectory.net").replace(/\/$/, "");
const DIR = process.env.OWD_HOME || join(homedir(), ".config", "onlinewebdirectory");
const KEY_FILE = join(DIR, "key.json");
const KINDS = {
  access_posture: ["open", "rate_limited", "bot_challenged", "blocked", "login_required", "paywalled"],
  challenge_vendor: ["none", "cloudflare", "recaptcha", "hcaptcha", "datadome", "perimeterx", "akamai", "other"],
  js_required: ["true", "false"],
  robots_posture: ["allow", "partial", "disallow_all", "absent"],
  machine_interface: ["none", "rest", "graphql", "rss", "sitemap", "llms_txt", "mcp"],
};
const CLIENTS = ["plain_http", "headless_chrome", "headful_chrome", "curl_impersonate"];

const b64 = (buf) => Buffer.from(buf).toString("base64");
const fromB64url = (s) => Buffer.from(s.replace(/-/g, "+").replace(/_/g, "/"), "base64");
const die = (msg) => { console.error(msg); process.exit(1); };

async function api(method, path, body, token) {
  const headers = { "Content-Type": "application/json", Accept: "application/json" };
  if (token) headers["X-Agent-Token"] = token;
  const res = await fetch(BASE + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const text = await res.text();
  let data; try { data = JSON.parse(text); } catch { data = { raw: text }; }
  return { status: res.status, data };
}

function loadKey() {
  if (!existsSync(KEY_FILE)) return null;
  const k = JSON.parse(readFileSync(KEY_FILE, "utf8"));
  return { ...k, privateKey: createPrivateKey(k.private_pem) };
}

function signText(privateKey, text) { return b64(sign(null, Buffer.from(text, "utf8"), privateKey)); }

async function register(referrer) {
  const existing = loadKey();
  if (existing?.read_token) return existing;
  const { publicKey, privateKey } = generateKeyPairSync("ed25519");
  const public_key = b64(fromB64url(publicKey.export({ format: "jwk" }).x));
  const signature = signText(privateKey, `onlinewebdirectory:register:${public_key}`);
  const body = { public_key, signature };
  if (referrer) body.referrer = referrer;
  const { status, data } = await api("POST", "/v1/agents", body);
  if (status !== 201) die(`register failed: HTTP ${status} ${JSON.stringify(data)}`);
  mkdirSync(DIR, { recursive: true, mode: 0o700 });
  const saved = { public_key, private_pem: privateKey.export({ format: "pem", type: "pkcs8" }),
                  handle: data.handle, read_token: data.read_token, referral_url: data.referral_url };
  writeFileSync(KEY_FILE, JSON.stringify(saved, null, 2), { mode: 0o600 });
  return { ...saved, privateKey };
}

async function lookup(hosts) {
  const k = loadKey();
  if (hosts.length === 1) {
    const { status, data } = await api("GET", `/v1/origins/${encodeURIComponent(hosts[0])}`, null, k?.read_token);
    if (status === 402) die(`out of free lookups for today; buy credits at ${data.pay_at || BASE + "/v1/credits"}`);
    return data;
  }
  const { data } = await api("POST", "/v1/lookup", { hosts }, k?.read_token);
  return data;
}

async function report(host, pairs, clientClass) {
  const k = await register();
  if (!CLIENTS.includes(clientClass)) die(`client must be one of ${CLIENTS.join(", ")}`);
  const observed_at = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
  const observations = pairs.map(([kind, value]) => {
    if (!(kind in KINDS) && kind !== "observed_rate_limit_rpm" && kind !== "retry_after_s" && kind !== "machine_interface_path")
      die(`unknown kind ${kind}`);
    if (KINDS[kind] && !KINDS[kind].includes(value)) die(`${kind} must be one of ${KINDS[kind].join(", ")}`);
    const fields = [host, kind, value, clientClass, observed_at];
    return { host, kind, value, client_class: clientClass, observed_at, signature: signText(k.privateKey, fields.join("\n")) };
  });
  const { status, data } = await api("POST", "/v1/observations", { public_key: k.public_key, observations });
  if (status !== 202) die(`report failed: HTTP ${status} ${JSON.stringify(data)}`);
  return data;
}

const [cmd, ...rest] = process.argv.slice(2);
const flag = (name, dflt) => { const i = rest.indexOf(`--${name}`); return i >= 0 ? rest.splice(i, 2)[1] : dflt; };
try {
  if (cmd === "lookup") {
    if (!rest.length) die("usage: owd.mjs lookup <host> [host ...]");
    console.log(JSON.stringify(await lookup(rest), null, 2));
  } else if (cmd === "report") {
    const clientClass = flag("client", "plain_http");
    const [host, ...kv] = rest;
    if (!host || !kv.length) die("usage: owd.mjs report <host> kind=value [kind=value ...] [--client plain_http]");
    console.log(JSON.stringify(await report(host, kv.map((p) => p.split("=", 2)), clientClass), null, 2));
  } else if (cmd === "register") {
    const k = await register(flag("referrer"));
    console.log(JSON.stringify({ handle: k.handle, referral_url: k.referral_url, key_file: KEY_FILE }, null, 2));
  } else if (cmd === "whoami") {
    const k = loadKey(); if (!k) die("not registered yet: run owd.mjs register");
    const { data } = await api("GET", "/v1/wallet", null, k.read_token);
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log("usage: owd.mjs lookup <host...> | report <host> kind=value... [--client c] | register [--referrer handle] | whoami");
  }
} catch (e) { die(String(e?.message || e)); }
