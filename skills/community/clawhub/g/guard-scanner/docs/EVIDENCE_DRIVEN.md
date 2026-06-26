# Evidence-Driven Metrics

guard-scanner uses a **single source of truth (SSoT)** architecture for all public metrics. This ensures that numbers in README, documentation, and tests are always in sync with the implementation.

## Architecture

```
┌─────────────────────────────────────┐
│ Source Code (patterns.js, etc.)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ generate-capabilities.js           │
│ Generates: docs/spec/capabilities.json
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ capabilities.json (SSoT)            │
│ - static_pattern_count: 352         │
│ - threat_category_count: 32         │
│ - runtime_check_count: 26           │
│ - mcp_tools: [...]                  │
└──────┬───────────────────────┬──────┘
       │                       │
       ▼                       ▼
┌──────────────┐      ┌────────────────┐
│ generate-    │      │ verify-        │
│ readme-      │      │ capabilities.js│
│ metrics.js   │      │ (CI check)     │
└──────┬───────┘      └────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ README.md                           │
│ (Auto-updated metrics)              │
└─────────────────────────────────────┘
```

## Scripts

### 1. `generate-capabilities.js`

**Purpose:** Generate `docs/spec/capabilities.json` from source code.

**Runs:**
- Counts patterns from `src/patterns.js`
- Counts runtime checks from `src/runtime-guard.js`
- Lists MCP tools from `src/mcp-server.js`
- Reads versions from `package.json` and `openclaw.plugin.json`

**Usage:**
```bash
node scripts/generate-capabilities.js
```

**Output:** `docs/spec/capabilities.json`

### 2. `generate-readme-metrics.js`

**Purpose:** Inject metrics from `capabilities.json` into `README.md`.

**Updates:**
- Header metrics line (categories, patterns, checks)
- Dependency badge
- Capability table entries
- MCP tool descriptions

**Usage:**
```bash
# Update README
node scripts/generate-readme-metrics.js

# CI mode: fail if drift detected
node scripts/generate-readme-metrics.js --check
```

### 3. `generate-readme-stats.js`

**Purpose:** Inject test counts from `npm test` output into README.

**Updates:**
- Test badge: `tests-336%20passed`
- Test results block

**Usage:**
```bash
# Update README
node scripts/generate-readme-stats.js

# CI mode: fail if drift detected
node scripts/generate-readme-stats.js --check
```

### 4. `verify-capabilities.js`

**Purpose:** Verify all documentation matches `capabilities.json`.

**Checks:**
- README.md metrics
- README_ja.md metrics
- SKILL.md metrics
- package.json version
- openclaw.plugin.json version
- Test file count

**Usage:**
```bash
node scripts/verify-capabilities.js
# Exits 1 if any drift detected
```

## CI Integration

The CI workflow enforces zero-tolerance for drift:

```yaml
# .github/workflows/ci.yml
- name: Generate capabilities manifest
  run: node scripts/generate-capabilities.js

- name: Check README metrics drift
  run: |
    node scripts/generate-readme-metrics.js --check
    node scripts/generate-readme-stats.js --check

- name: Verify all capability claims
  run: node scripts/verify-capabilities.js
```

## Local Development

**Sync all README metrics:**
```bash
npm run sync:readme
```

This runs:
1. `generate-capabilities.js` (update SSoT)
2. `generate-readme-metrics.js` (update metrics)
3. `generate-readme-stats.js` (update test counts)

## Adding New Metrics

1. **Add to source code:** Update `patterns.js`, `runtime-guard.js`, etc.
2. **Update generator:** Edit `generate-capabilities.js` to extract new metric
3. **Update README generator:** Edit `generate-readme-metrics.js` to inject into README
4. **Update verifier:** Edit `verify-capabilities.js` to check for drift
5. **Run sync:** `npm run sync:readme`
6. **Commit changes:** Include updated `capabilities.json` and `README.md`

## Philosophy

**Why evidence-driven?**

- **Trust:** Users can verify claims match implementation
- **Marketing-first avoidance:** Numbers come from code, not marketing
- **Drift prevention:** CI blocks PRs with mismatched numbers
- **Single source of truth:** One canonical source (`capabilities.json`)
- **Audit trail:** All changes go through generators

**Zero tolerance for hardcoded numbers in public docs.**

## MCP Integration

The `get_stats` MCP tool reads from `capabilities.json`:

```javascript
function handleGetStats() {
    const runtimeStats = getCheckStats();
    return successResult(
        `🛡️ guard-scanner v${VERSION}\n\n` +
        `Static Analysis:\n` +
        `  • ${STATIC_SUMMARY}\n` +  // from capabilities.json
        `  • ${runtimeStats.total} checks across ${Object.keys(runtimeStats.byLayer).length} layers\n` +
        // ...
    );
}
```

This ensures MCP clients always get accurate, up-to-date metrics.
