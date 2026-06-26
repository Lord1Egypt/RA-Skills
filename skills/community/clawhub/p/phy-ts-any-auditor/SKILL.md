---
name: TypeScript Any Auditor
description: TypeScript `any` sprawl auditor and type-coverage enforcer. Scans your codebase for explicit `any` annotations, implicit `any` leaks (untyped parameters, untyped return values), and `@ts-ignore` / `@ts-expect-error` suppressions. Reports a type-coverage percentage score (powered by the `type-coverage` npm package), ranks files by `any` density so you know where to fix first, checks your tsconfig.json for weak safety settings (missing `strict`, `noImplicitAny`, `strictNullChecks`), and generates a `.type-coverage` budget file for CI enforcement. Zero external API — wraps `npx type-coverage` and `tsc`. Triggers on "too many anys", "type coverage", "typescript any audit", "tighten types", "enable strict mode", "any sprawl", "/ts-any-audit".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - typescript
    - type-safety
    - code-quality
    - static-analysis
    - developer-tools
    - strict-mode
    - type-coverage
    - refactoring
    - ci-cd
---

# TypeScript Any Auditor

`any` is TypeScript's escape hatch. One migration shortcut becomes permanent. One untyped third-party binding leaks into five files. Six months later you run `tsc --strict` and get 847 errors.

Paste a directory path and get a ranked audit: type-coverage percentage, files with the most `any` usage, specific lines to fix first, and a CI budget file to stop the bleeding.

**No setup. No TypeScript config changes. Works on any TypeScript project.**

---

## Trigger Phrases

- "too many anys", "any sprawl", "any audit", "type coverage"
- "typescript any check", "find all the anys", "where are my anys"
- "enable strict mode", "tighten my types", "type safety audit"
- "how strict is my TypeScript", "tsconfig audit", "noImplicitAny"
- "type-coverage report", "CI type budget"
- "/ts-any-audit"

---

## How to Provide Input

```bash
# Option 1: Audit the current directory
/ts-any-audit

# Option 2: Specific directory
/ts-any-audit src/
/ts-any-audit packages/api/

# Option 3: Show exact lines (verbose mode)
/ts-any-audit --detail

# Option 4: Set a passing threshold
/ts-any-audit --threshold 90
# Exits non-zero if type coverage is below 90%

# Option 5: Check a specific file
/ts-any-audit src/services/UserService.ts

# Option 6: Generate CI budget file and tsconfig fixes only
/ts-any-audit --fix-plan
```

---

## Step 1: Verify TypeScript Project

```bash
# Check this is a TypeScript project
if [ ! -f "tsconfig.json" ] && [ -z "$(find . -name '*.ts' -not -path '*/node_modules/*' | head -1)" ]; then
  echo "❌ No tsconfig.json or .ts files found"
  echo "Looking one level up..."
  ls -la **/tsconfig.json 2>/dev/null | head -5
  exit 1
fi

# Count TypeScript files
TS_FILE_COUNT=$(find . -name "*.ts" -o -name "*.tsx" \
  -not -path "*/node_modules/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/.next/*" \
  2>/dev/null | wc -l | tr -d ' ')

echo "Found $TS_FILE_COUNT TypeScript files to analyze"
```

---

## Step 2: Audit tsconfig.json Safety Settings

Before scanning code, check whether the TypeScript config is set up to catch `any` issues:

