const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Configuration: category thresholds (days before a contact is "overdue")
// ---------------------------------------------------------------------------

const DEFAULT_THRESHOLDS = {
  "Inner Circle": parseInt(process.env.CRM_INNER_CIRCLE_DAYS || "30", 10),
  Professional: parseInt(process.env.CRM_PROFESSIONAL_DAYS || "90", 10),
  Friend: parseInt(process.env.CRM_FRIEND_DAYS || "60", 10),
  Casual: parseInt(process.env.CRM_CASUAL_DAYS || "120", 10),
};

// ---------------------------------------------------------------------------
// Data loading
// ---------------------------------------------------------------------------

function loadContacts(filePath) {
  const resolved = path.resolve(filePath || "contacts.json");
  if (!fs.existsSync(resolved)) {
    throw new Error(`Contacts file not found: ${resolved}`);
  }
  return JSON.parse(fs.readFileSync(resolved, "utf-8"));
}

// ---------------------------------------------------------------------------
// Scoring engine
// ---------------------------------------------------------------------------

function daysSince(dateStr) {
  const then = new Date(dateStr);
  const now = new Date();
  const diffMs = now - then;
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

function scoreContacts(contacts, thresholds) {
  return contacts.map((c) => {
    const days = daysSince(c.lastInteractionDate);
    const threshold = thresholds[c.category] || thresholds["Casual"];
    const overdue = days - threshold;
    return { ...c, days, threshold, overdue };
  });
}

function filterOverdue(scored) {
  return scored
    .filter((c) => c.overdue > 0)
    .sort((a, b) => b.overdue - a.overdue);
}

// ---------------------------------------------------------------------------
// Drafting assistant
// ---------------------------------------------------------------------------

function draftMessage(contact) {
  const topic = contact.lastTopic;
  const name = contact.name.split(" ")[0];
  const method =
    contact.contactMethod === "email"
      ? "email"
      : contact.contactMethod === "slack"
        ? "Slack"
        : "text";

  const templates = [
    `Hey ${name}, I saw something that reminded me of you — ${topic.toLowerCase()}. How's that going?`,
    `Hey ${name}! I was just thinking about ${topic.toLowerCase()}. Any updates? Would love to catch up.`,
    `${name}! It's been a minute. Last time we talked ${topic.toLowerCase()} — still on that? Let's reconnect soon.`,
  ];

  // Deterministic pick based on name so the same contact always gets the same template
  const idx = name.charCodeAt(0) % templates.length;
  return templates[idx];
}

// ---------------------------------------------------------------------------
// Main command: warm_up_check
// ---------------------------------------------------------------------------

function warmUpCheck({ limit, category, contactsPath } = {}) {
  const thresholds = { ...DEFAULT_THRESHOLDS };
  const maxResults = Math.max(1, limit || 3);

  const contacts = loadContacts(contactsPath);
  let filtered = category
    ? contacts.filter((c) => c.category.toLowerCase() === category.toLowerCase())
    : contacts;

  const scored = scoreContacts(filtered, thresholds);
  const overdue = filterOverdue(scored).slice(0, maxResults);

  if (overdue.length === 0) {
    return "All caught up! No contacts are overdue for a warm-up.";
  }

  // Build Markdown output
  const lines = [
    `**Warm-Up Check** (${overdue.length} suggestion${overdue.length > 1 ? "s" : ""})\n`,
    "| Name | Category | Days Since | Overdue By | Hook |",
    "|------|----------|------------|------------|------|",
  ];

  for (const c of overdue) {
    const hook = c.lastTopic.split(" ").slice(0, 6).join(" ") + "...";
    lines.push(
      `| ${c.name} | ${c.category} | ${c.days}d | +${c.overdue}d | ${hook} |`
    );
  }

  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("**Draft Messages:**\n");

  for (const c of overdue) {
    const draft = draftMessage(c);
    lines.push(`**${c.name}** (${c.contactMethod}):`);
    lines.push(`> ${draft}\n`);
  }

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Exports / CLI entry point
// ---------------------------------------------------------------------------

module.exports = { warmUpCheck, scoreContacts, filterOverdue, draftMessage };

// Allow direct invocation: node handler.js warm_up_check [--limit N] [--category CATEGORY]
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command !== "warm_up_check") {
    console.error('Usage: node handler.js warm_up_check [--limit N] [--category "Inner Circle"]');
    process.exit(1);
  }

  let limit;
  let category;

  for (let i = 1; i < args.length; i++) {
    if (args[i] === "--limit" && args[i + 1]) {
      limit = parseInt(args[++i], 10);
    } else if (args[i] === "--category" && args[i + 1]) {
      category = args[++i];
    }
  }

  const report = warmUpCheck({ limit, category, contactsPath: path.join(__dirname, "contacts.json") });
  console.log(report);
}
