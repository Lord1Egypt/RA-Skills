---
title: Configure transformIgnorePatterns for ESM packages
impact: MEDIUM
description: Jest does not transform node_modules by default. ESM-only packages fail with SyntaxError unless you configure transformIgnorePatterns to include them.
tags: config, transform, transformIgnorePatterns, esm, node_modules, SyntaxError
---

# Configure transformIgnorePatterns for ESM packages

## Problem

Jest's default `transformIgnorePatterns` skips `node_modules/`, meaning third-party packages are not transpiled. When a dependency ships ESM-only code (using `import`/`export` syntax), Jest throws `SyntaxError: Cannot use import statement outside a module` because Node.js in CJS mode cannot parse it.

## Incorrect

```javascript
// jest.config.js — default config
module.exports = {
  // transformIgnorePatterns defaults to ['/node_modules/']
  // ESM-only packages like `uuid`, `nanoid`, `chalk` v5 will fail:
  // SyntaxError: Cannot use import statement outside a module
};
```

## Correct

```javascript
// jest.config.js — allow specific ESM packages to be transformed
module.exports = {
  transformIgnorePatterns: [
    '/node_modules/(?!(uuid|nanoid|chalk|@esm-package)/)',
  ],
};
```

```javascript
// Using a regex pattern for multiple packages
module.exports = {
  transformIgnorePatterns: [
    '<rootDir>/node_modules/(?!(' +
      'uuid|' +
      'nanoid|' +
      'chalk|' +
      '@scope/esm-pkg' +
    ')/)',
  ],
};
```

## How It Works

The `transformIgnorePatterns` array contains regex patterns. Files matching these patterns are **not** transformed. The default `['/node_modules/']` skips all of `node_modules/`.

To transform specific packages, use a **negative lookahead**:

```
/node_modules/(?!(package-a|package-b)/)
```

This means: "ignore node_modules, **except** `package-a` and `package-b`."

## Common ESM-Only Packages

| Package | ESM since |
|---|---|
| `chalk` | v5 |
| `nanoid` | v4 |
| `uuid` | v9 |
| `execa` | v6 |
| `got` | v12 |
| `p-*` (p-limit, p-queue, etc.) | Various |

## Why

- Many popular packages now ship ESM-only, dropping CJS support.
- Jest uses CJS by default for its module system, so ESM code must be transpiled.
- Adding packages to the negative lookahead allows Jest's transformer (Babel, SWC, or ts-jest) to compile them.
- Alternative: Use `moduleNameMapper` to point at a CJS build if the package provides one.

```javascript
// Alternative: map to CJS build
module.exports = {
  moduleNameMapper: {
    '^uuid$': require.resolve('uuid'), // resolves to CJS entry
  },
};
```
