import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";

import {inferIntent, starterPromptRoutes} from "../src/orchestration/intent-router.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("OpenAI entry explicitly invokes the installed skill", () => {
  const source = fs.readFileSync(path.join(ROOT, "agents/openai.yaml"), "utf8");
  assert.match(source, /default_prompt:/u);
  assert.match(source, /\$majia-chatcut-koubo/u);
});

test("all four starter intents route deterministically", () => {
  const routes = starterPromptRoutes();
  assert.equal(routes.length, 4);
  for (const route of routes) {
    const actual = inferIntent(route.prompt);
    assert.equal(actual.action, route.expected.action, route.prompt);
    assert.equal(actual.mode, route.expected.mode, route.prompt);
  }
});

test("starter documentation keeps the live boundary explicit", () => {
  for (const relative of [
    "workflows/one-click-stable.md",
    "workflows/fast-cut.md",
    "workflows/pro-enhance.md",
    "workflows/resume.md",
  ]) {
    const source = fs.readFileSync(path.join(ROOT, relative), "utf8");
    assert.match(source, /UNVERIFIED/u, relative);
  }
});
