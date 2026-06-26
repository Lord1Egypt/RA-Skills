/**
 * Create a new Komodo resource with an optional initial config.
 * Config fields not provided will use Komodo defaults.
 *
 * Usage:
 *   bun run scripts/create.ts <type> <name> [json]
 *
 * Types:
 *   stack | deployment | build | repo | procedure | action
 *
 * Examples:
 *   bun run scripts/create.ts stack my-stack
 *   bun run scripts/create.ts stack my-stack '{"repo":"org/repo","branch":"main"}'
 *   bun run scripts/create.ts build my-build '{"repo":"org/repo","branch":"main"}'
 *   bun run scripts/create.ts deployment my-dep '{"image":"nginx:latest","server_id":"<id>"}'
 *   bun run scripts/create.ts repo my-repo '{"repo":"org/repo","branch":"main","server_id":"<id>"}'
 *   bun run scripts/create.ts procedure my-proc '{}'
 *   bun run scripts/create.ts action my-action '{"run_at_startup":false}'
 */
import { komodo } from "../openclaw.ts";

const TYPES = ["stack", "deployment", "build", "repo", "procedure", "action"] as const;
type ResourceType = (typeof TYPES)[number];

const [type, name, jsonConfig] = process.argv.slice(2);

if (!type || !name || !TYPES.includes(type as ResourceType)) {
  console.error("Usage: bun run scripts/create.ts <type> <name> [json]");
  console.error("Types:", TYPES.join(" | "));
  process.exit(1);
}

let config: Record<string, unknown> | undefined;
if (jsonConfig) {
  try {
    config = JSON.parse(jsonConfig);
  } catch {
    console.error("Invalid JSON config:", jsonConfig);
    process.exit(1);
  }
}

const resourceType = type as ResourceType;

console.log(`Creating ${type} "${name}"...`);
if (config) console.log("Config:", JSON.stringify(config, null, 2));

let result: { name: string; _id?: { $oid: string } };

switch (resourceType) {
  case "stack":
    result = await komodo.write("CreateStack", { name, config });
    break;
  case "deployment":
    result = await komodo.write("CreateDeployment", { name, config });
    break;
  case "build":
    result = await komodo.write("CreateBuild", { name, config });
    break;
  case "repo":
    result = await komodo.write("CreateRepo", { name, config });
    break;
  case "procedure":
    result = await komodo.write("CreateProcedure", { name, config });
    break;
  case "action":
    result = await komodo.write("CreateAction", { name, config });
    break;
}

console.log(`\nCreated ${type}:`);
console.log(`  Name : ${result.name}`);
console.log(`  ID   : ${result._id?.$oid ?? "—"}`);
