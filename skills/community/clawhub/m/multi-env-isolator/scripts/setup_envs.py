#!/usr/bin/env python3
"""
Multi-Environment Isolator — Generate isolated dev/test/prod environments.

Usage:
    python3 setup_envs.py <project_dir> --name "Project Name" \
        [--dev-port 8020] [--test-port 8010] [--prod-port 8000] \
        [--dev-user "Developer"] [--test-user "QA Tester"] \
        [--db-type sqlite|postgres] [--app-module "server.main:app"] \
        [--dev-db URL] [--test-db URL] [--prod-db URL]
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
    port = config[f"{env}_port"]
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


def generate_start_script(env: str, config: dict) -> str:
    """Generate startup shell script for a specific environment."""
    env_label = {"dev": "Development", "test": "Testing", "prod": "Production"}[env]
    port = config[f"{env}_port"]
    app_module = config["app_module"]
    name = config["name"]

    user_line = ""
    if env == "dev" and config.get("dev_user"):
        user_line = f'\necho "👩\u200d💻 Happy coding, {config["dev_user"]}!"'
    elif env == "test" and config.get("test_user"):
        user_line = f'\necho "🧪 Happy testing, {config["test_user"]}!"'

    reload_flag = "\n    --reload \\" if env == "dev" else ""
    workers = "$(nproc)" if env == "prod" else "1"
    workers_line = "" if env == "dev" else f"\n    --workers {workers} \\"
    log_level = {"dev": "debug", "test": "info", "prod": "warning"}[env]

    return f"""#!/bin/bash
# {'=' * 50}
# {name} - {env_label} Environment
# {'=' * 50}

set -e

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

export ENV_FILE="$PROJECT_DIR/.env.{env}"

echo "🚀 Starting {name} {env_label} Environment..."
echo "📍 Port: {port}"
echo "📍 Environment: $ENV_FILE"
echo "📍 Database: ./data/{env}/"{user_line}
echo ""

cd "$PROJECT_DIR"

[ -d "venv" ] && source venv/bin/activate

uvicorn {app_module} \\
    --host 127.0.0.1 \\
    --port {port} \\{reload_flag}{workers_line}
    --log-level {log_level}
"""


def generate_docs(config: dict) -> str:
    """Generate setup documentation."""
    name = config["name"]
    return f"""# {name} - Multi-Environment Setup

## Environments

| Environment | Port | Database | Purpose |
|-------------|------|----------|---------|
| Development | {config['dev_port']} | `data/dev/` | Feature development with hot reload |
| Testing | {config['test_port']} | `data/test/` | QA testing and validation |
| Production | {config['prod_port']} | `data/prod/` | Daily use |

## Quick Start

```bash
# Development
./scripts/start-dev.sh

# Testing
./scripts/start-test.sh

# Production
./scripts/start-prod.sh
```

## Directory Structure

```
{name.lower().replace(' ', '-')}/
├── .env.dev / .env.test / .env.prod
├── scripts/
│   ├── start-dev.sh
│   ├── start-test.sh
│   └── start-prod.sh
├── data/
│   ├── dev/    (database + media)
│   ├── test/   (database + media)
│   └── prod/   (database + media)
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

## Git Branch Strategy

```
main ──────────── Production ({config['prod_port']})
  ├── release/* ── Testing ({config['test_port']})
  └── feature/* ── Development ({config['dev_port']})
```

---
*Generated by multi-env-isolator*
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate isolated dev/test/prod environments"
    )
    parser.add_argument("project_dir", help="Target project directory")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--dev-port", type=int, default=8020)
    parser.add_argument("--test-port", type=int, default=8010)
    parser.add_argument("--prod-port", type=int, default=8000)
    parser.add_argument("--dev-user", default="")
    parser.add_argument("--test-user", default="")
    parser.add_argument("--db-type", default="sqlite", choices=["sqlite", "postgres"])
    parser.add_argument("--app-module", default="server.main:app")
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

    # Generate startup scripts
    for env in ["dev", "test", "prod"]:
        path = project / f"scripts/start-{env}.sh"
        if path.exists():
            print(f"  ⚠️  scripts/start-{env}.sh already exists, skipping")
            continue
        path.write_text(generate_start_script(env, config))
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
        print(f"  ✅ scripts/start-{env}.sh")

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
    print(f"  2. Start dev:  ./scripts/start-dev.sh")
    print(f"  3. Start test: ./scripts/start-test.sh")
    print(f"  4. Start prod: ./scripts/start-prod.sh")


if __name__ == "__main__":
    main()
