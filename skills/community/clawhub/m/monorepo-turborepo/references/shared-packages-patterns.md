# Shared Packages Patterns in Turborepo

## Package Types

### 1. UI Component Library (packages/ui)

```tsx
// packages/ui/src/button.tsx
import * as React from "react";

export interface ButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}

export function Button({
  children,
  variant = "primary",
  size = "md",
  onClick,
  disabled = false,
  className,
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant} btn-${size} ${className ?? ""}`}
    >
      {children}
    </button>
  );
}
```

```json
// packages/ui/package.json
{
  "name": "@repo/ui",
  "version": "0.0.1",
  "private": true,
  "main": "./src/index.tsx",
  "types": "./src/index.tsx",
  "exports": {
    ".": "./src/index.tsx",
    "./button": "./src/button.tsx",
    "./card": "./src/card.tsx"
  },
  "scripts": {
    "lint": "eslint src/ --max-warnings 0",
    "type-check": "tsc --noEmit"
  },
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

### 2. Utility Library (packages/utils)

```ts
// packages/utils/src/format.ts
export function formatDate(date: Date, locale = "zh-CN"): string {
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}

export function formatCurrency(
  amount: number,
  currency = "CNY",
  locale = "zh-CN"
): string {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
  }).format(amount);
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^\w-]+/g, "")
    .replace(/--+/g, "-")
    .trim();
}
```

### 3. Database Package (packages/database)

```ts
// packages/database/src/client.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log:
      process.env.NODE_ENV === "development"
        ? ["query", "error", "warn"]
        : ["error"],
  });

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}

export * from "@prisma/client";
```

```json
// packages/database/package.json
{
  "name": "@repo/database",
  "version": "0.0.1",
  "private": true,
  "main": "./src/client.ts",
  "scripts": {
    "build": "prisma generate",
    "db:push": "prisma db push",
    "db:migrate": "prisma migrate dev"
  }
}
```

## Consuming Shared Packages in Apps

```tsx
// apps/web/app/page.tsx
import { Button } from "@repo/ui/button";
import { formatDate } from "@repo/utils";
import { prisma } from "@repo/database";

export default async function Page() {
  const users = await prisma.user.findMany();
  return (
    <div>
      {users.map((u) => (
        <div key={u.id}>
          <p>{u.name} — {formatDate(new Date(u.createdAt))}</p>
          <Button variant="secondary">View Profile</Button>
        </div>
      ))}
    </div>
  );
}
```

## Versioning Strategy

| Strategy | When to Use |
|----------|-------------|
| `workspace:*` | Internal packages, always latest |
| Fixed version | External consumers, stable API |
| Changesets | Publishing to npm registry |

```bash
# Using changesets for versioning
npx changeset init
npx changeset add        # Create a changeset
npx changeset version    # Bump versions
npx changeset publish    # Publish to npm
```
