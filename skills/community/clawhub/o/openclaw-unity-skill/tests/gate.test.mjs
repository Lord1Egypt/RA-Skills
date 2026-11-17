// Tests for the runtime confirmation gate in extension/index.ts.
//
//   node --test tests/gate.test.mjs        (Node 22.18+ / 24 — strips TS types)
//
// No Unity Editor is needed: the gate is a pure function over the tool name,
// its parameters, the confirm flag and the environment.

import { test } from "node:test";
import assert from "node:assert/strict";

import {
  classifyTool,
  destructiveOperationsEnabled,
  evaluateDestructiveGate,
  projectChangingTools,
} from "../extension/index.ts";
import plugin from "../extension/index.ts";

const OFF = {};
const ON = { OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE: "1" };

/** Every tool documented in references/tools.md. */
const CATALOG = [
  "app.getState",
  "app.pause",
  "app.play",
  "app.stop",
  "asset.copy",
  "asset.delete",
  "asset.find",
  "asset.getPath",
  "asset.import",
  "asset.move",
  "asset.refresh",
  "batch.execute",
  "component.add",
  "component.get",
  "component.list",
  "component.remove",
  "component.set",
  "console.clear",
  "console.getErrors",
  "console.getLogs",
  "debug.hierarchy",
  "debug.log",
  "debug.screenshot",
  "editor.domainReload",
  "editor.focusWindow",
  "editor.getState",
  "editor.listWindows",
  "editor.pause",
  "editor.play",
  "editor.recompile",
  "editor.refresh",
  "editor.stop",
  "editor.unpause",
  "gameobject.create",
  "gameobject.delete",
  "gameobject.destroy",
  "gameobject.find",
  "gameobject.getAll",
  "gameobject.getData",
  "gameobject.setActive",
  "gameobject.setParent",
  "input.clickUI",
  "input.getMousePosition",
  "input.keyDown",
  "input.keyPress",
  "input.keyUp",
  "input.mouseClick",
  "input.mouseDrag",
  "input.mouseMove",
  "input.mouseScroll",
  "input.type",
  "material.assign",
  "material.create",
  "material.getInfo",
  "material.list",
  "material.modify",
  "package.add",
  "package.list",
  "package.remove",
  "package.search",
  "prefab.close",
  "prefab.create",
  "prefab.instantiate",
  "prefab.open",
  "prefab.save",
  "scene.getActive",
  "scene.getData",
  "scene.list",
  "scene.load",
  "scene.open",
  "scene.save",
  "scene.saveAll",
  "script.execute",
  "script.list",
  "script.read",
  "scriptableobject.create",
  "scriptableobject.getField",
  "scriptableobject.list",
  "scriptableobject.load",
  "scriptableobject.save",
  "scriptableobject.setField",
  "session.getInfo",
  "shader.getInfo",
  "shader.getKeywords",
  "shader.list",
  "test.getResults",
  "test.list",
  "test.run",
  "texture.create",
  "texture.getInfo",
  "texture.list",
  "texture.resize",
  "texture.setPixels",
  "transform.getPosition",
  "transform.getRotation",
  "transform.getScale",
  "transform.setPosition",
  "transform.setRotation",
  "transform.setScale",
];

/** The subset that only reads state — everything else must be gated. */
const READ_ONLY = new Set([
  "app.getState",
  "asset.find",
  "asset.getPath",
  "component.get",
  "component.list",
  "console.getErrors",
  "console.getLogs",
  "debug.hierarchy",
  "debug.log",
  "debug.screenshot",
  "editor.focusWindow",
  "editor.getState",
  "editor.listWindows",
  "gameobject.find",
  "gameobject.getAll",
  "gameobject.getData",
  "input.getMousePosition",
  "material.getInfo",
  "material.list",
  "package.list",
  "package.search",
  "scene.getActive",
  "scene.getData",
  "scene.list",
  "script.list",
  "script.read",
  "scriptableobject.getField",
  "scriptableobject.list",
  "scriptableobject.load",
  "session.getInfo",
  "shader.getInfo",
  "shader.getKeywords",
  "shader.list",
  "test.getResults",
  "test.list",
  "texture.getInfo",
  "texture.list",
  "transform.getPosition",
  "transform.getRotation",
  "transform.getScale",
]);

test("every catalogued tool is classified, and only read-only ones pass ungated", () => {
  const wrong = [];
  for (const tool of CATALOG) {
    const expected = READ_ONLY.has(tool) ? "read-only" : "project-changing";
    const actual = classifyTool(tool);
    if (actual !== expected) wrong.push(`${tool}: expected ${expected}, got ${actual}`);
  }
  assert.deepEqual(wrong, []);
  assert.equal(CATALOG.length, 99);
  assert.equal(CATALOG.filter((t) => READ_ONLY.has(t)).length, READ_ONLY.size);
});

test("read-only calls are unaffected by the gate", () => {
  for (const tool of CATALOG.filter((t) => READ_ONLY.has(t))) {
    const decision = evaluateDestructiveGate({ tool, env: OFF });
    assert.equal(decision.allowed, true, tool);
    assert.equal(decision.reason, "read-only", tool);
    assert.deepEqual(decision.tools, []);
  }
});

test("a project-changing call is refused without the operator opt-in", () => {
  const decision = evaluateDestructiveGate({
    tool: "asset.delete",
    parameters: { path: "Assets/Player.prefab" },
    confirm: true,
    env: OFF,
  });
  assert.equal(decision.allowed, false);
  assert.equal(decision.reason, "operator-opt-in-missing");
  assert.deepEqual(decision.tools, ["asset.delete"]);
  assert.match(decision.message, /OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1/);
});

