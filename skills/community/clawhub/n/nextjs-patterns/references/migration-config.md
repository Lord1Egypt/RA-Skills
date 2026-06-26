# Next.js 15 Migration & Configuration Guide

## Upgrading to Next.js 15

```bash
npx @next/codemod@canary upgrade latest
# or manual:
npm install next@latest react@latest react-dom@latest
```

## Key Breaking Changes (14 → 15)

### 1. Async Request APIs (Breaking)
`cookies()`, `headers()`, `params`, `searchParams` are now async:

```tsx
// Before (Next.js 14)
export default function Page({ params }) {
  const { id } = params
}

// After (Next.js 15)
export default async function Page({ params }) {
  const { id } = await params
}

// cookies and headers
import { cookies, headers } from "next/headers"
const cookieStore = await cookies()
const headersList = await headers()
```

### 2. Caching Defaults Changed
`fetch()` no longer caches by default (was `force-cache`, now `no-store`).
Add `{ cache: "force-cache" }` or set route-level `export const fetchCache = "default-cache"` to restore.

### 3. React 19 Compatibility
Next.js 15 supports React 19. New hooks available:
- `useActionState` (replaces `useFormState`)
- `useFormStatus`
- `use()` for reading promises/context

## next.config.ts (TypeScript config)

```ts
import type { NextConfig } from "next"

const config: NextConfig = {
  experimental: {
    ppr: "incremental",        // Partial Prerendering
    reactCompiler: true,       // React Compiler (auto-memoization)
  },
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "images.example.com" },
    ],
  },
  logging: {
    fetches: { fullUrl: true }, // Log all fetch calls in dev
  },
}

export default config
```

## Environment Variables

```bash
# .env.local
DATABASE_URL="postgresql://..."
NEXT_PUBLIC_API_URL="https://api.example.com"  # exposed to browser
```

```ts
// Access server-side
process.env.DATABASE_URL

// Access client-side (only NEXT_PUBLIC_ prefix)
process.env.NEXT_PUBLIC_API_URL
```

## Turbopack (Default in Dev)

```bash
next dev              # uses Turbopack by default in Next.js 15
next dev --turbopack  # explicit flag (same behavior)
next build            # Webpack still default for production builds
```

## TypeScript Path Aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"],
      "@/components/*": ["./components/*"],
      "@/lib/*": ["./lib/*"]
    }
  }
}
```
