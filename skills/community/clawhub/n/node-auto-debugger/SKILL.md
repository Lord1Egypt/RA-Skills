---
name: node-auto-debugger
description: Scan Node.js/Express/Next.js projects for bugs, security issues, and anti-patterns. Use when debugging a Node.js web app, running code audits, fixing client-side exceptions, hydration errors, hardcoded secrets, missing error handling, or preparing for production. Covers backend (Express/Fastify routes, async errors, undefined vars) and frontend (Next.js/React hydration, SSR crashes, wagmi/RainbowKit issues, missing 'use client' directives) plus config validation and optional build verification.
---

# Node.js Auto Debugger

Automated scanner for Node.js projects — finds bugs across backend, frontend, and config.

## Quick Start

```bash
node scripts/auto-debug.js <project-dir>
```

Options:
- `--build` — Also run `npm run build` and capture compilation errors

## What It Checks

### Backend (Express/Fastify)
- **Undefined variables** — `.push()` on undeclared variables
- **Missing try/catch** — async route handlers without error handling
- **Hardcoded secrets** — API keys, private keys, passwords in source

### Frontend (Next.js/React)
- **Missing 'use client'** — hooks or browser APIs without directive
- **Hydration risks** — `Date.now()`, `Math.random()` in render (should be in `useEffect` or `useState`)
- **SSR crashes** — `window`/`document` access outside `useEffect`
- **Missing loading states** — wagmi hooks without `isLoading`/`isFetching`

### Config
- **Missing next.config.js** — defaults warning
- **Missing build script** — package.json validation

## Output

Report saved to `<project>/AUTO-DEBUG-REPORT.md` with issues grouped by severity:
- 🔴 Critical — will crash or leak secrets
- 🟠 High — likely runtime errors
- 🟡 Medium — hydration mismatches, missing loading states
- 🟢 Low — minor issues

Exit code: 1 if any critical issues found, 0 otherwise.

## Fixing Hydration Issues (Next.js)

**Date.now()/new Date() in render:**
```tsx
// ❌ Bad — causes hydration mismatch
const now = Math.floor(Date.now() / 1000);

// ✅ Good — guard with isMounted
const [isMounted, setIsMounted] = useState(false);
useEffect(() => { setIsMounted(true); }, []);
const now = isMounted ? Math.floor(Date.now() / 1000) : 0;
```

**Math.random() in render:**
```tsx
// ❌ Bad — different on server vs client
<div style={{ left: `${Math.random() * 100}%` }} />

// ✅ Good — pre-generate in useState (runs once)
const [particles] = useState(() =>
  Array.from({ length: 10 }, () => ({
    left: `${Math.random() * 100}%`,
  }))
);
```

**window/document access:**
```tsx
// ❌ Bad — crashes during SSR
const width = window.innerWidth;

// ✅ Good — only after mount
const [width, setWidth] = useState(0);
useEffect(() => setWidth(window.innerWidth), []);
```
