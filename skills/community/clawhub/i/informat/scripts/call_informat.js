#!/usr/bin/env node

/**
 * Informat Platform - Unified System Method Calling
 * Usage:
 *   call_informat.js <methodName> --file params.json
 *   call_informat.js <methodName> '{"key":"value"}'
 *   call_informat.js <methodName>
 *   call_informat.js <methodName> --appId <appId> --file params.json
 *   call_informat.js <methodName> --appId <appId> '{"key":"value"}'
 *   call_informat.js <methodName> --appId <appId>
 */

var https = require("https");
var http = require("http");
var fs = require("fs");
var nodePath = require("path");
var urlMod = require("url");
var os = require("os");
var resolveThreadId = require("./resolve_thread_id");

// ---- Optionally load configuration from .env file ----
function loadEnv() {
  var envPath = nodePath.join(__dirname, ".env");
  var config = {};
  try {
    var lines = fs.readFileSync(envPath, "utf-8").split("\n");
    for (var i = 0; i < lines.length; i++) {
      var trimmed = lines[i].trim();
      if (!trimmed || trimmed.charAt(0) === "#") continue;
      var idx = trimmed.indexOf("=");
      if (idx === -1) continue;
      config[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim();
    }
  } catch (e) {
    if (!e || e.code === "ENOENT") return config;
    console.error("Failed to read optional .env file: " + envPath + ", " + e.message);
  }
  return config;
}

// ---- HTTP POST (with 60s timeout) ----
function post(targetUrl, headers, body, callback) {
  var parsed = new urlMod.URL(targetUrl);
  var mod = parsed.protocol === "https:" ? https : http;
  var req = mod.request(parsed, {
    method: "POST",
    headers: Object.assign({}, headers, { "Content-Length": Buffer.byteLength(body) }),
    timeout: 60000,
  }, function (res) {
    var chunks = [];
    res.on("data", function (c) { chunks.push(c); });
    res.on("end", function () {
      var text = Buffer.concat(chunks).toString("utf-8");
      if (res.statusCode < 200 || res.statusCode >= 300) {
        callback(new Error("Request failed (" + res.statusCode + "): " + text));
      } else {
        callback(null, text);
      }
    });
  });
  req.on("timeout", function () { req.destroy(new Error("Request timed out after 60s")); });
  req.on("error", function (e) { callback(e); });
  req.write(body);
  req.end();
}

// ---- Transient-error retry: a 5xx response, a network error, or a timeout is retried with backoff ----
// 4xx and JSON-RPC application errors are NOT retried (they are deterministic). Addresses intermittent gateway
// failures such as HTTP 550 seen on a single build call.
function isTransientError(err) {
  var m = (err && err.message) || "";
  if (/Request failed \(5\d\d\)/.test(m)) return true;
  if (/timed out/i.test(m)) return true;
  var code = err && err.code;
  if (code && /^(ECONNRESET|ETIMEDOUT|ECONNREFUSED|EAI_AGAIN|EPIPE|ENETUNREACH|ESOCKETTIMEDOUT|ECONNABORTED)$/.test(code)) return true;
  return false;
}
function postWithRetry(targetUrl, headers, bodyStr, callback) {
  var maxAttempts = 4;
  var delays = [500, 1500, 3500];
  (function attempt(n) {
    post(targetUrl, headers, bodyStr, function (err, text) {
      if (err && isTransientError(err) && n < maxAttempts) {
        setTimeout(function () { attempt(n + 1); }, delays[n - 1] || 3500);
        return;
      }
      callback(err, text);
    });
  })(1);
}

// ---- Main Flow ----
var cliArgs = process.argv.slice(2);

if (cliArgs.length === 0 || cliArgs[0] === "-h" || cliArgs[0] === "--help") {
  console.error("Usage:");
  console.error("  call_informat.js <methodName> --file params.json");
  console.error("  call_informat.js <methodName> '{\"key\":\"value\"}'");
  console.error("  call_informat.js <methodName>");
  console.error("  call_informat.js <methodName> --appId <appId> --file params.json");
  console.error("  call_informat.js <methodName> --appId <appId> '{\"key\":\"value\"}'");
  console.error("  call_informat.js <methodName> --appId <appId>");
  console.error("\nNote:");
  console.error("  - Methods starting with _company automatically use the team agent interface");
  console.error("  - Common methods (e.g. _get_current_time, _javascript_eval) don't require --appId");
  console.error("  - Other methods require --appId and use the application agent interface");
  process.exit(2);
}

var methodName = cliArgs[0];
var restArgs = cliArgs.slice(1);

// Parse named arguments
var methodArgs = {};
var appId = null;
var cliThreadId = null;
var fileUsed = false;
var positionalArgs = [];

function requireNextArg(flag, index) {
  var next = restArgs[index + 1];
  if (!next || next.charAt(0) === "-") {
    console.error("Missing value after " + flag);
    process.exit(1);
  }
  return next;
}

for (var i = 0; i < restArgs.length; i++) {
  if (restArgs[i] === "--appId" || restArgs[i] === "--appid") {
    appId = requireNextArg("--appId", i);
    i++;
  } else if (restArgs[i] === "--threadId" || restArgs[i] === "--threadid") {
    cliThreadId = requireNextArg("--threadId", i);
    i++;
  } else if (restArgs[i] === "--file" || restArgs[i] === "-f") {
    var filePath = nodePath.resolve(requireNextArg("--file", i));
    i++;
    try {
      var rawParams = fs.readFileSync(filePath, "utf-8");
      // Empty content (e.g. --file /dev/stdin with no heredoc fed) is treated as no args ({})
      // to avoid a JSON.parse("") failure; methods that require args get a clear backend error.
      if (rawParams && rawParams.trim() !== "") {
        methodArgs = JSON.parse(rawParams);
      }
      fileUsed = true;
    } catch (e) {
      console.error("Failed to read/parse file: " + filePath + " - " + e.message);
      process.exit(1);
    }
  } else {
    positionalArgs.push(restArgs[i]);
  }
}

// If no params from --file, try parsing positional arg as JSON
if (!fileUsed && positionalArgs.length > 0) {
  try { methodArgs = JSON.parse(positionalArgs[0]); } catch (e) { console.error("Invalid JSON: " + e.message); process.exit(1); }
}

// Common methods that don't require --appId
var noAppIdMethods = [
  "_read_office_file", "_read_informat_script_sdk", "_read_informat_expression_doc",
  "_list_informat_markdown", "_read_informat_markdown", "_app_get_web_url", "_app_doc",
  "_web_content", "_javascript_eval", "_render_html", "_get_current_time",
  "_get_current_user", "_send_system_email"
];
function isNoAppIdMethod(name) {
  for (var j = 0; j < noAppIdMethods.length; j++) {
    if (name === noAppIdMethods[j]) return true;
  }
  return false;
}

// Check if appId is required
if (!methodName.startsWith("_company") && !methodName.startsWith("_wb_") && !isNoAppIdMethod(methodName) && !appId) {
  console.error("Missing --appId. Usage: call_informat.js <methodName> --appId <appId>");
  process.exit(1);
}

var env = loadEnv();
var informatAgentThreadId = resolveThreadId(cliThreadId, process.env, env);

// ---- Session-level ack directory (shared by all gates) ----
// Keyed by INFORMAT_AGENT_THREAD_ID (unique per conversation, stable across resume); falls back to cwd for standalone use.
var sessionTag = informatAgentThreadId.replace(/[^A-Za-z0-9_-]/g, "_");
var ackDir = process.env.INFORMAT_ACK_DIR
  || (sessionTag ? nodePath.join(os.tmpdir(), "informat_ack", sessionTag) : nodePath.join(process.cwd(), ".informat_ack"));

// ---- Progress files (plan/counter) anchored to the session ack directory, independent of cwd ----
// cwd is unreliable: the process often runs from a read-only skill directory, so files written there cannot be located.
function progressPaths(aid) {
  var dir = nodePath.join(ackDir, "informat_progress");
  return { dir: dir, plan: nodePath.join(dir, aid + ".plan.json"), counter: nodePath.join(dir, aid + ".counter.json") };
}
function readJsonSafe(p) { try { return JSON.parse(fs.readFileSync(p, "utf-8")); } catch (e) { return null; } }

// ---- _plan_set: local pseudo-command that writes the blueprint targets to the session-stable location ----
// Usage: call_informat.js _plan_set --appId <id> '{"targets":{"table":13,"automatic":2,"script":5,"api":2,"workflow":2,"dashboard":5}}'
if (methodName === "_plan_set") {
  if (!appId) { console.error("Missing --appId for _plan_set"); process.exit(1); }
  var planTargets = (methodArgs && methodArgs.targets) || {};
  var ppSet = progressPaths(appId);
  try {
    fs.mkdirSync(ppSet.dir, { recursive: true });
    fs.writeFileSync(ppSet.plan, JSON.stringify({ targets: planTargets }, null, 2));
  } catch (e) { console.error("Failed to write plan.json: " + e.message); process.exit(1); }
  console.log(JSON.stringify({ ok: true, plan: ppSet.plan, targets: planTargets }, null, 2));
  process.exit(0);
}

// ===== Combined gate: doc-read (domain design doc) + read-ack (parameter schema), requested together =====
// (1) Domain methods (in DOC_GATES) are gated once per domain (after the DOCKEY and the first method schema are read);
// (2) other write methods are gated once per method (relaxed: _ack needs only the required parameter names);
// (3) read-only / no-arg methods are not gated.
var DOC_GATES = [
  { key: "bpmn", doc: "informat.bpmn.md", names: ["_bpmn_create_module", "_bpmn_create_process_define", "_bpmn_update_start_setting", "_bpmn_create_or_update_node", "_bpmn_create_or_update_flow"] },
  { key: "automatic", doc: "informat.automatic.md", names: ["_automatic_save_define"] },
  { key: "dashboard", doc: "informat.dashboard.uipreset.md", prefixes: ["_save_dashboard_"] },
  { key: "table", doc: "informat.table.md", prefixes: ["_create_table", "_edit_table", "_table_save", "_table_create_", "_table_update_", "_subtable_create", "_subtable_update"] },
  { key: "api", doc: "informat.api.md", names: ["_api_create_define", "_api_update_define"] },
  { key: "script", doc: "informat.script.md", names: ["_save_informat_script"] },
  { key: "schedule", doc: "informat.schedule.md", names: ["_schedule_create_define", "_schedule_update_define"] },
  { key: "website", doc: "informat.website.md", names: ["_website_create_module", "_website_create_directory", "_website_save_resource"] },
  { key: "aiassistant", doc: "informat.aiassistant.md", names: ["_aiassistant_create", "_aiassistant_update"] },
  { key: "approle", doc: "informat.app.role.md", names: ["_app_create_role", "_app_update_role", "_app_permission_create", "_app_permission_update"] },
  { key: "themestyle", doc: "informat.app.themestyle.md", names: ["_app_set_themestyle", "_app_update_basic_info"] },
  { key: "listeners", doc: "informat.listeners.md", names: ["_app_listener_create", "_app_listener_update"] },
  { key: "codestudio", doc: "informat.codestudio.md", names: ["_codestudio_create_module", "_codestudio_write_file", "_codestudio_create_script", "_codestudio_create_api"] },
];
function resolveDocGate(name) {
  for (var gi = 0; gi < DOC_GATES.length; gi++) {
    var g = DOC_GATES[gi];
    if (g.names && g.names.indexOf(name) >= 0) return { key: g.key, doc: g.doc };
    if (g.prefixes) {
      for (var pj = 0; pj < g.prefixes.length; pj++) {
        if (name.indexOf(g.prefixes[pj]) === 0) return { key: g.key, doc: g.doc };
      }
    }
  }
  return null;
}
// Read-only methods (query/list/read/check) are not gated: fabricated arguments merely return nothing.
function isReadOnlyMethod(name) {
  return /^_(query|read|list|get|app_doc|app_get|app_check|company_app_list|thread_list|task_list|task_doc)/.test(name);
}

var schemaBase = methodName.replace(/^_+/, "");
var schemaPath = nodePath.join(__dirname, "..", "references", "system_" + schemaBase + ".json");
function loadSchema(p) {
  try {
    var node = JSON.parse(fs.readFileSync(p, "utf-8"));
    var params = (node.function && node.function.parameters) || node.parameters || {};
    return { properties: params.properties || {}, required: Array.isArray(params.required) ? params.required : [] };
  } catch (e) { return null; }
}
function normAck(s) {
  return String(s == null ? "" : s).split(",").map(function (x) { return x.trim().toLowerCase(); })
    .filter(function (x) { return x.length > 0; }).sort().join(",");
}
var schema = loadSchema(schemaPath);
var propNames = schema ? Object.keys(schema.properties) : [];
// Prefer the required parameter names as the _ack basis; fall back to all parameter names if none are required.
var ackBasis = (schema && schema.required && schema.required.length > 0) ? schema.required : propNames;
var expectAck = normAck(ackBasis.join(","));

var docGate = resolveDocGate(methodName);
var domainKey = docGate ? docGate.key : null;
var domainMarker = domainKey ? nodePath.join(ackDir, "__doc_" + domainKey) : null;
var domainReady = false;
if (domainMarker) { try { domainReady = fs.existsSync(domainMarker); } catch (e) {} }

// doc-ack is required only for a domain method when the domain is not ready, the doc has a DOCKEY, and it was not provided correctly.
var expectDocToken = null;
var needDoc = false;
if (docGate && !domainReady) {
  try {
    var dmk = fs.readFileSync(nodePath.join(__dirname, "..", "references", "doc", "markdown", docGate.doc), "utf-8").match(/DOCKEY:\s*([A-Za-z0-9_-]+)/);
    if (dmk) expectDocToken = dmk[1].toLowerCase();
  } catch (e) {}
  if (expectDocToken) {
    var pDocAck = methodArgs && methodArgs._doc_ack;
    needDoc = !(pDocAck != null && String(pDocAck).trim().toLowerCase() === expectDocToken);
  }
}

// read-ack: domain methods check domain readiness (covering the whole domain at once); other write methods check a per-method marker.
var needAck = false, perMethodMarker = null;
var gateThisMethod = schema && propNames.length > 0 && !isReadOnlyMethod(methodName);
if (gateThisMethod) {
  if (domainKey) {
    if (!domainReady) needAck = !(normAck(methodArgs && methodArgs._ack) === expectAck && expectAck !== "");
  } else {
    perMethodMarker = nodePath.join(ackDir, schemaBase);
    var acked = false; try { acked = fs.existsSync(perMethodMarker); } catch (e) {}
    if (!acked) needAck = !(normAck(methodArgs && methodArgs._ack) === expectAck && expectAck !== "");
  }
}

if (needDoc || needAck) {
  var gmsg = ["[First operation of this kind: please read the documentation and parameter definitions before calling]"];
  var gstep = 1;
  if (needDoc) gmsg.push(gstep++ + ") Use Read to review the full domain design document references/doc/markdown/" + docGate.doc + "; take the header line 'DOCKEY: <token>' as the _doc_ack argument.");
  if (needAck) gmsg.push(gstep++ + ") Use Read to review the parameter definition references/system_" + schemaBase + ".json; pass the REQUIRED parameter names (" + ackBasis.length + " total, comma-separated, case/order insensitive) as the _ack argument.");
  gmsg.push("Re-call this method with " + (needDoc && needAck ? "_doc_ack and _ack" : (needDoc ? "_doc_ack" : "_ack")) + " alongside the normal business arguments to proceed. Do not guess without reading the documentation.");
  if (domainKey) gmsg.push("(The '" + domainKey + "' domain is gated only once here; other methods in the same domain are not gated individually thereafter, relying instead on local parameter validation.)");
  console.error(gmsg.join("\n"));
  process.exit(3);
}

// Passed → write the marker (domain-level covers the whole domain; non-domain is per method).
if (domainKey) {
  if (!domainReady) { try { fs.mkdirSync(ackDir, { recursive: true }); fs.writeFileSync(domainMarker, expectDocToken || "1"); } catch (e) {} }
} else if (gateThisMethod && perMethodMarker) {
  try { fs.mkdirSync(ackDir, { recursive: true }); fs.writeFileSync(perMethodMarker, expectAck); } catch (e) {}
}
if (methodArgs) {
  if (Object.prototype.hasOwnProperty.call(methodArgs, "_doc_ack")) delete methodArgs._doc_ack;
  if (Object.prototype.hasOwnProperty.call(methodArgs, "_ack")) delete methodArgs._ack;
}

// ===== Local schema validation (required / enum / top-level type) — runs on every call =====
if (schema) {
  var errs = [];
  for (var ri = 0; ri < schema.required.length; ri++) {
    var rk = schema.required[ri];
    if (methodArgs[rk] === undefined || methodArgs[rk] === null || methodArgs[rk] === "") {
      errs.push("Missing required parameter: " + rk);
    }
  }
  for (var pk in schema.properties) {
    if (!Object.prototype.hasOwnProperty.call(schema.properties, pk)) continue;
    if (!(pk in methodArgs)) continue;
    var spec = schema.properties[pk] || {};
    var val = methodArgs[pk];
    if (Array.isArray(spec.enum) && spec.enum.length > 0 && spec.enum.indexOf(val) === -1) {
      errs.push("Parameter " + pk + " has an illegal value: " + JSON.stringify(val) + "; allowed: " + JSON.stringify(spec.enum));
    }
    if (spec.type && val !== undefined && val !== null) {
      var ok = true;
      switch (spec.type) {
        case "string": ok = typeof val === "string"; break;
        case "number": ok = typeof val === "number"; break;
        case "integer": ok = typeof val === "number" && Math.floor(val) === val; break;
        case "boolean": ok = typeof val === "boolean"; break;
        case "array": ok = Array.isArray(val); break;
        case "object": ok = typeof val === "object" && !Array.isArray(val); break;
        default: ok = true;
      }
      if (!ok) errs.push("Parameter " + pk + " should be of type " + spec.type + ", got: " + (Array.isArray(val) ? "array" : typeof val));
    }
  }
  if (errs.length > 0) {
    console.error(
      "[Parameter validation failed: " + methodName + "]\n- " + errs.join("\n- ") +
      "\nPlease correct according to references/system_" + schemaBase + ".json and retry."
    );
    process.exit(4);
  }
}
// ===== End of combined gate + validation =====

// ===== Blueprint finish gate + auto-counting of build calls =====
// During full-app orchestration, the targets are registered to informat_progress/<appId>.plan.json, e.g.
//   { "targets": { "table":13, "automatic":2, "script":5, "api":2, "workflow":2, "dashboard":5 } }
// Successful build calls are counted by distinct name into informat_progress/<appId>.counter.json.
// Workflows are the exception: an empty process define must NOT count. A workflow is tallied only once its
// processDefineId has received at least one node AND at least one flow (see recordWorkflowStructure), so a hollow
// shell created by stopping after _bpmn_create_process_define does not satisfy the finish gate.
// At the _app_check_setting self-check, any category below its target triggers exit 7 with the gaps listed.
// No plan.json (not a full app / not aligned) → no gate; single operations are unaffected. Counter files persist across rounds and sessions.
var COUNT_RULES = {
  "_create_table_module": "table",
  "_automatic_save_define": "automatic",
  "_save_informat_script": "script",
  "_api_create_define": "api",
  "_save_dashboard_number_card": "dashboard",
  "_save_dashboard_pivot_card": "dashboard",
  "_save_dashboard_prochart_card": "dashboard",
  "_save_dashboard_record_card": "dashboard",
  "_save_dashboard_table_card": "dashboard",
  "_app_listener_create": "listener",
  "_schedule_create_define": "schedule"
};
var CATEGORY_LABELS = { table: "Table", automatic: "Automation", script: "Script", api: "API", workflow: "Workflow", dashboard: "Dashboard card", listener: "Listener", schedule: "Scheduled task" };
function recordBuild(aid, category, name) {
  if (!aid || !category) return;
  var pp = progressPaths(aid);
  var c = readJsonSafe(pp.counter) || {};
  if (!Array.isArray(c[category])) c[category] = [];
  var key = String(name == null ? ("#" + (c[category].length + 1)) : name).trim();
  if (key && c[category].indexOf(key) === -1) c[category].push(key);
  try { fs.mkdirSync(pp.dir, { recursive: true }); fs.writeFileSync(pp.counter, JSON.stringify(c, null, 2)); } catch (e) {}
}
// A workflow is counted only when its processDefineId has both a node and a flow; an empty process define is ignored.
function recordWorkflowStructure(aid, pdId, kind) {
  if (!aid || !pdId) return;
  var pp = progressPaths(aid);
  var c = readJsonSafe(pp.counter) || {};
  if (!Array.isArray(c._wf_nodes)) c._wf_nodes = [];
  if (!Array.isArray(c._wf_flows)) c._wf_flows = [];
  if (!Array.isArray(c.workflow)) c.workflow = [];
  var bag = kind === "node" ? c._wf_nodes : c._wf_flows;
  if (bag.indexOf(pdId) === -1) bag.push(pdId);
  if (c._wf_nodes.indexOf(pdId) !== -1 && c._wf_flows.indexOf(pdId) !== -1 && c.workflow.indexOf(pdId) === -1) {
    c.workflow.push(pdId);
  }
  try { fs.mkdirSync(pp.dir, { recursive: true }); fs.writeFileSync(pp.counter, JSON.stringify(c, null, 2)); } catch (e) {}
}
// Persist each sequence flow's edge (source→target + whether it carries a condition) per processDefineId, keyed by flow id,
// so the build-artifact gate can reject an infinite loop formed purely by unconditional flows.
function recordWorkflowEdge(aid, pdId, flowId, s, t, hasCond) {
  if (!aid || !pdId || !s || !t) return;
  var pp = progressPaths(aid);
  var c = readJsonSafe(pp.counter) || {};
  if (!c._wf_edges || typeof c._wf_edges !== "object") c._wf_edges = {};
  if (!c._wf_edges[pdId] || typeof c._wf_edges[pdId] !== "object") c._wf_edges[pdId] = {};
  c._wf_edges[pdId][flowId || (s + ">" + t)] = { s: s, t: t, c: !!hasCond };
  try { fs.mkdirSync(pp.dir, { recursive: true }); fs.writeFileSync(pp.counter, JSON.stringify(c, null, 2)); } catch (e) {}
}
// Record whether the app has modeled any M:N (Relation) or 1:N (LookupList) field, for the finish gate's relation-coverage check.
function recordTableModeling(aid, hasRelation, hasLookup) {
  if (!aid || (!hasRelation && !hasLookup)) return;
  var pp = progressPaths(aid);
  var c = readJsonSafe(pp.counter) || {};
  if (hasRelation) c._has_relation = true;
  if (hasLookup) c._has_lookup = true;
  try { fs.mkdirSync(pp.dir, { recursive: true }); fs.writeFileSync(pp.counter, JSON.stringify(c, null, 2)); } catch (e) {}
}
// Track per-dashboard (scope) cumulative column fill (cards flow in a 24-column grid), deduped by card name so a re-save
// is not double-counted. Used by the dashboard validator to reject a card whose width overflows the current row.
function recordDashboardLayout(aid, scope, width, cardKey) {
  if (!aid || !scope) return;
  var w = parseInt(width, 10); if (!(w > 0)) return;
  var pp = progressPaths(aid);
  var c = readJsonSafe(pp.counter) || {};
  if (!c._dash_width || typeof c._dash_width !== "object") c._dash_width = {};
  if (!c._dash_cards || typeof c._dash_cards !== "object") c._dash_cards = {};
  if (!Array.isArray(c._dash_cards[scope])) c._dash_cards[scope] = [];
  var key = String(cardKey == null ? ("#" + (c._dash_cards[scope].length + 1)) : cardKey);
  if (c._dash_cards[scope].indexOf(key) !== -1) return; // already counted (re-save) → do not add width again
  c._dash_cards[scope].push(key);
  c._dash_width[scope] = (parseInt(c._dash_width[scope], 10) || 0) + w;
  try { fs.mkdirSync(pp.dir, { recursive: true }); fs.writeFileSync(pp.counter, JSON.stringify(c, null, 2)); } catch (e) {}
}
if (methodName === "_app_check_setting" && appId) {
  var ppGate = progressPaths(appId);
  var plan = readJsonSafe(ppGate.plan);
  if (plan && plan.targets) {
    var counter = readJsonSafe(ppGate.counter) || {};
    var gaps = [];
    for (var cat in plan.targets) {
      if (!Object.prototype.hasOwnProperty.call(plan.targets, cat)) continue;
      var target = parseInt(plan.targets[cat], 10) || 0;
      var built = Array.isArray(counter[cat]) ? counter[cat].length : 0;
      if (built < target) {
        gaps.push("  - " + (CATEGORY_LABELS[cat] || cat) + ": planned " + target + ", built " + built + ", missing " + (target - built));
      }
    }
    var tblTarget = parseInt(plan.targets.table, 10) || 0;
    if (tblTarget >= 2 && !counter._has_relation && !counter._has_lookup) {
      gaps.push("  - Relation modeling: " + tblTarget + " tables planned but no Relation (M:N) or LookupList (1:N) field exists across them — the model is entirely flat / N:1. Per the table doc, a master table should expose its detail records via a LookupList (1:N) and any many-to-many link via a Relation (M:N); do not leave every link as a single RelationRecord.");
    }
    if (gaps.length > 0) {
      console.error(
        "[Blueprint not yet complete: finishing is not permitted]\n" +
        "Per informat_progress/" + appId + ".plan.json, the following components are below target:\n" +
        gaps.join("\n") +
        "\n\nPlease continue creating the missing components (linked to the blueprint, not added as filler), then call _app_check_setting again.\n" +
        "(This gate prevents premature completion: built counts are tallied automatically by name and cannot be bypassed by a verbal \"done\". To genuinely drop an item, modify the plan.json targets and state the reason.)"
      );
      process.exit(7);
    }
  }
}
// ===== End of finish gate =====

// ===== Script SDK doc gate: _save_informat_script must read script/<module>.md for the informat.<module>.* it uses =====
// Scans the script body for informat.<module>.* usage (lowercase namespaces only, so expression helpers like
// informat.String / informat.Date are excluded). For each module whose script/<module>.md exists but has not been
// read this session, blocks with exit 5 and lists the docs to read. Acknowledged via _sdk_read (comma-separated
// module names), which writes a __scriptdoc_<module> marker so the same module is not gated again this session.
if (methodName === "_save_informat_script") {
  var scriptBody = (methodArgs && typeof methodArgs.content === "string") ? methodArgs.content : "";
  var usedModules = {};
  var reMod = /informat\.([a-z][A-Za-z0-9]*)\./g, mMod;
  while ((mMod = reMod.exec(scriptBody)) !== null) { usedModules[mMod[1].toLowerCase()] = true; }
  var sdkProvided = {};
  if (methodArgs && methodArgs._sdk_read != null) {
    String(methodArgs._sdk_read).split(",").forEach(function (t) { var v = t.trim().toLowerCase(); if (v) sdkProvided[v] = true; });
  }
  var sdkNeed = [], sdkPass = [];
  for (var um in usedModules) {
    if (!Object.prototype.hasOwnProperty.call(usedModules, um)) continue;
    var sdkDoc = nodePath.join(__dirname, "..", "references", "doc", "markdown", "script", um + ".md");
    var hasDoc = false; try { hasDoc = fs.existsSync(sdkDoc); } catch (e) {}
    if (!hasDoc) continue;
    var sdkMarker = nodePath.join(ackDir, "__scriptdoc_" + um);
    var sdkRead = false; try { sdkRead = fs.existsSync(sdkMarker); } catch (e) {}
    if (sdkRead) continue;
    if (sdkProvided[um]) sdkPass.push(um); else sdkNeed.push(um);
  }
  if (sdkNeed.length > 0) {
    sdkNeed.sort();
    console.error(
      "[Before saving this script: read the SDK reference for each informat.* module it uses]\n" +
      "The script calls the following platform SDK modules whose reference documents have not been read this session;\n" +
      "their exact method signatures (argument count, order, and position) must come from the documents, not from memory:\n" +
      sdkNeed.map(function (m) { return "  - references/doc/markdown/script/" + m + ".md   (informat." + m + ".*)"; }).join("\n") +
      "\n\nCommon signature errors this prevents: placing tableId inside the query object instead of as the first argument; " +
      "calling informat.table.update(tableId, recordId, data) with three arguments instead of informat.table.update(tableId, data) with the id inside data.\n" +
      "Use Read to review each file above, then re-call _save_informat_script with _sdk_read set to the comma-separated module names (e.g. _sdk_read=\"" + sdkNeed.join(",") + "\").\n" +
      "(Modules acknowledged here are not gated again this session.)"
    );
    process.exit(5);
  }
  for (var sp = 0; sp < sdkPass.length; sp++) {
    try { fs.mkdirSync(ackDir, { recursive: true }); fs.writeFileSync(nodePath.join(ackDir, "__scriptdoc_" + sdkPass[sp]), "1"); } catch (e) {}
  }
}
if (methodArgs && Object.prototype.hasOwnProperty.call(methodArgs, "_sdk_read")) delete methodArgs._sdk_read;

// ===== Expression doc gate: a write payload containing a platform expression ${...} requires reading informat.expression.md =====
// Platform expressions use Informat's DSL (UEL), not JavaScript. Excludes _save_informat_script and _codestudio_*
// (their ${...} are native JS template literals). Acknowledged via _expr_ack = the doc's DOCKEY; writes a __exprdoc
// marker so it is gated only once per session.
function exprGateApplies(name) {
  // Exclude methods whose payload is native JS/HTML (their ${...} are template literals, not platform expressions).
  if (name === "_save_informat_script" || name === "_plan_set" || name === "_javascript_eval" || name === "_render_html") return false;
  if (/^_codestudio_/.test(name)) return false;
  if (isReadOnlyMethod(name)) return false;
  return true;
}
if (exprGateApplies(methodName)) {
  var argStr = "";
  try { argStr = JSON.stringify(methodArgs || {}); } catch (e) { argStr = ""; }
  if (argStr.indexOf("${") !== -1) {
    var exprMarker = nodePath.join(ackDir, "__exprdoc");
    var exprReady = false; try { exprReady = fs.existsSync(exprMarker); } catch (e) {}
    if (!exprReady) {
      var exprToken = null;
      try {
        var exprMatch = fs.readFileSync(nodePath.join(__dirname, "..", "references", "doc", "markdown", "informat.expression.md"), "utf-8").match(/DOCKEY:\s*([A-Za-z0-9_-]+)/);
        if (exprMatch) exprToken = exprMatch[1].toLowerCase();
      } catch (e) {}
      if (exprToken) {
        var pExprAck = methodArgs && methodArgs._expr_ack;
        var exprOk = pExprAck != null && String(pExprAck).trim().toLowerCase() === exprToken;
        if (!exprOk) {
          console.error(
            "[Before this operation: read the expression reference, as the payload contains a platform expression ${...}]\n" +
            "The arguments contain one or more ${...} platform expressions, which use Informat's DSL (UEL), not JavaScript.\n" +
            "Their syntax rules and available functions are defined in references/doc/markdown/informat.expression.md, which has not been read this session.\n" +
            "Use Read to review that document, then re-call this method with _expr_ack set to its DOCKEY token (the value after 'DOCKEY:' in the file header).\n" +
            "(Required only once per session; subsequent expression-bearing calls are not gated again.)"
          );
          process.exit(6);
        }
        try { fs.mkdirSync(ackDir, { recursive: true }); fs.writeFileSync(exprMarker, exprToken); } catch (e) {}
      }
    }
  }
}
if (methodArgs && Object.prototype.hasOwnProperty.call(methodArgs, "_expr_ack")) delete methodArgs._expr_ack;

// ===== Build-artifact gate: deterministic anti-decay checks at the moment of building =====
// Design docs are read early (during orchestration), but their rules are easily forgotten by the time the
// corresponding objects are actually built dozens of turns later — the artifact then ignores the doc entirely.
// The reliable remedy is memory-independent: when a build method runs, validate the payload against a small set of
// deterministic, zero-false-positive rules and, on violation, re-surface a compact checklist (no re-reading required).
// Each validator returns an array of violation strings; an empty array means pass. Rules are intentionally minimal so
// the gate fires only on genuine errors, never on legitimate variation.
var DASHBOARD_CARD_METHODS = {
  "_save_dashboard_number_card": "number", "_save_dashboard_prochart_card": "prochart",
  "_save_dashboard_record_card": "record", "_save_dashboard_pivot_card": "pivot", "_save_dashboard_table_card": "table"
};
function isEmptyVal(v) {
  if (v === undefined || v === null || v === "") return true;
  if (Array.isArray(v) && v.length === 0) return true;
  return false;
}
// Detect a cycle formed purely by unconditional sequence flows (an infinite loop). Conditional flows are excluded —
// a back/return edge that carries a conditionExpression is legitimate; only an all-unconditional loop is always wrong.
function unconditionalEdgesHaveCycle(edgeMap, addS, addT, addKey) {
  var adj = {};
  function add(s, t) { if (!adj[s]) adj[s] = []; adj[s].push(t); }
  for (var k in edgeMap) {
    if (!Object.prototype.hasOwnProperty.call(edgeMap, k)) continue;
    if (addKey && k === addKey) continue; // the persisted version of the current flow is superseded below
    var e = edgeMap[k]; if (!e || e.c) continue;
    add(e.s, e.t);
  }
  if (addS && addT) add(addS, addT); // current edge is unconditional (caller only calls in that case)
  var state = {};
  function dfs(n) {
    state[n] = 1;
    var outs = adj[n] || [];
    for (var i = 0; i < outs.length; i++) {
      var m = outs[i];
      if (state[m] === 1) return true;
      if (state[m] === undefined && dfs(m)) return true;
    }
    state[n] = 2; return false;
  }
  for (var s in adj) { if (state[s] === undefined && dfs(s)) return true; }
  return false;
}
// Drive the automation step check from the actual schema: load AutomaticFunction's per-step funcSetting definitions once.
var _autoDefsCache = null;
function getAutomaticFuncDefs() {
  if (_autoDefsCache) return _autoDefsCache;
  try {
    var raw = JSON.parse(fs.readFileSync(nodePath.join(__dirname, "..", "references", "system_automatic_save_define.json"), "utf-8"));
    var defs = raw && raw.function && raw.function.parameters && raw.function.parameters.definitions;
    _autoDefsCache = (defs && defs.AutomaticFunction && defs.AutomaticFunction.properties) || {};
  } catch (e) { _autoDefsCache = {}; }
  return _autoDefsCache;
}
function funcSettingKeyOf(type) {
  var t = String(type == null ? "" : type).replace(/\./g, "");
  if (!t) return "";
  return t.charAt(0).toLowerCase() + t.slice(1) + "FuncSetting";
}
// Supplement the schema's `required` for interaction-output steps whose content field is the whole point of the step
// but is NOT listed in the schema required array (so an empty toast/dialog/notification slips through). A bare string =
// that field must be non-empty; { any: [...] } = at least one of the listed fields must be non-empty. These steps render
// nothing on an empty content field, so this is a correctness check (no false positives on a meaningfully-filled step).
var AUTO_SEMANTIC_REQUIRED = {
  outputToastFuncSetting: ["toastValueVar"],
  outputConfirmFuncSetting: [{ any: ["confirmTitleVar", "confirmDialogTitleVar"] }],
  outputNotificationFuncSetting: [{ any: ["messageVar", "message"] }]
};
var ARTIFACT_VALIDATORS = {
  dashboard: function (name, a) {
    if (!DASHBOARD_CARD_METHODS[name]) return [];
    var v = [];
    if (a.enableCardStyle !== true) v.push("enableCardStyle must be true (uipreset §2.2); otherwise the preset cardStyle does not render and the card shows the bare default style.");
    if (a.subTitle != null && String(a.subTitle).trim() !== "" && String(a.subTitle).trim() === String(a.name == null ? "" : a.name).trim())
      v.push("subTitle duplicates name (uipreset §0.9); leave subTitle empty rather than repeating the card name.");
    if (DASHBOARD_CARD_METHODS[name] === "number") {
      var ns = a.numberSetting || {};
      if (ns.xPosition !== "center" || ns.yPosition !== "center")
        v.push("numberSetting.xPosition and numberSetting.yPosition must both be \"center\" (uipreset §0.10 / §2.3); a left/top-aligned number collides with the card title.");
    }
    // A chart with no data source / no series renders blank (the empty "项目状态分布" card you saw): proChartSetting.dataset
    // must be a non-empty array whose entries each bind a real source (tableId or expression), and series must be non-empty.
    if (DASHBOARD_CARD_METHODS[name] === "prochart") {
      var pcs = a.proChartSetting || {};
      var dsList = pcs.dataset;
      if (!Array.isArray(dsList) || dsList.length === 0) {
        v.push("proChartSetting.dataset is empty — the chart has no data source and renders blank. Add at least one dataset bound to a real table (tableId) with its aggregation/groupBy, then reference it in series.");
      } else {
        for (var di = 0; di < dsList.length; di++) {
          var dse = dsList[di] || {};
          if (isEmptyVal(dse.tableId) && isEmptyVal(dse.expression)) {
            v.push("proChartSetting.dataset[" + di + "] (\"" + (dse.name || dse.id || "") + "\") has neither a tableId nor an expression — pick the real source table for this data source (the blank '新增数据源' you saw).");
          }
        }
      }
      if (!Array.isArray(pcs.series) || pcs.series.length === 0) {
        v.push("proChartSetting.series is empty — the chart has no series to draw. Add at least one series (bar/line/pie/…) bound to the dataset.");
      }
    }
    // Sort field format: every orderByList entry (wherever nested) must be an object {field, type:asc|desc}, not a
    // packed string like "count#desc". A string item / a field containing '#' / a missing or invalid type is rejected.
    var badSort = false;
    (function scan(o) {
      if (!o || typeof o !== "object") return;
      if (Array.isArray(o)) { for (var i = 0; i < o.length; i++) scan(o[i]); return; }
      for (var k in o) {
        if (!Object.prototype.hasOwnProperty.call(o, k)) continue;
        if (k === "orderByList" && Array.isArray(o[k])) {
          for (var j = 0; j < o[k].length; j++) {
            var it = o[k][j];
            if (it === null || typeof it !== "object" || Array.isArray(it) ||
                isEmptyVal(it.field) || String(it.field).indexOf("#") !== -1 ||
                (it.type !== "asc" && it.type !== "desc")) { badSort = true; }
          }
        }
        scan(o[k]);
      }
    })(a);
    if (badSort) v.push("orderByList sort entries must each be an object {\"field\":<real field ID>,\"type\":\"asc\"|\"desc\"}; a packed string such as \"count#desc\", a field containing '#', or a missing/invalid type is rejected (dashboard sort spec).");
    // Grid placement: cards flow in a 24-column grid; a card whose width does not fit the current row's remaining space
    // wraps and leaves a gap (mis-placed layout). Only checked on a card's first placement (re-saves are skipped).
    if (a.scope && appId) {
      var dcnt = readJsonSafe(progressPaths(appId).counter) || {};
      var counted = (dcnt._dash_cards && dcnt._dash_cards[a.scope]) || [];
      var thisKey = String(a.name == null ? "" : a.name);
      var w = parseInt(a.width, 10) || 0;
      if (counted.indexOf(thisKey) === -1) {
        if (w > 24) {
          v.push("card width " + w + " exceeds the 24-column grid (max 24).");
        } else {
          var rem = ((parseInt(dcnt._dash_width && dcnt._dash_width[a.scope], 10) || 0)) % 24;
          if (rem !== 0 && rem + w > 24) {
            v.push("card width " + w + " does not fit the current dashboard row (scope " + a.scope + "): " + rem + "/24 columns are already filled, only " + (24 - rem) + " remain, so the 24-column flow wraps and leaves a gap (the mis-placement you see). Set this card's width to " + (24 - rem) + " to complete the row, or first make the previous row sum to 24 (uipreset §0.5). Build cards in visual order, since a dashboard places them by flow order + width.");
          }
        }
      }
    }
    return v;
  },
  automatic: function (name, a) {
    if (name !== "_automatic_save_define") return [];
    var v = [];
    var steps = a.funcSettingList;
    if (!Array.isArray(steps) || steps.length === 0) {
      v.push("funcSettingList is empty: an automation must contain at least one real step, not an empty/placeholder trigger.");
      return v;
    }
    var defs = getAutomaticFuncDefs();
    (function walk(list) {
      if (!Array.isArray(list)) return;
      for (var i = 0; i < list.length; i++) {
        var st = list[i] || {};
        var type = st.type;
        if (type === "If") {
          var kids = Array.isArray(st.children) ? st.children : [];
          var hasT = false, hasF = false;
          for (var c = 0; c < kids.length; c++) { if (kids[c] && kids[c].type === "If.true") hasT = true; if (kids[c] && kids[c].type === "If.false") hasF = true; }
          if (!hasT || !hasF) v.push("If step \"" + (st.name || st.id || type) + "\" must contain both an If.true and an If.false child branch (each with real steps).");
        }
        var key = funcSettingKeyOf(type);
        var def = key && defs[key];
        var req = (def && Array.isArray(def.required)) ? def.required : [];
        if (req.length > 0) {
          var setting = st[key];
          if (!setting || typeof setting !== "object") {
            v.push("Step \"" + (st.name || st.id || type) + "\" (" + type + ") is missing its " + key + " carrying the required fields: " + req.join(", ") + ".");
          } else {
            for (var r = 0; r < req.length; r++) {
              if (isEmptyVal(setting[req[r]])) v.push("Step \"" + (st.name || st.id || type) + "\" (" + type + "): " + key + "." + req[r] + " is empty — fill the real referenced value (query the target table / workflow module / script ID first), not a placeholder. Build automation only AFTER its dependencies exist.");
            }
          }
        }
        var semReq = key && AUTO_SEMANTIC_REQUIRED[key];
        if (semReq) {
          var setting2 = st[key];
          for (var sq = 0; sq < semReq.length; sq++) {
            var rule = semReq[sq];
            if (rule && typeof rule === "object" && Array.isArray(rule.any)) {
              var anyOk = false;
              for (var ai2 = 0; ai2 < rule.any.length; ai2++) { if (setting2 && !isEmptyVal(setting2[rule.any[ai2]])) { anyOk = true; break; } }
              if (!anyOk) v.push("Step \"" + (st.name || st.id || type) + "\" (" + type + "): one of " + rule.any.join(" / ") + " must carry the display text — this interaction step shows nothing when its content is empty (the blank toast/dialog you saw). Fill the message it should display.");
            } else if (!setting2 || isEmptyVal(setting2[rule])) {
              v.push("Step \"" + (st.name || st.id || type) + "\" (" + type + "): " + key + "." + rule + " is empty — this interaction step shows nothing when its content is empty (the blank toast/dialog you saw). Fill the message it should display.");
            }
          }
        }
        if (Array.isArray(st.children)) walk(st.children);
      }
    })(steps);
    return v;
  },
  bpmn: function (name, a) {
    var v = [];
    if (name === "_bpmn_create_or_update_node") {
      var n = a.node || {};
      if (n.type === "userTask") {
        if (isEmptyVal(n.assignee)) v.push("UserTask node \"" + (n.name || n.id) + "\": assignee is empty — every approval node needs an approver expression (e.g. ${Array.first(User.superiorUsers(initiator))}); for countersign/or-sign set it to ${elementVariable}.");
        var fset = n.taskSetting && n.taskSetting.formSetting;
        if (!fset || isEmptyVal(fset.tableId)) v.push("UserTask node \"" + (n.name || n.id) + "\": taskSetting.formSetting.tableId is empty — bind it to the start-form (main business) table.");
        if (!fset || !Array.isArray(fset.toolBarButtonList) || fset.toolBarButtonList.length === 0) v.push("UserTask node \"" + (n.name || n.id) + "\": formSetting.toolBarButtonList is empty — an approval node needs at least one action button (an approve and a reject button).");
      }
      return v;
    }
    if (name === "_bpmn_create_or_update_flow") {
      var f = a.flow || {};
      if (appId && a.processDefineId && f.sourceRef && f.targetRef) {
        var hasCond = !isEmptyVal(f.conditionExpression);
        if (!hasCond) {
          var cnt = readJsonSafe(progressPaths(appId).counter) || {};
          var emap = (cnt._wf_edges && cnt._wf_edges[a.processDefineId]) || {};
          if (unconditionalEdgesHaveCycle(emap, f.sourceRef, f.targetRef, f.id || (f.sourceRef + ">" + f.targetRef))) {
            v.push("Flow \"" + (f.name || f.id) + "\" (" + f.sourceRef + "→" + f.targetRef + ") closes a loop using only unconditional flows — an infinite cycle, which is not allowed. A back/return edge must carry a conditionExpression (${...} returning boolean), or model the return via a node button (action=TaskMoveToActivity) instead of a sequence flow.");
          }
        }
      }
      return v;
    }
    return v;
  },
  listeners: function (name, a) {
    var v = [];
    if (Array.isArray(a.eventList)) {
      for (var i = 0; i < a.eventList.length; i++) {
        if (a.eventList[i] !== null && typeof a.eventList[i] === "object") { v.push("eventList elements must be event-ID strings (e.g. \"record.update.after\"), not objects; table filtering goes in tableEventSetting.tableList (see listeners doc §5)."); break; }
      }
    }
    if (a.tableId != null) v.push("Top-level tableId is not a listener field; filter tables via tableEventSetting.tableList (array of table IDs) — see listeners doc §5.1.");
    if (a.invokeType === "automatic" && !(Array.isArray(a.automaticList) && a.automaticList.length > 0)) v.push("invokeType=automatic requires a non-empty automaticList; otherwise the listener has no execution body.");
    if (a.invokeType === "script" && !(a.scriptId && a.scriptFunc)) v.push("invokeType=script requires both scriptId and scriptFunc.");
    return v;
  },
  table: function (name, a) {
    if (name.indexOf("_create_table") !== 0 || !Array.isArray(a.fields)) return [];
    var v = [];
    for (var i = 0; i < a.fields.length; i++) {
      var f = a.fields[i] || {};
      if (f.id === "id" || f.id === "seq") { v.push("Field id \"" + f.id + "\" collides with a system-reserved field; name business keys xxxCode/xxxId instead (never bare id/seq)."); }
      var rs = f.relationSetting, rr = f.relationRecordSetting, ll = f.lookupListSetting;
      if (rs && !rs.tableId) v.push("Field \"" + (f.name || f.id) + "\": relationSetting.tableId is empty — a relation field must point to a real target table.");
      if (rr && !rr.tableId) v.push("Field \"" + (f.name || f.id) + "\": relationRecordSetting.tableId is empty — a related-record field must point to a real target table.");
      if (ll && !ll.tableId) v.push("Field \"" + (f.name || f.id) + "\": lookupListSetting.tableId is empty — a lookup field must point to a real source table.");
    }
    return v;
  },
  schedule: function (name, a) {
    var v = [];
    if (a.invokeType === "automatic" && !a.automaticId) v.push("invokeType=automatic requires automaticId (the schedule has no executor otherwise).");
    if (a.invokeType === "script" && !(a.scriptId && a.scriptFunc)) v.push("invokeType=script requires both scriptId and scriptFunc.");
    if (a.type === "cron" && !a.cron) v.push("type=cron requires a cron expression.");
    return v;
  }
};
// One concise checklist per domain, surfaced once per session on the first build of that domain (covers rules that
// cannot be machine-checked, e.g. theme consistency or chart-type choice). Throttled by a __rules_<domain> marker.
var DOMAIN_HINTS = {
  dashboard: "[Dashboard reminder] One §1 theme palette across all cards; pick a §3 layout template and make each row's width sum to 24; Number cards centered with the KPI gradient cardStyle; choose the chart per the §4 decision tree; sort via orderByList objects {field,type:asc|desc} (never a \"field#type\" string); no bare ECharts defaults (keep labels / gradient / rounded corners / shadow).",
  listeners: "[Listener reminder] eventList = event-ID strings from the doc §4 table; filter tables via tableEventSetting.tableList (array); set invokeType and its executor (automaticList, or scriptId+scriptFunc).",
  table: "[Table modeling reminder] Give each table a display field and enough business fields to be useful; prefer specific field types over generic text; model relations by semantics — RelationRecord (N:1), Relation (M:N), LookupList (1:N with a filter) — do not make every link a RelationRecord; relation/lookup fields need a real target tableId and a display columnList; never name a business key id/seq.",
  bpmn: "[Workflow reminder] A real process = StartEvent (built-in) + ≥2 UserTasks + EndEvent + all flows; every UserTask needs an assignee + formSetting (fields + approve/reject buttons) on the start-form table; branch via multiple conditional flows from one node plus one default flow; a back/return edge MUST carry a conditionExpression (no unconditional loops) or be a TaskMoveToActivity button; set node x/y; expressions follow informat.expression.md.",
  automatic: "[Automation reminder] Build automation AFTER its dependencies (tables / workflows / scripts) exist, and query their real IDs before writing each step; never leave a step reference empty (OutputBpmnProcess→bpmnModuleId+bpmnProcessDefineId+bpmnProcessStartFormTableId, OutputRecordCreate→recordCreateTableId, CallScript→scriptId+func, SetReturnValue→valueVar, If→expression+If.true/If.false children); expression fields use the platform DSL (informat.expression.md), not JavaScript.",
  api: "[API reminder] Bind scriptId+scriptFunc and set invokeType; choose method/view deliberately and keep the path meaningful.",
  schedule: "[Schedule reminder] Bind the executor (automaticId, or scriptId+scriptFunc); for cron type provide a valid cron expression.",
  script: "[Script reminder] Verify each informat.<module>.* call against script/<module>.md (arg count/order/position); tableId is always the first separate argument, never inside the query object.",
  website: "[Website reminder] Create the module, then directories and resources; keep navigation and resource references consistent.",
  aiassistant: "[AI assistant reminder] Give the assistant a clear role/instructions and bind the capabilities (skills/tools) it is meant to use.",
  approle: "[Role reminder] Define roles, then attach concrete permissions; do not leave a role without any permission scope.",
  themestyle: "[Theme reminder] Apply a coherent theme; keep colors and basic info consistent with the app's domain."
};
function domainOf(name) { var g = resolveDocGate(name); return g ? g.key : null; }
var artifactDomain = domainOf(methodName);
if (artifactDomain && ARTIFACT_VALIDATORS[artifactDomain] && methodArgs) {
  var artViolations = ARTIFACT_VALIDATORS[artifactDomain](methodName, methodArgs) || [];
  if (artViolations.length > 0) {
    var docName = (resolveDocGate(methodName) || {}).doc || "the domain design document";
    console.error(
      "[Build artifact rejected: it violates the " + artifactDomain + " design rules]\n" +
      "- " + artViolations.join("\n- ") +
      "\n\nFix the listed items and re-call. Full rules: references/doc/markdown/" + docName +
      ". (Deterministic check; fires only on an actual violation, no re-reading of the full document required.)"
    );
    process.exit(10);
  }
}
// ===== End of build-artifact gate =====

var host = (process.env.INFORMAT_HOST || env.INFORMAT_HOST || "").trim();
if (!host) { console.error("Missing INFORMAT_HOST"); process.exit(1); }
var agentToken = (process.env.INFORMAT_AGENT_TOKEN || env.INFORMAT_AGENT_TOKEN || "").trim();
if (!agentToken) { console.error("Missing INFORMAT_AGENT_TOKEN"); process.exit(1); }
if (host.charAt(host.length - 1) !== "/") host += "/";

// Build API path
var apiPath;
if (methodName.startsWith("_company_")) {
  apiPath = "web0/aiagent/company_agent";
} else if (methodName.startsWith("_wb_")) {
  apiPath = "web0/aiagent/wb_agent";
} else if (appId) {
  apiPath = "web0/aiagent/app_agent/" + appId;
} else {
  apiPath = "web0/aiagent/common_agent";
}

var url = host + apiPath;
var body = JSON.stringify({
  jsonrpc: "2.0", id: 1,
  params: {
    name: methodName,
    arguments: methodArgs,
    threadId: informatAgentThreadId || null,
  },
});

// ===== Serial lock: serializes build/designer write calls to avoid concurrent read-modify-write on the app module tree =====
// Each backend write is "load the whole module tree → add itself → save back", so parallel writes overwrite each other
// (a table is created but missing from the tree → publish reports refNotFound). A per-appId file lock forces queuing;
// it is released on response and on process exit. If the lock cannot be acquired, the call proceeds rather than being dropped.
function sleepMs(ms) {
  try { Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms); }
  catch (e) { var t0 = Date.now(); while (Date.now() - t0 < ms) {} }
}
function isAppMutating(name) {
  if (!appId) return false;
  if (/^_(query|read|list|get|app_check_setting|app_get|app_doc|company_app_list|thread_list|task_list|task_doc)/.test(name)) return false;
  return /(create|save|edit|update|delete|add|remove|set|move|sort|publish|bpmn|automatic|subtable|relation|listener|website|schedule|codestudio|table|dashboard|api_|role|themestyle)/i.test(name);
}
var buildLockPath = null;
function acquireBuildLock() {
  var lp = nodePath.join(ackDir, "__build_lock_" + (appId || "global"));
  try { fs.mkdirSync(ackDir, { recursive: true }); } catch (e) {}
  var start = Date.now();
  while (true) {
    try {
      var fd = fs.openSync(lp, "wx");
      try { fs.writeSync(fd, String(process.pid) + ":" + Date.now()); } catch (e) {}
      fs.closeSync(fd);
      buildLockPath = lp;
      return;
    } catch (e) {
      if (e.code !== "EEXIST") return;
      try {
        var st = fs.statSync(lp);
        if (Date.now() - st.mtimeMs > 90000) { try { fs.unlinkSync(lp); } catch (e2) {} continue; }
      } catch (e3) { continue; }
      if (Date.now() - start > 180000) return;
      sleepMs(120);
    }
  }
}
function releaseBuildLock() {
  if (buildLockPath) { try { fs.unlinkSync(buildLockPath); } catch (e) {} buildLockPath = null; }
}
process.on("exit", releaseBuildLock);
if (isAppMutating(methodName)) acquireBuildLock();
// ===== End of serial lock =====

