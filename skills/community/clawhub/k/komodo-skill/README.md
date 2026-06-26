# komo.do

A scripting toolkit for managing [Komodo](https://komo.do) infrastructure — list, inspect, create, update, deploy, and control resources via the Komodo Core API.

## Setup

### Option A — openclaw skill environment

If you are using this project as an openclaw skill, create or edit `openclaw.json` and add the credentials under `skills.entries.komodo-skill.env`:

```json
{
  "skills": {
    "entries": {
      "komodo-skill": {
        "enabled": true,
        "env": {
          "KOMODO_URL": "https://your-komodo-instance.com",
          "KOMODO_API_KEY": "your-api-key",
          "KOMODO_API_SECRET": "your-api-secret"
        }
      }
    }
  }
}
```

### Option B — environment variables

Set the variables before running any script:

```bash
export KOMODO_URL=https://your-komodo-instance.com
export KOMODO_API_KEY=your-api-key
export KOMODO_API_SECRET=your-api-secret
```

Or place them in a `.env` file.

## Running Scripts

Each script has two forms — pick whichever fits your environment:

```bash
# Compiled JS — no extra tooling required
node scripts/<script>.js [args]

# TypeScript source — requires Bun
bun run scripts/<script>.ts [args]
```

---

## Features

### List resources

Inspect all resources of a given type with detailed, human-readable output.

```bash
node scripts/list.js <type>
```

| Type | What you see |
|---|---|
| `servers` | State, address, region, periphery version, CPU %, memory, disk usage, load average |
| `stacks` | State, docker status, services & images, repo/branch, deployed vs latest commit |
| `deployments` | State, docker status, image, update availability, attached build |
| `builds` | State, version, last built timestamp, repo/branch, built vs latest commit |
| `repos` | State, last pulled/built timestamps, repo/branch, cloned/built/latest commit |
| `procedures` | State, stage count, last run, next scheduled run |
| `actions` | State, last run, next scheduled run |

---

### Create a resource

Create a new resource with an optional initial configuration. Unspecified fields use Komodo defaults.

```bash
node scripts/create.js <type> <name> [json-config]
```

```bash
node scripts/create.js stack my-stack
node scripts/create.js stack my-stack '{"repo":"org/repo","branch":"main"}'
node scripts/create.js deployment my-dep '{"image":"nginx:latest","server_id":"<id>"}'
node scripts/create.js build my-build '{"repo":"org/repo","branch":"main"}'
node scripts/create.js repo my-repo '{"repo":"org/repo","branch":"main","server_id":"<id>"}'
node scripts/create.js procedure my-proc
node scripts/create.js action my-action '{"run_at_startup":false}'
```

Supported types: `stack` `deployment` `build` `repo` `procedure` `action`

---

### Update resource config

Apply a partial JSON patch to any resource — only the fields you specify are changed, everything else stays as-is.

```bash
node scripts/update.js <type> <name> '<json>'
```

```bash
node scripts/update.js stack my-stack '{"branch":"main"}'
node scripts/update.js build my-build '{"version":{"major":2,"minor":0,"patch":0}}'
node scripts/update.js deployment my-dep '{"image":"nginx:1.27"}'
node scripts/update.js repo my-repo '{"branch":"develop"}'
node scripts/update.js procedure my-proc '{"schedule":"0 0 * * *","schedule_enabled":true}'
node scripts/update.js action my-action '{"run_at_startup":false}'
```

Supported types: `stack` `deployment` `build` `repo` `procedure` `action`

---

### Run a resource

Execute a procedure, action, or build and wait for it to finish. Prints the full result, duration, and logs.

```bash
node scripts/run.js <type> <name>
```

```bash
node scripts/run.js procedure my-proc
node scripts/run.js action my-action
node scripts/run.js build my-build
```

---

### Deploy a stack

Deploy a stack and wait for completion. Prints the update result and logs.

```bash
node scripts/deploy-stack.js <stack-name>
```

---

### Control a stack

```bash
node scripts/stack-ctrl.js <action> <stack-name>
```

Actions: `start` `stop` `restart` `pull` `destroy`

---

### Control a deployment

```bash
node scripts/deployment-ctrl.js <action> <deployment-name>
```

Actions: `deploy` `start` `stop` `restart` `pull` `destroy`

---

### Fetch logs

Stream logs from a stack, deployment, or container.

```bash
node scripts/get-logs.js stack <stack-name> [lines]
node scripts/get-logs.js deployment <deployment-name> [lines]
node scripts/get-logs.js container <server-name> <container-name> [lines]
```
