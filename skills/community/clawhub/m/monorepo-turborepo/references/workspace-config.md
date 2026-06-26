# Turborepo Workspace Configuration Reference

## Package Manager Setup

### pnpm (Recommended)
```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tools/*"
```

```json
// package.json
{
  "engines": {
    "node": ">=18",
    "pnpm": ">=8"
  },
  "packageManager": "pnpm@8.15.0"
}
```

### npm workspaces
```json
{
  "workspaces": ["apps/*", "packages/*"]
}
```

### yarn workspaces
```json
{
  "workspaces": {
    "packages": ["apps/*", "packages/*"],
    "nohoist": ["**/react-native/**"]
  }
}
```

---

## Shared Config Packages

### packages/config-typescript/

```json
// package.json
{
  "name": "@repo/typescript-config",
  "version": "0.0.0",
  "private": true,
  "files": ["base.json", "nextjs.json", "react-library.json"]
}
```

```json
// base.json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  }
}
```

```json
// nextjs.json — for Next.js apps
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./base.json",
  "compilerOptions": {
    "plugins": [{ "name": "next" }],
    "module": "ESNext",
    "jsx": "preserve",
    "incremental": true
  }
}
```

### packages/config-eslint/

```json
// package.json
{
  "name": "@repo/eslint-config",
  "version": "0.0.0",
  "private": true,
  "files": ["base.js", "next.js", "react-internal.js"],
  "devDependencies": {
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "eslint-config-prettier": "^9.0.0"
  }
}
```

```js
// base.js
module.exports = {
  extends: ["eslint:recommended", "prettier"],
  rules: {
    "no-console": "warn"
  },
  env: {
    node: true,
    es2022: true
  }
};
```

---

## App Configuration (apps/web)

```json
// apps/web/package.json
{
  "name": "web",
  "private": true,
  "scripts": {
    "build": "next build",
    "dev": "next dev",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/utils": "workspace:*"
  },
  "devDependencies": {
    "@repo/eslint-config": "workspace:*",
    "@repo/typescript-config": "workspace:*"
  }
}
```

---

## Environment Variables

```bash
# .env.turbo (root level)
TURBO_TOKEN=your_vercel_remote_cache_token
TURBO_TEAM=your_team_slug
TURBO_REMOTE_ONLY=false   # set true to only use remote cache
```

## Useful Turbo CLI Flags

```bash
turbo build --dry-run          # Preview what would run
turbo build --graph            # Output dependency graph
turbo build --concurrency=4    # Limit parallel tasks
turbo build --no-cache         # Skip cache reads
turbo build --force            # Ignore cache, re-run all
turbo build --summarize        # Output run summary JSON
```
