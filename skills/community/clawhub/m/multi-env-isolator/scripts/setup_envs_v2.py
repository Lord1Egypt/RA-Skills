#!/usr/bin/env python3
"""
Multi-Environment Isolator v2 — Generate isolated dev/test/prod environments with frontend support.

Usage:
    python3 setup_envs_v2.py <project_dir> --name "Project Name" \\
        --dev-backend-port 8000 --dev-frontend-port 3000 \\
        --test-backend-port 8001 --test-frontend-port 3001 \\
        --prod-backend-port 8002 --prod-frontend-port 4173 \\
        --dev-user "Valina" --test-user "Choco" \\
        --db-type sqlite|postgres --app-module "server.main:app" \\
        --frontend-dir "cloud_docs/frontend"
"""

import argparse
import os
import stat
import sys
from pathlib import Path


def generate_env_file(env: str, config: dict) -> str:
    """Generate .env file content for a specific environment."""
    settings = {
        "dev": {
            "APP_ENV": "development",
            "DEBUG": "True",
            "LOG_LEVEL": "DEBUG",
            "CORS_ORIGINS": '["*"]',
            "RATE_LIMIT_ENABLED": "False",
        },
        "test": {
            "APP_ENV": "testing",
            "DEBUG": "True",
            "LOG_LEVEL": "INFO",
            "CORS_ORIGINS": '["*"]',
            "RATE_LIMIT_ENABLED": "True",
        },
        "prod": {
            "APP_ENV": "production",
            "DEBUG": "False",
            "LOG_LEVEL": "WARNING",
            "CORS_ORIGINS": '["http://localhost:3000","http://127.0.0.1:3000"]',
            "RATE_LIMIT_ENABLED": "True",
        },
    }

    env_label = {"dev": "Development", "test": "Testing", "prod": "Production"}[env]
    s = settings[env]
    port = config[f"{env}_backend_port"]
    name = config["name"]

    # Database URL
    if config.get(f"{env}_db"):
        db_url = config[f"{env}_db"]
    elif config["db_type"] == "postgres":
        db_url = f"postgresql://localhost/{name.lower().replace(' ', '_')}_{env}"
    else:
        db_url = f"sqlite+aiosqlite:///./data/{env}/{name.lower().replace(' ', '_')}.db"

    lines = [
        f"# {'=' * 50}",
        f"# {name} - {env_label} Environment",
        f"# {'=' * 50}",
        "",
        "# Application",
        f"APP_NAME={name} ({env_label})",
        f"APP_ENV={s['APP_ENV']}",
        f"DEBUG={s['DEBUG']}",
        f"LOG_LEVEL={s['LOG_LEVEL']}",
        "",
        "# Server",
        f"HOST=127.0.0.1",
        f"PORT={port}",
        "",
        "# Database",
        f"DATABASE_URL={db_url}",
        "",
        "# Storage",
        f"STORAGE_TYPE=local",
        f"MEDIA_STORAGE_PATH=./data/{env}/media",
        "",
        "# Security",
        f"JWT_SECRET={env}-jwt-secret-change-me",
        f"JWT_ALGORITHM=HS256",
        f"JWT_EXPIRE_MINUTES=1440",
        "",
        "# CORS",
        f"CORS_ORIGINS={s['CORS_ORIGINS']}",
        f"CORS_ALLOW_CREDENTIALS=True",
        "",
        "# Rate Limiting",
        f"RATE_LIMIT_ENABLED={s['RATE_LIMIT_ENABLED']}",
    ]

    if s["RATE_LIMIT_ENABLED"] == "True":
        lines += [
            "RATE_LIMIT_REQUESTS=100",
            "RATE_LIMIT_WINDOW=60",
        ]

    return "\n".join(lines) + "\n"


