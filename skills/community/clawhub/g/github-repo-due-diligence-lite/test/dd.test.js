import { test } from "node:test";
import assert from "node:assert/strict";
import { summarize } from "../scripts/dd.js";

const fixture = (over = {}) => ({
  stargazers_count: 100,
  pushed_at: new Date(Date.now() - 30 * 86400000).toISOString(),
  license: { spdx_id: "MIT" },
  archived: false,
  ...over,
});

test("active repo", () => {
  const s = summarize("o", "r", fixture());
  assert.equal(s.health, "active");
  assert.equal(s.license, "MIT");
  assert.equal(s.repo, "o/r");
});

test("archived repo wins over other states", () => {
  const s = summarize("o", "r", fixture({ archived: true }));
  assert.equal(s.health, "archived");
});

test("stale >365 days", () => {
  const s = summarize("o", "r", fixture({ pushed_at: new Date(Date.now() - 400 * 86400000).toISOString() }));
  assert.equal(s.health, "stale (>1y)");
});

test("quiet 180-365 days, missing license → null", () => {
  const s = summarize("o", "r", fixture({ pushed_at: new Date(Date.now() - 200 * 86400000).toISOString(), license: null }));
  assert.equal(s.health, "quiet");
  assert.equal(s.license, null);
});

test("fields the lite drops produce upgrade hint", () => {
  const s = summarize("o", "r", fixture({ forks_count: 12, open_issues_count: 4, default_branch: "main", language: "JavaScript" }));
  assert.equal(s.upgrade.skill, "github-repo-due-diligence");
  assert.ok(s.upgrade.reasons.length > 0);
});

test("minimal response has no upgrade field", () => {
  assert.equal(summarize("o", "r", fixture()).upgrade, undefined);
});
