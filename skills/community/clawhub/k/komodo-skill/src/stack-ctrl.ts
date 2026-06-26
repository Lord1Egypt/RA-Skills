/**
 * Control a stack: start, stop, restart, pull, or destroy.
 * Usage: bun run scripts/stack-ctrl.ts <action> <stack-name>
 * Actions: start | stop | restart | pull | destroy
 */
import { komodo } from "../openclaw.ts";
import { printUpdate } from "./print-update.ts";

const ACTIONS = {
  start:   "StartStack",
  stop:    "StopStack",
  restart: "RestartStack",
  pull:    "PullStack",
  destroy: "DestroyStack",
} as const;

type StackAction = keyof typeof ACTIONS;

const [action, stack] = process.argv.slice(2);

if (!action || !stack || !(action in ACTIONS)) {
  console.error("Usage: bun run scripts/stack-ctrl.ts <action> <stack-name>");
  console.error("Actions:", Object.keys(ACTIONS).join(" | "));
  process.exit(1);
}

const op = ACTIONS[action as StackAction];
console.log(`${action} "${stack}"...`);
const result = await komodo.execute_and_poll(op, { stack });
printUpdate(result);
