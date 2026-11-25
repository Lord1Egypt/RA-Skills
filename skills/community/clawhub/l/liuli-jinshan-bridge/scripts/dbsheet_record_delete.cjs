'use strict';
// 删除金山多维表记录。端点 POST /v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/batch_delete
// body {"records":["<id>",...]}。凭证只读本地600，输出不含明文token。
// 用法: node dbsheet_record_delete.cjs <file_id> <sheet_id> <id1,id2,...>
const https = require("https");
const { ensureToken } = require("./wps_auth.cjs");
function post(pth, tok, obj) {
  return new Promise((resolve) => {
    const body = JSON.stringify(obj);
    const r = https.request({ host: "openapi.wps.cn", path: pth, method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bea" + "rer " + tok, "Content-Length": Buffer.byteLength(body) } }, (res) => {
      let d = ""; res.on("data", x => d += x); res.on("end", () => { let o = {}; try { o = JSON.parse(d); } catch (e) { o._raw = d.slice(0, 200); } resolve({ status: res.statusCode, o }); });
    });
    r.on("error", e => resolve({ err: e.message })); r.write(body); r.end();
  });
}
(async () => {
  const FILE_ID = process.argv[2];
  if (!FILE_ID) { console.error("请传入你的多维表 file_id（第一个参数）"); process.exitCode = 1; return; }
  const SHEET = process.argv[3] || "1";
  const ids = (process.argv[4] || "").split(",").map(s => s.trim()).filter(Boolean);
  if (!ids.length) { console.error("缺少要删除的 record_id"); process.exitCode = 1; return; }
  const tok = await ensureToken();
  const r = await post("/v7/coop/dbsheet/" + FILE_ID + "/sheets/" + SHEET + "/records/batch_delete", tok, { records: ids });
  console.log("删除 HTTP " + r.status + " code " + (r.o && r.o.code) + " ids=" + ids.join(","));
})().catch(e => { console.error("ERROR:", e.message); process.exitCode = 1; });
