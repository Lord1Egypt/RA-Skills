#!/usr/bin/env node
/*
Trajectory Compiler (full runnable)
- Reads a trace log
- Builds a DAG
- Lifts variables into a schema
- Emits a Skill folder with SKILL.md + schema + plan + run script
*/

const fs = require("node:fs");
const path = require("node:path");

function usage() {
  console.log(`Usage:
  node scripts/trajectory-compiler.js --trace <file> [--name <skill-name>] [--out <dir>] [--description <text>] [--json]
`);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    const token = argv[i];
    if (token.startsWith("--")) {
      const key = token.slice(2);
      const value = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
      args[key] = value;
    } else {
      args._.push(token);
    }
  }
  return args;
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeFile(p, content) {
  ensureDir(path.dirname(p));
  fs.writeFileSync(p, content, "utf8");
}

function toSkillName(name) {
  return String(name).trim().toLowerCase().replace(/\s+/g, "-");
}

function normalizeTrace(raw) {
  if (!raw) throw new Error("Empty trace log");
  if (Array.isArray(raw)) return raw;
  if (Array.isArray(raw.steps)) return raw.steps;
  if (raw.trace && Array.isArray(raw.trace.steps)) return raw.trace.steps;
  if (Array.isArray(raw.events)) {
    return raw.events
      .filter((e) => e.type === "tool_call" || e.type === "tool" || e.type === "toolResult")
      .map((e, idx) => ({
        id: e.id || `step${idx + 1}`,
        tool: e.tool || e.toolName,
        input: e.input || e.args || e.request,
        output: e.output || e.result || e.response
      }));
  }
  throw new Error("Unrecognized trace format. Expected {steps: []} or {events: []} or an array.");
}

function inferSchemaForValue(value) {
  if (value === null) return { type: ["string", "null"] };
  if (Array.isArray(value)) return { type: "array", items: {} };
  const t = typeof value;
  if (t === "string") return { type: "string" };
  if (t === "number") return { type: "number" };
  if (t === "boolean") return { type: "boolean" };
  if (t === "object") return { type: "object" };
  return { type: "string" };
}

function sanitizeParamName(name) {
  return name.replace(/[^a-zA-Z0-9_\-]/g, "_");
}

function parseRefString(raw) {
  const trimmed = raw.trim();
  if (!trimmed) return null;
  // Accept: stepId.output.path OR stepId.path
  const parts = trimmed.split(".");
  if (parts.length === 0) return null;
  const stepId = parts.shift();
  let pathRest = parts.join(".");
  if (pathRest.startsWith("output.")) pathRest = pathRest.slice("output.".length);
  if (pathRest === "output") pathRest = "";
  return { stepId, path: pathRest, raw: trimmed };
}

function isPlainObject(obj) {
  return obj && typeof obj === "object" && !Array.isArray(obj);
}

function parseTemplateString(str, addParam) {
  const tokens = [];
  let lastIndex = 0;
  const re = /\{\{\s*([^}]+)\s*\}\}/g;
  let match;
  while ((match = re.exec(str))) {
    if (match.index > lastIndex) {
      tokens.push({ type: "text", value: str.slice(lastIndex, match.index) });
    }
    const expr = match[1].trim();
    if (expr.startsWith("param:")) {
      const name = sanitizeParamName(expr.slice("param:".length).trim());
      addParam(name, "string", "Template param");
      tokens.push({ type: "param", name });
    } else {
      const ref = parseRefString(expr);
      if (ref) tokens.push({ type: "ref", ref: `${ref.stepId}.${ref.path ? "output." + ref.path : "output"}` });
      else {
        const name = sanitizeParamName(expr);
        addParam(name, "string", "Template param");
        tokens.push({ type: "param", name });
      }
    }
    lastIndex = re.lastIndex;
  }
  if (lastIndex < str.length) {
    tokens.push({ type: "text", value: str.slice(lastIndex) });
  }
  return tokens;
}

function collectRefs(value, refs = []) {
  if (Array.isArray(value)) {
    value.forEach((item) => collectRefs(item, refs));
    return refs;
  }
  if (isPlainObject(value)) {
    if (value.__ref__) {
      refs.push(value.__ref__);
      return refs;
    }
    if (value.__template__ && Array.isArray(value.__template__)) {
      for (const token of value.__template__) {
        if (token.type === "ref") refs.push(token.ref);
      }
      return refs;
    }
    Object.values(value).forEach((v) => collectRefs(v, refs));
    return refs;
  }
  return refs;
}

