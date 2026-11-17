#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const DEFAULT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const ROUTING_DOCUMENTS = Object.freeze([
  "README.md",
  "README.en.md",
  "SKILL.md",
  "AGENTS.md",
  "agents/openai.yaml",
  "workflows/one-click-stable.md",
  "workflows/fast-cut.md",
  "workflows/pro-enhance.md",
  "workflows/resume.md",
  "workflows/official-skill-map.md",
]);
const REQUIRED_ARTIFACTS = Object.freeze([
  ...ROUTING_DOCUMENTS,
  "profiles/balanced-stable.json",
  "profiles/tight-short.json",
  "profiles/trust-longform.json",
  "profiles/screen-demo.json",
  "schemas/runtime/run-manifest.schema.json",
  "schemas/runtime/decision-log.schema.json",
  "schemas/runtime/checkpoint.schema.json",
  "schemas/runtime/handoff-report.schema.json",
  "templates/runtime/project-brief.example.json",
  "templates/runtime/run-manifest.example.json",
  "templates/runtime/decision-log.example.json",
  "templates/runtime/handoff-report.md",
  "src/orchestration/orchestrator.mjs",
  "src/cli/koubo.mjs",
  "scripts/doctor.mjs",
  "scripts/validate-runtime-fixtures.mjs",
  "scripts/smoke-one-click.mjs",
  "scripts/validate-live-canary-claim.mjs",
]);
const OFFICIAL_SKILLS = Object.freeze(JSON.parse(fs.readFileSync(new URL("../reports/official-source-current.json", import.meta.url), "utf8")).hostedSkills);
const STARTER_PROMPTS = Object.freeze([
  /稳剪当前口播/u,
  /继续上次(?:剪辑|的马甲稳剪任务)/u,
  /(?:只做口误清理和字幕|清理口误.{0,20}基础字幕)/u,
  /专业增强/u,
]);

function usage(message) {
  process.stderr.write("Usage: node scripts/validate-docs-routing.mjs [--root <repository-root>] [--json]\n");
  if (message) process.stderr.write(`${message}\n`);
  process.exit(2);
}

function parseArguments(argv) {
  let root = DEFAULT_ROOT;
  let json = false;
  let rootSeen = false;
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (option === "--json") {
      if (json) usage("duplicate option: --json");
      json = true;
      continue;
    }
    if (option === "--root") {
      if (rootSeen) usage("duplicate option: --root");
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) usage("--root requires a value");
      root = path.resolve(value);
      rootSeen = true;
      index += 1;
      continue;
    }
    usage("unknown option");
  }
  return {root, json};
}

function inspectFile(root, relativePath) {
  const absolute = path.resolve(root, relativePath);
  const relative = path.relative(root, absolute);
  if (!relative || relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    return {ok: false, code: "outside-root"};
  }
  try {
    const stat = fs.lstatSync(absolute);
    if (!stat.isFile() || stat.isSymbolicLink()) return {ok: false, code: "unsafe"};
    return {ok: true, text: fs.readFileSync(absolute, "utf8")};
  } catch {
    return {ok: false, code: "missing"};
  }
}

