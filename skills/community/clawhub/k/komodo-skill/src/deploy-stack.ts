/**
 * Deploy a stack and wait for completion.
 * Usage: bun run scripts/deploy-stack.ts <stack-name>
 */
import { komodo } from "../openclaw.ts";
import { printUpdate } from "./print-update.ts";

const stack = process.argv[2];
if (!stack) {
  console.error("Usage: bun run scripts/deploy-stack.ts <stack-name>");
  process.exit(1);
}

console.log(`Deploying stack "${stack}"...`);
const result = await komodo.execute_and_poll("DeployStack", { stack });
printUpdate(result);
