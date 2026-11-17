import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import crypto from "node:crypto";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { createIntegrityGuard } from "../templates/native-memory-plugin/integrity.mjs";
import { registerCacheRecall, isPrivateWebchat, selectPrimaryCandidates, buildPrimaryContext, PLUGIN_ID } from "../templates/native-memory-plugin/adapter.mjs";
import { cleanExpansionSource, expandRecallQuery, recallQueryTerms } from "../templates/native-memory-plugin/query.mjs";

const digest = value => crypto.createHash("sha256").update(value).digest("hex");
const context = () => ({ messageProvider: "webchat", trigger: "user", sessionKey: "agent:main:main", agentId: "main", toolAuthority: { assertActive() {}, allows() { return true; } } });
const candidate = (change = {}) => ({ path: "MEMORY.md", startLine: 7, endLine: 7, source: "memory", triggers: "中文资料", snippet: "Synthetic preference evidence.", provenance: { originClass: "owner" }, ...change });

function harness(entries = [candidate()], options = {}) {
  const entry = path.resolve("audited-runtime/dist/extensions/active-memory/index.js");
  const config = { runtimeEntry: entry, agents: ["main"], maxEntries: 3, maxChars: 1800, ...options.config };
  const raw = { sentinel: { retained: true }, plugins: { enabled: true, entries: {
    "active-memory": { enabled: false, config: { untouched: true } },
    [PLUGIN_ID]: { enabled: true, config },
  } } };
  const hooks = new Map(), warnings = [], requests = [], observations = [];
  let reads = 0, checks = 0, lists = 0, valid = true;
  const api = {
    id: PLUGIN_ID, config: raw, pluginConfig: config,
    logger: { warn: value => warnings.push(value), info: value => observations.push(value) },
    on: (name, handler, hookOptions) => hooks.set(name, { handler, options: hookOptions }),
    runtime: { config: { current() { reads++; return raw; } } },
  };
  registerCacheRecall(api, {
    createGuard: () => ({ check() { checks++; if (!valid) throw new Error("private-path-not-logged"); } }),
    getManager: async params => {
      requests.push(params);
      if (options.getManagerDelayMs) await new Promise(resolve => setTimeout(resolve, options.getManagerDelayMs));
      return { manager: { listTriggerCandidates: async params => {
        lists++; assert.deepEqual(params, { limit: 512, activeProjectKeys: [] });
        return options.list ? await options.list() : entries;
      } } };
    },
  });
  return { raw, hooks, warnings, observations, requests, reads: () => reads, checks: () => checks, lists: () => lists, invalidate: () => { valid = false; } };
}

test("registration mounts one authority-scoped hook without loading a memory manager", () => {
  const h = harness();
  assert.deepEqual([...h.hooks.keys()], ["before_prompt_build"]);
  assert.deepEqual(h.hooks.get("before_prompt_build").options, { requiresToolAuthority: true, timeoutMs: 25000 });
  assert.equal(h.requests.length, 0);
  assert.equal(h.raw.plugins.entries["active-memory"].enabled, false);
});

test("diagnostics default off creates no observer or observation logs even after a hit", async () => {
  const h = harness();
  await h.hooks.get("before_prompt_build").handler({ prompt: "中文资料" }, context());
  assert.equal(h.hooks.has("llm_input"), false);
  assert.deepEqual(h.observations, []);
});

test("opt-in diagnostics separately count selection and declared model-input fields without leaking content", async () => {
  const h = harness([candidate()], { config: { diagnostics: true } });
  assert.deepEqual([...h.hooks.keys()], ["before_prompt_build", "llm_input"]);
  const result = await h.hooks.get("before_prompt_build").handler({ prompt: "中文资料" }, context());
  assert.deepEqual(h.observations, ["[hui-yi-native-memory] selected markerBlockCount=1 referenceCount=1"]);
  const ctx = { ...context(), toolAuthority: undefined, runId: "PRIVATE-RUN", sessionId: "PRIVATE-SESSION" };
  const event = Object.freeze({ prompt: "PRIVATE-QUERY", systemPrompt: result.prependContext,
    runId: "PRIVATE-RUN", sessionId: "PRIVATE-SESSION", historyMessages: ["PRIVATE-HISTORY"], tools: ["PRIVATE-TOOL"] });
  assert.equal(h.hooks.get("llm_input").handler(event, ctx), undefined);
  assert.equal(h.observations[1], "[hui-yi-native-memory] llm-input-observed markerBlockCount=1 referenceCount=1");
  h.hooks.get("llm_input").handler({ prompt: result.prependContext, systemPrompt: result.prependContext }, ctx);
  assert.equal(h.observations[2], "[hui-yi-native-memory] llm-input-observed markerBlockCount=2 referenceCount=2");
  assert.ok(h.observations.every(line => !/PRIVATE|MEMORY\.md|Synthetic|中文资料/.test(line)));
  assert.equal(h.requests.length, 1);
});

