# EXPORT-TOKEN-SPEC.md — Export/Import Token Spec

**Owner:** TCF (Technical Co-Founder)
**Reviewer:** SE (security review)
**Status:** Phase 0 draft — pending SE security review
**Created:** 2026-04-18

---

## Purpose

Define the export/import token format and security model for config-safety-v2. Tokens encode a normalized OpenClaw config in a safe, shareable, self-contained string.

**Design philosophy:** Tokens are safe to share. No credentials, no secrets, no risk from Slack/GitHub/email exposure.

---

## Resolved Decisions (from RESOLUTIONS.md)

- Credentials **MUST NOT** be in the token. Token contains `${KEY}` style references only.
- Importer resolves from env vars or `pass`. On failure → **abort with clear error** (no silent fallback).
- Token format: `mrconf:v1:base64url(json with credential references)`
- No compression in v1 (keep it simple — compression is a future optimization)

---

## Token Format

### Structure

```
mrconf:v1:<base64url-encoded-json>
```

| Component | Description |
|-----------|-------------|
| `mrconf` | Prefix — identifies this as an OpenClaw config token |
| `v1` | Version — allows format evolution |
| `<base64url-encoded-json>` | Normalized config with credential references |

### Encoding

- **Base64url** (URL-safe base64): `+` → `-`, `/` → `_`, no padding `=`
- Charset: `A-Z a-z 0-9 - _`

### JSON Shape (before encoding)

```typescript
interface ConfigToken {
  version: 1;
  exportedAt: string;        // ISO 8601 UTC
  normalizerVersion: string; // e.g., "1.0.0" — version of normalize.js used
  config: {
    // Normalized openclaw.json — credential references NOT replaced
    // References are ${ENV_VAR_NAME} style
    [key: string]: unknown;
  };
  credentialRefs: string[]; // List of all ${REF} placeholders in config
}
```

### Credential Reference Syntax

Within the config JSON, credential references use the following syntax:

```javascript
// In the exported JSON:
{
  "models": {
    "providers": {
      "cerebras": {
        "apiKey": "${CEREBRAS_API_KEY}"   // Reference — NOT the actual key
      }
    }
  }
}

// In a config token (string value starts with ${
```

**Reference regex:** `^\$\{([A-Z_][A-Z0-9_]*)\}$`

Only all-caps `ENV_VAR` style names are valid references. This prevents confusion with template literals or other `$` usages.

---

## Export Process

### `exportConfigToken(config: object): string`

1. **Normalize** the config: `normalizeOpenClawConfig(config)` → `normalizedConfig`
2. **Extract** all credential references from `normalizedConfig`:
   - Walk all string values
   - Match regex `^\$\{[A-Z_][A-Z0-9_]*\}$`
   - Collect all unique matches into `credentialRefs[]`
3. **Build** token payload:
   ```javascript
   {
     version: 1,
     exportedAt: new Date().toISOString(),
     normalizerVersion: "1.0.0",
     config: normalizedConfig,
     credentialRefs: uniqueMatches
   }
   ```
4. **Encode** with base64url (no padding)
5. **Prepend** `mrconf:v1:`
6. **Return** the final token string

### What Gets Exported

- **Normalized config** (whitespace trimmed, types coerced)
- **Credential references** as-is (e.g., `${CEREBRAS_API_KEY}`)
- **No actual credentials** — env vars, pass entries, or hardcoded values are never in the token

### What Does NOT Get Exported

- Actual API keys (even if present in the input config)
- Session state
- Temporary files
- File paths that are machine-specific

---

## Import Process

### `importConfigToken(token: string): object`

1. **Parse prefix:** Ensure token starts with `mrconf:v1:`. If wrong prefix → throw `TokenFormatError`.
2. **Decode base64url:** Extract JSON payload. If decode fails → throw `TokenDecodeError`.
3. **Parse JSON:** `JSON.parse(payload)`. If fails → throw `TokenJSONError`.
4. **Validate schema:**
   - `version === 1` — if not, throw `TokenVersionError` (future versions may have different decode rules)
   - `exportedAt` is valid ISO 8601
   - `config` is a plain object
   - `credentialRefs` is an array of strings
