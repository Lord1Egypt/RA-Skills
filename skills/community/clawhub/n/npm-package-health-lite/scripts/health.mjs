#!/usr/bin/env node
// npm-package-health-lite — public npm registry metadata, single request:
// latest version, last publish age, deprecation, license. No installs.
// Exit 0 ok, 1 fetch failed, 2 missing arg.
import https from "node:https";

function get(url) {
  return new Promise((resolve, reject) => {
    https
      .get(url, { headers: { "User-Agent": "npm-package-health-lite" }, timeout: 15000 }, (res) => {
        let b = "";
        res.on("data", (c) => (b += c));
        res.on("end", () => resolve({ status: res.statusCode, body: b }));
      })
      .on("error", reject)
      .on("timeout", function () { this.destroy(new Error("timeout")); });
  });
}

export function summarize(pkg, d) {
  const latest = d["dist-tags"]?.latest;
  const lastPublish = d.time?.[latest] ?? null;
  const ageDays = lastPublish ? Math.round((Date.now() - new Date(lastPublish)) / 86400000) : null;
  const deprecated = d.versions?.[latest]?.deprecated ?? null;
  const health = deprecated ? "deprecated" : ageDays != null && ageDays > 730 ? "stale (>2y)" : "ok";
  return {
    package: pkg,
    latest,
    lastPublish,
    ageDays,
    deprecated,
    license: d.versions?.[latest]?.license ?? d.license ?? null,
    health,
  };
}

if (process.argv[1]?.endsWith("health.mjs")) {
  const pkg = process.argv[2];
  if (!pkg) {
    console.error("usage: node health.mjs <package-name>");
    process.exit(2);
  }
  try {
    const meta = await get(`https://registry.npmjs.org/${encodeURIComponent(pkg)}`);
    if (meta.status !== 200) {
      console.error(JSON.stringify({ error: `npm returned ${meta.status}` }));
      process.exit(1);
    }
    console.log(JSON.stringify(summarize(pkg, JSON.parse(meta.body)), null, 2));
  } catch (e) {
    console.error(JSON.stringify({ error: e.message }));
    process.exit(1);
  }
}
