# Authentication and API Key Setup

Use this reference when the OKKI Go skill needs an API key, first-use signup, key persistence, or authenticated `curl` examples.

## Contents

1. Agent-led Install Wizard
2. Credential Resolution
3. Email Verification
4. Save API Key

## Agent-led Install Wizard

Use this flow when a user asks to install, set up, add, update, or enable OKKI Go. Do not rely on the npm package's interactive prompt. Ask the install questions in chat, map the answers to installer flags, then execute the installer yourself when the host provides shell/tool execution. Do not just display the command.

Do not ask the user to choose a language. Use the user's current conversation language for all prompts and explanations.

One-step execution path: when the user already named a runtime and install location, or a preinstalled agent knows its own known runtime and the default global location is appropriate, skip the wizard questions and execute the flagged installer directly.

Ask only for missing install choices:

1. AI assistant/runtime:
   - Claude Code -> `--claude`
   - OpenClaw -> `--openclaw`
   - OpenCode -> `--opencode`
   - Gemini CLI -> `--gemini`
   - Cursor -> `--cursor`
   - Windsurf -> `--windsurf`
   - Codex -> `--codex`
   - GitHub Copilot -> `--copilot`
   - Cline -> `--cline`
   - Accio Work -> `--accio`
   - Install all -> `--all`
   - Other -> ask for the assistant name and map to `--custom=<name>`
2. Install location:
   - Default global config -> `--global`
   - Current working directory -> `--local`
   - Custom base path -> ask for the base path and map to `--path <dir>`

After collecting answers, construct:

```bash
npx -y @okki-global/okki-go@latest <location flag> <runtime flag>
```

Then execute the installer. If the host requires command approval, request approval using the host's normal mechanism. If the host has no command execution capability, or the user refuses execution approval, explain that installation cannot be completed from this agent surface and provide the exact command as a fallback.

After successful install, continue with these next steps:

1. Get your API Key: direct the user to https://go.okki.ai to sign up and get an `sk-...` key, unless the user already has one.
2. Configure your key: prefer platform secrets/config when available; otherwise ask before saving to the user-level cache with `printf '%s\n' 'sk-xxxxxxxxxxxxxxxxxxxx' | node scripts/okki-auth.js login --with-api-key`.
3. Verify without printing the key: run `bash scripts/resolve-api-key.sh --check`.
4. Prompt the user to restart or open a new assistant session if the install target requires reloading skills.

## Credential Resolution

Before the first API call in each session, run:

```bash
bash scripts/resolve-api-key.sh --check
```

Results:

- `KEY_SET`: proceed.
- `NO_KEY`: follow email verification or use a user-provided `sk-` key.

Use a Codex-style credential flow: configure once, cache in the user-level OKKI Go config directory, then let future agent sessions check the cache before asking the user again.

Primary persistent storage:

- Credential cache: `${XDG_CONFIG_HOME:-$HOME/.config}/okki-go/credentials.json`, mode `0600`.
- Registered source: `${XDG_CONFIG_HOME:-$HOME/.config}/okki-go/auth-source.json`, mode `0600`, non-secret source metadata only.

Resolution order:

1. Registered source created by `node scripts/okki-auth.js login --with-api-key`; normally points to the user-level credential cache.
2. Explicit environment override: `OKKIGO_API_KEY`, `OKKI_GO_API_KEY`, or `OKKIGO_SKILL_API_KEY` for CLI/CI or platform-injected sessions.
3. Legacy local credentials file fallback: `${XDG_CONFIG_HOME:-$HOME/.config}/okki-go/credentials.json`, mode `0600`, JSON `{"apiKey":"sk-..."}`.

The runtime resolver does not scan platform-specific config directories. Installers or platforms may register a source during setup or inject an explicit environment variable, but routine skill execution should not guess where a given agent stores secrets.

Never store API keys in `SKILL.md`, repositories, transcripts, logs, examples, or command history beyond an explicit user-approved save command.

