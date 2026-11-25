'use strict';
// 读取金山多维表指定记录内容。正确端点：GET /v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/{record_id}
// 用法: node dbsheet_records_list.cjs <file_id> <sheet_id> [record_id1,record_id2,...]
// 不传 ids 时，按字母序号 A..Z 逐个读，遇 404/not found 即停。凭证只读本地600，输出不含明文token。
const https = require("https");
const { ensureToken } = require("./wps_auth.cjs");

function get(pth, tok) {
  return new Promise((resolve) => {
    const r = https.request({ host: "openapi.wps.cn", path: pth, method: "GET", headers: { Authorization: "Bea" + "rer " + tok } }, (res) => {
      let d = ""; res.on("data", x => d += x); res.on("end", () => { let o = {}; try { o = JSON.parse(d); } catch (e) { o._raw = d.slice(0, 200); } resolve({ status: res.statusCode, o }); });
    });
    r.on("error", e => resolve({ err: e.message })); r.end();
  });
}

function textOf(rec) {
  let f = rec.fields;
  if (typeof f === "string") { try { f = JSON.parse(f); } catch (e) { f = {}; } }
  if (f && f.Text !== undefined) return f.Text;
  const k = Object.keys(f || {})[0];
  return k ? f[k] : JSON.stringify(f);
}

(async () => {
  const FILE_ID = process.argv[2];
  if (!FILE_ID) { console.error("请传入你的多维表 file_id（第一个参数）"); process.exitCode = 1; return; }
  const SHEET = process.argv[3] || "1";
  const idsArg = process.argv[4];
  const tok = await ensureToken();
  const base = "/v7/coop/dbsheet/" + FILE_ID + "/sheets/" + SHEET + "/records/";
  let ids;
  if (idsArg) ids = idsArg.split(",").map(s => s.trim()).filter(Boolean);
  else ids = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
  let n = 0;
  for (const id of ids) {
    const r = await get(base + id, tok);
    const rec = r.o && r.o.data && r.o.data.record;
    if (r.status === 200 && rec) {
      console.log("  [" + (rec.id || id) + "] " + textOf(rec));
      n++;
    } else if (!idsArg) {
      break; // 自动扫描模式：连续空即停
    }
  }
  console.log("共读回 " + n + " 条记录");
})().catch(e => { console.error("ERROR:", e.message); process.exitCode = 1; });