```bash
python3 -c "
import json, sys

try:
    with open('tsconfig.json') as f:
        config = json.load(f)
except FileNotFoundError:
    print('❌ tsconfig.json not found')
    sys.exit(1)

compiler = config.get('compilerOptions', {})

# Critical safety flags
checks = {
    'strict':              (compiler.get('strict', False),          '🔴 MISSING — enables noImplicitAny, strictNullChecks, and 6 others at once'),
    'noImplicitAny':       (compiler.get('noImplicitAny', False) or compiler.get('strict', False),
                                                                     '🟠 MISSING — untyped params silently become any'),
    'strictNullChecks':    (compiler.get('strictNullChecks', False) or compiler.get('strict', False),
                                                                     '🟠 MISSING — null/undefined bypass type checking'),
    'noImplicitReturns':   (compiler.get('noImplicitReturns', False), '🟡 MISSING — functions may return undefined implicitly'),
    'noUncheckedIndexedAccess': (compiler.get('noUncheckedIndexedAccess', False), '🟡 MISSING — array[i] may be undefined'),
    'exactOptionalPropertyTypes': (compiler.get('exactOptionalPropertyTypes', False), 'ℹ️ MISSING — optional props allow undefined assignment'),
}

print('tsconfig.json Safety Audit:')
print('=' * 50)
for flag, (enabled, message) in checks.items():
    status = '✅' if enabled else '❌'
    print(f'{status} {flag}: {\"ON\" if enabled else message}')

# Check for dangerous allowances
if compiler.get('noImplicitAny') == False and not compiler.get('strict'):
    print()
    print('⚠️  noImplicitAny is explicitly disabled — this is the most common any-sprawl cause')
if compiler.get('suppressImplicitAnyIndexErrors'):
    print('⚠️  suppressImplicitAnyIndexErrors is ON — index signatures silently return any')
if compiler.get('allowJs') and not compiler.get('checkJs'):
    print('🟡 allowJs=true but checkJs=false — JS files bypass type checking entirely')
"
```

---

## Step 3: Run type-coverage

The `type-coverage` npm package counts the ratio of typed identifiers to total identifiers:

```bash
# Run type-coverage (zero install — uses npx)
echo "Running type-coverage analysis..."
npx --yes type-coverage \
  --detail \
  --strict \
  --ignore-files "**/*.d.ts" \
  --ignore-files "**/__tests__/**" \
  --ignore-files "**/*.test.ts" \
  --ignore-files "**/*.spec.ts" \
  2>&1 | head -100

# For per-file breakdown
npx --yes type-coverage \
  --detail \
  --strict \
  --report-semantic-not-covered \
  2>&1 | grep -E "\.ts[x]?:" | sort -t: -k3 -rn | head -30
```

**What `type-coverage` measures:**
- Counts all TypeScript nodes (identifiers, parameters, return types, variable declarations)
- For each node, checks if its resolved type contains `any`
- Reports: `typed / total = coverage%`
- `--strict` mode: also counts nodes typed as `any` via type inference (not just explicit `any`)

---

## Step 4: Grep for `any` Patterns

Supplement `type-coverage` with direct source scanning for common patterns:

```bash
# Pattern 1: Explicit 'any' annotations
echo "=== Explicit 'any' ==="
grep -rn ": any" . \
  --include="*.ts" --include="*.tsx" \
  --exclude-dir="node_modules" --exclude-dir="dist" --exclude-dir=".next" \
  | grep -v "\.d\.ts:" \
  | grep -v "\.test\.\|\.spec\." \
  | wc -l | xargs echo "Count:"

# Pattern 2: 'any[]' and 'Array<any>'
echo "=== Arrays of any ==="
grep -rn "any\[\]\|Array<any>" . \
  --include="*.ts" --include="*.tsx" \
  --exclude-dir="node_modules" | wc -l | xargs echo "Count:"

# Pattern 3: Casts to any: 'as any'
echo "=== Casts to any ==="
grep -rn " as any" . \
  --include="*.ts" --include="*.tsx" \
  --exclude-dir="node_modules" | wc -l | xargs echo "Count:"

# Pattern 4: ts-ignore suppressions (each one hides a type error)
echo "=== @ts-ignore suppressions ==="
grep -rn "@ts-ignore" . \
  --include="*.ts" --include="*.tsx" \
  --exclude-dir="node_modules" | wc -l | xargs echo "Count:"

# Pattern 5: @ts-expect-error (intended, but track them)
echo "=== @ts-expect-error ==="
grep -rn "@ts-expect-error" . \
  --include="*.ts" --include="*.tsx" \
  --exclude-dir="node_modules" | wc -l | xargs echo "Count:"

# Pattern 6: Untyped function parameters (implicit any if noImplicitAny is off)
echo "=== Untyped parameters (potential implicit any) ==="
grep -rn "function.*([^)]*[a-zA-Z_][a-zA-Z0-9_]*\s*," . \
  --include="*.ts" --include="*.tsx" \
  --exclude-dir="node_modules" | \
  grep -v ":" | head -20
```

---

## Step 5: Rank Files by `any` Density

Find the highest-priority files to fix:

