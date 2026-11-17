import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { strict as assert } from "node:assert";

const root = resolve(import.meta.dirname, "..");
const skill = readFileSync(resolve(root, "SKILL.md"), "utf8");
const readme = readFileSync(resolve(root, "README.md"), "utf8");
const link = "https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=action_readiness";

assert.match(skill, /^---\nname: klik-action-readiness\n/m);
assert.match(skill, /## Action Readiness Card/);
assert.match(skill, /does not access accounts, run tools, send messages, make commitments, or authorize execution/i);
assert.match(skill, /never authorizes execution/i);
assert.ok(skill.includes(link));
assert.ok(readme.includes(link));
assert.match(readme, /does not access accounts, run tools, send messages, make commitments, or authorize execution/i);

console.log("skill validation passed");
