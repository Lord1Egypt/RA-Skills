/**
 * Update the config of a Komodo resource by merging a partial JSON patch.
 * Only the fields you provide are changed — everything else stays as-is.
 *
 * Usage:
 *   bun run scripts/update.ts <type> <name> '<json>'
 *
 * Types:
 *   stack | deployment | build | repo | procedure | action
 *
 * Examples:
 *   bun run scripts/update.ts stack my-stack '{"branch":"main"}'
 *   bun run scripts/update.ts build my-build '{"version":{"major":2,"minor":0,"patch":0}}'
 *   bun run scripts/update.ts deployment my-dep '{"image":"nginx:1.27"}'
 *   bun run scripts/update.ts repo my-repo '{"branch":"develop"}'
 *   bun run scripts/update.ts procedure my-proc '{"description":"updated desc"}'
 *   bun run scripts/update.ts action my-action '{"schedule":"0 0 * * *","schedule_enabled":true}'
 */
import { komodo } from "../openclaw.ts";

const TYPES = ["stack", "deployment", "build", "repo", "procedure", "action"] as const;
type ResourceType = (typeof TYPES)[number];

const [type, name, jsonPatch] = process.argv.slice(2);

if (!type || !name || !jsonPatch || !TYPES.includes(type as ResourceType)) {
  console.error("Usage: bun run scripts/update.ts <type> <name> '<json>'");
  console.error("Types:", TYPES.join(" | "));
  process.exit(1);
}

let config: Record<string, unknown>;
try {
  config = JSON.parse(jsonPatch);
} catch {
  console.error("Invalid JSON patch:", jsonPatch);
  process.exit(1);
}

const resourceType = type as ResourceType;

// Resolve name → id, then apply patch
async function resolveId(): Promise<string> {
  switch (resourceType) {
    case "stack": {
      const r = await komodo.read("GetStack", { stack: name });
      return r._id!.$oid;
    }
    case "deployment": {
      const r = await komodo.read("GetDeployment", { deployment: name });
      return r._id!.$oid;
    }
    case "build": {
      const r = await komodo.read("GetBuild", { build: name });
      return r._id!.$oid;
    }
    case "repo": {
      const r = await komodo.read("GetRepo", { repo: name });
      return r._id!.$oid;
    }
    case "procedure": {
      const r = await komodo.read("GetProcedure", { procedure: name });
      return r._id!.$oid;
    }
    case "action": {
      const r = await komodo.read("GetAction", { action: name });
      return r._id!.$oid;
    }
  }
}

const id = await resolveId();
console.log(`Updating ${type} "${name}" (${id})...`);
console.log("Patch:", JSON.stringify(config, null, 2));

switch (resourceType) {
  case "stack":
    await komodo.write("UpdateStack", { id, config });
    break;
  case "deployment":
    await komodo.write("UpdateDeployment", { id, config });
    break;
  case "build":
    await komodo.write("UpdateBuild", { id, config });
    break;
  case "repo":
    await komodo.write("UpdateRepo", { id, config });
    break;
  case "procedure":
    await komodo.write("UpdateProcedure", { id, config });
    break;
  case "action":
    await komodo.write("UpdateAction", { id, config });
    break;
}

console.log(`Done.`);