5. **Resolve credential references:**
   ```
   For each ref in credentialRefs[]:
     value = process.env[ref]        // Try env var first
     if value === undefined:
       value = runPassShow(ref)       // Try pass (key = ref name, e.g., "cerebras/apikey")
     if value === undefined:
       throw CredentialMissingError(`${ref}: not found in env vars or pass`)
   ```
6. **Substitute** references in `config`:
   - Walk all string values
   - Replace `${REF}` with resolved value
7. **Validate substituted config** against Zod schema (run validator)
8. **Return** the final config object

### pass Resolution Details

- Pass keys use the reference name directly: `${CEREBRAS_API_KEY}` → `pass show cerebras/apikey`
- The `pass` binary must be available on the system
- If `pass` is not installed → skip pass lookup, fall through to error
- If pass lookup fails → throw `CredentialMissingError` (do NOT use empty string)

### Failure Modes

| Error | Cause | User message |
|-------|-------|--------------|
| `TokenFormatError` | Wrong prefix or corrupt token | `Invalid token format — expected mrconf:v1:...` |
| `TokenDecodeError` | Base64 decode failure | `Token is corrupt — could not decode` |
| `TokenJSONError` | JSON parse failure | `Token is corrupt — invalid JSON` |
| `TokenVersionError` | Unknown version | `Token version not supported — found v{N}, supported: v1` |
| `CredentialMissingError` | Env/pass doesn't have the key | `${REF}: credential not found. Set ${REF} in env or add to pass.` |

**No silent fallbacks.** Any failure aborts with a clear error.

---

## Security Constraints

1. **No credentials in token** — enforced by export process (API keys in config are never placed in token; only `${REF}` placeholders are)
2. **Token is safe to share** — can be pasted in Slack, email, GitHub issues, Discord
3. **No credential leakage in errors** — error messages include the ref name (`${REF}`) but never the resolved value
4. **Import validates before substitution** — malformed tokens can't cause injection
5. **JSON.parse only** — no `eval`, `Function`, or other code execution
6. **Reference regex is strict** — only `^[A-Z_][A-Z0-9_]*$` inside `${}` — prevents injection via crafted ref names

---

## Round-Trip Guarantee

**Property:** `importConfigToken(exportConfigToken(config))` produces a config identical to the input (modulo normalization).

**Caveat:** If the input config contains **actual API keys** (not references), the exported token will contain `${PLACEHOLDER}` references instead. The round-trip will **not** restore the original keys — it will restore **references**.

**Implication:** Users who export must ensure the destination machine has the same credential references resolved. This is intentional — actual keys should never be in the token.

---

## Validation Checklist (Import)

Before accepting a token, verify:
- [ ] Prefix is `mrconf:v1:`
- [ ] Base64url decodes without error
- [ ] JSON parses to object
- [ ] `version === 1`
- [ ] `exportedAt` is valid ISO 8601
- [ ] `config` is a plain object
- [ ] `credentialRefs` is an array of strings
- [ ] All `credentialRefs` resolve in env or pass (or fail with clear error)
- [ ] Final config passes Zod schema validation

---

## Version Evolution

If the token format needs to change in a future v2+:

1. **Increment version** in the prefix: `mrconf:v2:...`
2. **Add migration logic** in import:
   ```javascript
   if (token.version === 1) { /* v1 decode logic */ }
   elseif (token.version === 2) { /* v2 decode logic */ }
   else { throw new TokenVersionError(...) }
   ```
3. **Keep v1 decode logic** for backward compatibility
4. **New exports** always use the latest version

v1 tokens never auto-upgrade — they are decoded as v1 forever.

---

## Phase 2 Implementation Files

- `src/export.js` — `exportConfigToken(config)` → token string
- `src/import.js` — `importConfigToken(token)` → config object
- `src/resolve-refs.js` — credential reference resolution (env + pass)
- `src/errors.js` — TokenError class hierarchy
- `src/base64url.js` — base64url encode/decode helpers
- `test/export.test.js` — round-trip tests
- `test/import.test.js` — invalid token rejection tests
- `bin/openclaw-config-export` — CLI wrapper
- `bin/openclaw-config-import` — CLI wrapper
