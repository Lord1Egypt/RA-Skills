---
name: multi-env-isolator
description: |
  Generate isolated dev/test/prod environments for uvicorn/FastAPI Python web projects with frontend (Vue/React) support. Creates separate config files, startup scripts (backend + frontend), data directories, Playwright test integration, and documentation with one command. Use when:
  (1) Setting up a new FastAPI/uvicorn + Vue/React project that needs dev/test/prod separation
  (2) An existing project has only one environment and needs isolation for parallel work
  (3) A multi-agent team needs developers (Valina) and testers (Choco) working simultaneously without conflicts
  (4) Someone asks "how to separate development and production" or "set up environment isolation"
  (5) A project suffers from dev changes breaking production, or testers interfering with developers
  (6) You need Playwright E2E test integration with isolated test environment
  NOT for: Node.js-only, Go, Docker-based, or non-Python projects (backend startup scripts are uvicorn-specific).
---

# Multi-Environment Isolator

Generate isolated dev/test/prod environments for uvicorn/FastAPI projects with frontend support (Vue/React) with one command.

## What This Skill Does

This skill solves a common problem in multi-agent AI teams: **developers, testers, and production users stepping on each other's toes.** It generates a complete environment isolation setup so that:

- **Valina (Developer)** can freely break things on ports 8000/3000 without affecting anyone
- **Choco (Tester)** can validate releases on ports 8001/3001 with isolated test data and Playwright tests
- **Production** stays stable on ports 8002/4173, untouched by dev/test activity

Each environment gets its own config file, startup scripts (backend + frontend), database, media storage, and Playwright test configuration — completely isolated from the others.

## What Gets Generated

Running the setup script creates this structure inside the target project:

```
your-project/
├── .env.dev              # Dev config: DEBUG=True, hot reload, no rate limit
├── .env.test             # Test config: rate limiting enabled, QA settings
├── .env.prod             # Prod config: DEBUG=False, secure CORS, multi-worker
├── scripts/
│   # Backend scripts
│   ├── start-backend-dev.sh    # Starts dev server on port 8000 with --reload
│   ├── start-backend-test.sh   # Starts test server on port 8001
│   └── start-backend-prod.sh   # Starts prod server on port 8002 with auto workers
│   # Frontend scripts (Vue/React)
│   ├── start-frontend-dev.sh   # Starts dev frontend on port 3000
│   ├── start-frontend-test.sh  # Starts test frontend on port 3001
│   └── start-frontend-prod.sh  # Starts prod frontend on port 4173 (preview)
│   # Test scripts
│   └── run-playwright-tests.sh # Runs Playwright E2E tests on test environment
├── data/
│   ├── dev/              # Dev database + media uploads (safe to delete)
│   │   └── media/
│   ├── test/             # Test database + media uploads
│   │   └── media/
│   └── prod/             # Prod database + media uploads (back this up!)
│       └── media/
├── docs/
│   └── MULTI_ENV_SETUP.md  # Auto-generated setup guide for the team
├── cloud_docs/frontend/
│   └── playwright.config.ts  # Playwright test config (if frontend exists)
└── .gitignore            # Updated to exclude .env.* and data/
```

## How to Use

### Step 1: Run the setup script

```bash
python3 scripts/setup_envs.py /path/to/your-project \
  --name "Your Project Name" \
  --dev-backend-port 8000 \
  --dev-frontend-port 3000 \
  --test-backend-port 8001 \
  --test-frontend-port 3001 \
  --prod-backend-port 8002 \
  --prod-frontend-port 4173 \
  --dev-user "Valina" \
  --test-user "Choco" \
  --app-module "server.main:app" \
  --frontend-dir "cloud_docs/frontend"
```

All flags except `--name` are optional and have sensible defaults.

### Step 2: Start environments

```bash
# For Valina (Development)
./scripts/start-dev.sh        # Starts both backend (8000) and frontend (3000)

# For Choco (Testing)
./scripts/start-test.sh       # Starts both backend (8001) and frontend (3001)
./scripts/run-playwright-tests.sh  # Runs E2E tests

# For Production
./scripts/start-prod.sh       # Starts both backend (8002) and frontend (4173)
```

### Step 2: Customize configs

Edit the generated `.env.dev`, `.env.test`, `.env.prod` files to add project-specific settings like API keys, external service URLs, etc.

