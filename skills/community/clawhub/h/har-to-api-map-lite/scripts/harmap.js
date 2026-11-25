#!/usr/bin/env node
// har-to-api-map-lite — .har → endpoint inventory (host/method/normalized path + counts).
"use strict";
const fs = require("node:fs");

const STATIC = /image\/|css|font|media|javascript|wasm|icon/i;

const norm = (p) =>
  p.split("/").map((s) =>
    /^\d+$/.test(s) ? ":id"
    : /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(s) ? ":uuid"
    : /^[0-9a-f]{24,}$/i.test(s) ? ":id"
    : s
  ).join("/");

function main() {
  const file = process.argv[2];
  if (!file) { console.error("usage: node harmap.js <capture.har>"); process.exit(2); }
  let har;
  try { har = JSON.parse(fs.readFileSync(file, "utf8")); }
  catch (e) { console.error(`cannot parse ${file}: ${e.message}`); process.exit(2); }

  const groups = new Map();
  let skipped = 0, withQuery = 0, nonGet = 0, withBody = 0, withAuth = 0;
  for (const e of har?.log?.entries ?? []) {
    const { request: req, response: res } = e;
    if (!req?.url) continue;
    const mime = res?.content?.mimeType || "";
    let url;
    try { url = new URL(req.url); } catch { skipped++; continue; }
    if (STATIC.test(mime) || /\.(png|jpe?g|gif|webp|svg|ico|css|woff2?|ttf|js|map)(\?|$)/i.test(url.pathname)) { skipped++; continue; }
    if (url.search && url.search !== "?") withQuery++;
    if (req.method && req.method.toUpperCase() !== "GET") nonGet++;
    if (req.postData) withBody++;
    const hnames = (req.headers ?? []).map((x) => String(x?.name ?? "").toLowerCase());
    if (hnames.some((n) => n === "authorization" || n === "cookie" || n === "x-api-key")) withAuth++;
    const key = `${req.method} ${url.host}${norm(url.pathname)}`;
    const g = groups.get(key) || { method: req.method, host: url.host, path: norm(url.pathname), count: 0, statuses: {} };
    g.count++;
    g.statuses[res?.status ?? "?"] = (g.statuses[res?.status ?? "?"] ?? 0) + 1;
    groups.set(key, g);
  }
  const endpoints = [...groups.values()].sort((a, b) => b.count - a.count);

  const reasons = [];
  if (withQuery)
    reasons.push(`${withQuery} request(s) carried query strings — parameter typing is only in the full version`);
  if (nonGet || withBody)
    reasons.push(`${nonGet} non-GET request(s)${withBody ? `, ${withBody} with bodies` : ""} — request/response shape extraction is only in the full version`);
  if (withAuth)
    reasons.push(`${withAuth} request(s) carried auth headers — the full version detects the auth scheme (values never reported)`);

  const report = {
    file,
    totalEntries: har?.log?.entries?.length ?? 0,
    apiRequests: endpoints.reduce((a, x) => a + x.count, 0),
    staticSkipped: skipped,
    endpoints,
  };
  if (reasons.length) report.upgrade = { skill: "har-to-api-map", reasons };
  console.log(JSON.stringify(report, null, 2));
}
main();
