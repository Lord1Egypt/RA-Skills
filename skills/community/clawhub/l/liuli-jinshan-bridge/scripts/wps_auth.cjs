'use strict';
// 琉璃金山桥 · 鉴权 lib：确保有效的 WPS user access_token（refresh 自动续期）。
// 凭证只从 ~/.config/wps-openapi/ 读取；本文件与运行输出均不打印任何 token/secret 明文。
const fs = require("fs");
const https = require("https");
const querystring = require("querystring");
const path = require("path");
const os = require("os");

const DIR = process.env.WPS_OPENAPI_DIR || path.join(os.homedir(), ".config", "wps-openapi");

function rd(n) { try { return fs.readFileSync(path.join(DIR, n), "utf8").trim(); } catch (e) { return ""; } }
function wr(n, v) { fs.writeFileSync(path.join(DIR, n), v, { mode: 0o600 }); try { fs.chmodSync(path.join(DIR, n), 0o600); } catch (e) {} }

function jwtExp(tok) {
  try { const p = String(tok).split(".")[1]; const j = JSON.parse(Buffer.from(p, "base64url").toString("utf8")); return j.exp || 0; }
  catch (e) { return 0; }
}

function postForm(pth, obj) {
  return new Promise((resolve) => {
    const body = querystring.stringify(obj);
    const req = https.request({ host: "openapi.wps.cn", path: pth, method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded", "Content-Length": Buffer.byteLength(body) } },
      (res) => { let d = ""; res.on("data", x => d += x); res.on("end", () => { let o = {}; try { o = JSON.parse(d); } catch (e) { o._raw = d.slice(0, 160); } resolve({ status: res.statusCode, o }); }); });
    req.on("error", e => resolve({ err: e.message }));
    req.write(body); req.end();
  });
}

// 用 refresh_token 换新的 access_token（+滚动 refresh），只落 600，不外显
async function refresh() {
  const id = rd("client_id"), sec = rd("client_secret"), rt = rd("refresh_token");
  if (!rt) throw new Error("NO_REFRESH: 缺少 refresh_token，请先完成一次 user OAuth 授权（见 references/setup.md）");
  const ex = await postForm("/oauth2/token", { grant_type: "refresh_token", client_id: id, client_secret: sec, refresh_token: rt });
  if (!ex.o || !ex.o.access_token) throw new Error("REFRESH_FAIL HTTP " + (ex.status || ex.err) + " code " + ((ex.o && ex.o.code) || "-") + " " + ((ex.o && ex.o.msg) || ""));
  wr("access_token", ex.o.access_token);
  if (ex.o.refresh_token) wr("refresh_token", ex.o.refresh_token); // 轮换：旧 refresh 作废，新值已落 600
  return ex.o.access_token;
}

// 确保拿到未临期的 access_token；临期(<=5min)或缺失则自动 refresh
async function ensureToken() {
  let t = rd("access_token");
  const now = Math.floor(Date.now() / 1000);
  if (!t || jwtExp(t) < now + 300) t = await refresh();
  return t;
}

module.exports = { ensureToken, refresh, DIR, rd, wr };

// 直接运行：自测 token 健康
if (require.main === module && process.argv[2] === "--selftest") {
  (async () => {
    try {
      const t = await ensureToken();
      const exp = jwtExp(t);
      console.log("selftest OK: token 可用, at_len=" + t.length + ", 剩余秒=" + Math.max(0, exp - Math.floor(Date.now() / 1000)));
    } catch (e) {
      console.log("selftest FAIL:", e.message);
      process.exitCode = 1;
    }
  })();
}