### Step 3: Start an environment

```bash
# For development (hot reload enabled)
./scripts/start-dev.sh

# For testing
./scripts/start-test.sh

# For production
./scripts/start-prod.sh
```

Each script loads its own `.env.*` file, uses its own port, and writes to its own `data/` subdirectory.

## Command Reference

```
python3 scripts/setup_envs.py <project_dir> --name <name> [options]
```

| Flag | Default | Description |
|------|---------|-------------|
| `project_dir` | (required) | Path to the target project |
| `--name` | (required) | Project name, used in configs and docs |
| `--dev-port` | 8020 | Development server port |
| `--test-port` | 8010 | Testing server port |
| `--prod-port` | 8000 | Production server port |
| `--dev-user` | (none) | Developer name, shown in dev startup message |
| `--test-user` | (none) | Tester name, shown in test startup message |
| `--db-type` | sqlite | `sqlite` or `postgres` |
| `--app-module` | server.main:app | Uvicorn application module path |
| `--dev-db` | (auto) | Override dev database URL |
| `--test-db` | (auto) | Override test database URL |
| `--prod-db` | (auto) | Override prod database URL |

## Environment Differences at a Glance

| Setting | Dev (Valina) | Test (Choco) | Prod |
|---------|--------------|--------------|------|
| Backend Port | 8000 | 8001 | 8002 |
| Frontend Port | 3000 | 3001 | 4173 |
| `DEBUG` | True | True | **False** |
| Hot Reload | **Yes** | No | No |
| CORS | Allow All | Allow All | **Restricted** |
| Rate Limiting | **Off** | On | On |
| Workers | 1 (reload) | 1 | **Auto (CPU cores)** |
| Log Level | DEBUG | INFO | **WARNING** |
| Database | `data/dev/` | `data/test/` | `data/prod/` |
| Media | `data/dev/media/` | `data/test/media/` | `data/prod/media/` |
| Playwright Tests | ❌ Not recommended | **✅ Recommended** | ❌ Never |

## Recommended Git Branch Strategy

For teams using this setup:

```
main ──────────── Production (start-prod.sh) - Ports 8002/4173
  ├── release/* ── Testing (start-test.sh + run-playwright-tests.sh) - Ports 8001/3001
  └── feature/* ── Development (start-dev.sh) - Ports 8000/3000
```

1. **Valina (Developer)** works on `feature/*`, deploys to dev environment (8000/3000)
2. Merge to `release/*`, **Choco (Tester)** validates on test environment (8001/3001)
3. Choco runs Playwright tests: `./scripts/run-playwright-tests.sh`
4. Tester approves, merge to `main`, deploy to production (8002/4173)

### Parallel Development and Testing

**Key benefit**: Valina and Choco can work simultaneously without conflicts!

```
Time  | Valina (Dev)              | Choco (Test)
------|---------------------------|---------------------------
14:00 | start-dev.sh (8000/3000)  | -
14:05 | Continue coding...        | start-test.sh (8001/3001)
14:10 | Continue coding...        | run-playwright-tests.sh
14:20 | Continue coding...        | Tests pass! Report results
14:25 | Continue coding...        | stop-test.sh
```

**No port conflicts! No data interference!** ✅

## Important Notes

- **Existing files are not overwritten.** If `.env.dev` already exists, the script skips it and prints a warning. Safe to re-run.
- **Backend startup scripts are uvicorn-specific.** The generated `start-backend-*.sh` scripts use `uvicorn` commands. For other frameworks, modify the scripts after generation.
- **Frontend scripts support Vue/React.** The generated `start-frontend-*.sh` scripts use `npm run dev` and `npm run preview`. For Vite projects, they work out of the box.
- **Production JWT secret must be changed.** The generated `.env.prod` has a placeholder `JWT_SECRET`. Replace it with a strong random value before going live.
- **Back up production data.** The `data/prod/` directory contains the production database. Set up regular backups.
- **Playwright tests require Node.js.** The test script requires Playwright to be installed: `npm install -D @playwright/test`
- **Test data cleanup.** After running Playwright tests, consider cleaning up test data to keep the test environment clean.

## Detailed Config Reference

For all environment variables and troubleshooting: read `references/config-options.md`
