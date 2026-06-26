# ONBOARDING-SPEC.md — Onboarding Wizard Spec

**Owner:** TCF (Technical Co-Founder)
**Reviewer:** SE (edge cases)
**Status:** Phase 0 draft — pending SE edge case review
**Created:** 2026-04-18

---

## Purpose

Define what the interactive onboarding wizard does and doesn't do. The wizard is the user-facing entry point to config-safety-v2 — the thing that runs when a new user installs the skill or an existing user wants help understanding their config.

**Design philosophy:** Scope discipline is paramount. The wizard has ONE job: help users understand and validate their config safely. Every extra feature is a scope creep risk and a delay to shipping.

---

## Resolved Decision (from RESOLUTIONS.md)

- **Config-safety ONLY** — no provider setup, no API key entry, no agent defaults
- Wizard scope: normalization guidance + export/import + validation
- Scope creep risk is paramount — draw the line explicitly

---

## Wizard Purpose

The wizard answers one question: **"Is my openclaw.json configured correctly, and can I export or import it safely?"**

It does NOT:
- Set up API keys
- Choose models for the user
- Configure agents or personas
- Set up memory backends
- Run any external services

---

## In-Scope Interactions

### 1. Config Discovery

Ask the user where their config is (or detect automatically):
- Default: `~/.openclaw/openclaw.json`
- Custom path: user provides
- No config found: offer to start from a template

```
$ openclaw-config-onboard
🔍 Scanning for openclaw.json...
Found: ~/.openclaw/openclaw.json
Is this the config you want to work with? [Y/n]:
```

### 2. Config Audit (read-only)

Display a readable summary of what the wizard finds:

```
📋 Config Audit
─────────────────────────────────
Gateway:      localhost:18789
Plugins:      5 loaded (correlation-memory, exec-truncate, lossless-claw, memory-core, telegram)
Models:       3 configured (minimax/m2.7, cerebras/llama3.1-8b, zai/glm-4.7)
Default:      minimax/m2.7

⚠️  Warnings:
  • 2 credential references detected but not resolved:
      CEREBRAS_API_KEY, CEREBRAS_API_KEY
  • bootstrapMaxChars (40000) is below schema recommended minimum (50000)
```

**The wizard does NOT fix warnings automatically.** It surfaces them and lets the user decide.

### 3. Normalization (opt-in)

Offer to run the normalizer:

```
✨ Normalization
─────────────────────────────────
The normalizer found 3 issues:
  1. agents.defaults.model: trimmed 2 trailing whitespace chars
  2. agents.defaults.timeoutSeconds: coerced "30" → 30 (number)
  3. models.providers.cerebras.enabled: coerced "true" → true (boolean)

Apply these changes? [y/N]:
```

- If yes: apply and show diff
- If no: skip, proceed to next step
- **No changes are made without explicit user confirmation**

### 4. Validation

Run the validator (6 checks):

```
✅ Validation
─────────────────────────────────
All 6 checks passed:
  ✓ JSON parse
  ✓ Top-level keys
  ✓ Per-model fields
  ✓ agents.defaults fields
  ✓ Known-crash fields
  ✓ openclaw doctor

Your config is valid.
```

If validation fails:

```
❌ Validation Failed
─────────────────────────────────
Check 3 failed: Per-model fields
  • agents.defaults.models["glm-4.7"]: unknown field "note"
    → Known-crash field: "note" in per-model overrides causes instant crash

Fix this before continuing. Options:
  [1] Remove the "note" field from glm-4.7
  [2] Open config in editor
  [3] Exit (default)
>
```

### 5. Export Token (opt-in)

Offer to create an export token:

```
🔐 Export Token
─────────────────────────────────
Credential references in this config:
  • CEREBRAS_API_KEY
  • CEREBRAS_API_KEY

⚠️  These will be exported as ${REFERENCE} — actual keys are NOT included.
The token will be safe to share via Slack/email.

Create export token? [y/N]:
```

If yes: generate and display:

```
✅ Token Created
─────────────────────────────────
mrconf:v1:eyJ2ZXJzaW9uIjoxLCJleHBvcnRlZEF0IjoiMjAy...

Share this token to transfer your config to another machine.
The receiving machine must have the same credential references resolved
(CEREBRAS_API_KEY etc.) in environment variables or pass.
```

### 6. Import Token (opt-in)

Offer to import a token:

```
📥 Import Token
─────────────────────────────────
Paste your mrconf:v1:... token (or press Enter to cancel):
> mrconf:v1:eyJ2...

🔍 Validating token...
  ✓ Valid mrconf:v1 token
  ✓ 3 credential references found
  ✓ All references resolvable in current environment

⚠️  This will REPLACE your current config.
A backup will be saved to ~/.openclaw/openclaw.json.bak-20260418-165300

Continue? [y/N]: y

✅ Config imported successfully.
Restart gateway? [Y/n]:
```

---

## Out-of-Scope (Explicitly)

The wizard does NOT:

