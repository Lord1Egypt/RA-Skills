---
name: komodo-skill
description: "Interact with Komodo Core API using this project. Use when the user wants to list, manage, deploy, or execute operations against Komodo resources (servers, stacks, deployments, builds, repos, procedures, variables, alerts, etc.)."
argument-hint: "[what to do with Komodo]"
---

You are an expert at managing Komodo infrastructure using this project.
The `openclaw.ts` module exports a pre-configured `komodo` client authenticated via API key and secret from environment variables. All scripts in `scripts/` import from it.

## Environment Variables

| Variable            | Description                                          |
|---------------------|------------------------------------------------------|
| `KOMODO_URL`        | Base URL of Komodo Core (e.g. `https://komodo.example.com`) |
| `KOMODO_API_KEY`    | API key                                              |
| `KOMODO_API_SECRET` | API secret                                           |

## Available Scripts

Every script can be run two ways — pick whichever fits the environment:

```bash
node scripts/<script>.js [args]        # compiled JS, no tooling needed
bun run scripts/<script>.ts [args]     # TypeScript source, requires Bun
```

---

### `list` — Inspect resources

```bash
node scripts/list.js <type>
```

| Type | Output |
|---|---|
| `servers` | State, address, region, periphery version, CPU, memory, disk, load average |
| `stacks` | State, services & images, repo/branch, deployed vs latest commit |
| `deployments` | State, image, update availability, attached build |
| `builds` | State, version, last built, repo/branch, built vs latest commit |
| `repos` | State, last pulled/built, repo/branch, cloned/built/latest commit |
| `procedures` | State, stage count, last run, next scheduled run |
| `actions` | State, last run, next scheduled run |

---

### `create` — Create a resource

```bash
node scripts/create.js <type> <name> [json-config]
```

Config is optional — omit to use Komodo defaults.

```bash
node scripts/create.js stack my-stack '{"repo":"org/repo","branch":"main"}'
node scripts/create.js deployment my-dep '{"image":"nginx:latest","server_id":"<id>"}'
node scripts/create.js build my-build '{"repo":"org/repo","branch":"main"}'
node scripts/create.js repo my-repo '{"repo":"org/repo","branch":"main","server_id":"<id>"}'
node scripts/create.js procedure my-proc
node scripts/create.js action my-action '{"run_at_startup":false}'
```

Types: `stack` `deployment` `build` `repo` `procedure` `action`

---

### `update` — Patch resource config

Applies a partial JSON merge — only specified fields change, everything else stays.

```bash
node scripts/update.js <type> <name> '<json>'
```

```bash
node scripts/update.js stack my-stack '{"branch":"main"}'
node scripts/update.js deployment my-dep '{"image":"nginx:1.27"}'
node scripts/update.js build my-build '{"version":{"major":2,"minor":0,"patch":0}}'
node scripts/update.js repo my-repo '{"branch":"develop"}'
node scripts/update.js procedure my-proc '{"schedule":"0 0 * * *","schedule_enabled":true}'
node scripts/update.js action my-action '{"run_at_startup":false}'
```

Types: `stack` `deployment` `build` `repo` `procedure` `action`

---

### `run` — Execute and wait for completion

Runs a procedure, action, or build and blocks until done. Prints update ID, status, duration, and logs.

```bash
node scripts/run.js <type> <name>
```

```bash
node scripts/run.js procedure my-proc
node scripts/run.js action my-action
node scripts/run.js build my-build
```

---

### `deploy-stack` — Deploy a stack

Deploys a stack and waits for completion. Prints the full update result and logs.

```bash
node scripts/deploy-stack.js <stack-name>
```

---

### `stack-ctrl` — Control a stack

```bash
node scripts/stack-ctrl.js <action> <stack-name>
```

Actions: `start` `stop` `restart` `pull` `destroy`

---

### `deployment-ctrl` — Control a deployment

```bash
node scripts/deployment-ctrl.js <action> <deployment-name>
```

Actions: `deploy` `start` `stop` `restart` `pull` `destroy`

---

### `get-logs` — Fetch logs

```bash
node scripts/get-logs.js stack <stack-name> [tail]
node scripts/get-logs.js deployment <deployment-name> [tail]
node scripts/get-logs.js container <server-name> <container-name> [tail]
```

---

## Writing New Scripts

When adding a new script, follow this pattern:

```typescript
import { komodo } from "../openclaw.ts";
import { printUpdate } from "./print-update.ts"; // for execute_and_poll results

// Read
const items = await komodo.read("ListStacks", {});

// Write (create/update/delete)
await komodo.write("CreateVariable", { name: "KEY", value: "val" });

// Execute and wait for completion
const result = await komodo.execute_and_poll("DeployStack", { stack: "name" });
printUpdate(result);
```

Key rules:
- Always import `komodo` from `"../openclaw.ts"` — never initialize the client directly
- Always use `execute_and_poll` (not `execute`) when waiting for a task to finish
- Use `printUpdate(result)` from `./print-update.ts` to display execution results
- Read args from `process.argv` — never hardcode resource names or credentials
- After writing a new `.ts` script, rebuild with `bun run build` to produce the `.js` counterpart

## Instructions

When the user provides a request via `$ARGUMENTS`:

1. Identify the resource type and operation needed.
2. **Use an existing script first** — check the list above before writing new code.
3. If adapting an existing script, show the exact command to run.
4. If writing a new script, place it in `scripts/`, follow the pattern above, and remind the user to rebuild.
5. Always show both run options: `node scripts/<script>.js` and `bun run scripts/<script>.ts`.
6. For execution results (deploy, run, ctrl), the output always includes: update ID, status, success, duration, operator, and per-stage logs.

The user's request: $ARGUMENTS
