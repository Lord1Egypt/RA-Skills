---
name: Flag Janitor
description: Dead feature flag detector and cleanup planner. Scans source code and config files to find feature flags that are permanently-on, permanently-off, referenced but never defined, or defined but never used. Supports LaunchDarkly, Unleash, Flagsmith, environment-variable flags, and custom boolean flag patterns. Produces a prioritized cleanup report with exact code locations and safe-to-delete confirmation commands. Zero external API — works entirely from local files and git history. Triggers on "dead feature flags", "clean up flags", "feature flag audit", "remove old flags", "flag cleanup", "/flag-janitor".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - feature-flags
    - cleanup
    - technical-debt
    - dead-code
    - launchdarkly
    - unleash
    - developer-tools
    - refactoring
---

# Flag Janitor

Feature flags accumulate silently. A codebase that started with 5 flags for a safe launch ends up with 50 a year later — half of them permanently on, never cleaned up, making every code review harder and every new developer more confused.

Paste a directory path and get back every dead flag, where it lives, and the exact refactor needed to remove it safely.

**Supports any flag system. Zero external API. Works entirely from your local codebase.**

---

## Trigger Phrases

- "dead feature flags", "clean up feature flags", "feature flag audit"
- "remove old flags", "stale flags", "flag cleanup", "flag debt"
- "hardcoded feature flags", "always-on flags", "obsolete flags"
- "LaunchDarkly cleanup", "Unleash cleanup", "feature toggle debt"
- "/flag-janitor"

---

## How to Provide Input

```bash
# Option 1: Audit the current directory
/flag-janitor

# Option 2: Specific directory
/flag-janitor src/

# Option 3: With config file
/flag-janitor --config feature-flags.yaml

# Option 4: Specific flag system
/flag-janitor --system launchdarkly
/flag-janitor --system env-var
/flag-janitor --system custom --pattern "isFeatureEnabled\("

# Option 5: Single flag investigation
/flag-janitor --check ENABLE_NEW_CHECKOUT
```

---

## Step 1: Detect Flag System

Identify which flag system(s) are in use by scanning for SDK signatures:

```bash
# LaunchDarkly
grep -r "variation\|boolVariation\|LDClient\|ldclient" . \
  --include="*.ts" --include="*.js" --include="*.py" --include="*.go" \
  --include="*.rb" --include="*.java" -l 2>/dev/null | head -5

# Unleash
grep -r "isEnabled\|getVariant\|UnleashClient\|unleash" . \
  --include="*.ts" --include="*.js" --include="*.py" -l 2>/dev/null | head -5

# Flagsmith
grep -r "hasFeature\|getValue\|Flagsmith" . \
  --include="*.ts" --include="*.js" --include="*.py" -l 2>/dev/null | head -5

# Environment-variable flags (most common pattern)
grep -rE "process\.env\.[A-Z_]+(_FLAG|_ENABLED|_FEATURE|_TOGGLE)" . \
  --include="*.ts" --include="*.js" --include="*.mjs" -h 2>/dev/null | \
  grep -oE "[A-Z_]+(_FLAG|_ENABLED|_FEATURE|_TOGGLE)" | sort -u

grep -rE "os\.environ\.get\(['\"][A-Z_]+(_FLAG|_ENABLED|_FEATURE)['\"]" . \
  --include="*.py" -h 2>/dev/null | \
  grep -oE "[A-Z_]+(_FLAG|_ENABLED|_FEATURE)" | sort -u

# Custom boolean pattern (e.g., flags.isEnabled('my-flag'))
grep -rE "(flags|featureFlags|features)\.(isEnabled|get|check)\(['\"]([a-zA-Z-_]+)['\"]" . \
  --include="*.ts" --include="*.js" -h 2>/dev/null | \
  grep -oE "['\"]([a-zA-Z-_]+)['\"]" | tr -d "'" | tr -d '"' | sort -u
```

---

## Step 2: Build the Flag Registry

Collect every flag defined in config files:

### LaunchDarkly
```bash
# Local flag definitions (if using local config/fallback)
find . -name "*.json" -not -path "*/node_modules/*" | \
  xargs grep -l "variations\|flagKey\|rollout" 2>/dev/null | head -10

# SDK initialization file
grep -rn "variation\|allFlagsState" . --include="*.ts" --include="*.js" | \
  grep -oE "['\"][a-z][a-z0-9-_]+['\"]" | tr -d "'" | tr -d '"' | sort -u
```

### Environment-variable flags
```bash
# From .env files
grep -hE "^[A-Z_]+(_FLAG|_ENABLED|_FEATURE|_TOGGLE)=" .env* 2>/dev/null | \
  cut -d= -f1 | sort -u

# From .env.example
grep -hE "^[A-Z_]+(_FLAG|_ENABLED|_FEATURE|_TOGGLE)=" .env.example 2>/dev/null | \
  cut -d= -f1 | sort -u
```