postWithRetry(url, {
  "Content-Type": "application/json",
  "X-INFORMAT-AGENT-TOKEN": agentToken,
}, body, function (err, text) {
  releaseBuildLock();
  if (err) { console.error(err.message); process.exit(1); }
  var data;
  try { data = JSON.parse(text); } catch (e) { console.log(text); return; }
  if (data.error) {
    console.error("Error (" + data.error.code + "): " + data.error.message);
    process.exit(1);
  }
  // Successful build call → auto-count (used by the blueprint finish gate)
  var countCat = COUNT_RULES[methodName];
  if (countCat && appId) { recordBuild(appId, countCat, methodArgs && methodArgs.name); }
  if (appId && (methodName === "_bpmn_create_or_update_node" || methodName === "_bpmn_create_or_update_flow")) {
    recordWorkflowStructure(appId, methodArgs && methodArgs.processDefineId, methodName === "_bpmn_create_or_update_node" ? "node" : "flow");
  }
  if (appId && methodName === "_bpmn_create_or_update_flow" && methodArgs && methodArgs.flow) {
    var _ff = methodArgs.flow;
    recordWorkflowEdge(appId, methodArgs.processDefineId, _ff.id, _ff.sourceRef, _ff.targetRef, !(_ff.conditionExpression == null || String(_ff.conditionExpression).trim() === ""));
  }
  if (appId && (methodName === "_create_table_module" || methodName === "_edit_table_field" || /^_table_save/.test(methodName))) {
    var _blob = ""; try { _blob = JSON.stringify(methodArgs || {}); } catch (e) { _blob = ""; }
    recordTableModeling(appId, /"type"\s*:\s*"Relation"/.test(_blob), /"type"\s*:\s*"LookupList"/.test(_blob));
  }
  if (appId && DASHBOARD_CARD_METHODS[methodName] && methodArgs && methodArgs.scope) {
    recordDashboardLayout(appId, methodArgs.scope, methodArgs.width, methodArgs.name);
  }
  var contents = (data.result && data.result.content) || [];
  for (var i = 0; i < contents.length; i++) {
    var item = contents[i];
    if (item.type === "text") {
      try { console.log(JSON.stringify(JSON.parse(item.text), null, 2)); } catch (_) { console.log(item.text); }
    } else {
      console.log(JSON.stringify(item, null, 2));
    }
  }
  // Soft reminder: on the first successful build of a domain this session, append its concise checklist once
  // (covers rules that cannot be machine-checked, e.g. theme consistency / chart-type choice). Throttled by a marker.
  var hintDomain = domainOf(methodName);
  if (hintDomain && DOMAIN_HINTS[hintDomain]) {
    var hintMarker = nodePath.join(ackDir, "__rules_" + hintDomain);
    var hintSeen = false; try { hintSeen = fs.existsSync(hintMarker); } catch (e) {}
    if (!hintSeen) {
      console.log("\n" + DOMAIN_HINTS[hintDomain]);
      try { fs.mkdirSync(ackDir, { recursive: true }); fs.writeFileSync(hintMarker, "1"); } catch (e) {}
    }
  }
  // ===== Publish health gate: a non-empty issue list from _app_check_setting → non-zero exit, preventing a falsely-reported finish =====
  if (methodName === "_app_check_setting" && appId) {
    var issues = [];
    for (var ii = 0; ii < contents.length; ii++) {
      var c2 = contents[ii];
      if (c2 && c2.type === "text") {
        var parsed = null;
        try { parsed = JSON.parse(c2.text); } catch (e) {}
        if (Array.isArray(parsed)) issues = issues.concat(parsed);
        else if (parsed && Array.isArray(parsed.itemList)) issues = issues.concat(parsed.itemList);
      }
    }
    if (issues.length > 0) {
      var lines = issues.slice(0, 50).map(function (x) {
        return "  - " + (x && x.scopeName ? ("[" + x.scopeName + "] ") : "") + (x && x.message != null ? x.message : JSON.stringify(x));
      });
      console.error(
        "\n[Publish health check failed: completion may not be reported yet]\n" +
        "_app_check_setting returned " + issues.length + " configuration issue(s) (e.g. a table is created but not attached to the app module tree / key conflict / missing reference):\n" +
        lines.join("\n") +
        "\n\nThese issues cause publishing to fail or the module to be invisible in the app. Each must be fixed (recreate the missing module and ensure it is attached to the module tree, rename conflicts), then call _app_check_setting again until it returns an empty list, before reporting completion to the user. Do not finish while unresolved issues remain, and do not falsely report \"build complete\"."
      );
      process.exit(9);
    }
  }
});
