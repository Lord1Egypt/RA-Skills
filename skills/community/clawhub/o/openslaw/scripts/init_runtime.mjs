import { mkdirSync, existsSync, readFileSync, writeFileSync, copyFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { homedir } from "node:os";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(scriptDir, "..");
const templatesRoot = join(skillRoot, "assets", "runtime_templates");

function argValue(flag, fallback) {
  const index = process.argv.indexOf(flag);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

function ensureDir(path) {
  mkdirSync(path, { recursive: true });
}

function writeIfMissing(path, content) {
  if (!existsSync(path)) {
    writeFileSync(path, content, "utf8");
    console.log(`created ${path}`);
    return;
  }

  console.log(`kept ${path}`);
}

function copyTemplateIfMissing(templateName, targetPath) {
  if (!existsSync(targetPath)) {
    copyFileSync(join(templatesRoot, templateName), targetPath);
    console.log(`created ${targetPath}`);
    return;
  }

  console.log(`kept ${targetPath}`);
}

const projectRoot = resolve(argValue("--project-root", process.cwd()));
const credentialsRoot = resolve(argValue("--credentials-root", join(homedir(), ".config", "openslaw")));
const memoryDir = join(projectRoot, "memory");
const stateDir = join(projectRoot, ".openslaw");
const ordersDir = join(stateDir, "orders");
const credentialsPath = join(credentialsRoot, "credentials.json");

ensureDir(memoryDir);
ensureDir(stateDir);
ensureDir(ordersDir);
ensureDir(credentialsRoot);

writeIfMissing(
  join(memoryDir, "openslaw-profile.md"),
  "# OpenSlaw Profile\n\n- agent_id:\n- owner_email:\n- status:\n- runtime_kind:\n- last_status_checked_at:\n"
);
writeIfMissing(
  join(memoryDir, "openslaw-market-journal.md"),
  "# OpenSlaw Market Journal\n\n## Search Notes\n\n## Quote Notes\n\n## Purchase Authorization Notes\n\n## Context Harness Notes\n\n## Provider Comparisons\n\n## Automation And Notification Notes\n"
);
writeIfMissing(
  join(memoryDir, "openslaw-workboard.md"),
  "# OpenSlaw Workboard\n\n## Pending Purchase Confirmations\n\n## Pending Context Confirmations\n\n## Pending Automation Authorizations\n\n## Pending Notification Changes\n\n## Active Orders\n\n## Pending Reviews\n"
);

copyTemplateIfMissing("authorization_profile.template.json", join(stateDir, "authorization_profile.json"));
copyTemplateIfMissing("user_context.template.json", join(stateDir, "user_context.json"));
copyTemplateIfMissing("preferences.template.json", join(stateDir, "preferences.json"));
copyTemplateIfMissing("runtime_state.template.json", join(stateDir, "runtime_state.json"));
copyTemplateIfMissing("activity_log.template.jsonl", join(stateDir, "activity_log.jsonl"));
copyTemplateIfMissing("credentials_ref.template.json", join(stateDir, "credentials_ref.json"));

if (!existsSync(credentialsPath)) {
  writeFileSync(
    credentialsPath,
    JSON.stringify(
      {
        api_key: null,
        agent_id: null,
        updated_at: null
      },
      null,
      2
    ) + "\n",
    "utf8"
  );
  console.log(`created ${credentialsPath}`);
} else {
  console.log(`kept ${credentialsPath}`);
}

const refPath = join(stateDir, "credentials_ref.json");
const refPayload = JSON.parse(readFileSync(refPath, "utf8"));

if (refPayload.path !== "~/.config/openslaw/credentials.json") {
  refPayload.path = credentialsPath;
  writeFileSync(refPath, JSON.stringify(refPayload, null, 2) + "\n", "utf8");
  console.log(`updated ${refPath}`);
}
