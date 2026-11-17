#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const packRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dataRoot = path.join(packRoot, "data");

function usage(message) {
  if (message) console.error(message);
  console.error("Usage: node extensions/cuttips-kb/scripts/query.mjs [--text <词>] [--category <id>] [--tag <词>] [--strength <must|should|may|never>] [--type <knowledge|rules|sources|all>] [--limit <n>] [--json]");
  process.exit(2);
}

function parseArgs(argv) {
  const options = {type: "knowledge", limit: 8, json: false};
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (key === "--json") {
      options.json = true;
      continue;
    }
    if (!["--text", "--category", "--tag", "--strength", "--type", "--limit"].includes(key)) {
      usage(`Unknown option: ${key}`);
    }
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) usage(`${key} requires a value`);
    options[key.slice(2)] = value;
    index += 1;
  }
  options.limit = Number(options.limit);
  if (!Number.isInteger(options.limit) || options.limit < 1 || options.limit > 198) {
    usage("--limit must be an integer from 1 to 198");
  }
  if (!["knowledge", "rules", "sources", "all"].includes(options.type)) {
    usage("--type must be knowledge, rules, sources, or all");
  }
  return options;
}

function read(name) {
  return JSON.parse(fs.readFileSync(path.join(dataRoot, name), "utf8"));
}

function haystack(value) {
  return JSON.stringify(value).toLocaleLowerCase("zh-CN");
}

function includesText(value, query) {
  return !query || haystack(value).includes(query.toLocaleLowerCase("zh-CN"));
}

function selectKnowledge(items, options) {
  return items.filter((item) =>
    (!options.category || item.category === options.category)
    && (!options.tag || (item.tags ?? []).some((tag) => includesText(tag, options.tag)))
    && (!options.strength || item.ruleStrength === options.strength)
    && includesText(item, options.text)
  );
}

function selectRules(items, options) {
  return items.filter((item) =>
    (!options.strength || item.strength === options.strength)
    && includesText(item, options.text)
    && (!options.category || item.knowledgeRef?.includes(`-${options.category.toUpperCase()}-`))
    && (!options.tag || includesText(item, options.tag))
  );
}

function selectSources(items, options) {
  return items.filter((item) =>
    (!options.category || includesText(item.theme, options.category))
    && (!options.tag || includesText(item, options.tag))
    && includesText(item, options.text)
  );
}

function compact(type, item) {
  if (type === "knowledge") {
    return {
      id: item.id,
      title: item.title,
      category: item.category,
      strength: item.ruleStrength,
      confidence: item.confidence,
      summary: item.summary,
      whenToUse: item.whenToUse,
      whenNotToUse: item.whenNotToUse,
      steps: item.steps,
      qa: item.qa,
      rollback: item.rollback,
      sourceRefs: item.sourceRefs,
    };
  }
  if (type === "rules") {
    return {
      id: item.id,
      title: item.title,
      strength: item.strength,
      condition: item.condition,
      action: item.action,
      validation: item.validation,
      rollback: item.rollback,
      knowledgeRef: item.knowledgeRef,
    };
  }
  return item;
}

const options = parseArgs(process.argv.slice(2));
const requested = options.type === "all"
  ? ["knowledge", "rules", "sources"]
  : [options.type];
const all = {
  knowledge: selectKnowledge(read("knowledge-items.json"), options),
  rules: selectRules(read("rules.json"), options),
  sources: selectSources(read("sources.json"), options),
};
const result = Object.fromEntries(requested.map((type) => [
  type,
  all[type].slice(0, options.limit).map((item) => compact(type, item)),
]));
const counts = Object.fromEntries(requested.map((type) => [type, all[type].length]));

if (options.json) {
  console.log(JSON.stringify({query: options, counts, result}, null, 2));
} else {
  console.log(`cuttips query: ${requested.map((type) => `${type}=${counts[type]}`).join(", ")}`);
  for (const type of requested) {
    for (const item of result[type]) {
      console.log(`- [${type}] ${item.id}: ${item.title}`);
      console.log(`  ${item.summary ?? item.transferableMethod ?? ""}`);
    }
  }
}