def generate_backend_script(env: str, config: dict) -> str:
    """Generate backend startup shell script for a specific environment."""
    env_label = {"dev": "Development", "test": "Testing", "prod": "Production"}[env]
    port = config[f"{env}_backend_port"]
    app_module = config["app_module"]
    name = config["name"]

    user_line = ""
    if env == "dev" and config.get("dev_user"):
        user_line = f'\\necho "👩\u200d💻 Happy coding, {config["dev_user"]}!"'
    elif env == "test" and config.get("test_user"):
        user_line = f'\\necho "🧪 Happy testing, {config["test_user"]}!"'

    reload_flag = "\\n    --reload \\\\" if env == "dev" else ""
    workers = "$(nproc)" if env == "prod" else "1"
    workers_line = "" if env == "dev" else f"\\n    --workers {workers} \\\\"
    log_level = {"dev": "debug", "test": "info", "prod": "warning"}[env]

    return f"""#!/bin/bash
# {'=' * 50}
# {name} - Backend {env_label} Environment
# {'=' * 50}

set -e

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

export ENV_FILE="$PROJECT_DIR/.env.{env}"

echo "🚀 Starting {name} Backend {env_label} Environment..."
echo "📍 Port: {port}"
echo "📍 Environment: $ENV_FILE"
echo "📍 Database: ./data/{env}/"{user_line}
echo ""

cd "$PROJECT_DIR"

[ -d "venv" ] && source venv/bin/activate

uvicorn {app_module} \\\\
    --host 127.0.0.1 \\\\
    --port {port} \\\\{reload_flag}{workers_line}
    --log-level {log_level}
"""


def generate_frontend_script(env: str, config: dict) -> str:
    """Generate frontend startup shell script for a specific environment."""
    env_label = {"dev": "Development", "test": "Testing", "prod": "Production"}[env]
    port = config[f"{env}_frontend_port"]
    name = config["name"]
    frontend_dir = config.get("frontend_dir", "cloud_docs/frontend")

    if env == "prod":
        command = "npm run preview"
        port_comment = "(preview server)"
    else:
        command = "npm run dev"
        port_comment = "(dev server)"

    return f"""#!/bin/bash
# {'=' * 50}
# {name} - Frontend {env_label} Environment
# {'=' * 50}

set -e

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/../{frontend_dir}"

echo "🎨 Starting {name} Frontend {env_label} Environment..."
echo "📍 Port: {port} {port_comment}"
echo "📍 Directory: $FRONTEND_DIR"
echo ""

cd "$FRONTEND_DIR"

[ -d "node_modules" ] || {{
    echo "⚠️  node_modules not found. Running npm install..."
    npm install
}}

export PORT={port}
{command}
"""


def generate_playwright_script(config: dict) -> str:
    """Generate Playwright test runner script."""
    name = config["name"]
    frontend_dir = config.get("frontend_dir", "cloud_docs/frontend")

    return f"""#!/bin/bash
# {'=' * 50}
# {name} - Playwright E2E Tests
# {'=' * 50}

set -e

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/../{frontend_dir}"

echo "🧪 Running {name} Playwright E2E Tests..."
echo "📍 Test Environment: Backend 8001, Frontend 3001"
echo "📍 Test Directory: $FRONTEND_DIR/tests"
echo ""

cd "$FRONTEND_DIR"

[ -d "node_modules" ] || {{
    echo "⚠️  node_modules not found. Running npm install..."
    npm install
}}

[ -f "playwright.config.ts" ] || {{
    echo "❌ playwright.config.ts not found!"
    echo "   Make sure Playwright is installed: npm install -D @playwright/test"
    exit 1
}}

npx playwright test "$@"

echo ""
echo "✅ Playwright tests complete!"
echo ""
echo "View report: npx playwright show-report"
"""


