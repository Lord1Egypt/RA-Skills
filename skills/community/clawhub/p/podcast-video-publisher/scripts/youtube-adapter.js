/**
 * YouTube adapter — uploads a track or oration to the channel via the
 * YouTube Data API v3. Implements the same Broadcaster interface as
 * Bluesky/Mastodon/Telegram/Nostr but takes an extra `media` field
 * because YouTube needs an actual video file, not just a text + link.
 *
 * Auth: OAuth2 refresh token. Generate once via scripts/youtube-grant.js,
 * which writes .youtube.json at the project root with
 *   { client_id, client_secret, refresh_token, channel_id, ... }.
 *
 * Quota note: video.insert costs 1600 units; default daily quota is
 * 10,000 — i.e. ~6 uploads/day. We never auto-upload more than once per
 * call from the announce script, so the cron can't burst into the
 * daily ceiling.
 *
 * Behaviour when no media is provided: post() resolves to
 * `{ ok: false, error: "no_media" }` so the broadcaster fan-out can
 * keep going without YouTube blocking text-only routes (Bluesky etc).
 */

"use strict";

const fs = require("fs");
const fsp = fs.promises;
const path = require("path");
const https = require("https");
const { URL } = require("url");

const TOKEN_URL = "https://oauth2.googleapis.com/token";
const UPLOAD_URL =
  "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status";

// In-process token cache so consecutive uploads in the same process
// don't burn through Google's per-minute token endpoint quota.
const _cache = { access_token: "", expires_at: 0 };

class YouTubeAdapter {
  constructor(rootDir) {
    this.name = "youtube";
    this._rootDir = rootDir || ".";
    this._creds = null;
    const credPath = path.join(this._rootDir, ".youtube.json");
    if (fs.existsSync(credPath)) {
      try {
        this._creds = JSON.parse(fs.readFileSync(credPath, "utf8"));
      } catch (_) {
        this._creds = null;
      }
    }
  }

  isEnabled() {
    return !!(this._creds && this._creds.client_id && this._creds.refresh_token);
  }

  async post({ text, link, topic, media }) {
    if (!this.isEnabled()) {
      return { ok: false, error: "not_configured" };
    }
    if (!media || !media.path) {
      return { ok: false, error: "no_media" };
    }
    if (!fs.existsSync(media.path)) {
      return { ok: false, error: `media_missing: ${media.path}` };
    }

    let access;
    try {
      access = await this._accessToken();
    } catch (e) {
      return { ok: false, error: `token_refresh_failed: ${e.message}` };
    }

    const title = (media.title || "Untitled").slice(0, 100);
    const description =
      (text || "") +
      (link ? `\n\n${link}` : "") +
      (topic ? `\n\n#${topic}` : "");
    // YouTube descriptions cap at 5000 chars.
    const descTrimmed = description.slice(0, 5000);

    const tags = Array.isArray(media.tags) ? media.tags.slice(0, 15) : [];

    const meta = {
      snippet: {
        title,
        description: descTrimmed,
        tags,
        categoryId: media.categoryId || "10", // 10 = Music
      },
      status: {
        privacyStatus: media.privacy || "public",
        selfDeclaredMadeForKids: false,
      },
    };

    let body, contentType;
    try {
      ({ body, contentType } = await this._buildMultipart(meta, media.path));
    } catch (e) {
      return { ok: false, error: `multipart_build_failed: ${e.message}` };
    }

    let resp;
    try {
      resp = await this._uploadMultipart(body, contentType, access);
    } catch (e) {
      return { ok: false, error: `upload_io: ${e.message}` };
    }
    if (resp.status !== 200) {
      const detail =
        resp.body && resp.body.error && resp.body.error.message
          ? resp.body.error.message
          : (typeof resp.body === "string" ? resp.body.slice(0, 200) : JSON.stringify(resp.body).slice(0, 200));
      return { ok: false, error: `upload_status_${resp.status}: ${detail}` };
    }
    const id = resp.body && resp.body.id;
    if (!id) {
      return { ok: false, error: "no_video_id_in_response" };
    }

    // Optional: add to the configured playlist. Fire-and-forget on
    // failure — we don't want a bad playlist setting to roll back the
    // successful upload. Quota cost: 50 units per playlistItem insert
    // (vs 1600 for the upload itself), so this is cheap.
    let playlist_status = null;
    if (this._creds.playlist_id) {
      try {
        const pl = await this._addToPlaylist(id, this._creds.playlist_id, access);
        playlist_status = pl.ok ? "added" : `playlist_failed: ${pl.error}`;
      } catch (e) {
        playlist_status = `playlist_failed: ${e.message}`;
      }
    }

    return {
      ok: true,
      url: `https://www.youtube.com/watch?v=${id}`,
      id,
      playlist: playlist_status,
    };
  }