function transformInput(value, context, params) {
  const { stepId, path } = context;

  function addParam(name, valueSample, description) {
    if (!params.has(name)) {
      const schema = inferSchemaForValue(valueSample);
      if (valueSample !== undefined) schema.default = valueSample;
      params.set(name, {
        name,
        schema,
        description: description || `Parameter from ${stepId}.${path.join(".") || "input"}`
      });
    }
    return name;
  }

  if (value === null || typeof value !== "object") {
    const paramName = sanitizeParamName(`param_${stepId}_${path.join("_") || "value"}`);
    const name = addParam(paramName, value, `From ${stepId}.${path.join(".") || "input"}`);
    return { __param__: name };
  }

  if (Array.isArray(value)) {
    const containsRefs = value.some((v) => isPlainObject(v) && (v.ref || v.$ref || v.from || v.param));
    if (!containsRefs) {
      const paramName = sanitizeParamName(`param_${stepId}_${path.join("_") || "array"}`);
      const name = addParam(paramName, value, `From ${stepId}.${path.join(".") || "input"}`);
      return { __param__: name };
    }
    return value.map((item, idx) =>
      transformInput(item, { stepId, path: [...path, String(idx)] }, params)
    );
  }

  // Handle explicit annotations
  if (value.const === true) {
    return value.value !== undefined ? value.value : null;
  }
  if (value.param) {
    const name = sanitizeParamName(value.param);
    addParam(name, value.value, value.description || `From ${stepId}.${path.join(".") || "input"}`);
    return { __param__: name };
  }
  if (value.ref || value.$ref) {
    const keys = Object.keys(value);
    const refKey = value.ref ? "ref" : "$ref";
    const isStandaloneRef = keys.length === 1 && keys[0] === refKey;
    if (isStandaloneRef) {
      const ref = parseRefString(value.ref || value.$ref);
      if (!ref) throw new Error(`Invalid ref: ${value.ref || value.$ref}`);
      return { __ref__: `${ref.stepId}.${ref.path ? "output." + ref.path : "output"}` };
    }
  }
  if (value.from && value.from.step) {
    const ref = { stepId: value.from.step, path: value.from.path || "" };
    return { __ref__: `${ref.stepId}.${ref.path ? "output." + ref.path : "output"}` };
  }

  // Template string
  if (typeof value === "string" && value.includes("{{") && value.includes("}}")) {
    const tokens = parseTemplateString(value, (name, _, desc) => addParam(name, "", desc));
    return { __template__: tokens };
  }

  // Plain object: decide whether to lift or recurse
  const hasNestedRefs = Object.values(value).some((v) =>
    (typeof v === "string" && v.includes("{{") && v.includes("}}")) ||
    (isPlainObject(v) && (v.ref || v.$ref || v.from || v.param))
  );

  if (!hasNestedRefs) {
    const paramName = sanitizeParamName(`param_${stepId}_${path.join("_") || "object"}`);
    const name = addParam(paramName, value, `From ${stepId}.${path.join(".") || "input"}`);
    return { __param__: name };
  }

  const out = {};
  for (const [key, val] of Object.entries(value)) {
    out[key] = transformInput(val, { stepId, path: [...path, key] }, params);
  }
  return out;
}

function buildDag(steps, planSteps) {
  const edges = [];
  const depMap = new Map();
  for (const step of planSteps) depMap.set(step.id, new Set());

  for (const step of planSteps) {
    const refs = collectRefs(step.input || {});
    for (const refStr of refs) {
      const ref = parseRefString(refStr);
      if (!ref) continue;
      if (!depMap.has(ref.stepId)) {
        throw new Error(`Unknown dependency step: ${ref.stepId}`);
      }
      depMap.get(step.id).add(ref.stepId);
      edges.push({ from: ref.stepId, to: step.id, via: refStr });
    }
  }

  const requiredOutput = new Set(edges.map((e) => e.from));

  return { edges, dependencies: depMap, requiredOutput };
}

