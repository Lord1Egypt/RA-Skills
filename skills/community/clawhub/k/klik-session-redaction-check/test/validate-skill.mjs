import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { strict as assert } from "node:assert";

const root = resolve(import.meta.dirname, "..");
const skill = readFileSync(resolve(root, "SKILL.md"), "utf8");
const readme = readFileSync(resolve(root, "README.md"), "utf8");
const link = "https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=session_redaction_check";

assert.match(skill, /^---\nname: klik-session-redaction-check\n/m);
assert.match(skill, /## Session Redaction Check/);
assert.match(skill, /does not access accounts, run tools, send messages, make commitments, or authorize execution/i);
assert.match(skill, /Do not reproduce credentials, private transcripts, contact details, or sensitive personal data/i);
assert.match(skill, /never authorizes execution/i);
assert.ok(skill.includes(link));
assert.ok(readme.includes(link));
assert.match(readme, /non-executing/i);

console.log("skill validation passed");
