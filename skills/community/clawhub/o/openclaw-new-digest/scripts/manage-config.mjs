#!/usr/bin/env node

import {
  loadConfig,
  saveConfig,
  configPath,
  nowISO,
} from "./lib/storage.mjs";

function usage() {
  console.error(
    `Usage: manage-config.mjs <command> [options]

Commands:
  show                 Display current configuration
  init                 Create default configuration (will not overwrite existing)
  set-slot             Add or update a slot
  remove-slot          Remove a slot by name
  set-defaults         Update default settings
  reset                Reset to factory defaults (overwrites existing!)

set-slot options (all required for new slot, optional for update):
  --name <name>        Slot identifier (e.g. morning, noon, evening, custom-name)
  --time <HH:MM>       Push time (e.g. 08:00)
  --topic <topic>      Topic label (e.g. "Finance", "AI/Agent")
  --label <label>      Display label (e.g. "金融早报")
  --keywords <kw>      Comma-separated keywords
  --priority <desc>    Priority description (free text)
  --sources <src>      Comma-separated sources: twitter,tavily,hackernews

remove-slot options:
  --name <name>        Slot name to remove

set-defaults options:
  --summary-length <range>    e.g. "100-300"
  --summary-language <lang>   e.g. "zh-CN"
  --items-per-push <range>    e.g. "3-10"
  --time-window-hours <n>     e.g. 24

Examples:
  node manage-config.mjs show
  node manage-config.mjs init
  node manage-config.mjs set-slot --name morning --time 08:30 --topic Finance --label 金融早报 --keywords "crypto,bitcoin,stock" --sources "twitter,tavily,hackernews"
  node manage-config.mjs remove-slot --name evening
  node manage-config.mjs set-defaults --summary-language en
  node manage-config.mjs reset`
  );
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const command = args[0];

function parseArgs() {
  const opts = {};
  for (let i = 1; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const val = args[++i];
      if (val === undefined) { console.error(`Missing value for ${a}`); process.exit(2); }
      opts[key] = val;
    }
  }
  return opts;
}

function defaultConfig() {
  return {
    slots: [
      {
        name: "morning",
        time: "08:00",
        hour: 8,
        window: [7, 9],
        topic: "Finance",
        label: "金融早报",
        keywords: ["crypto", "bitcoin", "ethereum", "finance", "stock"],
        priority: "crypto > financial events > US stocks = HK stocks > A-shares",
        sources: ["twitter", "tavily", "hackernews"],
        influence_thresholds: { twitter_likes: 100, hackernews_score: 50, tavily_relevance: 60 },
      },
      {
        name: "noon",
        time: "12:00",
        hour: 12,
        window: [11, 13],
        topic: "AI / Agent",
        label: "AI午报",
        keywords: ["AI", "LLM", "GPT", "agent", "machine learning"],
        priority: "LLM progress > AI applications > agent frameworks > AI debates",
        sources: ["twitter", "tavily", "hackernews"],
        influence_thresholds: { twitter_likes: 100, hackernews_score: 50, tavily_relevance: 60 },
      },
      {
        name: "evening",
        time: "18:00",
        hour: 18,
        window: [17, 19],
        topic: "General (divergent)",
        label: "晚间热点",
        keywords: ["technology", "science", "trending"],
        priority: "finance + AI extended to tech, science, society hotspots",
        sources: ["twitter", "tavily", "hackernews"],
        influence_thresholds: { twitter_likes: 200, hackernews_score: 80, tavily_relevance: 60 },
      },
    ],
    defaults: {
      summary_length: "100-300",
      summary_language: "zh-CN",
      items_per_push: "3-10",
      time_window_hours: 24,
    },
    created_at: nowISO(),
    updated_at: nowISO(),
  };
}

function parseTime(timeStr) {
  const m = timeStr.match(/^(\d{1,2}):(\d{2})$/);
  if (!m) return null;
  return Number.parseInt(m[1], 10);
}

function printConfig(config) {
  console.log("## News Digest Configuration\n");

  console.log("### Slots\n");
  if (!config.slots || config.slots.length === 0) {
    console.log("No slots configured. Run `manage-config.mjs init` or `manage-config.mjs set-slot` to add slots.\n");
  } else {
    console.log("| Name | Time | Topic | Label | Keywords |");
    console.log("|------|------|-------|-------|----------|");
    for (const s of config.slots) {
      const kw = (s.keywords ?? []).join(", ");
      console.log(`| ${s.name} | ${s.time} | ${s.topic} | ${s.label} | ${kw} |`);
    }
    console.log();
    for (const s of config.slots) {
      console.log(`**${s.name}** (${s.label})`);
      console.log(`- Time: ${s.time} (window: ${s.window?.[0] ?? "?"}:00-${s.window?.[1] ?? "?"}:00)`);
      console.log(`- Priority: ${s.priority}`);
      console.log(`- Sources: ${(s.sources ?? []).join(", ")}`);
      console.log(`- Thresholds: Twitter likes > ${s.influence_thresholds?.twitter_likes ?? "?"}, HN score > ${s.influence_thresholds?.hackernews_score ?? "?"}, Tavily relevance > ${s.influence_thresholds?.tavily_relevance ?? "?"}%`);
      console.log();
    }
  }

  console.log("### Defaults\n");
  const d = config.defaults ?? {};
  console.log(`- Summary length: ${d.summary_length ?? "100-300"} chars`);
  console.log(`- Summary language: ${d.summary_language ?? "zh-CN"}`);
  console.log(`- Items per push: ${d.items_per_push ?? "3-10"}`);
  console.log(`- Time window: ${d.time_window_hours ?? 24} hours`);
  console.log();
  console.log(`Config path: ${configPath()}`);
  console.log(`Last updated: ${config.updated_at ?? "unknown"}`);
}