function topoSort(steps, depMap) {
  const inDeg = new Map();
  for (const step of steps) inDeg.set(step.id, 0);
  for (const [id, deps] of depMap.entries()) {
    for (const dep of deps) {
      inDeg.set(id, (inDeg.get(id) || 0) + 1);
    }
  }

  const queue = steps.filter((s) => (inDeg.get(s.id) || 0) === 0).map((s) => s.id);
  const order = [];
  const depMapClone = new Map();
  for (const [k, v] of depMap.entries()) depMapClone.set(k, new Set(v));

  while (queue.length) {
    const id = queue.shift();
    order.push(id);
    for (const [node, deps] of depMapClone.entries()) {
      if (deps.has(id)) {
        deps.delete(id);
        inDeg.set(node, inDeg.get(node) - 1);
        if (inDeg.get(node) === 0) queue.push(node);
      }
    }
  }

  if (order.length !== steps.length) {
    throw new Error("Cycle detected in DAG");
  }
  return order;
}

function synthesizeSchema(params, descriptionOverride) {
  const schema = {
    type: "object",
    description: descriptionOverride || "Auto-generated skill schema",
    properties: {},
    required: []
  };
  for (const param of params.values()) {
    schema.properties[param.name] = {
      ...param.schema,
      description: param.description
    };
    schema.required.push(param.name);
  }
  return schema;
}

function synthesizeSkillMd(skillName, description) {
  return `---\nname: ${skillName}\ndescription: "${description}"\n---\n\n# ${skillName}\n\nAuto-generated from a trajectory trace.\n\n## Usage\nProvide parameters matching the generated schema in references/schema.json.\n`;
}

function synthesizeRunFlow(plan) {
  const lines = [];
  lines.push("# Skill Run Flow");
  lines.push("");
  lines.push("This file is auto-generated. It explains the execution order and dependencies.");
  lines.push("");
  for (const step of plan.steps) {
    const deps = step.dependencies && step.dependencies.length ? step.dependencies.join(", ") : "none";
    lines.push(`- **${step.id}** (${step.tool})`);
    lines.push(`  - depends on: ${deps}`);
  }
  lines.push("");
  return lines.join("\n");
}

function buildRunFlow(plan) {
  return plan.steps.map((step) => ({
    id: step.id,
    tool: step.tool,
    depends_on: step.dependencies || []
  }));
}

function formatRunFlow(runFlow) {
  const lines = ["Run flow (dependency order):"];
  for (const step of runFlow) {
    const deps = step.depends_on && step.depends_on.length ? step.depends_on.join(", ") : "none";
    lines.push(`- ${step.id} (${step.tool}) depends on: ${deps}`);
  }
  return lines.join("\n");
}

function synthesizeRunScript() {
  return `const fs = require("node:fs");\nconst path = require("node:path");\n\nconst plan = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "references", "plan.json"), "utf8"));\n\nfunction getPath(obj, pathStr) {\n  if (!pathStr) return obj;\n  return pathStr.split(".").reduce((acc, key) => (acc ? acc[key] : undefined), obj);\n}\n\nfunction resolveValue(value, params, results) {\n  if (Array.isArray(value)) return value.map((v) => resolveValue(v, params, results));\n  if (value && typeof value === "object") {\n    if (value.__param__) {\n      if (!(value.__param__ in params)) throw new Error(\`Missing param: \${value.__param__}\`);\n      return params[value.__param__];\n    }\n    if (value.__ref__) {\n      const parts = value.__ref__.split(".");\n      const stepId = parts.shift();\n      let pathStr = parts.join(".");\n      if (pathStr.startsWith("output.")) pathStr = pathStr.slice("output.".length);\n      if (pathStr === "output") pathStr = "";\n      if (!results[stepId]) throw new Error(\`Missing dependency output: \${stepId}\`);\n      return getPath(results[stepId].output, pathStr);\n    }\n    if (value.__template__) {\n      return value.__template__.map((token) => {\n        if (token.type === "text") return token.value;\n        if (token.type === "param") {\n          if (!(token.name in params)) throw new Error(\`Missing param: \${token.name}\`);\n          return params[token.name];\n        }\n        if (token.type === "ref") {\n          const parts = token.ref.split(".");\n          const stepId = parts.shift();\n          let pathStr = parts.join(".");\n          if (pathStr.startsWith("output.")) pathStr = pathStr.slice("output.".length);\n          if (pathStr === "output") pathStr = "";\n          if (!results[stepId]) throw new Error(\`Missing dependency output: \${stepId}\`);\n          return getPath(results[stepId].output, pathStr);\n        }\n        return "";\n      }).join("");\n    }\n    const out = {};\n    for (const [k, v] of Object.entries(value)) out[k] = resolveValue(v, params, results);\n    return out;\n  }\n  return value;\n}\n\nasync function executeStep(step, input, tools) {\n  const tool = tools[step.tool];\n  if (!tool) throw new Error(\`Tool not available: \${step.tool}\`);\n  return tool(input);\n}\n\nasync function run(params, tools) {\n  const results = {};\n  for (const step of plan.steps) {\n    const input = resolveValue(step.input || {}, params, results);\n    let output;\n    if (step.retry && step.retry.count > 0) {\n      let attempt = 0;\n      let lastErr;\n      while (attempt <= step.retry.count) {\n        try {\n          output = await executeStep(step, input, tools);\n          break;\n        } catch (err) {\n          lastErr = err;\n          attempt += 1;\n          if (step.retry.delayMs) await new Promise((r) => setTimeout(r, step.retry.delayMs));\n        }\n      }\n      if (output === undefined && lastErr) throw lastErr;\n    } else {\n      output = await executeStep(step, input, tools);\n    }\n\n    if (step.requiresOutput && (output === undefined || output === null)) {\n      throw new Error(\`Step \${step.id} produced empty output\`);\n    }\n    results[step.id] = { output };\n  }\n  return { status: "Success", results };\n}\n\nmodule.exports = run;\n`;
}

