"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const PKG_DIR = path.resolve(__dirname, "..");

test("keep-query _meta.json has expected name and mcp url", () => {
  const meta = JSON.parse(fs.readFileSync(path.join(PKG_DIR, "_meta.json"), "utf8"));
  assert.equal(meta.name, "keep-query");
  assert.equal(meta.requires.mcp, "https://mcp.gotokeep.com/skills-mcp-gateway-page/v1");
});

test("keep-query SKILL.md documents query_tool and MCP gateway", () => {
  const skill = fs.readFileSync(path.join(PKG_DIR, "SKILL.md"), "utf8");
  assert.match(skill, /name:\s*keep-query/);
  assert.match(skill, /query_tool/);
  assert.match(skill, /skills-mcp-gateway-page\/v1/);
  assert.match(skill, /keep-record/);
});

test("keep-query mcp-call.js sets KEEP_INVOKE_SOURCE=keep-query", () => {
  const script = fs.readFileSync(path.join(PKG_DIR, "scripts", "mcp-call.js"), "utf8");
  assert.match(script, /KEEP_INVOKE_SOURCE\s*=\s*["']keep-query["']/);
});
