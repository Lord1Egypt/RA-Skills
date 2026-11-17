#!/usr/bin/env node
/**
 * podcast-finisher.js — self-healing tail of the GSP podcast upgrade.
 *
 * Loop A (every 2h):  retry thumbnails.set for episodes still missing one
 *                     (YouTube 429s after ~10 rapid sets; cooldown is long).
 * Loop B (every 10m): probe a playlistItems.update with an explicit
 *                     position. While the podcast playlist sort is
 *                     "date published" this fails with "sort type need to
 *                     be MANUAL"; the moment the playlist is switched to
 *                     Manual ordering in YouTube Studio the probe succeeds
 *                     and the loop sets positions 1..12 in one pass.
 *
 * Exits when both jobs are done (or after MAX_HOURS).
 */
"use strict";

const fs = require("fs");
const path = require("path");
const https = require("https");
const { URL } = require("url");

const ROOT = path.resolve(__dirname, "..");
const PODCASTS = path.join(ROOT, "workspace", "podcasts");
const META_PATH = path.join(PODCASTS, "metadata.json");
const STATE_PATH = path.join(PODCASTS, "upload-state.json");
const PL = "PLr8fsczlhL9I4C5f1_TVHzfKXFusfUC0A";
const MAX_HOURS = 24;

const { YouTubeAdapter } = require(path.join(__dirname, "youtube-adapter"));
const { setThumbnail } = require(path.join(__dirname, "youtube-set-thumbnail"));

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const ts = () => new Date().toISOString().slice(11, 19);

function api(method, url, access, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const payload = body ? JSON.stringify(body) : null;
    const req = https.request({ method, hostname: u.hostname, path: u.pathname + u.search,
      headers: { Authorization: `Bearer ${access}`,
        ...(payload ? { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(payload) } : {}) } },
      (res) => { let d = ""; res.on("data", (c) => d += c); res.on("end", () => {
        let j; try { j = JSON.parse(d); } catch (_) { j = d; }
        resolve({ status: res.statusCode, body: j }); }); });
    req.on("error", reject);
    if (payload) req.write(payload);
    req.end();
  });
}

async function thumbsPass(adapter, meta, state) {
  let pending = 0;
  for (const ep of meta) {
    const vid = state.uploads[ep.num];
    if (!vid || state.thumbs[ep.num]) continue;
    try {
      await setThumbnail(vid, ep.cover, ROOT);
      state.thumbs[ep.num] = true;
      fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
      console.log(`[${ts()}] [thumbs] set for GSP-${String(ep.num).padStart(3, "0")}`);
    } catch (e) {
      pending++;
      console.log(`[${ts()}] [thumbs] ep ${ep.num} still failing: ${e.message.slice(0, 80)}`);
    }
  }
  return pending === 0;
}

async function orderPass(adapter, meta, state) {
  const access = await adapter._accessToken();
  // probe with episode 1
  const probeEp = meta.find((e) => state.playlist[e.num] && state.uploads[e.num]);
  if (!probeEp) { console.log(`[${ts()}] [order] no playlist items in state`); return false; }
  const probe = await api("PUT", "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", access, {
    id: state.playlist[probeEp.num],
    snippet: { playlistId: PL, resourceId: { kind: "youtube#video", videoId: state.uploads[probeEp.num] },
      position: probeEp.num - 1 },
  });
  if (probe.status !== 200) {
    const msg = probe.body && probe.body.error && probe.body.error.message || "";
    if (/MANUAL/i.test(msg)) return false; // still auto-sorted — keep waiting
    console.log(`[${ts()}] [order] probe failed otherwise: ${msg.slice(0, 100)}`);
    return false;
  }
  console.log(`[${ts()}] [order] playlist is MANUAL now — setting all positions`);
  for (const ep of meta) {
    if (!state.playlist[ep.num] || !state.uploads[ep.num] || ep.num === probeEp.num) continue;
    const r = await api("PUT", "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", access, {
      id: state.playlist[ep.num],
      snippet: { playlistId: PL, resourceId: { kind: "youtube#video", videoId: state.uploads[ep.num] },
        position: ep.num - 1 },
    });
    console.log(`[${ts()}] [order] GSP-${String(ep.num).padStart(3, "0")} -> pos ${ep.num - 1} (${r.status})`);
    await sleep(1500);
  }
  await sleep(10000);
  const l = await api("GET", `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=${PL}&maxResults=50`, access);
  console.log(`[${ts()}] FINAL PLAYLIST ORDER:`);
  for (const it of l.body.items || []) console.log(`   ${String(it.snippet.position).padStart(2)}  ${it.snippet.title.slice(0, 44)}`);
  return true;
}

(async () => {
  const meta = JSON.parse(fs.readFileSync(META_PATH, "utf8"));
  const adapter = new YouTubeAdapter(ROOT);
  const deadline = Date.now() + MAX_HOURS * 3600 * 1000;
  let thumbsDone = false, orderDone = false;
  let lastThumbs = 0;
  console.log(`[${ts()}] finisher started (order probe 10m, thumbs retry 2h, max ${MAX_HOURS}h)`);
  while (Date.now() < deadline && (!thumbsDone || !orderDone)) {
    const state = JSON.parse(fs.readFileSync(STATE_PATH, "utf8"));
    if (!thumbsDone && Date.now() - lastThumbs > 2 * 3600 * 1000 - 60000) {
      lastThumbs = Date.now();
      thumbsDone = await thumbsPass(adapter, meta, state);
      if (thumbsDone) console.log(`[${ts()}] [thumbs] all set ✔`);
    }
    if (!orderDone) {
      orderDone = await orderPass(adapter, meta, state);
      if (orderDone) console.log(`[${ts()}] [order] done ✔`);
    }
    if (thumbsDone && orderDone) break;
    await sleep(10 * 60 * 1000);
  }
  console.log(`[${ts()}] finisher exiting — thumbs=${thumbsDone} order=${orderDone}`);
})().catch((e) => { console.error("fatal:", e.stack || e.message); process.exit(1); });
