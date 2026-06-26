import { existsSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(scriptDir, "..");
const projectRoot = resolve(process.argv.includes("--project-root") ? process.argv[process.argv.indexOf("--project-root") + 1] : process.cwd());
const credentialsRoot = resolve(process.argv.includes("--credentials-root") ? process.argv[process.argv.indexOf("--credentials-root") + 1] : join(process.env.HOME ?? "", ".config", "openslaw"));

const requiredSkillPaths = [
  "SKILL.md",
  "DOCS.md",
  "AUTH.md",
  "DEVELOPERS.md",
  "references/api.md",
  "references/playbook.md",
  "manual/index.html",
  "assets/runtime_templates/authorization_profile.template.json",
  "assets/runtime_templates/user_context.template.json",
  "assets/runtime_templates/preferences.template.json",
  "assets/runtime_templates/runtime_state.template.json",
  "assets/runtime_templates/activity_log.template.jsonl",
  "assets/runtime_templates/credentials_ref.template.json",
  "scripts/init_runtime.mjs",
  "scripts/check_skill.mjs",
  "scripts/package_skill.mjs",
  "scripts/sync_hosted_docs.mjs"
];

const requiredRuntimePaths = [
  "memory/openslaw-profile.md",
  "memory/openslaw-market-journal.md",
  "memory/openslaw-workboard.md",
  ".openslaw/authorization_profile.json",
  ".openslaw/user_context.json",
  ".openslaw/preferences.json",
  ".openslaw/runtime_state.json",
  ".openslaw/activity_log.jsonl",
  ".openslaw/credentials_ref.json",
  ".openslaw/orders"
];

let failed = false;

for (const relativePath of requiredSkillPaths) {
  const fullPath = join(skillRoot, relativePath);
  if (!existsSync(fullPath)) {
    failed = true;
    console.error(`missing skill path: ${fullPath}`);
    continue;
  }

  console.log(`ok skill path: ${fullPath}`);
}

for (const relativePath of requiredRuntimePaths) {
  const fullPath = join(projectRoot, relativePath);
  if (!existsSync(fullPath)) {
    failed = true;
    console.error(`missing runtime path: ${fullPath}`);
    continue;
  }

  console.log(`ok runtime path: ${fullPath}`);
}

const ordersPath = join(projectRoot, ".openslaw", "orders");
if (existsSync(ordersPath) && !statSync(ordersPath).isDirectory()) {
  failed = true;
  console.error(`runtime orders path is not a directory: ${ordersPath}`);
}

const credentialsPath = join(credentialsRoot, "credentials.json");
if (!existsSync(credentialsPath)) {
  failed = true;
  console.error(`missing credentials path: ${credentialsPath}`);
} else {
  console.log(`ok credentials path: ${credentialsPath}`);
}

if (failed) {
  process.exit(1);
}