function compile(trace, options) {
  const steps = normalizeTrace(trace).map((step, idx) => ({
    id: String(step.id || `step${idx + 1}`),
    tool: step.tool || step.toolName || step.name,
    input: step.input || step.args || step.request || {},
    output: step.output || step.result || step.response
  }));

  for (const step of steps) {
    if (!step.tool) throw new Error(`Missing tool for step ${step.id}`);
  }

  const params = new Map();
  const planSteps = steps.map((step) => {
    const inputTemplate = transformInput(step.input, { stepId: step.id, path: [] }, params);
    return { id: step.id, tool: step.tool, input: inputTemplate };
  });

  const dag = buildDag(steps, planSteps);
  const order = topoSort(planSteps, dag.dependencies);
  const stepsById = new Map(planSteps.map((s) => [s.id, s]));
  const orderedSteps = order.map((id) => stepsById.get(id));

  for (const step of orderedSteps) {
    step.dependencies = Array.from(dag.dependencies.get(step.id) || []);
    step.requiresOutput = dag.requiredOutput.has(step.id);
  }

  const schema = synthesizeSchema(params, options.descriptionOverride);

  return {
    plan: {
      steps: orderedSteps,
      edges: dag.edges,
      inputs: Array.from(params.values()).map((p) => ({
        name: p.name,
        description: p.description
      }))
    },
    schema
  };
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.trace) {
    usage();
    process.exit(1);
  }

  const raw = readJson(args.trace);
  const skillName = toSkillName(args.name || raw.expected_skill_name || `compiled-skill-${Date.now()}`);
  const description = args.description || raw.description_override || "Compiled trajectory skill";

  const outRoot = args.out || process.env.OPENCLAW_SKILLS_DIR || path.join(process.env.HOME || "~", ".openclaw", "workspace", "skills");
  const skillDir = path.join(outRoot, skillName);

  const { plan, schema } = compile(raw, { descriptionOverride: description });
  const runFlow = buildRunFlow(plan);
  const runFlowText = formatRunFlow(runFlow);

  writeFile(path.join(skillDir, "SKILL.md"), synthesizeSkillMd(skillName, description));
  writeFile(path.join(skillDir, "references", "plan.json"), JSON.stringify(plan, null, 2));
  writeFile(path.join(skillDir, "references", "schema.json"), JSON.stringify(schema, null, 2));
  writeFile(path.join(skillDir, "references", "run-flow.md"), synthesizeRunFlow(plan));
  writeFile(path.join(skillDir, "scripts", "run.js"), synthesizeRunScript());

  const summary = {
    status: "Success",
    generated_skill_id: skillName,
    skill_schema_preview: schema,
    run_flow_path: path.join(skillDir, "references", "run-flow.md"),
    run_flow: runFlow
  };

  if (args.json) {
    console.log(JSON.stringify(summary, null, 2));
  } else {
    console.log(`Generated skill at: ${skillDir}`);
    console.log(`Skill ID: ${skillName}`);
    console.log(runFlowText);
  }
}

try {
  main();
} catch (err) {
  console.error(`Failed: ${err.message}`);
  process.exit(1);
}