test("diagnostic observer ignores nonmatches, unknown fields, external scopes and runtime disable", () => {
  const h = harness([], { config: { diagnostics: true } });
  const handler = h.hooks.get("llm_input").handler, ctx = { ...context(), toolAuthority: undefined };
  const marker = "<hui_yi_primary_memory>PRIVATE (Source: MEMORY.md#L7-L7)</hui_yi_primary_memory>";
  handler({ prompt: "PRIVATE-QUERY", historyMessages: [marker], unknownField: marker }, ctx);
  handler({ prompt: "<hui_yi_primary_memory>PRIVATE unclosed" }, ctx);
  handler({ prompt: marker }, { ...ctx, messageProvider: "feishu" });
  handler({ prompt: marker }, { ...ctx, agentId: "other" });
  h.raw.plugins.entries[PLUGIN_ID].config.diagnostics = false;
  handler({ prompt: marker }, ctx);
  assert.deepEqual(h.observations, []);
  assert.deepEqual(h.warnings, []);
  assert.equal(h.requests.length, 0);
});

test("external, shared, background and missing-authority events never read config or cache", async () => {
  const h = harness(), reads = h.reads(), checks = h.checks();
  for (const change of [
    { messageProvider: "feishu" }, { messageProvider: undefined },
    { sessionKey: "agent:main:feishu:group:example" },
    { sessionKey: "agent:main:webchat:channel:example" },
    { sessionKey: "agent:main:subagent:example" },
    { trigger: "heartbeat" }, { toolAuthority: undefined },
  ]) assert.equal(await h.hooks.get("before_prompt_build").handler({ prompt: "中文资料" }, { ...context(), ...change }), undefined);
  assert.equal(h.requests.length, 0); assert.equal(h.reads(), reads); assert.equal(h.checks(), checks);
  assert.equal(isPrivateWebchat({ ...context(), sessionKey: "agent:main:explicit:example" }), true);
});

test("current tool policy, revoked authority and mismatched agent prevent cache access", async () => {
  const h = harness();
  for (const ctx of [
    { ...context(), toolAuthority: { assertActive() {}, allows() { return false; } } },
    { ...context(), toolAuthority: { assertActive() { throw new Error("revoked"); }, allows() { return true; } } },
    { ...context(), agentId: "other" },
    { ...context(), agentId: "other", sessionKey: "agent:other:main" },
  ]) assert.equal(await h.hooks.get("before_prompt_build").handler({ prompt: "中文资料" }, ctx), undefined);
  assert.equal(h.requests.length, 0);
});

test("Chinese natural sentence recalls only primary cache and preserves host config and event", async () => {
  const h = harness(), snapshot = structuredClone(h.raw);
  const event = Object.freeze({ prompt: "请按我的中文资料整理习惯处理这份材料", messages: Object.freeze([]) });
  const result = await h.hooks.get("before_prompt_build").handler(event, context());
  assert.ok(result.prependContext.includes("<hui_yi_primary_memory>"));
  assert.ok(result.prependContext.includes("MEMORY.md#L7-L7"));
  assert.equal(event.currentUserMessage, undefined);
  assert.equal(h.requests[0].cfg, h.raw);
  assert.equal(h.requests[0].purpose, "default");
  assert.equal(h.requests[0].agentId, "main");
  assert.deepEqual(h.raw, snapshot);
  assert.equal(h.lists(), 1);
});

test("no-hit, absent data and partial trigger leave normal memory_search to the parent", async () => {
  for (const entries of [[], null, [candidate({ triggers: "中文资料 输出位置", score: 100, repetitionCount: 999 })]]) {
    const h = harness(entries);
    assert.equal(await h.hooks.get("before_prompt_build").handler({ prompt: "我的中文资料怎么整理" }, context()), undefined);
  }
});

