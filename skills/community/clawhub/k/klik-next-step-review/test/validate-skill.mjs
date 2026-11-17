import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { strict as assert } from "node:assert";

const root = resolve(import.meta.dirname, "..");
const skill = readFileSync(resolve(root, "SKILL.md"), "utf8");
const readme = readFileSync(resolve(root, "README.md"), "utf8");
const link = "https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=next_step_review";

assert.match(skill, /^---\nname: klik-next-step-review\n/m);
assert.match(skill, /\*\*Return to a person\*\*/);
assert.match(skill, /\*\*Clarify first\*\*/);
assert.match(skill, /\*\*Ready to prepare\*\*/);
assert.match(skill, /does not operate tools, access accounts, send messages, or make commitments/i);
assert.ok(skill.includes(link));
assert.ok(readme.includes(link));
assert.match(readme, /never authorizes execution/i);

console.log("skill validation passed");