For API calls, resolve the key immediately before `curl` and avoid printing it:

```bash
OKKIGO_API_KEY="$(bash scripts/resolve-api-key.sh --print)" && \
xargs -0 curl -s -X GET "${OKKIGO_BASE_URL:-https://go.okki.ai}/api/v1/credit/balance" \
  -H "Authorization: ApiKey $OKKIGO_API_KEY" \
  < <(node scripts/lib/runtime-attribution.js --curl-null)
```

For configuration debugging only, use `bash scripts/resolve-api-key.sh --source`; it prints the source name, not the secret.

For redacted diagnostics:

```bash
node scripts/okki-auth.js status --json
node scripts/okki-auth.js doctor --json
```

## Email Verification

1. Show legal documents and require exact acceptance before asking for email:

```text
Before creating an OKKI Go account and API Key, please read:

Terms of Service v2026-04-23: https://go.okki.ai/legal/terms
Privacy Policy v2026-04-23: https://go.okki.ai/legal/privacy

If you agree to continue, reply:
I have read and agree to the Terms of Service and acknowledge the Privacy Policy.
```

Chinese:

```text
创建 OKKI Go 账号和 API Key 前，请先阅读：

服务条款 v2026-04-23: https://go.okki.ai/legal/terms
隐私政策 v2026-04-23: https://go.okki.ai/legal/privacy

如同意继续，请回复：
我已阅读并同意《服务条款》，并确认已阅读《隐私政策》。
```

Do not treat vague replies such as "OK", "continue", "好的", "继续", or "发验证码吧" as valid acceptance.

2. After acceptance, ask for email. Report analytics with only `email_domain`, never the full email.

3. Send verification code:

```bash
xargs -0 curl -s -X POST "${OKKIGO_BASE_URL:-https://go.okki.ai}/api/v1/auth/register-email" \
  -H "Content-Type: application/json" \
  -d '{
    "email":"<user email>",
    "legalAcceptance": {
      "accepted": true,
      "termsVersion": "2026-04-23",
      "privacyVersion": "2026-04-23",
      "termsUrl": "https://go.okki.ai/legal/terms",
      "privacyUrl": "https://go.okki.ai/legal/privacy",
      "channel": "agent",
      "skillVersion": "1.3.3",
      "locale": "en-US",
      "affirmationText": "I have read and agree to the Terms of Service and acknowledge the Privacy Policy."
    }
  }' < <(node scripts/lib/runtime-attribution.js --curl-null) | jq '.'
```

4. Exchange the 6-digit code for an API key:

```bash
xargs -0 curl -s -X POST "${OKKIGO_BASE_URL:-https://go.okki.ai}/api/v1/auth/verify-email" \
  -H "X-OpenClaw-Provision-Api-Key: true" \
  -H "Content-Type: application/json" \
  -d '{"email":"<user_email>","code":"<6_digit_code>"}' \
  < <(node scripts/lib/runtime-attribution.js --curl-null) | jq '.'
```

## Save API Key

After obtaining `apiKey`, verify it starts with `sk-`, tell the user where it will be saved, and ask for explicit consent. Saving the key is separate from legal acceptance.

Preferred save order:

1. Platform config command, if the host supports one.
2. User-level OKKI Go credential cache on macOS/Linux:

```bash
printf '%s\n' 'sk-xxxxxxxxxxxxxxxxxxxx' | node scripts/okki-auth.js login --with-api-key
```

3. Shell profile only for terminal-launched agents when local credentials are not acceptable.
4. Windows PowerShell user-level environment variable:

```powershell
[System.Environment]::SetEnvironmentVariable("OKKIGO_API_KEY", "sk-xxxxxxxxxxxxxxxxxxxx", "User")
```

5. Windows CMD:

```cmd
setx OKKIGO_API_KEY "sk-xxxxxxxxxxxxxxxxxxxx"
```

After saving through platform config or user-level env vars, prompt the user to restart the assistant session. The local credentials file is available immediately to tools that can read user config.
