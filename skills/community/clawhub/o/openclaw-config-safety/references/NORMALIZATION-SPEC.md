# NORMALIZATION-SPEC.md — Config Normalization Spec

**Owner:** SE (Staff Engineer)
**Reviewer:** TCF
**Status:** Phase 0 draft — pending TCF review
**Created:** 2026-04-18

---

## Purpose

Define what `normalizeOpenClawConfig()` does for every significant field in `openclaw.json`. The normalizer is a pre-validate pass that corrects trivial drift before the full Zod schema validation runs.

**Design philosophy:** Normalize only what is unambiguously correct. Fail on anything that requires judgment.

---

## Resolved Decisions (from RESOLUTIONS.md)

- Normalize trivial drift only: trim whitespace, type coerce strings→booleans/numbers
- **FAIL LOUDLY** on missing required fields — never silently fill with defaults
- Model alias normalization: informational only, read-only mapping
- Unknown fields: pass-through (don't reject)

---

## Field Taxonomy

### Category A — String Fields (trim whitespace)

| Field path | Normalization rule | Rationale |
|-----------|-------------------|-----------|
| `agents.defaults.model` | Trim whitespace | Free-form model ID string |
| `agents.defaults.workspace` | Trim trailing slashes only | Path — trailing slash meaningful on some FS |
| `agents.defaults.models[<key>].alias` | Trim whitespace | User-defined alias string |
| `models.providers[<provider>].apiKey` | **DO NOT NORMALIZE** | API keys are opaque; trimming could corrupt |
| `models.providers[<provider>].baseURL` | Trim leading/trailing whitespace | URL whitespace is never meaningful |
| `gateway.bind` | Trim whitespace | Host/port string |
| `gateway.remoteUrl` | Trim whitespace | URL string |
| `plugins.entries[<key>]` (string value) | Trim whitespace | Config paths, enable flags |

**Fields to pass through untouched (no trim):**
- `models.providers[<provider>].apiKey` — opaque tokens, whitespace may be significant
- Any field whose value is a cryptographic hash, token, or secret

---

### Category B — Boolean Coercion (string → boolean)

| Field path | Coercion rule | Rationale |
|-----------|--------------|-----------|
| `agents.defaults.compaction.enabled` | `"true"`→`true`, `"false"`→`false` | JSON round-trip can stringify |
| `agents.defaults.memorySearch.enabled` | `"true"`→`true`, `"false"`→`false` | Same |
| `models.providers[<provider>].enabled` | `"true"`/`"false"`→boolean | Provider toggle |
| `plugins.allow[<plugin>]` | N/A — already array of booleans | Not applicable |
| `plugins.entries[<key>].enabled` | `"true"`/`"false"`→boolean | Plugin toggle |

**Coercion rules:**
- `"true"` (string) → `true` (boolean)
- `"false"` (string) → `false` (boolean)
- `true` / `false` → unchanged
- `"1"`, `"yes"` → **DO NOT COERCE** — too ambiguous
- `null`, `undefined` → leave as-is (let Zod catch missing required fields)

---

### Category C — Number Coercion (string → number)

| Field path | Coercion rule | Rationale |
|-----------|--------------|-----------|
| `agents.defaults.timeoutSeconds` | Parse integer string | Timeout values often stringify |
| `agents.defaults.compaction.threshold` | Parse integer string | Same |
| `agents.defaults.bootstrapMaxChars` | Parse integer string | Size limit |
| `gateway.port` | Parse integer string | Port number |
| `models.providers[<provider>].input`< 1 char | **DO NOT COERCE** | Cost fields are floats, not integers |
| `models.providers[<provider>].contextWindow` | Parse integer string | Token counts |

**Coercion rules:**
- `"123"` → `123` (integer)
- `"123.45"` → `123.45` (float)
- Non-numeric strings (`"abc"`, `""`) → **DO NOT COERCE**, leave as-is
- `NaN`, `Infinity` → **DO NOT COERCE**, leave as-is
- Numbers outside safe integer range → flag as warning but don't reject

---

### Category D — Array Fields (pass-through)

Arrays are passed through untouched. The normalizer does not reorder, dedupe, or filter arrays.

Exception: if an array contains non-string elements where strings are expected (e.g., model arrays with numbers), surface a warning but don't mutate.

---

### Category E — Object Fields (deep pass-through)

Nested objects are traversed recursively. The normalizer does not restructure objects, merge keys, or fill defaults.

**Traversal rule:** Recurse into known object paths. Pass through unknown object keys without modification.

---

## Required Fields

If any of these top-level fields are **absent**, the normalizer **must fail** with a clear error:

| Required field | Error message |
|---------------|--------------|
| `agents` | `openclaw.json is missing required top-level field: agents` |
| `models` | `openclaw.json is missing required top-level field: models` |
| `plugins` | `openclaw.json is missing required top-level field: plugins` |

**If a required field is present but empty (`{}` or `null`):**
- Let Zod validation handle it — the normalizer does not fill defaults
- Surface as: `WARNING: agents is present but empty; this may cause runtime issues`

**If a required nested field is missing:**
- Do not fill with defaults
- Let Zod catch it
- Example: `agents.defaults.models` missing → normalizer passes through; Zod fails

---

## Model Alias Normalization (Informational Only)

The normalizer maintains a **read-only** alias → canonical ID mapping. On detection:

```
Input alias:  "deepseek-r1-distill-qwen-32b"
Canonical:    "nvidia/deepseek-ai/deepseek-r1-distill-qwen-32b"
Action:       Surface as INFO, do not rewrite
```

**Alias mapping table (canonical → known aliases):**

| Canonical ID | Known aliases |
|-------------|--------------|
| `nvidia/deepseek-ai/deepseek-r1-distill-qwen-32b` | `deepseek-r1-32b`, `deepseek-r1` |
| `minimax/MiniMax-M2.7` | `minimax-m2.7`, `m2.7` |
| `nvidia/llama-3.2-1b-instruct` | `llama-1b`, `llama3.2-1b` |
| `zai/glm-4.7` | `glm-4.7`, `glm4.7` |

**Output format:**
```javascript
{
  normalized: <config>,
  aliasInfo: [
    { field: "agents.defaults.model", alias: "deepseek-r1-32b", canonical: "nvidia/deepseek-ai/..." }
  ]
}
```

The `aliasInfo` array is informational only. The config is returned unchanged except for whitespace/type fixes.

---

## What NOT to Touch

1. **`status` or `note` fields** in per-model overrides — these are known-crash fields; the validator handles them
2. **Any field with value starting with `secret://`** — external secret references, opaque to normalizer
3. **Custom plugin config blobs** (`plugins.entries[<plugin>]` objects) — pass through untouched
4. **`env` subtrees** — environment-specific overrides, opaque

---

## Error Handling

All normalization errors must:
- Be thrown, not logged silently
- Include the field path (e.g., `agents.defaults.models["foo"].timeoutSeconds`)
- **Never include the field value** (credential exposure risk)
- Include a human-readable reason

```javascript
// Example error
throw new NormalizationError(
  "agents.defaults.timeoutSeconds: cannot coerce string 'abc' to number — not a valid number"
);
```

**Error class:**
```javascript
class NormalizationError extends Error {
  constructor(field, message) {
    super(`normalizeOpenClawConfig: ${field}: ${message}`);
    this.name = "NormalizationError";
    this.field = field; // NOT the value — path only
  }
}
```

---

## Edge Cases

| Input | Expected behavior |
|-------|------------------|
| `null` | Pass through as-is |
| `undefined` | Remove from parent object (let Zod catch missing) |
| `""` (empty string) | Pass through — empty is a valid value |
| `"   "` (whitespace only) | Trim to `""` |
| `NaN` | Pass through as-is |
| `Infinity` | Pass through as-is |
| `-Infinity` | Pass through as-is |
| `1e308` (near overflow) | Pass through with WARNING |
| `[]` (empty array) | Pass through untouched |
| `{}` (empty object) | Pass through untouched |
| `["a", "b"]` (array of strings) | Pass through untouched |
| Very long strings (>1MB) | Truncate at 1MB with WARNING |
| Circular references | Detect and throw `NormalizationError: circular reference at <path>` |
| Deeply nested objects (>50 levels) | Warn and pass through (potential stack overflow) |

---

## Security Considerations

1. **No credential exposure in errors** — field paths only, never values
2. **API keys are not trimmed or coerced** — treated as opaque
3. **Token values never logged** — debug output must sanitize values with `REDACTED( length )`
4. **No execution of field values** — normalization is pure data transformation, no eval

---

## API Surface

```javascript
// normalize(config: object) => { normalized: object, aliasInfo: AliasInfo[], warnings: string[] }
function normalizeOpenClawConfig(config) { ... }

// normalizeFile(path: string) => Promise<NormalizedResult>
async function normalizeFile(path) { ... }
```

**Return shape:**
```typescript
interface NormalizedResult {
  normalized: OpenClawConfig;       // The normalized config
  aliasInfo: AliasInfo[];           // Informational alias detections
  warnings: string[];               // Non-fatal issues (coercion failures, etc.)
  changed: boolean;                // true if any normalization was applied
}
```

---

## Phase 1 Implementation Files

- `src/normalize.js` — core function
- `src/alias-map.js` — canonical alias mapping table
- `src/errors.js` — NormalizationError class
- `test/normalize.test.js` — comprehensive unit tests
