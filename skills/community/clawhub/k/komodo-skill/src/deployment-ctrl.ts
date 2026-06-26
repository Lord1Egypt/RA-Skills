/**
 * Control a deployment: deploy, start, stop, restart, pull, or destroy.
 * Usage: bun run scripts/deployment-ctrl.ts <action> <deployment-name>
 * Actions: deploy | start | stop | restart | pull | destroy
 */
import { komodo } from "../openclaw.ts";
import { printUpdate } from "./print-update.ts";

const ACTIONS = {
  deploy:  "Deploy",
  start:   "StartDeployment",
  stop:    "StopDeployment",
  restart: "RestartDeployment",
  pull:    "PullDeployment",
  destroy: "DestroyDeployment",
} as const;

type DeploymentAction = keyof typeof ACTIONS;

const [action, deployment] = process.argv.slice(2);

if (!action || !deployment || !(action in ACTIONS)) {
  console.error("Usage: bun run scripts/deployment-ctrl.ts <action> <deployment-name>");
  console.error("Actions:", Object.keys(ACTIONS).join(" | "));
  process.exit(1);
}

const op = ACTIONS[action as DeploymentAction];
console.log(`${action} "${deployment}"...`);
const result = await komodo.execute_and_poll(op, { deployment });
printUpdate(result);
