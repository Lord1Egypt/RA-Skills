#!/usr/bin/env node

import { readFile } from "node:fs/promises";

function usage() {
  console.error("Usage: workspace-change-plan.mjs <change-set.json>");
  process.exit(2);
}

function requireString(value, label) {
  if (typeof value !== "string" || !value.trim()) {
    throw new Error(`${label} must be a non-empty string`);
  }
  return value.trim();
}

function normalizeRisk(value) {
  const risk = typeof value === "string" ? value.trim().toLowerCase() : "medium";
  if (["low", "medium", "high"].includes(risk)) return risk;
  return "medium";
}

function renderPlan(input) {
  const title = requireString(input.title, "title");
  const owner = requireString(input.owner, "owner");
  if (!Array.isArray(input.changes) || input.changes.length === 0) {
    throw new Error("changes must be a non-empty array");
  }

  const lines = [
    `# ${title}`,
    "",
    `Owner: ${owner}`,
    "",
    "## Read-only Checks",
    "",
    "- Confirm active admin account and target Workspace domain.",
    "- Export current users, groups, permissions, or settings touched by the change.",
    "- Save rollback evidence before applying writes.",
    "",
    "## Proposed Changes",
    "",
  ];

  input.changes.forEach((change, index) => {
    const number = index + 1;
    const kind = requireString(change.kind, `changes[${index}].kind`);
    const target = requireString(change.target, `changes[${index}].target`);
    const action = requireString(change.action, `changes[${index}].action`);
    const rollback = requireString(change.rollback, `changes[${index}].rollback`);
    const risk = normalizeRisk(change.risk);
    lines.push(`${number}. ${kind}: ${target}`);
    lines.push(`   - Action: ${action}`);
    lines.push(`   - Risk: ${risk}`);
    lines.push(`   - Rollback: ${rollback}`);
    lines.push("");
  });

  lines.push("## Approval Gate");
  lines.push("");
  lines.push("- Do not run write commands until the target list and rollback plan are approved.");
  lines.push("- After writes, rerun the read-only checks and attach the before/after evidence.");
  return lines.join("\n");
}

async function main() {
  const file = process.argv[2];
  if (!file) usage();
  const raw = await readFile(file, "utf8");
  const parsed = JSON.parse(raw);
  console.log(renderPlan(parsed));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
