'use strict';
// 读取金山多维表 schema：列出子表(sheet)与字段(field)。凭证只读本地 600，输出不含明文 token。
const https = require("https");
const { ensureToken } = require("./wps_auth.cjs");

function get(pth, tok) {
  return new Promise((resolve) => {
    const req = https.request({ host: "openapi.wps.cn", path: pth, method: "GET",
      headers: { Authorization: "Bea" + "rer " + tok } },
      (res) => { let d = ""; res.on("data", x => d += x); res.on("end", () => { let o = {}; try { o = JSON.parse(d); } catch (e) { o._raw = d.slice(0, 200); } resolve({ status: res.statusCode, o }); }); });
    req.on("error", e => resolve({ err: e.message }));
    req.end();
  });
}

(async () => {
  const file_id = process.argv[2];
  if (!file_id) { console.error("用法: node dbsheet_schema.cjs <file_id>"); process.exit(2); }
  const tok = await ensureToken();
  const r = await get("/v7/coop/dbsheet/" + file_id + "/schema", tok);
  console.log("HTTP " + r.status + " | code " + (r.o && r.o.code !== undefined ? r.o.code : "-") + " | msg " + ((r.o && (r.o.msg || r.o.error_description)) || "-"));
  const data = (r.o && r.o.data) || {};
  const sheets = data.sheets || data.tables || [];
  console.log("子表数: " + sheets.length);
  sheets.forEach(s => {
    const fields = s.fields || s.columns || [];
    const fs_ = fields.map(f => (f.name || f.title || "?") + "[" + (f.type || "?") + "]").join(", ");
    console.log("  - sheet_id=" + (s.id || s.sheet_id) + " 表名=" + (s.name || s.title || "-") + " 记录数=" + (s.records_count !== undefined ? s.records_count : "?"));
    if (fs_) console.log("      字段: " + fs_);
  });
})().catch(e => { console.error("ERROR:", e.message); process.exitCode = 1; });
