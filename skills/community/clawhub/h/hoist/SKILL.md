---
name: hoist
description: Deploy and manage apps, servers, databases, domains, and environment variables on VPS providers using the Hoist CLI.
homepage: https://github.com/g4f4r0/hoist
metadata: {"openclaw":{"skillKey":"hoist","homepage":"https://github.com/g4f4r0/hoist","requires":{"bins":["hoist"]},"install":[{"id":"node","kind":"node","package":"hoist-cli","bins":["hoist"],"label":"Install Hoist CLI (npm)"}]}}
---

# Hoist CLI

Hoist is an AI-native CLI built specifically for AI agents. When called from an agent (non-TTY), it automatically outputs structured JSON and skips interactive prompts. Just run commands directly.

## How You Should Behave

You are the user's infrastructure guide. Be thorough and transparent:

- Always explain what you are about to do before doing it. Tell the user which commands you will run, what resources will be created, and what the estimated cost is.
- Ask for confirmation before any action that creates, modifies, or destroys resources. This includes creating servers, deploying apps, adding databases, deleting domains, rotating keys, and setting env vars.
- Never assume critical deployment inputs. If the user says "deploy this", ask which server, which service, and which port unless `hoist.json` already resolves them clearly.
- Present options clearly. When there are choices like region, server type, or database version, list them with context like price, location, and specs so the user can make an informed decision.
- After every action, verify it worked. Run `hoist status` and report the result.
- If something fails, investigate before retrying. Follow the troubleshooting workflow below.

## Smart Defaults

Hoist auto-detects and fills in sensible defaults when called from an agent:
- Deploys all app services if `--service` is omitted
- Auto-resolves `--server` from the service config in hoist.json
- Generates random server names if `--name` is omitted
- Uses cheapest server type and first region as defaults

Even though defaults exist, always present the plan to the user and get confirmation before executing.

## When to Use

- "Deploy this app" -> `hoist deploy`
- "Create a server" -> `hoist server create`
- "Set up Postgres" -> `hoist deploy --template postgres --server <s>`
- "Add a domain" -> `hoist domain add example.com`
- "What's running?" -> `hoist status`
- "Something is broken" -> `hoist logs <service>`, then `hoist logs traefik`, then `hoist doctor`
- "Check everything" -> `hoist doctor`

## When NOT to Use

- Provider setup without env vars. `hoist init` and `hoist provider add` need `HOIST_*_API_KEY` env vars or an interactive human terminal.
- General coding. Hoist is for infrastructure only.

---

## Decision Tree

```
Is hoist installed? (`which hoist`)
+-- NO -> Run: `npm install -g hoist-cli`
+-- YES -> Is hoist configured? (`hoist provider list`)
    +-- NO -> Are HOIST_*_API_KEY env vars set?
        +-- YES -> Run: `hoist init`
        +-- NO -> Tell user to run: `hoist init`
    +-- YES -> Does hoist.json exist?
        +-- NO -> Create hoist.json after asking about project name and services
        +-- YES -> What does the user want?
            +-- New server -> `hoist server create`
            +-- Import server -> `hoist server import --ip <ip>`
            +-- Deploy app -> `hoist deploy`
            +-- Add database -> `hoist deploy --template postgres --server <s>`
            +-- Add domain -> `hoist domain add <domain>`
            +-- Set env vars -> `hoist env set <service> KEY=VAL`
            +-- Check status -> `hoist status`
            +-- Something broken -> `hoist logs <service>` + `hoist doctor`
```

---

## Sensitive Operations - Human in the Loop

| Command | Behavior |
|---------|----------|
| `hoist init` | If `HOIST_*_API_KEY` env vars are set, auto-configures. Otherwise prompts interactively, so tell the user to run it. |
| `hoist provider add` | Requires `--type` and reads the API key from a `HOIST_*_API_KEY` env var. If the env var is missing, tell the user to set it first. |
| `hoist keys rotate` | Rotates SSH keys on all servers. Always confirm first. |
| `hoist server destroy` | Destroys a server permanently. Always confirm first. |
| `hoist template destroy` | Destroys a database and its data. Always confirm first. |
| `hoist domain delete` | Removes a domain and SSL config. Always confirm first. |

Environment variables: `HOIST_HETZNER_API_KEY`, `HOIST_VULTR_API_KEY`, `HOIST_DIGITALOCEAN_API_KEY`, `HOIST_HOSTINGER_API_KEY`, `HOIST_LINODE_API_KEY`, `HOIST_SCALEWAY_API_KEY`

---

## Commands

For full command reference, see [COMMANDS.md](COMMANDS.md).