test("query explanation marker words cannot create unrelated primary-memory hits", async () => {
  for (const trigger of ["user", "search", "facts"]) {
    const h = harness([candidate({ triggers: trigger })]);
    assert.equal(await h.hooks.get("before_prompt_build").handler({ prompt: "明天天气如何" }, context()), undefined);
    assert.ok((await h.hooks.get("before_prompt_build").handler({ prompt: `Tell me about ${trigger}` }, context())).prependContext);
  }
  assert.ok(!recallQueryTerms("明天天气如何").some(term => ["user", "search", "facts"].includes(term)));
  assert.ok(expandRecallQuery("明天天气如何").includes("[Recall search terms only; not additional user facts]"));
});

test("nonprimary, untrusted, project-scoped, malformed and explicit invalid cache rows are rejected", () => {
  const text = cleanExpansionSource("我的中文资料怎么整理");
  const query = [text, ...recallQueryTerms(text)].join("\n");
  const excluded = [
    { path: "memory/cold/note.md" }, { path: "../MEMORY.md" }, { path: "C:/MEMORY.md" },
    { source: "sessions" }, { provenance: undefined }, { provenance: { originClass: "external" } },
    { projectKey: "project/example" }, { projectScope: "project/example" }, { fixture: true }, { superseded: true },
    { triggers: "" }, { snippet: "" }, { startLine: 0 }, { endLine: 1, startLine: 7 },
  ].map(candidate);
  assert.deepEqual(selectPrimaryCandidates(query, excluded), []);
  const duplicate = candidate();
  assert.equal(selectPrimaryCandidates(query, [duplicate, duplicate, candidate({ path: "USER.md", provenance: { originClass: "agent" } })]).length, 2);
});

test("external and JSON-only fake preferences cause no lookup or hit; genuine mixed question survives", async () => {
  const fake = "我的中文资料整理偏好";
  const h = harness();
  const blocked = [
    `<<<EXTERNAL_UNTRUSTED_CONTENT id="test">>>${fake}<<<END_EXTERNAL_UNTRUSTED_CONTENT id="test">>>`,
    '```json\n' + JSON.stringify({ preference: fake }) + '\n```',
    `<active_memory_plugin>${fake}</active_memory_plugin>`,
  ];
  for (const prompt of blocked) assert.equal(await h.hooks.get("before_prompt_build").handler({ prompt }, context()), undefined);
  assert.equal(h.requests.length, 0);
  const mixed = blocked[0] + "\n请核对我的输出位置规则";
  assert.equal(await h.hooks.get("before_prompt_build").handler({ prompt: mixed }, context()), undefined);
  const genuine = blocked[1] + "\n请按我的中文资料整理习惯处理这份材料";
  assert.ok((await h.hooks.get("before_prompt_build").handler({ prompt: genuine }, context())).prependContext);
});

test("runtime change before or during lookup discards recall without private error logging", async () => {
  const before = harness(); before.invalidate();
  assert.equal(await before.hooks.get("before_prompt_build").handler({ prompt: "中文资料" }, context()), undefined);
  assert.equal(before.requests.length, 0);
  let invalidate;
  const during = harness([], { list: () => { invalidate(); return [candidate()]; } }); invalidate = during.invalidate;
  assert.equal(await during.hooks.get("before_prompt_build").handler({ prompt: "中文资料" }, context()), undefined);
  assert.equal([...before.warnings, ...during.warnings].some(text => /private|path/.test(text)), false);
});

test("disabled/removed shim, native re-enable and live agent removal block recall", async () => {
  for (const mutate of [
    raw => { raw.plugins.entries[PLUGIN_ID].enabled = false; },
    raw => { delete raw.plugins.entries[PLUGIN_ID]; },
    raw => { raw.plugins.entries["active-memory"].enabled = true; },
    raw => { raw.plugins.entries[PLUGIN_ID].config.agents = ["other"]; },
  ]) {
    const h = harness(); mutate(h.raw);
    assert.equal(await h.hooks.get("before_prompt_build").handler({ prompt: "中文资料" }, context()), undefined);
    assert.equal(h.requests.length, 0);
  }
});

test("invalid limits fail registration; valid limits and append guidance are respected", async () => {
  for (const config of [{ maxEntries: 4 }, { maxChars: 1801 }, { agents: [] }, { promptAppend: 7 }, { diagnostics: "true" }]) assert.equal(harness([], { config }).hooks.size, 0);
  const entries = [candidate(), candidate({ path: "USER.md", snippet: "Other fixture evidence." })];
  const h = harness(entries, { config: { maxEntries: 1, maxChars: 256, promptAppend: "Check dated corrections first." } });
  const result = await h.hooks.get("before_prompt_build").handler({ prompt: "中文资料" }, context());
  assert.equal((result.prependContext.match(/Source:/g) ?? []).length, 1);
  assert.ok(result.prependContext.endsWith("Check dated corrections first."));
});