### Custom YAML/JSON config
```bash
find . -name "flags.yaml" -o -name "feature-flags.json" -o -name "toggles.yaml" \
  -not -path "*/node_modules/*" 2>/dev/null | \
  xargs grep -hE "^  [a-z][a-z0-9-_]+:" 2>/dev/null | \
  sed 's/://g' | tr -d ' ' | sort -u
```

---

## Step 3: Classify Every Flag

For each flag found, determine its status:

### Class A: PERMANENTLY-ON (hardcoded true)

```bash
# Flags forced to always evaluate as true
grep -rn "ENABLE_NEW_UI.*=.*true\|ENABLE_NEW_UI.*===.*true\|ENABLE_NEW_UI.*!==.*false" . \
  --include="*.ts" --include="*.js" --include="*.py" | head -20

# Flags where the fallback value IS the flag value (never varies)
# Pattern: boolVariation('flag-key', true) where false branch is dead code
grep -rn "variation.*true.*true\|boolVariation.*,\s*true" . 2>/dev/null | head -10
```

### Class B: PERMANENTLY-OFF (hardcoded false / always disabled)

```bash
grep -rn "ENABLE_.*=.*false\|ENABLE_.*===.*false" . \
  --include="*.ts" --include="*.js" --include="*.py" 2>/dev/null | head -20

# Also: flags that always return the off-state default
grep -rn "variation.*false.*false\|boolVariation.*,\s*false" . 2>/dev/null | head -10
```

### Class C: REFERENCED BUT UNDEFINED (will crash / silently fail)

```bash
# Build two sets: flags referenced in code vs flags defined in config
# Then: code_flags - config_flags = referenced but undefined
```

Cross-reference:
- All flag names extracted from source code (Step 1)
- All flag names extracted from config files (Step 2)
- Flags in set A but not set B → **MISSING from config** → crashes or silently fails

### Class D: DEFINED BUT UNREFERENCED (dead config entries)

Flags in config but never referenced in source code. Pure dead weight — no code path uses them.

### Class E: TEST-ONLY (appears in tests, never in production code)

```bash
# Flag referenced only in test files
for flag in $ALL_FLAGS; do
  PROD_REFS=$(grep -rl "$flag" src/ lib/ app/ 2>/dev/null | grep -v "test\|spec" | wc -l)
  TEST_REFS=$(grep -rl "$flag" . 2>/dev/null | grep -E "test|spec" | wc -l)
  [ "$PROD_REFS" -eq 0 ] && [ "$TEST_REFS" -gt 0 ] && echo "$flag: test-only"
done
```

### Class F: RECENTLY ADDED (< 30 days) — skip

```bash
# Don't recommend deleting flags added in last 30 days — they may still be rolling out
git log --since="30 days ago" --diff-filter=A --name-only --format="" -- "*.ts" "*.js" "*.py" | \
  grep -E "(flag|feature|toggle)" | head -10
```

---

## Step 4: Staleness Check

For each non-Class-F flag, determine how long it has been unchanged:

```bash
# When was this flag's surrounding code last modified?
git log --follow -n1 --format="%ar" -- "$(grep -rl 'ENABLE_NEW_CHECKOUT' src/ | head -1)"

# How long has the flag been in its current state (on/off)?
git log --all --oneline -- .env | grep "ENABLE_NEW_CHECKOUT" | tail -1
```

Flag age tiers:
- < 30 days: **Active** — skip
- 30-90 days: **Aging** — watch list
- 90-180 days: **Stale** — review recommended
- > 180 days: **Dead** — safe to remove with test coverage

---

## Step 5: Output Report

```markdown
## Flag Janitor Report
Project: [name] | $(date) | System: env-var + custom
Flags analyzed: 42 | Dead flags found: 18 | Estimated LOC to remove: ~340

### Summary

| Category | Count | Action |
|----------|-------|--------|
| 🔴 Permanently-ON (hardcoded true) | 7 | Remove flag + keep enabled branch |
| 🔴 Permanently-OFF (hardcoded false) | 3 | Remove flag + delete disabled branch |
| 🟠 Referenced but undefined | 2 | Define in config OR remove from code |
| 🟡 Defined but unreferenced | 4 | Remove from config |
| 🟡 Test-only | 2 | Remove from both tests and config |
| ⚪ Active (< 30 days) | 12 | Skip |
| ✅ Live (varies in production) | 12 | Keep |

---

### 🔴 PERMANENTLY-ON — Remove the flag, keep the behavior

These flags always evaluate to `true`. The feature is always enabled. Remove the flag and
inline the enabled code path.

**`ENABLE_NEW_CHECKOUT`** (185 days old)
- Defined in: `.env.production=true`, `.env.staging=true`, `.env.example=true`
- Referenced in: `src/checkout/CheckoutPage.tsx:14`, `src/cart/CartSummary.tsx:88`
- Status: Always `true` across all environments for 185 days

Safe to remove — inline the `true` branch:
```typescript
// Before:
if (process.env.ENABLE_NEW_CHECKOUT === 'true') {
  return <NewCheckout />;
} else {
  return <LegacyCheckout />;
}

