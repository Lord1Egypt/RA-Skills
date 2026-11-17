#!/usr/bin/env node
/**
 * youtube-set-thumbnail.js — replace the thumbnail of an existing
 * YouTube video. Reuses the OAuth token-refresh path from the
 * YouTubeAdapter so we don't fork credential handling.
 *
 * Quota cost: ~50 units per call (videos.update is 50; thumbnails.set
 * uploads through the same multipart endpoint).
 *
 * Usage:
 *   node scripts/youtube-set-thumbnail.js --video-id <id> --image <path>
 *
 * Or as a library:
 *   const { setThumbnail } = require('./scripts/youtube-set-thumbnail');
 *   await setThumbnail(videoId, imagePath, rootDir);
 */

"use strict";

const fs = require("fs");
const path = require("path");
const https = require("https");
const { URL } = require("url");

const ROOT = path.resolve(__dirname, "..");
const TOKEN_URL = "https://oauth2.googleapis.com/token";
const THUMB_URL =
  "https://www.googleapis.com/upload/youtube/v3/thumbnails/set?uploadType=media";

// Read .youtube.json from the project root (same file the broadcaster uses).
function loadCreds() {
  const p = path.join(ROOT, ".youtube.json");
  if (!fs.existsSync(p)) throw new Error(`.youtube.json missing at ${p}`);
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function postRaw(url, body, headers) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = https.request(
      {
        method: "POST",
        hostname: u.hostname,
        path: u.pathname + u.search,
        headers: { ...headers, "Content-Length": Buffer.byteLength(body) },
      },
      (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => {
          const text = Buffer.concat(chunks).toString("utf8");
          try { resolve({ status: res.statusCode, body: JSON.parse(text) }); }
          catch { resolve({ status: res.statusCode, body: text }); }
        });
      },
    );
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

async function getAccessToken(creds) {
  const params = new URLSearchParams({
    client_id: creds.client_id,
    client_secret: creds.client_secret,
    refresh_token: creds.refresh_token,
    grant_type: "refresh_token",
  }).toString();
  const r = await postRaw(TOKEN_URL, params, {
    "Content-Type": "application/x-www-form-urlencoded",
  });
  if (r.status !== 200 || !r.body.access_token) {
    throw new Error(`token refresh failed: ${r.status} ${JSON.stringify(r.body)}`);
  }
  return r.body.access_token;
}

function uploadThumbnail(videoId, imageBuf, mime, accessToken) {
  return new Promise((resolve, reject) => {
    const url = THUMB_URL + `&videoId=${encodeURIComponent(videoId)}`;
    const u = new URL(url);
    const req = https.request(
      {
        method: "POST",
        hostname: u.hostname,
        path: u.pathname + u.search,
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": mime,
          "Content-Length": imageBuf.length,
        },
      },
      (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => {
          const text = Buffer.concat(chunks).toString("utf8");
          try { resolve({ status: res.statusCode, body: JSON.parse(text) }); }
          catch { resolve({ status: res.statusCode, body: text }); }
        });
      },
    );
    req.on("error", reject);
    req.write(imageBuf);
    req.end();
  });
}

async function setThumbnail(videoId, imagePath, rootDir = ROOT) {
  const creds = loadCreds.call({ ROOT: rootDir });
  if (!fs.existsSync(imagePath)) throw new Error(`image missing: ${imagePath}`);
  const buf = fs.readFileSync(imagePath);
  const ext = path.extname(imagePath).toLowerCase();
  const mime = ext === ".png" ? "image/png" : ext === ".jpg" || ext === ".jpeg" ? "image/jpeg" : "image/png";
  const access = await getAccessToken(creds);
  const r = await uploadThumbnail(videoId, buf, mime, access);
  if (r.status !== 200) {
    const detail = r.body && r.body.error ? r.body.error.message : JSON.stringify(r.body).slice(0, 200);
    throw new Error(`thumbnails.set status_${r.status}: ${detail}`);
  }
  return r.body;
}

async function cli() {
  const argv = process.argv.slice(2);
  const arg = (n) => {
    const i = argv.indexOf(n);
    return i >= 0 ? argv[i + 1] : "";
  };
  const videoId = arg("--video-id");
  const image = arg("--image");
  if (!videoId || !image) {
    console.error('Usage: youtube-set-thumbnail.js --video-id <id> --image <path>');
    process.exit(64);
  }
  try {
    const r = await setThumbnail(videoId, image);
    console.log(`[thumb] ok: video ${videoId} thumbnails set:`, JSON.stringify(r).slice(0, 300));
  } catch (e) {
    console.error(`[thumb] FAILED: ${e.message}`);
    process.exit(1);
  }
}

if (require.main === module) cli();

module.exports = { setThumbnail };
