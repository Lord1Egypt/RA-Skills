/**
 * News Digest Bootstrap Hook for OpenClaw
 *
 * Reads slot configuration from data/config.json (user-defined schedule).
 * If no config exists, reminds the agent to run first-time setup.
 */

const path = require("path");
const fs = require("fs");

function loadConfig() {
  const skillRoot = path.join(__dirname, "..", "..");
  const dataDir =
    (process.env.NEWS_DIGEST_DATA_DIR || "").trim() ||
    path.join(skillRoot, "data");
  const configFile = path.join(dataDir, "config.json");

  if (!fs.existsSync(configFile)) return null;
  try {
    return JSON.parse(fs.readFileSync(configFile, "utf-8"));
  } catch {
    return null;
  }
}

function buildReminder() {
  const config = loadConfig();
  const now = new Date();
  const hour = now.getHours();
  const timeStr = now.toTimeString().slice(0, 5);

  const lines = ["## News Digest Reminder\n"];

  if (!config || !config.slots || config.slots.length === 0) {
    lines.push(
      `**Current time**: ${timeStr}`,
      "",
      "**No schedule configured yet.** This is likely first-time use.",
      "",
      "Please ask the user to set up their preferred push schedule:",
      "1. Ask how many daily pushes they want (e.g. 2-4)",
      "2. For each push, ask: time, topic/theme, keywords, priority rules",
      "3. Save using: `node {baseDir}/scripts/manage-config.mjs set-slot --name <name> --time <HH:MM> --topic <topic> --label <label> --keywords <kw1,kw2> --sources twitter,tavily,hackernews`",
      "",
      "Or create defaults first: `node {baseDir}/scripts/manage-config.mjs init`",
      "Then show config: `node {baseDir}/scripts/manage-config.mjs show`"
    );
    return lines.join("\n");
  }

  const activeSlot = config.slots.find((s) => {
    const w = s.window ?? [Math.max(0, (s.hour ?? 0) - 1), Math.min(23, (s.hour ?? 0) + 1)];
    return hour >= w[0] && hour <= w[1];
  });

  if (activeSlot) {
    lines.push(
      `**Current time**: ${timeStr}`,
      `**Active slot**: ${activeSlot.label} (${activeSlot.name})`,
      `**Topic**: ${activeSlot.topic}`,
      `**Keywords**: ${(activeSlot.keywords ?? []).join(", ")}`,
      "",
      "You should execute the news digest push workflow now:",
      "1. Read config: `node {baseDir}/scripts/manage-config.mjs show`",
      "2. Check recent feedback: `node {baseDir}/scripts/query.mjs feedback --days 3`",
      "3. Fetch data from configured sources, filter, summarize, format, store, and deliver",
      "",
      "Refer to the News Digest skill (SKILL.md) for the full workflow."
    );
  } else {
    const nextSlot = config.slots.find((s) => (s.hour ?? 0) > hour) || config.slots[0];
    lines.push(
      `**Current time**: ${timeStr}`,
      `**Next push**: ${nextSlot ? `${nextSlot.label} at ${nextSlot.time}` : "none scheduled"}`,
      "",
      "No push is due right now. The News Digest skill is available for:",
      "- View schedule: `node {baseDir}/scripts/manage-config.mjs show`",
      "- Query push history: `node {baseDir}/scripts/query.mjs pushes --days 3`",
      "- Review feedback: `node {baseDir}/scripts/query.mjs feedback --days 3`",
      "- Search past content: `node {baseDir}/scripts/query.mjs search --keyword \"keyword\" --days 7`",
      "- Manual on-demand push if requested by the user"
    );
  }

  return lines.join("\n");
}

const handler = async (event) => {
  if (!event || typeof event !== "object") return;
  if (event.type !== "agent" || event.action !== "bootstrap") return;
  if (!event.context || typeof event.context !== "object") return;

  const sessionKey = event.context.sessionKey ?? "";
  if (sessionKey.includes(":subagent:")) return;

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: "NEWS_DIGEST_REMINDER.md",
      content: buildReminder(),
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
