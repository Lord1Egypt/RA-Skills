'use strict';
// 在金山多维表新增一条记录（最小可用：单个主字段）。凭证只读本地 600，输出不含明文 token。
const https = require("https");
const { ensureToken } = require("./wps_auth.cjs");

function postJSON(pth, tok, obj) {
  return new Promise((resolve) => {
    const body = JSON.stringify(obj);
    const req = https.request({ host: "openapi.wps.cn", path: pth, method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bea" + "rer " + tok, "Content-Length": Buffer.byteLength(body) } },
      (res) => { let d = ""; res.on("data", x => d += x); res.on("end", () => { let o = {}; try { o = JSON.parse(d); } catch (e) { o._raw = d.slice(0, 200); } resolve({ status: res.statusCode, o }); }); });
    req.on("error", e => resolve({ err: e.message }));
    req.write(body); req.end();
  });
}

(async () => {
  const [file_id, sheet_id, field, value] = process.argv.slice(2);
  if (!file_id || !sheet_id || field === undefined || value === undefined) {
    console.error("用法: node dbsheet_record_create.cjs <file_id> <sheet_id> <主字段名> <值>");
    process.exit(2);
  }
  const tok = await ensureToken();
  const fields_value = JSON.stringify({ [field]: value });
  const url = "/v7/coop/dbsheet/" + file_id + "/sheets/" + sheet_id + "/records/create";
  const r = await postJSON(url, tok, { records: [{ fields_value }] });
  const rec = (r.o && r.o.data && ((r.o.data.records && r.o.data.records[0]) || r.o.data[0])) || {};
  console.log("HTTP " + r.status + " | code " + (r.o && r.o.code !== undefined ? r.o.code : "-") + " | msg " + ((r.o && (r.o.msg || r.o.error_description)) || "-") + " | record_id " + (rec.id || rec.record_id || "-"));
})().catch(e => { console.error("ERROR:", e.message); process.exitCode = 1; });
