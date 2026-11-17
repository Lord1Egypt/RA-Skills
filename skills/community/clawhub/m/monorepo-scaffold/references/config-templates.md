# Config Templates

Boilerplate contents for commonly-generated files, referenced from `stack-recipes.md`. Treat every value here as a sensible starting point to adapt to what the interview actually surfaced (project name, chosen tools, license) — never paste these verbatim without substituting the real project details.

---

## Root `package.json` (pnpm + Turborepo, Recipe A)

```json
{
  "name": "<project-name>",
  "private": true,
  "packageManager": "pnpm@9.0.0",
  "engines": { "node": ">=20" },
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "typecheck": "turbo run typecheck",
    "format": "prettier --write \"**/*.{ts,tsx,md,json}\""
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.5.0",
    "prettier": "^3.3.0"
  }
}
```

Pin actual current versions at scaffold time rather than trusting the numbers above verbatim — check what's current if the sandbox has registry access; otherwise use these as reasonable recent baselines and tell the user to run their package manager's update check.

## `pnpm-workspace.yaml`

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

## `turbo.json`

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {},
    "test": {},
    "typecheck": {}
  }
}
```

## Root `tsconfig.base.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "composite": false
  }
}
```

Each package's own `tsconfig.json` should `extends` this with `"extends": "../../tsconfig.base.json"` (adjust relative path to depth) and add its own `include`/`outDir`.

## `.gitignore` (JS/TS baseline — extend per stack)

```
node_modules/
dist/
build/
.next/
.turbo/
.nx/
.env
.env.local
*.log
.DS_Store
coverage/
```

## `.editorconfig`

```
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
```

## `.nvmrc`

```
20
```

(Use whatever Node major version was agreed in the interview; 20 is a reasonable current LTS default if unspecified — say that's the default when using it.)

## GitHub Actions CI (`.github/workflows/ci.yml`, pnpm + Turborepo)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - run: pnpm turbo run lint test build
```

For affected-only CI, replace the last step with something like `pnpm turbo run lint test build --filter=...[origin/main]` and confirm `fetch-depth` is sufficient for Turborepo to diff against the base branch.

## Changesets init (only if publishing is in scope)

```bash
pnpm add -Dw @changesets/cli
pnpm changeset init
```

This creates `.changeset/config.json`. Set `"access"` to `"public"` or `"restricted"` based on whether packages are meant to be publicly published, and set `"baseBranch"` to match the repo's actual default branch.

## Root README structure

Every scaffold gets a README with at least these sections, filled in with real project-specific content — not placeholder lorem ipsum:

```markdown
# <Project Name>

<one-line purpose, from the interview>

## Structure

<folder tree, or a short description of what lives in apps/ vs packages/>

## Getting started

\`\`\`bash
<install command>
<dev command>
\`\`\`

## Scripts

| Command | Description |
|---|---|
| `<pm> dev` | Run all apps in development |
| `<pm> build` | Build all apps and packages |
| `<pm> lint` | Lint the whole repo |
| `<pm> test` | Run all tests |

## Packages

- `apps/<name>` — <what it does>
- `packages/<name>` — <what it does>
```

## `Dockerfile` skeleton (per app, Node example — adapt base image/steps per language)

```dockerfile
FROM node:20-slim AS base
WORKDIR /app
RUN corepack enable

FROM base AS deps
COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./
COPY apps/<app>/package.json apps/<app>/
COPY packages/ packages/
RUN pnpm install --frozen-lockfile

FROM deps AS build
COPY . .
RUN pnpm turbo run build --filter=<app>...

FROM base AS runner
COPY --from=build /app/apps/<app>/dist ./dist
CMD ["node", "dist/index.js"]
```

Adapt heavily per app — this is a starting skeleton for a Node service, not a universal template. A frontend app being containerized for static hosting, or a Python/Go service, needs a genuinely different Dockerfile, not this one with names swapped.

## `docker-compose.yml` (only if local services like a database are needed)

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

Only include services the interview actually surfaced a need for — don't add a database container speculatively.