def generate_docs(config: dict) -> str:
    """Generate setup documentation."""
    name = config["name"]
    return f"""# {name} - Multi-Environment Setup

## Environments

| Environment | Backend | Frontend | Database | Purpose |
|-------------|---------|----------|----------|---------|
| Development | {config['dev_backend_port']} | {config['dev_frontend_port']} | `data/dev/` | Feature development with hot reload |
| Testing | {config['test_backend_port']} | {config['test_frontend_port']} | `data/test/` | QA testing and Playwright E2E |
| Production | {config['prod_backend_port']} | {config['prod_frontend_port']} | `data/prod/` | Daily use |

## Quick Start

### For Developers (Valina)

```bash
# Start both backend and frontend
./scripts/start-dev.sh
```

### For Testers (Choco)

```bash
# Start test environment
./scripts/start-test.sh

# Run Playwright E2E tests
./scripts/run-playwright-tests.sh
```

### For Production

```bash
# Start production environment
./scripts/start-prod.sh
```

## Directory Structure

```
{name.lower().replace(' ', '-')}/
├── .env.dev / .env.test / .env.prod
├── scripts/
│   ├── start-dev.sh           # Start both backend + frontend
│   ├── start-backend-dev.sh   # Backend only
│   ├── start-frontend-dev.sh  # Frontend only
│   ├── start-test.sh
│   ├── start-prod.sh
│   └── run-playwright-tests.sh
├── data/
│   ├── dev/    (database + media)
│   ├── test/   (database + media)
│   └── prod/   (database + media)
├── cloud_docs/frontend/
│   └── playwright.config.ts
└── docs/
    └── MULTI_ENV_SETUP.md
```

## Environment Differences

| Setting | Dev | Test | Prod |
|---------|-----|------|------|
| DEBUG | True | True | False |
| Hot Reload | Yes | No | No |
| CORS | Allow All | Allow All | Restricted |
| Rate Limit | Off | On | On |
| Workers | 1 (reload) | 1 | Auto (CPU) |
| Log Level | DEBUG | INFO | WARNING |
| Playwright Tests | ❌ | ✅ | ❌ |

## Git Branch Strategy

```
main ──────────── Production ({config['prod_backend_port']}/{config['prod_frontend_port']})
  ├── release/* ── Testing ({config['test_backend_port']}/{config['test_frontend_port']})
  └── feature/* ── Development ({config['dev_backend_port']}/{config['dev_frontend_port']})
```

## Parallel Development and Testing

**Key benefit**: Valina and Choco can work simultaneously without conflicts!

```
Time  | Valina (Dev)                    | Choco (Test)
------|---------------------------------|----------------------------------
14:00 | start-dev.sh (8000/3000)        | -
14:05 | Continue coding...              | start-test.sh (8001/3001)
14:10 | Continue coding...              | run-playwright-tests.sh
14:20 | Continue coding...              | Tests pass! Report results
14:25 | Continue coding...              | stop-test.sh
```

**No port conflicts! No data interference!** ✅

---
*Generated by multi-env-isolator v2*
"""