```bash
# Per-file any count — sorted by count descending
python3 -c "
import subprocess, os, re
from pathlib import Path
from collections import defaultdict

# Find all TS/TSX files
ts_files = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in {'node_modules', 'dist', '.next', 'build', '.git'}]
    for f in files:
        if f.endswith(('.ts', '.tsx')) and not f.endswith('.d.ts') and 'test' not in f and 'spec' not in f:
            ts_files.append(os.path.join(root, f))

counts = {}
for fpath in ts_files:
    try:
        content = Path(fpath).read_text()
        any_count = len(re.findall(r': any[^A-Za-z]|as any[^A-Za-z]|any\[\]|Array<any>|@ts-ignore', content))
        if any_count > 0:
            counts[fpath] = any_count
    except:
        pass

# Sort and print top 20
print('Top files by any usage:')
print(f'{\"File\":<60} {\"Count\":>6}')
print('-' * 68)
for fpath, count in sorted(counts.items(), key=lambda x: -x[1])[:20]:
    short_path = fpath.replace('./', '')
    print(f'{short_path:<60} {count:>6}')

print()
print(f'Total: {len(counts)} files with any usage | {sum(counts.values())} any occurrences')
"
```

---

## Step 6: Output Report

```markdown
## TypeScript Any Audit
Project: my-app | TypeScript files: 142 | Date: 2026-03-18

---

### Type Coverage Score

```
Type Coverage: 84.3% (12,847 typed / 15,238 total nodes)

Target:  90%  🔴 Below threshold
Current: 84.3%
Gap:     ~870 additional nodes need types to reach 90%
```

---

### tsconfig.json Safety Audit

| Flag | Status | Impact |
|------|--------|--------|
| `strict` | ❌ MISSING | Enables 8 strict checks at once |
| `noImplicitAny` | ❌ MISSING | Untyped params silently become `any` |
| `strictNullChecks` | ❌ MISSING | `null`/`undefined` bypass type checking |
| `noImplicitReturns` | ❌ MISSING | Functions may return `undefined` implicitly |
| `noUncheckedIndexedAccess` | ❌ MISSING | `arr[i]` can be `undefined` without warning |

**Quick Fix:** Add `"strict": true` to compilerOptions — this single flag enables all critical checks. Expect N new errors; treat each as a bug catch, not a build failure.

---

### `any` Usage Breakdown

| Pattern | Count | Risk |
|---------|-------|------|
| `: any` explicit | 47 | 🔴 Direct type erasure |
| `as any` casts | 23 | 🔴 Bypasses type checker |
| `any[]` / `Array<any>` | 12 | 🟠 Untyped collections |
| `@ts-ignore` | 8 | 🟠 Hides real errors |
| `@ts-expect-error` | 3 | 🟡 Tracked suppressions |
| **Total** | **93** | |

---

### Top Files to Fix First

| File | `any` Count | % of File | Quick Win? |
|------|------------|-----------|------------|
| `src/api/client.ts` | 18 | High | 🟢 Yes — API response types |
| `src/utils/transform.ts` | 14 | High | 🟢 Yes — add generic types |
| `src/components/DataTable.tsx` | 12 | Medium | 🟡 Props typing needed |
| `src/store/reducers/userReducer.ts` | 9 | Medium | 🟡 Redux state types |
| `src/lib/auth.ts` | 8 | Low | 🔴 Auth code — fix urgently |
| `src/services/EmailService.ts` | 7 | Low | 🟢 Yes — simple return types |

**Quick wins (fix 2-3 files, gain ~5% coverage):** `api/client.ts` and `utils/transform.ts` account for 34% of your `any` usage.

---

### Detailed Findings: src/api/client.ts

```typescript
// Line 14: untyped response
const response: any = await fetch(url);           // ❌ type: any

// Fix:
interface ApiResponse<T> {
  data: T;
  error?: string;
}
const response: ApiResponse<User> = await fetchJson<User>(url);

// Line 42: cast to bypass type check
const user = (data as any).user;                  // ❌ as any cast

// Fix:
interface LoginResponse { user: User; token: string; }
const parsed = data as LoginResponse;
const user = parsed.user;

// Line 67: implicit any parameter
function transform(item) { ... }                  // ❌ implicit any param

