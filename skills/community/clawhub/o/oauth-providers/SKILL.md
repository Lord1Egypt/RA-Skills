---
name: oauth-providers
version: 1.1.0
description: Adds an "OAuth" settings tab to the OpenClaw Control UI for connecting AI model providers. Supports Anthropic Claude Pro/Max subscription tokens (setup-token flow), OpenAI Codex PKCE OAuth with manual-paste fallback for WSL2, and API keys for Anthropic, OpenAI, Google (Gemini), and OpenRouter. Includes auth profile order troubleshooting, badge rendering logic, and architecture reference for the auth-profiles system. Credentials are stored encrypted in auth-profiles.json and secrets.json.
---

# OAuth Providers Tab

Adds a polished **OAuth** settings tab to the OpenClaw Control UI.

## What It Installs

| File | Purpose |
|---|---|
| `ui/src/ui/views/ai-providers.ts` | Lit HTML view — provider cards, mode tabs, OAuth spinner, manual-paste field |
| `ui/src/ui/controllers/ai-providers.ts` | State management, RPC calls, provider catalogue |
| `src/gateway/server-methods/auth-login.ts` | Gateway RPC handlers for all auth flows |

Plus wiring changes in:
- `ui/src/ui/app.ts` — 6 `@state()` properties
- `ui/src/ui/app-render.ts` — render block for `state.tab === "ai-providers"`
- `ui/src/ui/app-settings.ts` — tab load trigger
- `ui/src/ui/navigation.ts` — `Tab` type, `TAB_PATHS`, `iconForTab`
- `src/gateway/server-methods.ts` — register `authLoginHandlers`
- `src/gateway/server-methods/plugins-ui.ts` — `BUILTIN_UI_VIEWS` entry
- `ui/src/i18n/locales/en.ts` — `"ai-providers"` label (`"OAuth"`) and subtitle

## Auth Flows

### OpenAI — Codex PKCE OAuth
- Button opens the system browser via `openUrl()`
- Callback captured on `localhost:1455/auth/callback`
- Calls `loginOpenAICodex()` from `@mariozechner/pi-ai`
- Credentials written by `writeOAuthCredentials()` + `applyAuthProfileConfig()`
- **WSL2 manual-paste fallback**: On WSL2, `127.0.0.1:1455` is unreachable from Windows. The UI shows a paste field where the user can paste the full redirect URL (`http://localhost:1455/auth/callback?code=...&state=...`). The gateway RPC `auth.login.openai-codex.submit-code` resolves a deferred promise that races with the local callback server via `onManualCodeInput`.
- Session state: `aiProvidersOauthSessionId` set by `startOpenAICodexOAuth` → used by `aiProvidersSubmitCode` to call the RPC

### Anthropic — Subscription Token (setup-token)
- User runs `claude setup-token` in terminal to generate a `sk-ant-oat01-...` token
- Pastes token into UI
- Validated by `validateAnthropicSetupToken()`, stored via `buildTokenProfileId()` + `upsertAuthProfile()`
- **Auto-detect button**: Reads existing `accessToken` from `~/.claude/.credentials.json` (under `claudeAiOauth`) and stores it via `auth.login.anthropic-auto` RPC
- **⚠️ Important**: Anthropic has blocked some subscription usage outside Claude Code. The docs warn: *"This credential is only authorized for use with Claude Code."* Setup-token support is "technical compatibility only" with policy risk. If you get a "not authorized" error, an API key is required.

### API Keys (all providers)
- Encrypted to `~/.openclaw/secrets.json` via existing `secrets.write` RPC
- Env vars: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `OPENROUTER_API_KEY`

## Gateway RPCs

| Method | Description |
|---|---|
| `auth.login.status` | List all configured auth profiles |
| `auth.login.anthropic-token` | Validate + store Anthropic setup-token |
| `auth.login.anthropic-auto` | Auto-detect token from `~/.claude/.credentials.json` |
| `auth.login.openai-codex` | Run PKCE OAuth (opens browser) |
| `auth.login.openai-codex.submit-code` | Manual paste of redirect URL (WSL2 fallback) |
| `auth.login.remove` | Remove a profile by `profileId` |