def generate_combined_start_script(env: str, config: dict) -> str:
    """Generate combined start script that starts both backend and frontend."""
    env_label = {"dev": "Development", "test": "Testing", "prod": "Production"}[env]
    name = config["name"]

    return f"""#!/bin/bash
# {'=' * 50}
# {name} - Start {env_label} Environment (Backend + Frontend)
# {'=' * 50}

set -e

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"

echo "🚀 Starting {name} {env_label} Environment (Backend + Frontend)..."
echo ""

# Start backend in background
echo "📍 Starting backend..."
"$SCRIPT_DIR/start-backend-{env}.sh" &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo ""
echo "📍 Starting frontend..."
"$SCRIPT_DIR/start-frontend-{env}.sh"

# Wait for backend process
wait $BACKEND_PID
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate isolated dev/test/prod environments with frontend support"
    )
    parser.add_argument("project_dir", help="Target project directory")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--dev-backend-port", type=int, default=8000)
    parser.add_argument("--dev-frontend-port", type=int, default=3000)
    parser.add_argument("--test-backend-port", type=int, default=8001)
    parser.add_argument("--test-frontend-port", type=int, default=3001)
    parser.add_argument("--prod-backend-port", type=int, default=8002)
    parser.add_argument("--prod-frontend-port", type=int, default=4173)
    parser.add_argument("--dev-user", default="Valina")
    parser.add_argument("--test-user", default="Choco")
    parser.add_argument("--db-type", default="sqlite", choices=["sqlite", "postgres"])
    parser.add_argument("--app-module", default="server.main:app")
    parser.add_argument("--frontend-dir", default="cloud_docs/frontend")
    parser.add_argument("--dev-db", default="")
    parser.add_argument("--test-db", default="")
    parser.add_argument("--prod-db", default="")
    args = parser.parse_args()

    config = vars(args)
    project = Path(args.project_dir)

    print(f"🔧 Generating multi-environment setup for: {args.name}")
    print(f"📍 Target: {project.resolve()}")
    print()

    # Create directories
    for d in [
        "data/dev/media", "data/test/media", "data/prod/media",
        "scripts", "docs",
    ]:
        (project / d).mkdir(parents=True, exist_ok=True)
        print(f"  📁 {d}/")

    # Generate .env files
    for env in ["dev", "test", "prod"]:
        path = project / f".env.{env}"
        if path.exists():
            print(f"  ⚠️  .env.{env} already exists, skipping")
            continue
        path.write_text(generate_env_file(env, config))
        print(f"  ✅ .env.{env}")

    # Generate backend scripts
    for env in ["dev", "test", "prod"]:
        path = project / f"scripts/start-backend-{env}.sh"
        if path.exists():
            print(f"  ⚠️  scripts/start-backend-{env}.sh already exists, skipping")
            continue
        path.write_text(generate_backend_script(env, config))
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
        print(f"  ✅ scripts/start-backend-{env}.sh")

    # Generate frontend scripts
    for env in ["dev", "test", "prod"]:
        path = project / f"scripts/start-frontend-{env}.sh"
        if path.exists():
            print(f"  ⚠️  scripts/start-frontend-{env}.sh already exists, skipping")
            continue
        path.write_text(generate_frontend_script(env, config))
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
        print(f"  ✅ scripts/start-frontend-{env}.sh")

    # Generate combined start scripts
    for env in ["dev", "test", "prod"]:
        path = project / f"scripts/start-{env}.sh"
        if path.exists():
            print(f"  ⚠️  scripts/start-{env}.sh already exists, skipping")
            continue
        path.write_text(generate_combined_start_script(env, config))
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
        print(f"  ✅ scripts/start-{env}.sh")

    # Generate Playwright test script
    playwright_path = project / "scripts/run-playwright-tests.sh"
    if playwright_path.exists():
        print(f"  ⚠️  scripts/run-playwright-tests.sh already exists, skipping")
    else:
        playwright_path.write_text(generate_playwright_script(config))
        playwright_path.chmod(playwright_path.stat().st_mode | stat.S_IEXEC)
        print(f"  ✅ scripts/run-playwright-tests.sh")

    # Generate docs
    docs_path = project / "docs/MULTI_ENV_SETUP.md"
    docs_path.write_text(generate_docs(config))
    print(f"  ✅ docs/MULTI_ENV_SETUP.md")

    # Add to .gitignore
    gitignore = project / ".gitignore"
    ignore_entries = [".env.dev", ".env.test", ".env.prod", "data/"]
    if gitignore.exists():
        existing = gitignore.read_text()
        new_entries = [e for e in ignore_entries if e not in existing]
        if new_entries:
            with open(gitignore, "a") as f:
                f.write("\n# Multi-environment isolation\n")
                for e in new_entries:
                    f.write(f"{e}\n")
            print(f"  ✅ .gitignore updated")
    else:
        gitignore.write_text(
            "# Multi-environment isolation\n"
            + "\n".join(ignore_entries) + "\n"
        )
        print(f"  ✅ .gitignore created")

    print()
    print("✅ Multi-environment setup complete!")
    print()
    print("Next steps:")
    print(f"  1. Edit .env.* files for project-specific settings")
    print(f"  2. Start dev:   ./scripts/start-dev.sh")
    print(f"  3. Start test:  ./scripts/start-test.sh")
    print(f"  4. Run tests:   ./scripts/run-playwright-tests.sh")
    print(f"  5. Start prod:  ./scripts/start-prod.sh")


if __name__ == "__main__":
    main()
