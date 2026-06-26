/**
 * Fetch logs from a stack, deployment, or container.
 * Usage:
 *   bun run scripts/get-logs.ts stack <stack-name> [tail]
 *   bun run scripts/get-logs.ts deployment <deployment-name> [tail]
 *   bun run scripts/get-logs.ts container <server-name> <container-name> [tail]
 */
import { komodo } from "../openclaw.ts";

const [type, ...rest] = process.argv.slice(2);

if (!type || !rest[0]) {
  console.error("Usage:");
  console.error("  bun run scripts/get-logs.ts stack <stack-name> [tail]");
  console.error("  bun run scripts/get-logs.ts deployment <deployment-name> [tail]");
  console.error("  bun run scripts/get-logs.ts container <server-name> <container-name> [tail]");
  process.exit(1);
}

if (type === "stack") {
  const [name, tailStr] = rest;
  const tail = tailStr ? Number(tailStr) : 100;
  const log = await komodo.read("GetStackLog", { stack: name!, tail });
  if (log.stdout) process.stdout.write(log.stdout);
  if (log.stderr) process.stderr.write(log.stderr);
} else if (type === "deployment") {
  const [name, tailStr] = rest;
  const tail = tailStr ? Number(tailStr) : 100;
  const log = await komodo.read("GetDeploymentLog", { deployment: name!, tail });
  if (log.stdout) process.stdout.write(log.stdout);
  if (log.stderr) process.stderr.write(log.stderr);
} else if (type === "container") {
  const [server, container, tailStr] = rest;
  if (!server || !container) {
    console.error("container requires <server-name> and <container-name>");
    process.exit(1);
  }
  const tail = tailStr ? Number(tailStr) : 100;
  const log = await komodo.read("GetContainerLog", { server, container, tail });
  if (log.stdout) process.stdout.write(log.stdout);
  if (log.stderr) process.stderr.write(log.stderr);
} else {
  console.error(`Unknown type "${type}". Use: stack | deployment | container`);
  process.exit(1);
}
