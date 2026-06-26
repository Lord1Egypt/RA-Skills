---
name: ink
description: >
  Deploy and manage cloud services on Ink (ml.ink): create projects, deploy
  services, provision databases, manage DNS and custom domains, configure
  workspaces, and monitor deployments. Use this skill whenever the user mentions
  Ink, ml.ink, deployments, services, databases, or cloud infrastructure on Ink,
  even if they don't say "Ink" explicitly.
allowed-tools: Bash(ink:*), Bash(which:*), Bash(command:*), Bash(npm:*), Bash(npx:*), Bash(brew:*), Bash(git:*), Write
---

# Use Ink

[Ink](https://ml.ink) is a cloud platform designed for AI agents to deploy and manage services autonomously. It makes deployments simple enough that fully autonomous agents can handle the entire lifecycle: create, deploy, monitor, and scale services without human intervention.

## Preflight

Before any operation, verify the CLI is installed and authenticated:

```bash
command -v ink                    # CLI installed
ink whoami                        # authenticated
```

If the CLI is missing, install it:

```bash
npm install -g @mldotink/cli      # npm (macOS, Linux, Windows)
brew install mldotink/tap/ink     # Homebrew (macOS)
```

If not authenticated, run `ink login`.

## Configuration

Ink CLI resolves context in this order (highest priority first):

1. **CLI flags** -- `--api-key`, `--workspace`, `--project`
2. **Environment** -- `INK_API_KEY`
3. **Local config** -- `.ink` file in current directory
4. **Global config** -- `~/.config/ink/config`

Use `ink whoami` to check current auth. Use `--json` on any command for machine-readable output.

## Git: Two Options

Ink supports two git providers. Use `ink whoami` to see which are available.

### Option 1: Ink Internal Git (default)

Zero-setup, works for everyone. No GitHub account needed.

```bash
ink repos create my-app           # creates repo, shows git remote URL
git remote add ink <url>          # add the remote
git push ink main                 # push code -- auto-triggers deployment
```

### Option 2: GitHub

Requires GitHub OAuth and GitHub App connected at https://ml.ink (Settings > GitHub).

```bash
ink deploy my-app --repo username/repo-name --host github --port 3000
```

### Auto-Redeploy

Both git providers trigger automatic redeployment on push. After pushing code, just poll `ink status <name>` to track progress -- you do not need to redeploy manually.

## Secrets & Environment Variables

Use `ink secrets` to manage env vars on running services. Changes are merged server-side and trigger an automatic redeploy.

**For sensitive values** (API keys, tokens, credentials), use `ink secrets import` to avoid leaking to shell history:

```bash
# From file
ink secrets import my-app --file .env

# From stdin (preferred for agents)
cat > .env.secrets <<EOF
DATABASE_URL=libsql://my-db-myworkspace.turso.io
DATABASE_AUTH_TOKEN=eyJhbG...
API_KEY=sk_live_xxx
EOF
ink secrets import my-app --file .env.secrets
rm .env.secrets
```

**For non-sensitive values**, `ink secrets set` is fine:

```bash
ink secrets set my-app NODE_ENV=production LOG_LEVEL=info
```

**Other operations:**

```bash
ink secrets list my-app                          # list current vars
ink secrets unset my-app OLD_KEY                 # remove a single var
ink secrets delete my-app KEY1 KEY2              # remove multiple vars
ink secrets import my-app --file .env --replace  # replace ALL vars (removes unspecified)
```

For initial deploy, use `--env-file` to pass secrets:

```bash
ink deploy my-app --repo my-app --port 3000 --env-file .env
```

Use `--env` only for non-sensitive values like `NODE_ENV=production`.

## Common Operations

```bash
ink services                                      # list all services
ink status my-app                                 # service details
ink logs my-app                                   # tail logs
ink deploy my-app --repo my-app --port 3000       # deploy new service
ink redeploy my-app                               # redeploy existing
ink redeploy my-app --memory 1Gi --vcpu 1         # redeploy with new config
ink delete my-app                                 # delete service

ink db create my-db                               # create database
ink db list                                       # list databases
ink db token my-db                                # get connection credentials
ink db delete my-db                               # delete database

ink secrets set my-app KEY=value                  # set env vars (merges)
ink secrets import my-app --file .env             # import from file
ink secrets list my-app                           # list env vars
ink secrets unset my-app KEY                      # remove env var
ink secrets delete my-app KEY1 KEY2               # remove multiple

ink domains add my-app app.example.com            # add custom domain
ink domains remove my-app app.example.com         # remove custom domain

ink dns zones                                     # list DNS zones
ink dns records example.com                       # list records
ink dns add example.com --name sub --type A --content 1.2.3.4
ink dns delete example.com <record-id>

ink repos create my-app                           # create internal git repo
ink repos token my-app                            # get push token

ink projects list                                 # list projects
ink workspaces                                    # list workspaces
```

## Deployment Flows

### Deploy a service

```bash
# 1. Create a repo and push code
ink repos create my-app
git remote add ink <gitRemote_from_output>
git push ink main

# 2. Deploy
ink deploy my-app --repo my-app --port 3000

# 3. Check status (status goes: queued -> building -> deploying -> active)
ink status my-app
```

### Deploy a full-stack app (API + frontend)

```bash
# 1. Deploy backend
ink repos create my-api
git remote add ink <url>
git push ink main
ink deploy my-api --repo my-api --port 8080

# 2. Wait for backend to be active
ink status my-api

# 3. Deploy frontend with backend URL
ink repos create my-frontend
git remote add ink-frontend <url>
git push ink-frontend main
ink deploy my-frontend --repo my-frontend --port 3000 \
  --env VITE_API_URL=https://my-api.ml.ink
```

### Deploy with a database

```bash
# 1. Create database
ink db create my-db --json
# Save databaseUrl and authToken from output

# 2. Deploy service
ink deploy my-app --repo my-app --port 3000

# 3. Set database credentials (merges with existing vars, triggers redeploy)
cat > .env.secrets <<EOF
DATABASE_URL=<databaseUrl from step 1>
DATABASE_AUTH_TOKEN=<authToken from step 1>
EOF
ink secrets import my-app --file .env.secrets
rm .env.secrets
```

### Deploy a static site or SPA

For frontend apps (React, Vue, Vite, Next.js static export, etc.) that build to a directory of static files. No `--port` needed — Ink serves via nginx automatically.

```bash
ink repos create my-site
git remote add ink <url>
git push ink main
ink deploy my-site --repo my-site --publish-dir dist
```

Use `--publish-dir` to specify where the build output goes (`dist`, `build`, `out`, etc.). Ink runs the build step then serves the result as static files.

For SPAs with an API backend, pass the API URL as a build-time env var:

```bash
ink deploy my-site --repo my-site --publish-dir dist \
  --env VITE_API_URL=https://my-api.ml.ink
```

### Deploy from a monorepo

```bash
# 1. Create one repo for the monorepo
ink repos create my-monorepo
git remote add ink <url>
git push ink main

# 2. Deploy backend from backend/ subdirectory
ink deploy mono-api --repo my-monorepo --root-dir backend --port 8080

# 3. Deploy frontend from frontend/ subdirectory (public URL is not a secret)
ink deploy mono-web --repo my-monorepo --root-dir frontend --publish-dir dist \
  --env VITE_API_URL=https://mono-api.ml.ink
```

### Deploy from GitHub

Requires GitHub OAuth and App connected at https://ml.ink.

```bash
ink deploy my-app --repo username/repo-name --host github --port 3000
```

Pushes to the GitHub repo automatically trigger redeployment via webhook.

### Add a custom domain

Requires a DNS zone delegated to Ink first (via https://ml.ink/dns).

```bash
ink dns zones                                     # verify zone is active
ink domains add my-app app.example.com            # auto-creates DNS + TLS
```

### Update a service (scale, env vars, config)

Use `ink secrets` for env var changes. Use `ink redeploy` for resource/config changes. Pushing code auto-redeploys -- you don't need to call redeploy for that.

```bash
# Add or update non-sensitive env vars
ink secrets set my-app NODE_ENV=production LOG_LEVEL=info

# Add secrets via file (avoids shell history exposure)
ink secrets import my-app --file .env.secrets

# Scale up memory and CPU
ink redeploy my-app --memory 1Gi --vcpu 1
```

### Debug a failing deployment

```bash
ink status my-app                                 # check status and error
ink logs my-app                                   # check runtime logs
```

## Service Configuration

| Option | Values | Default |
|--------|--------|---------|
| Memory | 128Mi, 256Mi, 512Mi, 1024Mi, 2048Mi, 4096Mi | 256Mi |
| vCPUs | 0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 1, 2, 3, 4 | 0.25 |
| Region | eu-central-1 | eu-central-1 |
| Branch | any git branch | main |

## Guidelines

- **Install the CLI first.** If `command -v ink` fails, install with `npm install -g @mldotink/cli`.
- **Check `ink services` before deploying** to see if a service already exists. Use `ink deploy` for new services and `ink redeploy` for existing ones.
- **Pushing code auto-redeploys.** After `git push`, just poll `ink status` to track progress.
- **Use `--json` flag** for machine-readable output when you need to parse results.
- **Memory:** 128Mi, 256Mi (default), 512Mi, 1024Mi, 2048Mi, 4096Mi.
- **vCPUs:** 0.1, 0.2, 0.25 (default), 0.3, 0.4, 0.5, 1, 2, 3, 4.
- When deploying, confirm the repo URL and branch with the user first.
- **Use `ink secrets import` for sensitive values** (credentials, tokens, API keys). Write to a temp file, import, delete the file. Never pass secrets as CLI arguments — they leak to shell history and process listings.
- **Use `ink secrets set` only for non-sensitive vars** like `NODE_ENV=production`. Never use `ink redeploy --env` to update vars — it replaces all vars.
- Never hardcode or guess secret values. Secrets should come from the user, from `ink db token`, or from other Ink CLI output.
- Show the service URL after successful deployment.
- Zone delegation (for custom domains) must be set up by the user at https://ml.ink/dns before you can use `ink domains add`.

