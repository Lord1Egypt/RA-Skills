#!/usr/bin/env node

/**
 * Keyword Suggester
 * Analyzes user feedback to generate keyword adjustment suggestions.
 *
 * Usage:
 *   node keyword-suggester.mjs --slot morning --days 7
 *   node keyword-suggester.mjs --date 2026-03-06 --slot morning
 */

import {
  readJSON,
  feedbackPath,
  listDates,
  loadConfig,
} from "./lib/storage.mjs";

function usage() {
  console.error(
    `Usage: keyword-suggester.mjs [options]

Options:
  --slot <slot>     Slot name: morning, noon, evening (required)
  --date <date>     Target date (YYYY-MM-DD), defaults to today
  --days <n>        Look back n days (default: 7)

Examples:
  node keyword-suggester.mjs --slot morning --days 7
  node keyword-suggester.mjs --date 2026-03-06 --slot morning
`
  );
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

let slot = null;
let date = null;
let days = 7;

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--slot") {
    slot = args[++i];
    continue;
  }
  if (a === "--date") {
    date = args[++i];
    continue;
  }
  if (a === "--days") {
    days = Number.parseInt(args[++i] ?? "7", 10);
    continue;
  }
  if (a.startsWith("-")) {
    console.error(`Unknown arg: ${a}`);
    usage();
  }
}

if (!slot) {
  console.error("Error: --slot is required.");
  usage();
}

// Load current config to get existing keywords
const config = loadConfig();
const slotConfig = config?.slots?.find((s) => s.name === slot);
const currentKeywords = slotConfig?.keywords ?? [];

function dateRange(numDays, targetDate = null) {
  const dates = [];
  const now = targetDate ? new Date(targetDate) : new Date();
  for (let i = 0; i < numDays; i++) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    dates.push(`${y}-${m}-${day}`);
  }
  return dates;
}

function analyzeFeedback(feedbacks) {
  const positiveSignals = [];
  const negativeSignals = [];
  const neutralSignals = [];

  // Keywords commonly associated with positive/negative feedback
  // Order matters: check negative patterns that override positive ones first
  const negativePatterns = [
    // Chinese negative patterns
    /不太|不很|不怎|不喜|不感|不想要|不感兴趣|无聊|没用|太短|太长|不够|太少|不想|不要|删掉|移除|没意思|没兴趣|腻了|烦了/,
    // English negative patterns
    /not (interested|like|want|need)|dislike|boring|useless|too short|too long|not enough|don'?t want|remove|tired of|stop/,
  ];

  const positivePatterns = [
    // Chinese positive patterns
    /喜欢|感兴趣|不错|很好|棒|感谢|有用|有帮助|正是|正是我想|正是我需|及时|实用|希望|想要|多要/,
    // English positive patterns
    /good|great|love|like|interested|useful|helpful|thanks|thank|exactly|what I need|good job|more|want|need|please add/,
  ];

  for (const fb of feedbacks) {
    const text = fb.text;

    let isPositive = false;
    let isNegative = false;

    // Check negative patterns first (they override positive)
    for (const pattern of negativePatterns) {
      if (pattern.test(text)) {
        isNegative = true;
        break;
      }
    }

    // Only check positive if not negative
    if (!isNegative) {
      for (const pattern of positivePatterns) {
        if (pattern.test(text)) {
          isPositive = true;
          break;
        }
      }
    }

    const signal = {
      id: fb.id,
      text: fb.text,
      item_id: fb.item_id,
      date: fb.created_at,
    };

    if (isPositive) {
      positiveSignals.push(signal);
    } else if (isNegative) {
      negativeSignals.push(signal);
    } else {
      neutralSignals.push(signal);
    }
  }

  return { positiveSignals, negativeSignals, neutralSignals };
}

// Main execution
const dates = date ? [date] : dateRange(days);
const allFeedbacks = [];

console.log(`## Keyword Suggestion Analysis for "${slot}"\n`);
console.log(`Date range: ${dates[dates.length - 1]} to ${dates[0]}`);
console.log(`Current keywords: ${currentKeywords.join(", ") || "(none)"}\n`);

// Collect feedback records
for (const d of dates) {
  const path = feedbackPath(d, slot);
  const record = readJSON(path);
  if (record?.feedbacks) {
    for (const fb of record.feedbacks) {
      allFeedbacks.push({ ...fb, date: d });
    }
  }
}

if (allFeedbacks.length === 0) {
  console.log("No feedback found for the specified criteria.");
  console.log("\n### AI Prompt Template\n");
  console.log(
`Analyze recent push content and suggest new keywords:

Current keywords: ${currentKeywords.join(", ")}

Analyze the push content and identify 3-5 potential new keywords that could help capture more relevant content. Exclude keywords already in the current list.

Output format (JSON):
{
  "suggestions": [
    { "keyword": "defi", "reason": "Frequently appearing in recent news", "priority": "high" }
  ]
}
`
  );
  process.exit(0);
}

// Analyze feedback
const analysis = analyzeFeedback(allFeedbacks);

console.log(`### Feedback Summary\n`);
console.log(`Total feedback: ${allFeedbacks.length}`);
console.log(`- Positive signals: ${analysis.positiveSignals.length}`);
console.log(`- Negative signals: ${analysis.negativeSignals.length}`);
console.log(`- Neutral: ${analysis.neutralSignals.length}\n`);

if (analysis.positiveSignals.length > 0) {
  console.log("#### Positive Feedback (user likes content):\n");
  for (const fb of analysis.positiveSignals) {
    console.log(`- [${fb.date}] ${fb.text}`);
  }
  console.log();
}

if (analysis.negativeSignals.length > 0) {
  console.log("#### Negative Feedback (user dislikes content):\n");
  for (const fb of analysis.negativeSignals) {
    console.log(`- [${fb.date}] ${fb.text}`);
  }
  console.log();
}

// Generate structured output for AI
const output = {
  meta: {
    slot,
    date_range: { start: dates[dates.length - 1], end: dates[0] },
    current_keywords: currentKeywords,
    total_feedback: allFeedbacks.length,
  },
  analysis: {
    positive_count: analysis.positiveSignals.length,
    negative_count: analysis.negativeSignals.length,
    neutral_count: analysis.neutralSignals.length,
  },
  positive_signals: analysis.positiveSignals.map((fb) => ({
    text: fb.text,
    item_id: fb.item_id,
    date: fb.date,
  })),
  negative_signals: analysis.negativeSignals.map((fb) => ({
    text: fb.text,
    item_id: fb.item_id,
    date: fb.date,
  })),
  all_feedback: allFeedbacks.map((fb) => ({
    text: fb.text,
    item_id: fb.item_id,
    date: fb.date,
  })),
};

console.log("### Structured Output (for AI analysis)\n");
console.log(JSON.stringify(output, null, 2));

// AI prompt template
console.log("\n### AI Prompt Template\n");
console.log(
`Analyze user feedback and suggest keyword adjustments:

Current keywords: ${currentKeywords.join(", ")}

Feedback analysis:
- Positive signals (${analysis.positiveSignals.length}): ${analysis.positiveSignals.map(f => f.text).join("; ")}
- Negative signals (${analysis.negativeSignals.length}): ${analysis.negativeSignals.map(f => f.text).join("; ")}

Based on this feedback, generate keyword adjustment suggestions.

Output format (JSON):
{
  "suggestions": [
    {
      "action": "add|remove|increase_weight|decrease_weight",
      "keyword": "defi",
      "reason": "User requested more DeFi content",
      "priority": "high|medium|low"
    }
  ],
  "summary": "Brief explanation of the recommended changes"
}
`
);
