import { test } from "node:test";
import assert from "node:assert/strict";
import { summarize } from "../scripts/health.mjs";

const fixture = (over = {}) => ({
  "dist-tags": { latest: "1.0.0" },
  time: { "1.0.0": new Date(Date.now() - 30 * 86400000).toISOString() },
  versions: { "1.0.0": { license: "MIT" } },
  ...over,
});

test("healthy package", () => {
  const s = summarize("pkg", fixture());
  assert.equal(s.health, "ok");
  assert.equal(s.latest, "1.0.0");
  assert.equal(s.license, "MIT");
});

test("deprecated wins", () => {
  const s = summarize("pkg", fixture({ versions: { "1.0.0": { deprecated: "use x instead" } } }));
  assert.equal(s.health, "deprecated");
  assert.equal(s.deprecated, "use x instead");
});

test("stale >730 days", () => {
  const s = summarize("pkg", fixture({ time: { "1.0.0": new Date(Date.now() - 800 * 86400000).toISOString() } }));
  assert.equal(s.health, "stale (>2y)");
});

test("missing license → null, missing time → ageDays null, health ok", () => {
  const s = summarize("pkg", { "dist-tags": { latest: "1.0.0" }, versions: { "1.0.0": {} } });
  assert.equal(s.license, null);
  assert.equal(s.ageDays, null);
  assert.equal(s.health, "ok");
});
