---
title: Import Server/Worker from Correct Subpaths
impact: CRITICAL
description: Use `msw/node` for setupServer and `msw/browser` for setupWorker. Never import these from `msw`.
tags: setup, import, node, browser, subpath
---

# Import Server/Worker from Correct Subpaths

## Problem

Developers import `setupServer` from `'msw'` instead of `'msw/node'`. The top-level `'msw'` export only contains `http`, `graphql`, `HttpResponse`, etc.

## Incorrect

```typescript
// BUG: setupServer is not exported from 'msw'
import { setupServer } from 'msw'
```

## Correct

```typescript
// Node.js (tests, SSR)
import { setupServer } from 'msw/node'

// Browser (Storybook, development)
import { setupWorker } from 'msw/browser'

// Handlers and response utilities come from 'msw'
import { http, HttpResponse, graphql } from 'msw'
```

## Import Map

| Export | Import from |
|--------|-------------|
| `http`, `graphql`, `HttpResponse`, `delay`, `bypass`, `passthrough` | `'msw'` |
| `setupServer` | `'msw/node'` |
| `setupWorker` | `'msw/browser'` |

## Why

MSW v2 uses subpath exports to tree-shake correctly. Importing `setupServer` from `'msw'` produces an import error. The split ensures browser code doesn't bundle Node.js dependencies and vice versa.