  async _addToPlaylist(videoId, playlistId, access) {
    return new Promise((resolve, reject) => {
      const body = JSON.stringify({
        snippet: {
          playlistId,
          resourceId: { kind: "youtube#video", videoId },
        },
      });
      const u = new URL(
        "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet"
      );
      const req = https.request(
        {
          method: "POST",
          hostname: u.hostname,
          path: u.pathname + u.search,
          headers: {
            Authorization: `Bearer ${access}`,
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(body),
          },
        },
        (res) => {
          const chunks = [];
          res.on("data", (c) => chunks.push(c));
          res.on("end", () => {
            const text = Buffer.concat(chunks).toString("utf8");
            let parsed;
            try { parsed = JSON.parse(text); } catch (_) { parsed = text; }
            if (res.statusCode === 200 && parsed && parsed.id) {
              resolve({ ok: true, item_id: parsed.id });
            } else {
              const detail =
                parsed && parsed.error && parsed.error.message
                  ? parsed.error.message
                  : (typeof parsed === "string" ? parsed.slice(0, 200) : JSON.stringify(parsed).slice(0, 200));
              resolve({ ok: false, error: `status_${res.statusCode}: ${detail}` });
            }
          });
        }
      );
      req.on("error", reject);
      req.write(body);
      req.end();
    });
  }

  // ── internals ─────────────────────────────────────────────

  async _accessToken() {
    const now = Date.now();
    // 60-sec safety margin before expiry.
    if (_cache.access_token && _cache.expires_at - 60_000 > now) {
      return _cache.access_token;
    }
    const params = new URLSearchParams({
      client_id: this._creds.client_id,
      client_secret: this._creds.client_secret,
      refresh_token: this._creds.refresh_token,
      grant_type: "refresh_token",
    }).toString();
    const resp = await postRaw(TOKEN_URL, params, {
      "Content-Type": "application/x-www-form-urlencoded",
    });
    if (resp.status !== 200 || !resp.body || !resp.body.access_token) {
      throw new Error(
        `token_status_${resp.status}: ${
          typeof resp.body === "string"
            ? resp.body.slice(0, 200)
            : JSON.stringify(resp.body).slice(0, 200)
        }`
      );
    }
    _cache.access_token = resp.body.access_token;
    _cache.expires_at = now + Math.max(60, resp.body.expires_in - 60) * 1000;
    return _cache.access_token;
  }

  async _buildMultipart(meta, mediaPath) {
    const boundary = "kannaka-yt-" + Math.random().toString(16).slice(2);
    const metaPart =
      `--${boundary}\r\n` +
      `Content-Type: application/json; charset=UTF-8\r\n\r\n` +
      `${JSON.stringify(meta)}\r\n`;
    const mediaHeader =
      `--${boundary}\r\n` +
      `Content-Type: video/mp4\r\n\r\n`;
    const trailer = `\r\n--${boundary}--\r\n`;
    const fileBuf = await fsp.readFile(mediaPath);
    const body = Buffer.concat([
      Buffer.from(metaPart, "utf8"),
      Buffer.from(mediaHeader, "utf8"),
      fileBuf,
      Buffer.from(trailer, "utf8"),
    ]);
    return {
      body,
      contentType: `multipart/related; boundary=${boundary}`,
    };
  }

  async _uploadMultipart(body, contentType, access) {
    return new Promise((resolve, reject) => {
      const u = new URL(UPLOAD_URL);
      const req = https.request(
        {
          method: "POST",
          hostname: u.hostname,
          path: u.pathname + u.search,
          headers: {
            Authorization: `Bearer ${access}`,
            "Content-Type": contentType,
            "Content-Length": body.length,
          },
        },
        (res) => {
          const chunks = [];
          res.on("data", (c) => chunks.push(c));
          res.on("end", () => {
            const text = Buffer.concat(chunks).toString("utf8");
            try {
              resolve({ status: res.statusCode, body: JSON.parse(text) });
            } catch (_) {
              resolve({ status: res.statusCode, body: text });
            }
          });
        }
      );
      req.on("error", reject);
      req.write(body);
      req.end();
    });
  }
}

// Helper: small POST utility shared with the grant script style.
function postRaw(url, body, headers) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = https.request(
      {
        method: "POST",
        hostname: u.hostname,
        path: u.pathname + u.search,
        headers: {
          ...headers,
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => {
          const text = Buffer.concat(chunks).toString("utf8");
          try {
            resolve({ status: res.statusCode, body: JSON.parse(text) });
          } catch (_) {
            resolve({ status: res.statusCode, body: text });
          }
        });
      }
    );
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

module.exports = { YouTubeAdapter };
