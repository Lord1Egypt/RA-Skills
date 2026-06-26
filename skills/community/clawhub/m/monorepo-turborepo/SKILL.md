---
name: monorepo-turborepo
description: Use when setting up or managing a Turborepo-based monorepo. Covers workspace configuration, task pipelines, caching strategies, shared packages, and CI/CD integration for multi-package repositories with Turborepo.
---

# Monorepo with Turborepo

A practical guide to building and managing scalable monorepos using Turborepo.

## When to Use
- Setting up a new monorepo with multiple apps/packages
- Optimizing build/test pipelines with caching
- Sharing UI components, utilities, or configs across apps
- Configuring CI for monorepo with selective builds

## Core Workflow

### 1. Initialize Monorepo

```bash
npx create-turbo@latest my-monorepo
cd my-monorepo
```

**Workspace layout:**
```
my-monorepo/
├── apps/
│   ├── web/          # Next.js app
│   └── docs/         # Docusaurus
├── packages/
│   ├── ui/           # Shared components
│   ├── config/       # Shared ESLint/TS configs
│   └── utils/        # Shared utilities
├── turbo.json
└── package.json
```

### 2. Configure turbo.json Pipeline

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "type-check": {
      "dependsOn": ["^build"],
      "outputs": []
    }
  }
}
```

### 3. Package.json Root Config

```json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "test": "turbo test",
    "type-check": "turbo type-check",
    "clean": "turbo clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "latest"
  }
}
```

### 4. Shared Package Setup (packages/ui)

```json
// packages/ui/package.json
{
  "name": "@repo/ui",
  "version": "0.0.1",
  "exports": {
    "./*": {
      "import": "./src/*.tsx",
      "require": "./src/*.tsx"
    }
  },
  "scripts": {
    "build": "tsc",
    "lint": "eslint src/",
    "dev": "tsc --watch"
  }
}
```

### 5. Remote Caching (Vercel)

```bash
npx turbo login
npx turbo link
```

Or with custom remote cache:
```bash
turbo build --api="https://your-cache-server.com" --token="$TURBO_TOKEN" --team="your-team"
```

### 6. Selective Builds (Filter)

```bash
# Build only affected packages
turbo build --filter=...[HEAD^1]

# Build specific app and its dependencies
turbo build --filter=web...

# Exclude a package
turbo build --filter=!docs
```

### 7. CI/CD Integration (GitHub Actions)

See `references/ci-github-actions.yml` for a complete workflow.

## Key Principles

- **`^` prefix** in `dependsOn` means "build all dependencies first"
- **`outputs`** defines what gets cached; be explicit
- **`cache: false`** for dev/watch tasks
- **`persistent: true`** for long-running processes
- Always define `exports` in package.json for shared packages

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cache miss every run | Check `outputs` paths are correct |
| Circular dependency | Use `turbo graph` to visualize |
| Package not found | Verify `workspaces` glob in root package.json |
| Slow cold build | Enable remote caching |
