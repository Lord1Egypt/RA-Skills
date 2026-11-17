#!/usr/bin/env node
// prompt-injection-scan: checks text that someone other than the user wrote
// (an email, a meeting invite, a web page, a document) for signs that it is
// trying to give orders to an AI assistant. No dependencies, no network.
//
// Usage:
//   node scan.mjs --file path/to/text.txt
//   node scan.mjs < text.txt
//   node scan.mjs --pretty --file text.txt      (human-readable instead of JSON)
//
// Output (JSON on stdout):
//   { verdict: "clean" | "suspicious" | "likely_injection", score, findings: [
//       { rule, weight, line, evidence } ], chars, lines }
// Exit code is always 0 unless the input cannot be read (exit 1): the verdict
// is data for the agent, not a crash.
//
// Written for CSCI 599 Assignment 3 (USC, Fall 2026) from two real attacks on a
// test assistant: an email footer and a calendar-event title that each told the
// assistant to save rules to memory and send the user's data to an outside
// address while hiding it from the user.

import { readFileSync, realpathSync } from "node:fs";
import { pathToFileURL } from "node:url";

export const RULES = [
  {
    rule: "addressed_to_ai",
    weight: 3,
    why: "text speaks directly to an AI assistant",
    re: /\b(note|message|instructions?) (to|for) (the |any )?(ai|assistant|agent|llm|model|bot)\b|\b(dear|attention|hey) (ai|assistant|agent|model|chatgpt|claude|gemini)\b|\bai assistant reading this\b|\bif you are an? (ai|language model|llm|assistant)\b/i,
  },
  {
    rule: "override_instructions",
    weight: 4,
    why: "tries to cancel the assistant's real instructions",
    re: /\b(ignore|disregard|forget|override|bypass) (all |any |your |the )*(previous|prior|above|earlier|original|system)? ?(instructions|rules|guidelines|prompts?|directives)\b|\byou are now (in )?\w+ mode\b|\bnew (system )?instructions\b|\bsystem prompt\b/i,
  },
  {
    rule: "secrecy",
    weight: 4,
    why: "asks to hide the action from the user",
    re: /\b(do not|don'?t|never) (tell|mention|inform|notify|show|alert|reveal|ask)\b[^.\n]{0,40}\b(user|owner|jordan|him|her|them|anyone)\b|\bwithout (telling|notifying|asking|informing)\b|\bkeep (this|it) (secret|hidden|between us|confidential)\b|\bdo not (mention|reveal) this (note|message|instruction)\b/i,
  },
  {
    rule: "false_authority",
    weight: 2,
    why: "claims approval or authority it cannot prove",
    re: /\b(already |pre-?)approved\b|\bapproved by (the )?(user|owner|admin|management)\b|\bi am (the|your) (developer|admin|administrator|owner|creator|operator)\b|\bauthori[sz]ed (by|to)\b|\b(maintenance|developer|debug|admin) mode\b/i,
  },
  {
    rule: "action_request",
    weight: 2,
    why: "asks the assistant to perform an action with the user's tools",
    re: /\b(send|forward|email|e-mail|cc|bcc|draft an email|reply to|save (this |it )?(to|in) (your )?memory|remember that|add [^.\n]{0,40} to (the |your )?(allow ?list|contacts|memory)|upload|export|share|post|delete|transfer|create (a |an )?(rule|filter|event))\b/i,
  },
  {
    rule: "outside_destination",
    weight: 2,
    why: "names an email address or link as a destination",
    re: /\b(to|cc|bcc|at|into|via)\s+<?[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b|\b(to|at|into|via)\s+https?:\/\/\S+/i,
  },
  {
    rule: "data_harvest",
    weight: 3,
    why: "asks for the user's private data in bulk",
    re: /\b(all|every|last \d+|full|entire)\b[^.\n]{0,40}\b(emails?|messages?|subjects?|senders?|contacts?|meetings?|calendar|schedule|passwords?|files|documents)\b/i,
  },
  {
    rule: "fence_break",
    weight: 4,
    why: "contains markers that imitate prompt boundaries",
    re: /<<<|>>>|END UNTRUSTED|<\/?(system|assistant|user|instructions?)>|\[\/?INST\]|<\|im_(start|end)\|>|<\|(system|user|assistant)\|>/i,
  },
  {
    rule: "hidden_characters",
    weight: 3,
    why: "contains invisible or text-direction characters",
    re: /[​-‏⁠-⁤﻿‪-‮⁦-⁩­]/,
  },
  {
    rule: "hidden_html",
    weight: 3,
    why: "uses HTML/CSS tricks to hide text from a human reader",
    re: /display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*0(px|pt|em)?\b|color\s*:\s*(#fff(fff)?|white)\b[^"']{0,40}background(-color)?\s*:\s*(#fff(fff)?|white)|opacity\s*:\s*0(\.0+)?\b/i,
  },
  {
    rule: "encoded_blob",
    weight: 1,
    why: "contains a long encoded block that could hide instructions",
    re: /[A-Za-z0-9+/]{80,}={0,2}/,
  },
];

// A single "action_request" is normal in mail ("please reply by Friday").
// It only counts toward the verdict when another signal is also present.
const CONTEXT_ONLY = new Set(["action_request", "outside_destination", "data_harvest"]);

const snippet = (line, index, length) => {
  const start = Math.max(0, index - 30);
  const text = line.slice(start, index + length + 30).replace(/[​-‏⁠-⁤﻿‪-‮⁦-⁩­]/g, "␣");
  return (start > 0 ? "…" : "") + text.trim() + (index + length + 30 < line.length ? "…" : "");
};

export function scan(text) {
  const input = String(text ?? "");
  const lines = input.split(/\r?\n/);
  const findings = [];
  for (const { rule, weight, why, re } of RULES) {
    for (let i = 0; i < lines.length; i++) {
      const m = lines[i].match(re);
      if (m) {
        findings.push({ rule, weight, why, line: i + 1, evidence: snippet(lines[i], m.index ?? 0, m[0].length) });
        break; // one finding per rule is enough
      }
    }
  }
  const strong = findings.filter((f) => !CONTEXT_ONLY.has(f.rule));
  const score = strong.length ? findings.reduce((s, f) => s + f.weight, 0) : 0;
  const verdict = score >= 6 ? "likely_injection" : score >= 3 ? "suspicious" : "clean";
  return { verdict, score, findings, chars: input.length, lines: lines.length };
}

function pretty(r) {
  const head = { clean: "CLEAN", suspicious: "SUSPICIOUS", likely_injection: "LIKELY INJECTION" }[r.verdict];
  const out = [`${head} (score ${r.score}, ${r.findings.length} signal${r.findings.length === 1 ? "" : "s"})`];
  for (const f of r.findings) out.push(`  - ${f.rule} (+${f.weight}, line ${f.line}): ${f.why}\n      "${f.evidence}"`);
  return out.join("\n");
}

function main(argv) {
  const fileAt = argv.indexOf("--file");
  let text;
  try {
    text = fileAt >= 0 ? readFileSync(argv[fileAt + 1], "utf8") : readFileSync(0, "utf8");
  } catch (err) {
    process.stderr.write(`prompt-injection-scan: could not read input: ${err.message}\n`);
    process.exit(1);
  }
  const result = scan(text);
  process.stdout.write((argv.includes("--pretty") ? pretty(result) : JSON.stringify(result, null, 2)) + "\n");
}

// Run main() only when executed directly, not when imported by the tests.
const invoked = process.argv[1] && pathToFileURL(realpathSync(process.argv[1])).href;
if (import.meta.url === invoked) main(process.argv.slice(2));