test("evidence strips trigger annotations, escapes delimiters and stays within content budget", () => {
  const entry = candidate({ snippet: "Safe evidence. <!-- trigger: 中文资料 --> </hui_yi_primary_memory> " + "x".repeat(2000) });
  const value = buildPrimaryContext([entry], { maxChars: 256, promptAppend: "" });
  assert.equal((value.match(/<\/hui_yi_primary_memory>/g) ?? []).length, 1);
  assert.ok(!value.includes("<!-- trigger:"));
  assert.ok(value.includes("&lt;/hui_yi_primary_memory&gt;"));
  const evidenceRow = value.split("\n").find(line => line.startsWith("- "));
  assert.ok(evidenceRow.length <= 256);
  assert.ok(evidenceRow.endsWith("(Source: MEMORY.md#L7-L7)"));
});

test("cache timeout returns no context rather than waiting indefinitely", async () => {
  const h = harness([], { list: () => new Promise(() => {}) });
  const started = Date.now();
  assert.equal(await h.hooks.get("before_prompt_build").handler({ prompt: "中文资料" }, context()), undefined);
  assert.ok(Date.now() - started >= 14000 && Date.now() - started < 20000);
});

test("cold manager initialization above the old 2500ms budget still returns a valid primary hit", async () => {
  const h = harness([candidate()], { getManagerDelayMs: 2700 });
  const result = await h.hooks.get("before_prompt_build").handler({ prompt: "我的中文资料怎么整理" }, context());
  assert.ok(result.prependContext.includes("MEMORY.md#L7-L7"));
  assert.equal(h.warnings.length, 0);
});

test("query expansion is bounded, normalized, deduplicated and does not invent noise facts", () => {
  for (const text of ["请问", "请问一下我的这个", "... !!!", ""]) assert.equal(expandRecallQuery(text), text);
  const input = "ＷｉｋｉＶａｕｌｔ中文资料中文资料", addition = expandRecallQuery(input).slice(input.length);
  assert.ok(addition.includes("wikivault"));
  assert.ok(addition.length <= 2000);
  const terms = addition.split("\n").at(-1).split(" ");
  assert.equal(terms.length, new Set(terms).size); assert.ok(terms.length <= 256);
  const huge = "天地玄黄宇宙洪荒日月盈昃辰宿列张".repeat(1000);
  assert.ok(expandRecallQuery(huge).length - huge.length <= 2000);
});

test("expansion cleaning matches the audited native cleaner without raw fallback", t => {
  const file = path.join(process.env.LOCALAPPDATA ?? "", "OpenClaw/npm/node_modules/openclaw/dist/query-BoM0vDJB.mjs");
  if (!fs.existsSync(file)) return t.skip("audited cleaner unavailable");
  const source = fs.readFileSync(file, "utf8"), start = source.indexOf("function stripExternalUntrustedBlocks("), end = source.indexOf("function clampSearchQuery(");
  assert.ok(start >= 0 && end > start);
  const nativeClean = new Function(source.slice(start, end) + "; return text => normalizeSearchQueryText(stripActiveMemoryXmlBlocks(stripJsonFences(stripExternalUntrustedBlocks(text))));")();
  const fake = "虚构的个人偏好中文资料";
  const fixtures = [
    `<<<EXTERNAL_UNTRUSTED_CONTENT id="x">>>${fake}<<<END_EXTERNAL_UNTRUSTED_CONTENT id="x">>>`,
    '```json\n' + JSON.stringify({ preference: fake }) + '\n```',
    '```javascript\n' + fake + '\n```', `<active_memory_plugin>${fake}</active_memory_plugin>`,
    `Context:\nConversation info: ${fake}\nSender: ${fake}\nUntrusted context: ${fake}\nSource: External\n---\nUntrusted Discord message body\n⚠️ Agent couldn't generate a response\nPlease try again.`,
  ];
  for (const fixture of fixtures) {
    assert.equal(cleanExpansionSource(fixture), nativeClean(fixture));
    assert.equal(cleanExpansionSource(fixture), ""); assert.equal(expandRecallQuery(fixture), fixture);
    const mixed = fixture + "\n请按我的输出位置偏好保存文件";
    assert.equal(cleanExpansionSource(mixed), nativeClean(mixed));
    const addition = expandRecallQuery(mixed).slice(mixed.length);
    assert.ok(addition.includes("输出位置")); assert.ok(!addition.includes("中文资料"));
  }
  const longBlock = `<<<EXTERNAL_UNTRUSTED_CONTENT>>>${fake.repeat(1000)}<<<END_EXTERNAL_UNTRUSTED_CONTENT>>>`;
  assert.equal(expandRecallQuery(longBlock), longBlock);
});