## Auth Badge System

The chat UI displays a badge next to assistant messages indicating which auth method was used.

### Badge Rendering (`grouped-render.ts`)

| profileId pattern | Badge | CSS class |
|---|---|---|
| `__mode:oauth` | **OAuth** (green) | `auth-badge--oauth` |
| Contains `:manual` or `claude-cli` or starts with `anthropic:oat` | **OAuth** (green) | `auth-badge--oauth` |
| Starts with `anthropic:` (catch-all) | **API** (blue) | `auth-badge--api` |
| Starts with `openai:` | **Fallback** | `auth-badge--fallback` |
| Everything else | **API** | `auth-badge--fallback` |

The badge is determined by `group.authProfileId` in the message group. If the wrong profile is active, the wrong badge appears.

See [references/auth-badge.ts.excerpt](references/auth-badge.ts.excerpt) for the full function.

## Auth Profile Order — Architecture & Troubleshooting

### How Profile Selection Works

The gateway selects which auth profile to use via `resolveAuthProfileOrder()` in `src/agents/auth-profiles/order.ts`:

```
storedOrder (auth-profiles.json)  →  takes precedence
configuredOrder (openclaw.json)   →  fallback if no stored order
explicitProfiles (config keys)    →  fallback if no explicit order
storeProfiles (all in store)      →  last resort
```

**Critical**: `auth-profiles.json` order ALWAYS wins over `openclaw.json` order. If `auth-profiles.json` has a stale `order` array, the correct order in `openclaw.json` will never be consulted.

See [references/auth-order.ts.excerpt](references/auth-order.ts.excerpt) for the key code.

### Common Issue: Stale Order / Ghost Profiles

**Symptom**: Badge shows "API" or "Fallback" even though the subscription token is configured correctly.

**Cause**: `auth-profiles.json` has an `order` array referencing non-existent profiles (e.g. `anthropic:manual` from an old setup). The existing profile (like `anthropic:default`) gets selected instead of the subscription token profile.

**Diagnosis**:
```bash
# Check current auth status
openclaw models status

# Check what auth-profiles.json actually has
python3 -c "
import json
with open('$HOME/.openclaw/agents/main/agent/auth-profiles.json') as f:
    d = json.load(f)
print('order:', d.get('order'))
print('lastGood:', d.get('lastGood'))
print('profiles:', list(d['profiles'].keys()))
"
```

**Fix**:
```bash
# Option 1: Remove stale order so openclaw.json becomes authoritative
python3 -c "
import json
path = '$HOME/.openclaw/agents/main/agent/auth-profiles.json'
with open(path) as f: d = json.load(f)
d.pop('order', None)
d.pop('lastGood', None)
with open(path, 'w') as f: json.dump(d, f, indent=2)
print('Stale order removed')
"

# Option 2: Set order via CLI (writes to auth-profiles.json)
openclaw models auth order set --provider anthropic anthropic:claude-cli anthropic:default

# Then restart gateway
(sleep 3 && systemctl --user restart openclaw-gateway) &
```

**Why Option 1 is preferred**: The CLI writes to `auth-profiles.json`, but gateway restarts or other processes can overwrite it. Removing the stored order lets `openclaw.json` (which is the canonical config) be the authority.

### Repair Logic

`resolveAuthProfileOrder()` has a repair path (lines 96-100): if ALL profiles in the base order are missing from the store, it scans all stored profiles for the provider. But this only triggers when EVERY profile is missing — if even one exists (like `anthropic:default`), the repair doesn't kick in.

### Config Verification

Ensure `openclaw.json` has the correct auth section:
```json
{
  "auth": {
    "profiles": {
      "anthropic:claude-cli": { "provider": "anthropic", "mode": "oauth" },
      "anthropic:default": { "provider": "anthropic", "mode": "api_key" }
    },
    "order": {
      "anthropic": ["anthropic:claude-cli", "anthropic:default"]
    }
  }
}
```

