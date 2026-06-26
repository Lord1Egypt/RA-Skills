# Dev Workflow & CLI

## Project Setup

### Recommended Tooling

| Tool | Purpose | Recommendation |
|------|---------|----------------|
| **Bundler** | Build TypeScript → JS | Vite (with `obsidian-vault-plugin` or manual config) |
| **Package Manager** | Dependencies | pnpm |
| **Linter** | Code quality | ESLint + `eslint-plugin-obsidianmd` |
| **Type Checking** | TypeScript errors | `tsc --noEmit` |
| **Obsidian CLI** | Hot reload | `obsidian plugin:reload` (v1.12.4+) |

### Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, 'main.ts'),
      formats: ['cjs'],  // Obsidian uses require()
      fileName: 'main',
    },
    rollupOptions: {
      external: [
        'obsidian',
        'electron',
        '@codemirror/autocomplete',
        '@codemirror/collab',
        '@codemirror/commands',
        '@codemirror/language',
        '@codemirror/lint',
        '@codemirror/search',
        '@codemirror/state',
        '@codemirror/view',
        '@lezer/common',
        '@lezer/highlight',
        '@lezer/lr',
        // Node built-ins if needed
        'fs', 'path', 'os', 'crypto',
      ],
      output: {
        // Obsidian loads plugins via require()
        exports: 'default',
      },
    },
    outDir: 'dist',
    // Source maps for debugging
    sourcemap: 'inline',
  },
})
```

### package.json

```json
{
  "name": "my-obsidian-plugin",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "dev": "vite build --watch",
    "build": "vite build",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --ext .ts",
    "test": "vitest",
    "version": "node version-bump.mjs && git add manifest.json versions.json"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "eslint": "^8.0.0",
    "eslint-plugin-obsidianmd": "^0.1.9",
    "obsidian": "latest",
    "typescript": "^5.0.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "declaration": false,
    "outDir": "dist",
    "sourceMap": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "types": ["node"],
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

## Obsidian CLI (v1.12.4+)

### Setup

```bash
# Verify installation
obsidian --version

# List available vaults
obsidian vaults
```

### Plugin Dev Loop

```bash
# Build + reload (one-liner)
npm run build && obsidian plugin:reload id=<plugin-id>

# With type checking first
npm run typecheck && npm run build && obsidian plugin:reload id=<plugin-id>
```

### Dev Commands

```bash
# Check for errors (catches silent failures)
obsidian dev:errors

# Inspect DOM
obsidian dev:dom selector=".my-plugin-view"

# Take screenshot
obsidian dev:screenshot

# Evaluate JS in Obsidian context
obsidian eval code="app.plugins.plugins"

# Console output
obsidian dev:console level=error

# CSS inspection
obsidian dev:css selector=".my-plugin-button" prop=background-color

# Mobile simulation
obsidian dev:mobile on
```

### File Operations via CLI

```bash
# Read a file
obsidian file="My Note"

# Create a file
obsidian create name="New Note" content="# Hello"

# Search
obsidian search query="my plugin"

# Daily notes
obsidian daily:append content="Plugin dev progress: added settings tab"
```

### Plugin Management

```bash
# List installed plugins
obsidian plugins list

# Enable/disable
obsidian plugin:enable my-plugin
obsidian plugin:disable my-plugin

# Install from community
obsidian plugin:install my-plugin
```

## Without Obsidian CLI

### Manual Hot Reload

```bash
# Copy built files to test vault
npm run build && \
cp main.js manifest.json styles.css /path/to/TestVault/.obsidian/plugins/<plugin-id>/

# Reload in Obsidian: Ctrl/Cmd+P → "Reload app without saving"
```

### Watch Mode with File Copy

```bash
# Using nodemon or watchexec
npx watchexec -w dist/main.js -- cp dist/main.js /path/to/TestVault/.obsidian/plugins/<plugin-id>/
```

## ESLint Configuration (Flat Config — v9+)

```typescript
// eslint.config.mjs
import tsparser from "@typescript-eslint/parser";
import { defineConfig } from "eslint/config";
import obsidianmd from "eslint-plugin-obsidianmd";

export default defineConfig([
  ...obsidianmd.configs.recommended,
  {
    files: ["**/*.ts"],
    languageOptions: {
      parser: tsparser,
      parserOptions: { project: "./tsconfig.json" },
    },
    rules: {
      "obsidianmd/ui/sentence-case": ["warn", {
        brands: ["MyBrand"],
        acronyms: ["API", "URL"],
      }],
    },
  },
]);
```

> For legacy `.eslintrc.json` (ESLint v8), see [eslint-plugin-obsidianmd docs](https://github.com/obsidianmd/eslint-plugin). All 28 rules are documented in [[reference/eslint-rules.md]].

## Version Bump Script

```javascript
// version-bump.mjs
import { readFileSync, writeFileSync } from 'fs'

const targetVersion = process.env.npm_package_version

// Update manifest.json
const manifest = JSON.parse(readFileSync('manifest.json', 'utf8'))
const { minAppVersion } = manifest
manifest.version = targetVersion
writeFileSync('manifest.json', JSON.stringify(manifest, null, '\t'))

// Update versions.json
const versions = JSON.parse(readFileSync('versions.json', 'utf8'))
versions[targetVersion] = minAppVersion
writeFileSync('versions.json', JSON.stringify(versions, null, '\t'))
```

## Best Practices

1. **Always typecheck before build** — `tsc --noEmit && vite build`
2. **Use `formats: ['cjs']`** — Obsidian uses `require()`
3. **Externalize all Obsidian/CM6 imports** — don't bundle them
4. **Inline source maps** — easier debugging
5. **Use Obsidian CLI** for hot reload if available (v1.12.4+)
6. **Run ESLint** with `eslint-plugin-obsidianmd` rules
7. **Never auto git commit/push** — always ask user first