// After (delete flag + legacy branch):
return <NewCheckout />;
```

Files to update: `src/checkout/CheckoutPage.tsx`, `src/cart/CartSummary.tsx`, `.env*` files

---

**`ENABLE_SEARCH_V2`** (211 days old)
- Referenced in: `src/search/SearchBar.tsx:22`, `src/pages/Results.tsx:67`
- Status: `true` in all environments, never been `false` since day 45

---

### 🔴 PERMANENTLY-OFF — Remove flag + delete the dead branch

**`ENABLE_BETA_PRICING`** (290 days old)
- Always `false` since being disabled 290 days ago
- Code inside the `true` branch has never run in production
- Referenced in: `src/pricing/PricingPage.tsx:103`

Safe to remove — delete the flag and the entire `true` branch (dead code):
```typescript
// Before:
if (process.env.ENABLE_BETA_PRICING === 'true') {
  return <BetaPricing />;  // ← delete this
}
return <StandardPricing />;

// After:
return <StandardPricing />;
```

---

### 🟠 REFERENCED BUT UNDEFINED — Will silently fail or crash

**`ENABLE_SMART_RECOMMENDATIONS`**
- Referenced in: `src/recommendations/Engine.ts:45`, `src/home/HomePage.tsx:112`
- Defined in: **NOWHERE** — not in `.env`, `.env.example`, or config files
- Risk: `process.env.ENABLE_SMART_RECOMMENDATIONS` evaluates to `undefined`, likely behaving as `false` unintentionally

Fix: Add to `.env.example` with explicit value:
```bash
# Recommendations engine (set to 'true' when ready to enable)
ENABLE_SMART_RECOMMENDATIONS=false
```

---

### 🟡 DEFINED BUT UNREFERENCED — Dead config entries

These flags exist in config but no code reads them:

| Flag | Defined In | Last Modified | Safe to Delete? |
|------|-----------|--------------|----------------|
| `ENABLE_OLD_ANALYTICS` | `.env.example` | 320 days ago | ✅ Yes |
| `FEATURE_DARK_MODE_BETA` | `flags.yaml:14` | 180 days ago | ✅ Yes |
| `ENABLE_V1_API_COMPAT` | `.env.production` | 8 days ago | ⚠️ Wait (recent) |
| `EXPERIMENTAL_EDITOR` | `flags.yaml:28` | 95 days ago | 🟡 Review first |

---

### Cleanup Commands

```bash
# 1. Remove permanently-on flags (keep enabled branch)
# Manual: edit each file listed above

# 2. Remove dead config entries
grep -v "ENABLE_OLD_ANALYTICS\|FEATURE_DARK_MODE_BETA" .env.example > .env.example.tmp
mv .env.example.tmp .env.example

# 3. Remove from flags.yaml
# Edit manually — remove lines 14 and 28

# 4. Confirm after cleanup
grep -rn "ENABLE_OLD_ANALYTICS\|ENABLE_BETA_PRICING\|ENABLE_SEARCH_V2" . \
  --include="*.ts" --include="*.js" --include="*.env*" 2>/dev/null
# Should return zero results
```

---

### Estimated Impact After Cleanup

| Metric | Before | After |
|--------|--------|-------|
| Conditional branches from flags | 42 | 24 |
| Lines of dead code | ~340 | 0 |
| Flags to maintain | 42 | 24 |
| `.env.example` entries | 38 | 32 |
```

---

## Safe Removal Checklist

Before deleting any flag:

```
□ Flag is permanently-on or permanently-off for > 90 days
□ Git log confirms no recent changes to flag value
□ Test suite covers the branch that will remain
□ No pending PR branches reference this flag
□ Flag is not mentioned in any open issue/ticket
□ Remove from: source code, .env files, .env.example, config YAML, test files
□ Run tests after removal
```

---

## Quick Mode

Fast count without full analysis:

```
Flag Janitor Quick Scan:
🔴 7 permanently-on  🔴 3 permanently-off
🟠 2 undefined       🟡 4 dead config entries

Total removable: 16 flags (~280 LOC)
Run /flag-janitor for full report with file locations
```

---

## Why Flags Don't Get Cleaned Up

The standard lifecycle is:
1. Engineer adds flag for safe rollout
2. Flag ships to 100% of users
3. **Engineer meant to remove it "next sprint"**
4. "Next sprint" never comes
5. 6 months later, 8 engineers are reading `if (ENABLE_NEW_UI)` wondering if it's safe to delete

This skill automates step 4: it proves a flag is safe to delete (permanently-on/off + old enough) and generates the exact edit needed, reducing the removal from a 30-minute "is it safe?" investigation to a 2-minute confirmation.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
