#!/usr/bin/env node
/**
 * youtube-grant.js — one-shot OAuth grant for the YouTube uploader adapter.
 *
 * Flow:
 *   1. Prompts for client_id + client_secret (or reads them from
 *      ~/.youtube-client.json if present).
 *   2. Spins up a localhost HTTP listener on a random port.
 *   3. Opens the system browser to Google's OAuth consent URL.
 *   4. After you click through + grant, browser redirects back to
 *      http://127.0.0.1:<port>/?code=... — we capture the code.
 *   5. Exchanges code for access_token + refresh_token at Google's
 *      /token endpoint.
 *   6. Writes .youtube.json (in the kannaka-radio root) with everything
 *      the broadcaster adapter needs:
 *        { client_id, client_secret, refresh_token, channel_id, scopes }
 *
 * After this runs once, scripts/post-track-announce.js (and any future
 * use of the YouTube adapter) just calls into the API using the saved
 * refresh token. You don't have to re-grant unless you revoke from
 * Google.
 *
 * Run:
 *   node scripts/youtube-grant.js
 *
 * Stop the script: Ctrl-C. If the browser doesn't open automatically,
 * the URL is printed — paste it into any browser.
 */

"use strict";

const fs = require("fs");
const path = require("path");
const http = require("http");
const https = require("https");
const readline = require("readline");
const { URL } = require("url");
const { exec } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const SAVE_PATH = path.join(ROOT, ".youtube.json");

// `youtube` (full read/write) instead of just `youtube.upload + readonly`
// because playlistItems.insert (used by the adapter to auto-add each
// upload to a playlist) requires playlist write permission, which only
// the full scope grants. .readonly + .upload are insufficient — Google
// returns "Request had insufficient authentication scopes" (403) on
// playlist mutations under those.
const SCOPES = [
  "https://www.googleapis.com/auth/youtube",
  "https://www.googleapis.com/auth/youtube.upload",
].join(" ");

function ask(rl, q) {
  return new Promise((resolve) => rl.question(q, (a) => resolve(a.trim())));
}

function openBrowser(url) {
  const cmd = process.platform === "win32"
    ? `start "" "${url}"`
    : process.platform === "darwin"
    ? `open "${url}"`
    : `xdg-open "${url}"`;
  exec(cmd, (err) => {
    if (err) {
      // Non-fatal — user can copy the URL themselves.
    }
  });
}