The `mode` field in `openclaw.json` profiles is checked against the `type` field in `auth-profiles.json` credentials. A `mode: "oauth"` config is compatible with both `type: "oauth"` and `type: "token"` credentials (special-cased in `resolveAuthProfileEligibility`).

## Installation Steps

1. Copy `references/view.ts` → `ui/src/ui/views/ai-providers.ts`
2. Copy `references/controller.ts` → `ui/src/ui/controllers/ai-providers.ts`
3. Copy `references/auth-login.ts` → `src/gateway/server-methods/auth-login.ts`
4. Wire into the UI (see wiring changes above — follow patterns from other tabs like `apikeys`)
5. Register `authLoginHandlers` in `src/gateway/server-methods.ts`
6. `npm run build` — zero new TS errors expected
7. Restart gateway: `(sleep 3 && systemctl --user restart openclaw-gateway) &`
8. Open **Settings → OAuth** in the Control UI

## Provider Catalogue

Defined in `PROVIDER_CATALOGUE` in `references/controller.ts`. To add a provider:

```ts
{
  id: "mistral",
  name: "Mistral AI",
  logo: "🌊",
  color: "#ff7000",
  description: "Mistral Large, Codestral — fast European models",
  connectOptions: [
    { mode: "api-key", label: "API Key", hint: "Get a key from console.mistral.ai", profileMode: "api_key" },
  ],
}
```

## Known Gotchas

1. **Auth order precedence**: `auth-profiles.json` order beats `openclaw.json`. If badge shows wrong auth mode, check for stale order in auth-profiles.json first.
2. **Gateway restart overwrites**: Manual edits to `auth-profiles.json` can be overwritten by gateway processes. Prefer editing `openclaw.json` for persistent config.
3. **WSL2 loopback isolation**: The OpenAI Codex OAuth callback server binds to `127.0.0.1:1455` (hardcoded in `@mariozechner/pi-ai`). Windows browsers can't reach WSL2 localhost. Use the manual-paste field.
4. **`claude setup-token` requires interactive TTY**: Uses Ink/raw mode — cannot be run non-interactively. The auto-detect button reads `~/.claude/.credentials.json` as a workaround.
5. **Anthropic policy risk**: `sk-ant-oat01-*` tokens may be blocked outside Claude Code. If API calls return authorization errors, switch to an API key.
6. **`lastGood` persistence**: The `lastGood` field in `auth-profiles.json` can cause the gateway to skip the configured order and jump straight to a previously-working profile. Remove it along with `order` when troubleshooting.

## Source Files

- [references/controller.ts](references/controller.ts) — full controller with PROVIDER_CATALOGUE and all action handlers
- [references/view.ts](references/view.ts) — full Lit HTML view with manual-paste field
- [references/auth-login.ts](references/auth-login.ts) — full gateway RPC handlers including WSL2 fallback + auto-detect
- [references/auth-order.ts.excerpt](references/auth-order.ts.excerpt) — auth profile order resolution logic (key snippet)
- [references/auth-badge.ts.excerpt](references/auth-badge.ts.excerpt) — badge rendering function (key snippet)

## Changelog

### v1.1.0
- Added WSL2 manual-paste fallback for OpenAI Codex OAuth (`onManualCodeInput` + `auth.login.openai-codex.submit-code` RPC)
- Added Anthropic auto-detect button (`auth.login.anthropic-auto` RPC) — reads from `~/.claude/.credentials.json`
- Added auth badge rendering reference (`renderAuthBadge()` from `grouped-render.ts`)
- Added auth profile order architecture documentation with troubleshooting guide
- Added stale order/ghost profile diagnosis and fix procedures
- Documented `resolveAuthProfileOrder()` precedence: stored order > config order > explicit profiles > store profiles
- Added known gotchas section covering order precedence, gateway overwrites, WSL2 loopback, TTY requirements, and Anthropic policy risk

### v1.0.0
- Initial release with Anthropic setup-token, OpenAI Codex PKCE OAuth, and API key flows