- Providers: `provider add`, `provider list`, `provider test`, `provider update`, `provider set-default`, `provider delete`
- Servers: `server create`, `server import`, `server list`, `server status <name>`, `server ssh <name>`, `server destroy <name>`, `server regions`, `server types`, `server stats <name>`
- Deploy: `deploy`, `deploy --service <name>`, `deploy --template <type> --server <s>`, `deploy --repo <url> --branch <branch>`, `rollback --service <name>`
- Templates: `template list`, `template info <name>`, `template services`, `template inspect <name>`, `template backup <name>`, `template destroy <name>`, `template stop/start/restart <name>`, `template public <name>`, `template private <name>`
- Domains: `domain add <domain>`, `domain add <domain> --service <name>`, `domain list`, `domain delete <domain>`
- Env vars: `env set <service> KEY=VAL`, `env get <service> <key>`, `env list <service>`, `env delete <service> <key>`, `env import <service> <file>`, `env export <service>`, `echo KEY=VAL | env set <service> --stdin`
- Observability: `logs <service>`, `logs traefik`, `logs <service> --follow`, `status`, `doctor`
- Skills: `skills sync`, `skills export [dir]`
- Other: `keys show`, `keys rotate`, `config validate`, `--status`

---

## Project Config

Read `hoist.json` in the project root for current project context.

```json
{
  "project": "my-app",
  "servers": { "prod": { "provider": "hetzner-1" } },
  "services": {
    "api": { "server": "prod", "type": "app", "source": ".", "port": 3000 }
  }
}
```

---

## Deployment Procedure

Walk the user through each step. Ask for confirmation before proceeding:

1. Server - Which server? If none exist, ask the user which provider, region, type, and name they want. Present available options with pricing.
2. Service - App or database? If no Dockerfile exists, generate one using [DOCKERFILES.md](DOCKERFILES.md) and show it to the user before deploying.
3. Domain - Ask whether they want a custom domain. User must point both `example.com` and `www.example.com` to the server IP.
4. Env vars - Ask about `DATABASE_URL`, API keys, and other runtime config. If a database was just created, suggest the connection URL.
5. Confirm - Summarize the server, service, domain, env vars, and estimated cost, then ask for final approval.

---

## After Deploying

1. `hoist status` - verify services are running and check for drift
2. `hoist logs <service>` - verify the app started correctly
3. `hoist domain add <domain>` - add the custom domain and SSL if requested

## After Adding a Database

1. `hoist template inspect <name>` - get credentials and the connection string
2. `hoist env set <app> DATABASE_URL=<connection-string>` - inject it into the app
3. `hoist template public <name> --server <s>` - only if the user explicitly needs public access
4. Tell the user the database is ready and whether the app was restarted with the new connection string.

---

## Troubleshooting Workflow

When something goes wrong, use these tools to investigate:

### 1. Check app logs

```bash
hoist logs <service> --lines 200
```

Look for crash loops, startup errors, missing env vars, database failures, and wrong ports.

### 2. Check proxy logs

```bash
hoist logs traefik --lines 200
```

Look for 502 errors, ACME cert failures, and TLS issues.

### 3. Check infrastructure

```bash
hoist doctor
```

Checks SSH connectivity, Docker, Traefik, firewall state, and provider auth.

### 4. Check project state

```bash
hoist status
```

Shows which services are running versus configured, along with drift and resource status.

### Common Issues and Fixes

| Symptom | How to investigate | Fix |
|---------|-------------------|-----|
| 502 Bad Gateway | `hoist logs <service>` then `hoist logs traefik` | Fix the app crash or port mismatch, then redeploy. |
| Site not loading | `hoist status` | Redeploy the service with `hoist deploy --service <name>`. |
| SSL cert invalid | `hoist logs traefik` | Verify DNS points to the server IP and wait for the next ACME retry. |
| DNS not resolving | `hoist domain list` | User must add or fix the DNS A record. |
| Wrong response | `hoist logs <service>` | Fix the app and redeploy. |
| Database unreachable | `hoist template inspect <name>` | Start the template service or fix the connection string. |

### When to Rollback

Only rollback when a deploy introduced a regression and the previous version was working.

```bash
hoist rollback --service <name>
```

Always confirm first and verify with `hoist status` after the rollback.

---

## Error Reference

| Error | Solution |
|-------|----------|
| `Run hoist init first` | If env vars are set, run `hoist init`. Otherwise tell the user to run it interactively. |
| `Provider not found` | Check `hoist provider list` for the correct label. |
| `Server not found` | Check `hoist server list`. |
| `SSH connection failed` | Run `hoist doctor` and verify the server IP. |
| `No hoist.json found` | Create `hoist.json` in the project root. |
| `references unknown server` | Make the service `server` value match the `servers` section. |
| `Re-run with --confirm` | Destructive action. The error includes the exact command to re-run. |
| `Multiple app services found` | Specify `--service <name>`. |

---

## Golden Rules

1. Explain first, act second. Always tell the user what you plan to do and get confirmation before running commands that create, modify, or destroy resources.
2. Just run commands. JSON output and confirmations are handled automatically. Do not add extra machine flags.
3. Parse stdout for JSON and check the exit code.
4. Never handle API keys directly. Use env vars or tell the user to run setup commands.
5. Investigate failures instead of retrying blindly. Use `hoist logs <service>`, `hoist logs traefik`, `hoist doctor`, and `hoist status`.
6. After every action, verify it worked and report the result.
7. Server names in `hoist.json` must match the names used during creation.