if (command === "show") {
  const config = loadConfig();
  if (!config) {
    console.log("## No Configuration Found\n");
    console.log("No config file exists yet. The agent should ask the user to set up their preferred schedule and topics.\n");
    console.log("To create default config: `node manage-config.mjs init`");
    console.log("To set up a custom slot: `node manage-config.mjs set-slot --name morning --time 08:00 --topic Finance --label 金融早报 --keywords \"crypto,bitcoin\" --sources \"twitter,tavily,hackernews\"`");
  } else {
    printConfig(config);
  }

} else if (command === "init") {
  const existing = loadConfig();
  if (existing) {
    console.log("## Configuration Already Exists\n");
    console.log("Use `show` to view, `set-slot` to modify, or `reset` to overwrite.");
    process.exit(0);
  }
  const config = defaultConfig();
  saveConfig(config);
  console.log("## Default Configuration Created\n");
  printConfig(config);

} else if (command === "set-slot") {
  const opts = parseArgs();
  if (!opts.name) {
    console.error("Error: --name is required for set-slot.");
    process.exit(1);
  }

  let config = loadConfig();
  if (!config) {
    config = { slots: [], defaults: defaultConfig().defaults, created_at: nowISO(), updated_at: nowISO() };
  }

  const idx = config.slots.findIndex((s) => s.name === opts.name);
  const existing = idx >= 0 ? config.slots[idx] : {};

  const hour = opts.time ? parseTime(opts.time) : existing.hour;
  if (opts.time && hour === null) {
    console.error(`Error: invalid time format "${opts.time}". Use HH:MM.`);
    process.exit(1);
  }

  const slot = {
    name: opts.name,
    time: opts.time ?? existing.time ?? "08:00",
    hour: hour ?? existing.hour ?? 8,
    window: hour != null ? [Math.max(0, hour - 1), Math.min(23, hour + 1)] : (existing.window ?? [7, 9]),
    topic: opts.topic ?? existing.topic ?? opts.name,
    label: opts.label ?? existing.label ?? opts.name,
    keywords: opts.keywords ? opts.keywords.split(",").map((k) => k.trim()) : (existing.keywords ?? []),
    priority: opts.priority ?? existing.priority ?? "",
    sources: opts.sources ? opts.sources.split(",").map((s) => s.trim()) : (existing.sources ?? ["twitter", "tavily", "hackernews"]),
    influence_thresholds: existing.influence_thresholds ?? { twitter_likes: 100, hackernews_score: 50, tavily_relevance: 60 },
  };

  if (idx >= 0) {
    config.slots[idx] = slot;
  } else {
    config.slots.push(slot);
  }

  config.slots.sort((a, b) => (a.hour ?? 0) - (b.hour ?? 0));
  saveConfig(config);

  console.log(`## Slot "${opts.name}" ${idx >= 0 ? "Updated" : "Added"}\n`);
  console.log(`- Time: ${slot.time}`);
  console.log(`- Topic: ${slot.topic}`);
  console.log(`- Label: ${slot.label}`);
  console.log(`- Keywords: ${slot.keywords.join(", ")}`);
  console.log(`- Sources: ${slot.sources.join(", ")}`);

} else if (command === "remove-slot") {
  const opts = parseArgs();
  if (!opts.name) {
    console.error("Error: --name is required for remove-slot.");
    process.exit(1);
  }

  const config = loadConfig();
  if (!config) {
    console.error("Error: no config file exists.");
    process.exit(1);
  }

  const before = config.slots.length;
  config.slots = config.slots.filter((s) => s.name !== opts.name);

  if (config.slots.length === before) {
    console.log(`Slot "${opts.name}" not found. Available: ${config.slots.map((s) => s.name).join(", ")}`);
    process.exit(0);
  }

  saveConfig(config);
  console.log(`## Slot "${opts.name}" Removed\n`);
  console.log(`Remaining slots: ${config.slots.map((s) => `${s.name} (${s.time})`).join(", ") || "none"}`);

} else if (command === "set-defaults") {
  const opts = parseArgs();
  let config = loadConfig();
  if (!config) {
    config = defaultConfig();
  }

  if (opts["summary-length"]) config.defaults.summary_length = opts["summary-length"];
  if (opts["summary-language"]) config.defaults.summary_language = opts["summary-language"];
  if (opts["items-per-push"]) config.defaults.items_per_push = opts["items-per-push"];
  if (opts["time-window-hours"]) config.defaults.time_window_hours = Number.parseInt(opts["time-window-hours"], 10);

  saveConfig(config);
  console.log("## Defaults Updated\n");
  console.log(`- Summary length: ${config.defaults.summary_length}`);
  console.log(`- Summary language: ${config.defaults.summary_language}`);
  console.log(`- Items per push: ${config.defaults.items_per_push}`);
  console.log(`- Time window: ${config.defaults.time_window_hours} hours`);

} else if (command === "reset") {
  const config = defaultConfig();
  saveConfig(config);
  console.log("## Configuration Reset to Defaults\n");
  printConfig(config);

} else {
  console.error(`Unknown command: ${command}`);
  usage();
}