test("a project-changing call is refused with the opt-in but no confirm", () => {
  for (const confirm of [undefined, false, "no", 0, {}, "TRUE-ish"]) {
    const decision = evaluateDestructiveGate({
      tool: "script.execute",
      parameters: { code: "AssetDatabase.DeleteAsset(\"Assets\")" },
      confirm,
      env: ON,
    });
    assert.equal(decision.allowed, false, String(confirm));
    assert.equal(decision.reason, "confirmation-missing", String(confirm));
    assert.match(decision.message, /confirm: true/);
  }
});

test("a project-changing call proceeds with the opt-in and confirm", () => {
  for (const confirm of [true, "true", "1", "yes"]) {
    const decision = evaluateDestructiveGate({
      tool: "script.execute",
      parameters: { code: "Debug.Log(1)" },
      confirm,
      env: ON,
    });
    assert.equal(decision.allowed, true, String(confirm));
    assert.equal(decision.reason, "confirmed", String(confirm));
  }
});

test("batch.execute is as risky as the riskiest command it carries", () => {
  const readOnlyBatch = {
    commands: [{ tool: "debug.hierarchy" }, { tool: "scene.getActive" }],
  };
  assert.equal(classifyTool("batch.execute", readOnlyBatch), "read-only");
  assert.equal(
    evaluateDestructiveGate({ tool: "batch.execute", parameters: readOnlyBatch, env: OFF }).allowed,
    true
  );

  const mixedBatch = {
    commands: [{ tool: "debug.hierarchy" }, { tool: "gameobject.destroy", params: { name: "Player" } }],
  };
  assert.equal(classifyTool("batch.execute", mixedBatch), "project-changing");
  assert.deepEqual(projectChangingTools("batch.execute", mixedBatch), ["gameobject.destroy"]);
  const refused = evaluateDestructiveGate({
    tool: "batch.execute",
    parameters: mixedBatch,
    confirm: true,
    env: OFF,
  });
  assert.equal(refused.allowed, false);
  assert.match(refused.message, /gameobject\.destroy/);
});

test("the gate fails closed on unknown, unnamed and malformed calls", () => {
  assert.equal(classifyTool("mygame.resetSave"), "project-changing");
  assert.equal(classifyTool("totally.unknown"), "project-changing");
  assert.equal(classifyTool(""), "project-changing");
  assert.equal(classifyTool(undefined), "project-changing");
  assert.equal(classifyTool("batch.execute", {}), "project-changing");
  assert.equal(classifyTool("batch.execute", { commands: [] }), "project-changing");
  assert.equal(classifyTool("batch.execute", { commands: ["oops"] }), "project-changing");
  assert.equal(
    classifyTool("batch.execute", {
      commands: [{ tool: "batch.execute", params: { commands: [{ tool: "asset.delete" }] } }],
    }),
    "project-changing"
  );
  // A custom read-only tool still passes: the allowlist is on the verb.
  assert.equal(classifyTool("mygame.getScore"), "read-only");
});

test("the operator opt-in is read from either environment variable", () => {
  assert.equal(destructiveOperationsEnabled({}), false);
  assert.equal(destructiveOperationsEnabled({ OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE: "0" }), false);
  assert.equal(destructiveOperationsEnabled({ OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE: "" }), false);
  assert.equal(destructiveOperationsEnabled({ OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE: "true" }), true);
  assert.equal(destructiveOperationsEnabled({ OPENCLAW_UNITY_ALLOW_DESTRUCTIVE: "1" }), true);
});

// ---------------------------------------------------------------------------
// The gate has to be wired into the tool, not merely defined next to it.
// These drive the registered unity_execute tool through a stub plugin API.
// Run with --test-force-exit: register() starts the session-cleanup interval.

const registeredTools = new Map();
plugin.register({
  logger: { info() {}, warn() {}, error() {}, debug() {} },
  registerHttpRoute() {},
  registerTool(definition) {
    registeredTools.set(definition.name, definition);
  },
  registerCli() {},
});
const execute = (args) => registeredTools.get("unity_execute").execute("test-call", args);

test("unity_execute refuses a project-changing call end to end", async () => {
  delete process.env.OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE;
  delete process.env.OPENCLAW_UNITY_ALLOW_DESTRUCTIVE;

  const result = await execute({
    tool: "asset.delete",
    parameters: { path: "Assets/Prefabs/Player.prefab" },
    confirm: true,
  });
  assert.equal(result.details.success, false);
  assert.equal(result.details.gate.reason, "operator-opt-in-missing");
  assert.match(result.details.error, /OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1/);
});

test("unity_execute passes a read-only call straight through", async () => {
  const result = await execute({ tool: "debug.hierarchy" });
  // The gate is not what stops it — there is simply no Editor attached here.
  assert.match(result.details.error, /No Unity session connected/);
  assert.equal(result.details.gate, undefined);
});

test("unity_execute previews a project-changing call under dryRun", async () => {
  const result = await execute({
    tool: "asset.delete",
    parameters: { path: "Assets/Prefabs/Player.prefab" },
    dryRun: true,
  });
  assert.equal(result.details.dryRun, true);
  assert.equal(result.details.executed, false);
  assert.equal(result.details.risk, "project-changing");
  assert.equal(result.details.requiresConfirmation, true);
  assert.equal(result.details.wouldRun, false);
});

test("unity_execute proceeds once the operator opted in and the call confirms", async () => {
  process.env.OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE = "1";
  try {
    const result = await execute({
      tool: "asset.delete",
      parameters: { path: "Assets/Prefabs/Player.prefab" },
      confirm: true,
    });
    // Past the gate: it now fails on the missing Editor, not on permission.
    assert.match(result.details.error, /No Unity session connected/);
    assert.equal(result.details.gate, undefined);
  } finally {
    delete process.env.OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE;
  }
});
