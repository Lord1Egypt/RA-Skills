/**
 * Run a Komodo resource and wait for completion.
 *
 * Usage:
 *   bun run scripts/run.ts <type> <name>
 *
 * Types:
 *   procedure | action | build
 *
 * Examples:
 *   bun run scripts/run.ts procedure my-proc
 *   bun run scripts/run.ts action my-action
 *   bun run scripts/run.ts build my-build
 */
import { komodo } from "../openclaw.ts";
import { printUpdate } from "./print-update.ts";

const TYPES = ["procedure", "action", "build"] as const;
type RunType = (typeof TYPES)[number];

const [type, name] = process.argv.slice(2);

if (!type || !name || !TYPES.includes(type as RunType)) {
  console.error("Usage: bun run scripts/run.ts <type> <name>");
  console.error("Types:", TYPES.join(" | "));
  process.exit(1);
}

console.log(`Running ${type} "${name}"...`);

let result;
switch (type as RunType) {
  case "procedure":
    result = await komodo.execute_and_poll("RunProcedure", { procedure: name });
    break;
  case "action":
    result = await komodo.execute_and_poll("RunAction", { action: name });
    break;
  case "build":
    result = await komodo.execute_and_poll("RunBuild", { build: name });
    break;
}

printUpdate(result);
