#!/usr/bin/env node
/**
 * podcast-upload-batch.js — upload the Ghost Signals slideshow renders
 * to YouTube and assemble the Podcasts-section playlist.
 *
 * Reads workspace/podcasts/metadata.json (array; see below) and keeps a
 * resumable state file workspace/podcasts/upload-state.json so a quota
 * interruption (403 quotaExceeded) picks up where it left off.
 *
 * metadata.json entry:
 *   { num, title, description, tags[], video, cover, oldVideoId? }
 *
 * Phases (run all by default, or --phase <name>):
 *   upload    videos.insert for each episode (missing eps 2-7 first,
 *             then upgrades 1, 8-12) — 1600 quota units each
 *   thumbs    thumbnails.set with the rendered cover — 50 units each
 *   playlist  remove the old episode-1 item from the podcast playlist,
 *             then insert eps 1..12 in order — 50 units each
 *   retire    unlist each replaced video and prepend an "upgraded
 *             edition" pointer to its description — 50 units each
 *   verify    read back playlist + new video status, print summary
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
const PODCAST_PLAYLIST = "PLr8fsczlhL9I4C5f1_TVHzfKXFusfUC0A"; // "Ghost Signals with Kannaka" (podcastStatus=enabled)
const UPLOAD_ORDER = [2, 3, 4, 5, 6, 7, 1, 8, 9, 10, 11, 12];

const { YouTubeAdapter } = require(path.join(__dirname, "youtube-adapter"));
const { setThumbnail } = require(path.join(__dirname, "youtube-set-thumbnail"));

function loadJson(p, fallback) {
  if (!fs.existsSync(p)) return fallback;
  return JSON.parse(fs.readFileSync(p, "utf8"));
}
function saveState(state) {
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

function api(method, url, access, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const payload = body ? JSON.stringify(body) : null;
    const req = https.request({
      method, hostname: u.hostname, path: u.pathname + u.search,
      headers: {
        Authorization: `Bearer ${access}`,
        ...(payload ? { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(payload) } : {}),
      },
    }, (res) => {
      const chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => {
        const text = Buffer.concat(chunks).toString("utf8");
        let parsed;
        try { parsed = JSON.parse(text); } catch (_) { parsed = text; }
        resolve({ status: res.statusCode, body: parsed });
      });
    });
    req.on("error", reject);
    if (payload) req.write(payload);
    req.end();
  });
}
function errDetail(r) {
  return r.body && r.body.error && r.body.error.message
    ? r.body.error.message
    : JSON.stringify(r.body).slice(0, 200);
}

async function phaseUpload(adapter, meta, state) {
  for (const num of UPLOAD_ORDER) {
    const ep = meta.find((e) => e.num === num);
    if (!ep) continue;
    if (state.uploads[num]) { console.log(`[upload] GSP-${String(num).padStart(3, "0")} already up: ${state.uploads[num]}`); continue; }
    if (!fs.existsSync(ep.video)) { console.log(`[upload] GSP-${String(num).padStart(3, "0")} render missing, skipping: ${ep.video}`); continue; }
    const sizeMB = (fs.statSync(ep.video).size / 1e6).toFixed(0);
    console.log(`[upload] GSP-${String(num).padStart(3, "0")} "${ep.title}" (${sizeMB} MB)...`);
    const r = await adapter.post({
      text: ep.description,
      media: { path: ep.video, title: ep.title, tags: ep.tags, privacy: "public", categoryId: "10" },
    });
    if (!r.ok) {
      console.error(`[upload] FAILED GSP-${String(num).padStart(3, "0")}: ${r.error}`);
      if (/quota/i.test(r.error)) { console.error("[upload] quota exhausted — re-run after quota reset (midnight PT) to resume"); return false; }
      return false;
    }
    state.uploads[num] = r.id;
    saveState(state);
    console.log(`[upload] ok: ${r.url}`);
  }
  return true;
}

async function phaseThumbs(meta, state) {
  for (const ep of meta) {
    const vid = state.uploads[ep.num];
    if (!vid || state.thumbs[ep.num]) continue;
    if (!fs.existsSync(ep.cover)) { console.log(`[thumbs] no cover for ep ${ep.num}`); continue; }
    try {
      await setThumbnail(vid, ep.cover, ROOT);
      state.thumbs[ep.num] = true;
      saveState(state);
      console.log(`[thumbs] set for GSP-${String(ep.num).padStart(3, "0")} (${vid})`);
    } catch (e) {
      console.error(`[thumbs] FAILED ep ${ep.num}: ${e.message}`);
      if (/quota/i.test(e.message)) return false;
    }
  }
  return true;
}

async function phasePlaylist(adapter, meta, state) {
  const access = await adapter._accessToken();
  // remove the pre-upgrade episode-1 item so ordering starts clean
  if (!state.removedOldItem) {
    const r = await api("GET",
      `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=${PODCAST_PLAYLIST}&maxResults=50`, access);
    if (r.status !== 200) { console.error(`[playlist] list failed: ${errDetail(r)}`); return false; }
    const newIds = new Set(Object.values(state.uploads));
    for (const it of r.body.items || []) {
      if (!newIds.has(it.snippet.resourceId.videoId)) {
        const d = await api("DELETE", `https://www.googleapis.com/youtube/v3/playlistItems?id=${it.id}`, access);
        if (d.status === 204) console.log(`[playlist] removed old item "${it.snippet.title}"`);
        else { console.error(`[playlist] remove failed: ${errDetail(d)}`); return false; }
      }
    }
    state.removedOldItem = true;
    saveState(state);
  }
  for (const ep of meta) {
    const vid = state.uploads[ep.num];
    if (!vid || state.playlist[ep.num]) continue;
    const r = await api("POST", "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", access, {
      snippet: { playlistId: PODCAST_PLAYLIST, resourceId: { kind: "youtube#video", videoId: vid } },
    });
    if (r.status === 200 && r.body.id) {
      state.playlist[ep.num] = r.body.id;
      saveState(state);
      console.log(`[playlist] added GSP-${String(ep.num).padStart(3, "0")}`);
    } else { console.error(`[playlist] add failed ep ${ep.num}: ${errDetail(r)}`); return false; }
  }
  return true;
}

async function phaseOrder(adapter, meta, state) {
  // playlistItems.insert append order is not reliably preserved — set
  // explicit positions so the Podcasts tab reads episode 1 -> 12.
  const access = await adapter._accessToken();
  for (const ep of meta) {
    const itemId = state.playlist[ep.num];
    const vid = state.uploads[ep.num];
    if (!itemId || !vid) continue;
    const r = await api("PUT", "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", access, {
      id: itemId,
      snippet: {
        playlistId: PODCAST_PLAYLIST,
        resourceId: { kind: "youtube#video", videoId: vid },
        position: ep.num - 1,
      },
    });
    if (r.status === 200) console.log(`[order] GSP-${String(ep.num).padStart(3, "0")} -> position ${ep.num - 1}`);
    else { console.error(`[order] failed ep ${ep.num}: ${errDetail(r)}`); return false; }
  }
  return true;
}

async function phaseRetire(adapter, meta, state) {
  const access = await adapter._accessToken();
  for (const ep of meta) {
    if (!ep.oldVideoId || state.retired[ep.oldVideoId]) continue;
    const newId = state.uploads[ep.num];
    if (!newId) continue; // never retire before the replacement exists
    const g = await api("GET",
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${ep.oldVideoId}`, access);
    if (g.status !== 200 || !g.body.items || !g.body.items.length) {
      console.error(`[retire] fetch failed ${ep.oldVideoId}: ${errDetail(g)}`); return false;
    }
    const v = g.body.items[0];
    const pointer =
      `⬆️ UPGRADED EDITION (with Kannaka's KAX artwork): https://www.youtube.com/watch?v=${newId}\n` +
      `Full series — Podcasts tab: https://www.youtube.com/playlist?list=${PODCAST_PLAYLIST}\n\n`;
    const snippet = {
      title: v.snippet.title,
      description: pointer + v.snippet.description,
      tags: v.snippet.tags || [],
      categoryId: v.snippet.categoryId,
    };
    const r = await api("PUT", "https://www.googleapis.com/youtube/v3/videos?part=snippet,status", access, {
      id: ep.oldVideoId, snippet,
      status: { privacyStatus: "unlisted", selfDeclaredMadeForKids: false },
    });
    if (r.status === 200) {
      state.retired[ep.oldVideoId] = true;
      saveState(state);
      console.log(`[retire] unlisted ${ep.oldVideoId} (ep ${ep.num}) with pointer to ${newId}`);
    } else { console.error(`[retire] update failed ${ep.oldVideoId}: ${errDetail(r)}`); return false; }
  }
  return true;
}

async function phaseVerify(adapter, meta, state) {
  const access = await adapter._accessToken();
  const r = await api("GET",
    `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,status&playlistId=${PODCAST_PLAYLIST}&maxResults=50`, access);
  console.log(`\n=== PODCAST PLAYLIST (${PODCAST_PLAYLIST}) ===`);
  for (const it of (r.body.items || [])) {
    console.log(`  ${String(it.snippet.position).padStart(2)}  ${it.snippet.resourceId.videoId}  "${it.snippet.title}"`);
  }
  const ids = Object.values(state.uploads);
  if (ids.length) {
    const v = await api("GET",
      `https://www.googleapis.com/youtube/v3/videos?part=status,processingDetails&id=${ids.join(",")}`, access);
    console.log(`\n=== NEW VIDEO STATUS ===`);
    for (const it of (v.body.items || [])) {
      console.log(`  ${it.id}  privacy=${it.status.privacyStatus}  upload=${it.status.uploadStatus}` +
        (it.processingDetails ? `  processing=${it.processingDetails.processingStatus}` : ""));
    }
  }
  return true;
}

async function main() {
  const meta = loadJson(META_PATH, null);
  if (!meta) { console.error(`missing ${META_PATH}`); process.exit(2); }
  const state = loadJson(STATE_PATH, { uploads: {}, thumbs: {}, playlist: {}, retired: {}, removedOldItem: false });
  const adapter = new YouTubeAdapter(ROOT);
  if (!adapter.isEnabled()) { console.error("youtube adapter not configured"); process.exit(2); }

  const only = (() => { const i = process.argv.indexOf("--phase"); return i >= 0 ? process.argv[i + 1] : null; })();
  const phases = {
    upload: () => phaseUpload(adapter, meta, state),
    thumbs: () => phaseThumbs(meta, state),
    playlist: () => phasePlaylist(adapter, meta, state),
    order: () => phaseOrder(adapter, meta, state),
    retire: () => phaseRetire(adapter, meta, state),
    verify: () => phaseVerify(adapter, meta, state),
  };
  const order = only ? [only] : ["upload", "thumbs", "playlist", "order", "retire", "verify"];
  for (const name of order) {
    if (!phases[name]) { console.error(`unknown phase ${name}`); process.exit(64); }
    console.log(`\n──── phase: ${name} ────`);
    const ok = await phases[name]();
    if (!ok) { console.error(`phase ${name} incomplete — state saved, re-run to resume`); process.exit(1); }
  }
  console.log("\nall phases complete");
}
main().catch((e) => { console.error("fatal:", e.stack || e.message); process.exit(3); });