test("integrity guard rejects upgrades, changed files, hardlinks, junctions and removed shim", () => {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), "huiyi-native-guard-"));
  const entry = path.join(base, "dist/extensions/active-memory/index.js"), packageFile = path.join(base, "package.json"), self = path.join(base, "shim.mjs");
  try {
    fs.mkdirSync(path.dirname(entry), { recursive: true }); fs.writeFileSync(entry, "audited-runtime");
    fs.writeFileSync(packageFile, JSON.stringify({ version: "2026.9.5" })); fs.writeFileSync(self, "shim");
    const options = { hashes: [digest("audited-runtime")] }, guard = createIntegrityGuard(entry, [self], options); guard.check();
    fs.writeFileSync(packageFile, JSON.stringify({ version: "2026.9.6" })); assert.throws(() => guard.check());
    fs.writeFileSync(packageFile, JSON.stringify({ version: "2026.9.5" }));
    fs.writeFileSync(entry, "changed-runtime"); assert.throws(() => guard.check()); fs.writeFileSync(entry, "audited-runtime");
    const hardlink = path.join(base, "linked.js"); fs.linkSync(entry, hardlink); assert.throws(() => guard.check()); fs.unlinkSync(hardlink);
    const linked = path.join(base, "linked-runtime"); fs.symlinkSync(path.dirname(entry), linked, process.platform === "win32" ? "junction" : "dir");
    assert.throws(() => createIntegrityGuard(entry, [path.join(linked, "index.js")], options).check()); fs.unlinkSync(linked);
    fs.unlinkSync(self); assert.throws(() => guard.check());
  } finally {
    const resolved = path.resolve(base), parent = path.resolve(os.tmpdir());
    assert.ok(resolved.startsWith(parent + path.sep) && path.basename(resolved).startsWith("huiyi-native-guard-"));
    fs.rmSync(resolved, { recursive: true, force: true });
  }
});

test("real PluginInstance registers one or two final public-SDK hooks according to diagnostics", async t => {
  const runtimeRoot = path.join(process.env.LOCALAPPDATA ?? "", "OpenClaw/npm/node_modules/openclaw");
  const loaderFile = path.join(runtimeRoot, "dist/plugin-setup-module-uAITKMY8.mjs");
  if (!fs.existsSync(loaderFile)) return t.skip("audited loader unavailable");
  const source = fileURLToPath(new URL("../templates/native-memory-plugin/index.mjs", import.meta.url));
  const entry = path.join(runtimeRoot, "dist/extensions/active-memory/index.js");
  const { a: bind, n: PluginInstance } = createRequire(loaderFile)(loaderFile);
  for (const diagnostics of [false, true]) {
    const config = { runtimeEntry: entry, agents: ["main"], maxEntries: 3, maxChars: 1800, diagnostics };
    const raw = { plugins: { enabled: true, entries: { "active-memory": { enabled: false }, [PLUGIN_ID]: { enabled: true, config } } } };
    const instance = new PluginInstance(PLUGIN_ID), hooks = [], warnings = [], started = Date.now();
    try {
    bind({ instance, origin: "config", source, rootDir: path.dirname(source) });
    const module = instance.loadModule(source);
    module.default.register({ id: PLUGIN_ID, config: raw, pluginConfig: config,
      logger: { warn: message => warnings.push(message) }, runtime: { config: { current: () => raw } },
      on: (name, _handler, options) => hooks.push({ name, options }),
    });
    assert.deepEqual(warnings, []);
    assert.deepEqual(hooks.map(hook => hook.name), diagnostics ? ["before_prompt_build", "llm_input"] : ["before_prompt_build"]);
    assert.equal(hooks[0].options.requiresToolAuthority, true);
    assert.equal(raw.plugins.entries["active-memory"].enabled, false);
    assert.ok(Date.now() - started < 20000);
    } finally { await instance.dispose(); }
  }
});