function postForm(url, params) {
  return new Promise((resolve, reject) => {
    const body = new URLSearchParams(params).toString();
    const u = new URL(url);
    const req = https.request({
      method: "POST",
      hostname: u.hostname,
      path: u.pathname + u.search,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": Buffer.byteLength(body),
      },
    }, (res) => {
      let chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => {
        const text = Buffer.concat(chunks).toString("utf8");
        try {
          resolve({ status: res.statusCode, body: JSON.parse(text) });
        } catch (_) {
          resolve({ status: res.statusCode, body: text });
        }
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

function getJson(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = https.request({
      method: "GET",
      hostname: u.hostname,
      path: u.pathname + u.search,
      headers,
    }, (res) => {
      let chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => {
        const text = Buffer.concat(chunks).toString("utf8");
        try {
          resolve({ status: res.statusCode, body: JSON.parse(text) });
        } catch (_) {
          resolve({ status: res.statusCode, body: text });
        }
      });
    });
    req.on("error", reject);
    req.end();
  });
}

async function main() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  // Read client credentials. We accept paste-in or a side-file at
  // ~/.youtube-client.json with shape {client_id, client_secret}.
  let client_id = "", client_secret = "";
  const sidePath = path.join(process.env.HOME || process.env.USERPROFILE || ".", ".youtube-client.json");
  if (fs.existsSync(sidePath)) {
    try {
      const j = JSON.parse(fs.readFileSync(sidePath, "utf8"));
      // Google's downloaded OAuth JSON wraps under "installed".
      const root = j.installed || j;
      client_id = root.client_id || "";
      client_secret = root.client_secret || "";
      if (client_id && client_secret) {
        console.log(`[grant] using credentials from ${sidePath}`);
      }
    } catch (_) {}
  }
  if (!client_id) client_id = await ask(rl, "Paste OAuth client_id: ");
  if (!client_secret) client_secret = await ask(rl, "Paste OAuth client_secret: ");
  if (!client_id || !client_secret) {
    console.error("[grant] client_id and client_secret are required");
    process.exit(64);
  }

  // Spin up loopback listener — Google deprecated OOB in 2022, so
  // we use http://127.0.0.1:<port> as the redirect URI.
  let redirectUri = "";
  const code = await new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const u = new URL(req.url, "http://127.0.0.1");
      if (u.pathname !== "/") {
        res.writeHead(404).end();
        return;
      }
      const c = u.searchParams.get("code");
      const error = u.searchParams.get("error");
      res.writeHead(200, { "Content-Type": "text/html" });
      if (error) {
        res.end(`<html><body><h1>OAuth error</h1><pre>${error}</pre><p>You can close this tab.</p></body></html>`);
        server.close();
        return reject(new Error(`OAuth error: ${error}`));
      }
      if (!c) {
        res.end(`<html><body><h1>Missing code</h1><p>The redirect didn't carry a code parameter.</p></body></html>`);
        server.close();
        return reject(new Error("missing code in redirect"));
      }
      res.end(`<html><body><h1>Granted ✓</h1><p>You can close this tab and return to the terminal.</p></body></html>`);
      server.close();
      resolve(c);
    });
    server.listen(0, "127.0.0.1", () => {
      const { port } = server.address();
      redirectUri = `http://127.0.0.1:${port}/`;
      const consentUrl = "https://accounts.google.com/o/oauth2/v2/auth?" + new URLSearchParams({
        client_id,
        redirect_uri: redirectUri,
        response_type: "code",
        scope: SCOPES,
        access_type: "offline",
        prompt: "consent",
      }).toString();
      console.log("\n[grant] opening browser to:");
      console.log("        " + consentUrl);
      console.log("\n[grant] (if it doesn't open, copy that URL into any browser)\n");
      openBrowser(consentUrl);
    });
    server.on("error", reject);
  });
  console.log("[grant] received code; exchanging for tokens...");

  const tokenResp = await postForm("https://oauth2.googleapis.com/token", {
    code,
    client_id,
    client_secret,
    redirect_uri: redirectUri,
    grant_type: "authorization_code",
  });
  if (tokenResp.status !== 200 || !tokenResp.body || !tokenResp.body.refresh_token) {
    console.error("[grant] token exchange failed:", tokenResp.status, tokenResp.body);
    process.exit(2);
  }
  const { refresh_token, access_token, expires_in } = tokenResp.body;

  // Pull channel ID for nicer broadcaster output (so the adapter can log
  // "uploaded to <channel name>"). Best-effort — failure doesn't block.
  let channel_id = "", channel_title = "";
  try {
    const ch = await getJson(
      "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
      { Authorization: `Bearer ${access_token}` },
    );
    if (ch.status === 200 && ch.body.items && ch.body.items[0]) {
      channel_id = ch.body.items[0].id;
      channel_title = ch.body.items[0].snippet.title;
    }
  } catch (_) {}

  const out = {
    client_id,
    client_secret,
    refresh_token,
    channel_id,
    channel_title,
    scopes: SCOPES,
    granted_at: new Date().toISOString(),
    note: "Generated by scripts/youtube-grant.js. Do not commit.",
  };
  fs.writeFileSync(SAVE_PATH, JSON.stringify(out, null, 2));
  fs.chmodSync(SAVE_PATH, 0o600);

  console.log(`\n[grant] saved ${SAVE_PATH}`);
  console.log(`[grant] channel: ${channel_title || "(unknown)"} (${channel_id || "no id"})`);
  console.log(`[grant] access_token expires in ${expires_in}s; refresh_token is permanent.`);
  console.log(`[grant] next: scripts/youtube-upload-test.js to verify upload works.`);
  rl.close();
}

main().catch((err) => {
  console.error("[grant] fatal:", err && err.message ? err.message : err);
  process.exit(1);
});