// Fix:
function transform(item: RawApiItem): ProcessedItem { ... }
```

---

### Hotspot: @ts-ignore Suppressions

```
src/lib/legacy-adapter.ts:88  // @ts-ignore — imported JS module has no types
src/components/Chart.tsx:134  // @ts-ignore — third-party lib missing declaration
src/api/websocket.ts:201      // @ts-ignore — TODO: fix this properly
src/utils/csv.ts:45           // @ts-ignore
src/hooks/useAuth.ts:12       // @ts-ignore
```

**@ts-ignore at `useAuth.ts:12` is in auth code — high priority.** Run `npx tsc --noEmit` and check what error it's hiding.

---

### Fix Priority Plan

**Phase 1 — Quick wins (1-2 hours, +6% coverage):**
1. `src/api/client.ts` — add generic type to fetch wrapper → fixes 18 anys downstream
2. `src/utils/transform.ts` — add input/output types to 4 functions
3. `src/lib/auth.ts` — resolve `@ts-ignore`, type the auth response

**Phase 2 — Medium effort (1 day, +5% coverage):**
4. `src/components/DataTable.tsx` — define Props interface with typed `columns` and `data`
5. `src/store/reducers/userReducer.ts` — type the Redux state and action types

**Phase 3 — Enable strict mode:**
6. Add `"noImplicitAny": true` to tsconfig first (less disruptive than full `strict`)
7. Fix the ~40 new errors it surfaces
8. Then add `"strictNullChecks": true`
9. Finally: `"strict": true`

---

### Generated CI Budget File

Save as `.type-coverage` in project root to enforce coverage in CI:

```json
{
  "atLeast": 85,
  "strict": true,
  "ignoreCatch": true,
  "ignoreFiles": ["**/*.d.ts", "**/*.test.ts", "**/*.spec.ts"]
}
```

Add to CI pipeline:
```bash
# In .github/workflows/ci.yml or equivalent:
- name: Check type coverage
  run: npx type-coverage --atLeast 85 --strict
```

Increment `atLeast` by 2% per sprint until you reach your target (typically 95%).

---

### Suppression Audit

When you can't immediately fix an `any`, use `@ts-expect-error` instead of `@ts-ignore`:

```typescript
// ❌ @ts-ignore — silently passes even when the error is fixed
// @ts-ignore
const x = thirdPartyLib.method(arg);

// ✅ @ts-expect-error — fails CI when the underlying error is fixed (tells you to remove the suppression)
// @ts-expect-error: ThirdPartyLib missing types — tracked in #123
const x = thirdPartyLib.method(arg);
```

Convert your 8 `@ts-ignore` to `@ts-expect-error` as the lowest-effort improvement.
```

---

## Quick Mode

Fast summary without line-by-line detail:

```
TypeScript Any Audit: my-app
Coverage: 84.3% (target: 90%) 🔴 Below threshold
- 93 any occurrences (47 explicit, 23 casts, 8 ts-ignore)
- Top file: src/api/client.ts (18 anys — fix this first)
- tsconfig: missing strict, noImplicitAny, strictNullChecks
- Quick win: fix api/client.ts + utils/transform.ts → +6% coverage

Run /ts-any-audit --detail for exact line numbers
```

---

## Migration Strategy: Zero to Strict

If starting from an untyped or loosely-typed codebase:

```bash
# Step 1: Measure baseline
npx type-coverage --strict

# Step 2: Add tsconfig strictness incrementally
# Week 1: "noImplicitAny": true
# Week 2: "strictNullChecks": true
# Week 3: "strict": true
# Week 4: "noUncheckedIndexedAccess": true

# Step 3: Set CI budget at current - 2% (prevent regression while improving)
# e.g., currently 84% → set --atLeast 82 in CI
# Next sprint: increase to 85%, then 88%, target 95%

# Step 4: Use @ts-expect-error instead of @ts-ignore for all remaining suppressions
# Each one must have a ticket number: // @ts-expect-error: see JIRA-1234

# Step 5: Fix suppressions over time; they fail CI when the issue is resolved
```

---

## Why `any` Matters

The TypeScript compiler's job is to prove your program is correct before it runs. Every `any` is a hole in that proof. When enough holes accumulate:

- Refactors break without compile-time warning
- null-dereferences reach production ("cannot read property 'x' of undefined")
- IDE autocompletion stops working on `any`-typed variables
- New team members lose context — no types = no documentation

Type coverage above 90% correlates strongly with fewer runtime type errors. Above 95%, TypeScript's guarantees become nearly complete.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