| Out-of-scope | Reason |
|-------------|--------|
| Provider setup (add/edit/remove API keys) | OpenClaw's setup flow handles this |
| Model selection | Users choose their own models |
| Agent persona configuration | Outside config-safety scope |
| Memory backend setup | Outside config-safety scope |
| Plugin installation/uninstallation | Separate CLI operation |
| Gateway startup/shutdown | Separate CLI operation |
| Tailscale/network config | Outside config-safety scope |

If users ask for these, the wizard outputs:

```
That feature is outside this wizard's scope.
For provider setup, see: openclaw help providers
For agent configuration, see: openclaw help agents
```

---

## User Flow (Happy Path)

```
openclaw-config-onboard
  ↓
[1] Config Discovery → confirm path
  ↓
[2] Config Audit → view summary
  ↓
[3] Normalization (opt-in) → apply fixes
  ↓
[4] Validation → run checks
  ↓
[5] Export Token (opt-in) → generate + display
  OR
[5] Import Token (opt-in) → paste + import + restart
  ↓
Done
```

---

## TTY vs Non-TTY Behavior

**TTY (interactive terminal):** Full wizard experience as described above.

**Non-TTY (piped/redirected/script):** Graceful fallback:

```
$ openclaw-config-onboard --validate
$ openclaw-config-onboard --export
$ openclaw-config-onboard --import <token>
$ openclaw-config-onboard --help
```

| Flag | Behavior |
|------|----------|
| `--validate` | Run validation, exit 0 if pass, exit 1 if fail, print results |
| `--export` | Export token to stdout (no TTY prompt needed) |
| `--import <token>` | Import token (non-interactive, exit 0 on success) |
| `--normalize` | Normalize in place (modifies file), exit 0 if changes made |
| `--audit` | Print config audit summary, no modifications |
| `--help` | Show usage |
| *(no flag, non-TTY)* | Print help text and exit 1 |

**Principle:** All operations are available non-interactively. Interactive prompts are only required for confirmation steps that could cause data loss.

---

## Rollback Behavior

**Backup before any write:**

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d-%H%M%S)
```

**On import failure (malformed token, validation fails):**
```bash
cp ~/.openclaw/openclaw.json.bak-<timestamp> ~/.openclaw/openclaw.json
echo "Import failed. Config restored from backup."
exit 1
```

**On gateway restart failure:**
```bash
openclaw gateway restart
if [ $? -ne 0 ]; then
  cp ~/.openclaw/openclaw.json.bak-<timestamp> ~/.openclaw/openclaw.json
  openclaw gateway restart  # restore working config
  echo "Gateway failed to start. Config restored. Investigate before restarting."
  exit 1
}
```

**On normalization failure:** No file is touched. The user sees the error and decides.

---

## Post-Write Verification

After any write to `openclaw.json`:

```bash
openclaw gateway restart
openclaw sessions > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ Gateway is up."
else
  echo "❌ Gateway failed to restart. Restoring backup..."
  cp ~/.openclaw/openclaw.json.bak-<timestamp> ~/.openclaw/openclaw.json
  openclaw gateway restart
fi
```

**The wizard waits for gateway confirmation before reporting success.**

---

## Credential Handling

The wizard:
- **Never prompts** for actual credentials
- **Never displays** resolved credential values
- **Only validates** that credential references (`${REF}`) are present in the config
- **On export:** warns that references will be in the token
- **On import:** resolves references from env/pass, fails if missing

**Masking rule:** Any output that would show a credential value must show `REDACTED(length N)` instead.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (operation completed) |
| 1 | Failure (validation failed, import failed, file error, gateway down) |
| 2 | Invalid arguments or `--help` |
| 3 | Partial success (changes applied but gateway restart failed — backup restored) |

---

## Phase 3 Implementation Files

- `bin/openclaw-config-onboard` — main wizard CLI
- `src/audit.js` — config summary generator
- `src/prompt.js` — TTY prompt helpers (yes/no, text input, menu)
- `src/config-patch.js` — safe config merge for import
- `src/doctor-check.js` — post-write `openclaw doctor` wrapper
- `src/restore-backup.js` — backup + restore helpers
- `test/onboard.test.js` — non-interactive edge cases
- `test/audit.test.js` — audit output format tests

---

## Error Message Standards

All wizard errors must:
- Be human-readable (not "Error: ENOENT")
- Explain what happened and what to do next
- **Never** show credential values
- Use emojis sparingly (only for status indicators: ✅ ❌ ⚠️ 🔍)

```
❌ Validation failed: openclaw.json is not valid JSON
   → Check the file with: cat ~/.openclaw/openclaw.json
   → Or restore from backup: ls ~/.openclaw/openclaw.json.bak-*

❌ Import failed: token version not supported
   → This token was created with a newer version of this tool.
   → Upgrade: clawhub update config-safety-v2

❌ Credential missing: CEREBRAS_API_KEY
   → Set CEREBRAS_API_KEY in your environment
   → Or add to pass: pass insert -m cerebras/apikey
   → Then run this command again.
```