function localTargets(markdown) {
  const targets = [];
  const patterns = [
    /!?\[[^\]]*\]\(([^)]+)\)/gu,
    /<(?:img|a)\b[^>]+(?:src|href)=["']([^"']+)["'][^>]*>/giu,
  ];
  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(markdown))) {
      let target = match[1].trim();
      if (target.startsWith("<") && target.endsWith(">")) target = target.slice(1, -1);
      target = target.split(/\s+["']/u, 1)[0];
      if (/^(?:https?:|mailto:|data:|#)/iu.test(target)) continue;
      const withoutFragment = target.split("#", 1)[0].split("?", 1)[0];
      if (withoutFragment) targets.push(withoutFragment);
    }
  }
  return targets;
}

function addFinding(findings, code, file, detail = null) {
  findings.push({code, file, ...(detail ? {detail} : {})});
}

function requireTerms(findings, file, text, terms, code) {
  for (const term of terms) {
    if (!text.includes(term)) addFinding(findings, code, file, term);
  }
}

function audit(root) {
  const findings = [];
  const documents = new Map();
  for (const file of REQUIRED_ARTIFACTS) {
    const inspected = inspectFile(root, file);
    if (!inspected.ok) addFinding(findings, "DOC_ROUTE_ARTIFACT_UNAVAILABLE", file, inspected.code);
    if (ROUTING_DOCUMENTS.includes(file) && inspected.ok) documents.set(file, inspected.text);
  }

  for (const [file, text] of documents) {
    if (!file.endsWith(".md")) continue;
    for (const target of localTargets(text)) {
      let decoded;
      try {
        decoded = decodeURIComponent(target);
      } catch {
        addFinding(findings, "DOC_ROUTE_LINK_ENCODING_INVALID", file, target);
        continue;
      }
      const resolved = path.resolve(root, path.dirname(file), decoded);
      const relative = path.relative(root, resolved);
      if (!relative || relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
        addFinding(findings, "DOC_ROUTE_LINK_OUTSIDE_ROOT", file, target);
        continue;
      }
      try {
        const stat = fs.lstatSync(resolved);
        if (stat.isSymbolicLink()) addFinding(findings, "DOC_ROUTE_LINK_SYMLINK", file, target);
      } catch {
        addFinding(findings, "DOC_ROUTE_LINK_MISSING", file, target);
      }
    }
  }

  const readme = documents.get("README.md") ?? "";
  requireTerms(findings, "README.md", readme, ["用马甲稳剪", "run", "status", "resume", "report"], "DOC_ROUTE_QUICKSTART_INCOMPLETE");
  if (!/(?:快速开始|30\s*秒)/u.test(readme)) addFinding(findings, "DOC_ROUTE_QUICKSTART_HEADING_MISSING", "README.md");
  if (!/(?:UNVERIFIED|unverified|未验证)/u.test(readme)) addFinding(findings, "DOC_ROUTE_EVIDENCE_BOUNDARY_MISSING", "README.md");

  const skill = documents.get("SKILL.md") ?? "";
  requireTerms(
    findings,
    "SKILL.md",
    skill,
    [
      "workflows/one-click-stable.md",
      "workflows/fast-cut.md",
      "workflows/pro-enhance.md",
      "workflows/resume.md",
      "workflows/official-skill-map.md",
    ],
    "DOC_ROUTE_SKILL_WORKFLOW_MISSING",
  );
  if (!/(?:UNVERIFIED|unverified|未验证|须另有.{0,12}证据)/iu.test(skill)) addFinding(findings, "DOC_ROUTE_EVIDENCE_BOUNDARY_MISSING", "SKILL.md");

  const map = documents.get("workflows/official-skill-map.md") ?? "";
  requireTerms(findings, "workflows/official-skill-map.md", map, OFFICIAL_SKILLS, "DOC_ROUTE_OFFICIAL_SKILL_MISSING");
  if (!/(?:当前|实时).{0,20}(?:工具|参数|定义|合同)/u.test(map)) addFinding(findings, "DOC_ROUTE_LIVE_TOOL_SOURCE_MISSING", "workflows/official-skill-map.md");

  const starters = [
    documents.get("agents/openai.yaml") ?? "",
    documents.get("workflows/one-click-stable.md") ?? "",
    documents.get("workflows/fast-cut.md") ?? "",
    documents.get("workflows/pro-enhance.md") ?? "",
    documents.get("workflows/resume.md") ?? "",
  ].join("\n");
  STARTER_PROMPTS.forEach((pattern, index) => {
    if (!pattern.test(starters)) {
      addFinding(findings, "DOC_ROUTE_STARTER_PROMPT_MISSING", "agents/openai.yaml+workflows", String(index + 1));
    }
  });

  const agents = documents.get("AGENTS.md") ?? "";
  requireTerms(findings, "AGENTS.md", agents, ["starter prompt", "handoff"], "DOC_ROUTE_AGENT_POLICY_MISSING");
  if (!/run manifest/iu.test(agents)) addFinding(findings, "DOC_ROUTE_AGENT_POLICY_MISSING", "AGENTS.md", "run manifest");
  if (!/high[- ]risk/iu.test(agents)) addFinding(findings, "DOC_ROUTE_AGENT_POLICY_MISSING", "AGENTS.md", "high-risk");

  const oneClick = documents.get("workflows/one-click-stable.md") ?? "";
  requireTerms(findings, "workflows/one-click-stable.md", oneClick, ["样片", "review_ready", "UNVERIFIED"], "DOC_ROUTE_STABLE_WORKFLOW_INCOMPLETE");
  const resume = documents.get("workflows/resume.md") ?? "";
  requireTerms(findings, "workflows/resume.md", resume, ["超时", "回读", "手工修改", "UNVERIFIED"], "DOC_ROUTE_RESUME_WORKFLOW_INCOMPLETE");

  return {
    ok: findings.length === 0,
    documents: documents.size,
    artifacts: REQUIRED_ARTIFACTS.length,
    officialSkills: OFFICIAL_SKILLS.length,
    starterPrompts: STARTER_PROMPTS.length,
    findings,
  };
}

const options = parseArguments(process.argv.slice(2));
const result = audit(options.root);
if (options.json) {
  process.stdout.write(`${JSON.stringify(result)}\n`);
} else if (result.ok) {
  process.stdout.write(`docs routing audit passed: ${result.documents} routing document(s), ${result.officialSkills} official skill route(s), ${result.starterPrompts} starter prompt(s)\n`);
} else {
  for (const finding of result.findings) {
    process.stderr.write(`${finding.code} path=${finding.file}${finding.detail ? ` detail=${finding.detail}` : ""}\n`);
  }
}
if (!result.ok) process.exitCode = 1;
