
# Troubleshooting

Common issues and fixes for multi-agent OpenClaw setups.

## Node.js Compatibility

**Requirement:** Node.js v18, v20, v22, or v24 only. **v25+ is not supported.**

If you have v25+, use `nvm` to install a supported version:

```bash
nvm install 22
nvm use 22
node --version  # Verify it shows v22.x.x
```

Then restart OpenClaw:
```bash
openclaw restart
```

## Configuration Errors

### "No API provider registered for api: anthropic"

**Cause:** Anthropic provider block was added to `models.json`. This causes conflicts.

**Fix:** Remove the anthropic provider block from the free agent's `models.json`. OpenClaw handles Anthropic internally — do not register it manually.

```bash
# Check if anthropic is in models.json
grep -i anthropic ~/.openclaw/agents/free-agent/agent/models.json

# Edit and remove the anthropic provider block
nano ~/.openclaw/agents/free-agent/agent/models.json
```

Then restart:
```bash
openclaw restart
```

### "Model could not be resolved"

**Cause:** Model field uses a file path instead of a provider/id string.

**Fix:** Use correct format: `provider/modelid`

**Wrong:**
```json
"model": { "primary": "/path/to/claude.json" }
```

**Correct:**
```json
"model": { "primary": "anthropic/claude-sonnet-4-6" }
```

### Wrong Agent Routing (Messages Go to Wrong Bot)

**Cause:** Bindings have identical or missing `accountId` values.

**Fix:** Ensure each binding has a unique `accountId`:

```json
{
  "bindings": [
    { "agentId": "main", "match": { "channel": "telegram", "accountId": "default" } },
    { "agentId": "free-agent", "match": { "channel": "telegram", "accountId": "tg2" } }
  ]
}
```

Also clear old sessions:
```bash
openclaw sessions cleanup \
  --store /Users/YOUR_USERNAME/.openclaw/agents/main/store \
  --enforce --fix-missing
openclaw restart
```

## Authentication Errors

### OpenRouter "No API key found"

**Cause:** Missing or incorrectly placed `auth-profiles.json`.

**Fix:** Create `auth-profiles.json` in the free agent's agentDir:

```bash
cat > ~/.openclaw/agents/free-agent/agent/auth-profiles.json <<'EOF'
{
  "version": 1,
  "profiles": {
    "openrouter:default": {
      "type": "api_key",
      "provider": "openrouter",
      "key": "sk-or-v1-YOUR_OPENROUTER_KEY"
    }
  },
  "lastGood": {
    "openrouter": "openrouter:default"
  }
}
EOF
```

Then restart:
```bash
openclaw restart
```

### Anthropic Billing Cooldown

**Cause:** Account hit usage limits or API key was revoked.

**Fix:** 
1. Check balance at https://console.anthropic.com/account/billing/overview
2. Top up your account if needed
3. Verify API key is valid and still active
4. Re-authenticate if key changed:
   ```bash
   # Use interactive onboard (never pass keys on CLI):
   openclaw onboard
   ```

## Runtime Errors

### ENOENT: Old Machine Paths

**Cause:** Config references paths from a previous machine or user.

**Fix:** Search and replace all hardcoded paths:

```bash
grep -r "old-username" ~/.openclaw/
grep -r "/home/olduser" ~/.openclaw/
# Edit affected files and use /Users/YOUR_USERNAME/
```

Common locations:
- `~/.openclaw/openclaw.json` (agentDir, workspace paths)
- `~/.openclaw/agents/*/agent/models.json`
- `~/.openclaw/agents/*/agent/auth-profiles.json`

## Verification Steps

Run these commands to verify setup:

```bash
# Check OpenClaw status and config
openclaw doctor

# Verify both agents are registered
grep -A 2 '"id"' ~/.openclaw/openclaw.json | grep -E 'id|name'

# Test Anthropic auth (uses env var, no key in command)
curl -s https://api.anthropic.com/v1/models \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"

# Test OpenRouter auth (uses env var or interactive)
# Do NOT paste real keys into curl commands — use env vars
openclaw doctor
```

## Debugging Tips

**Enable verbose logging:**
```bash
DEBUG=* openclaw start
```

**Inspect active sessions:**
```bash
ls -la ~/.openclaw/agents/*/store/sessions/
```

**Check recent logs:**
```bash
tail -100f ~/.openclaw/logs/agent.log
```

**Validate JSON syntax:**
```bash
jq . ~/.openclaw/openclaw.json
jq . ~/.openclaw/agents/free-agent/agent/auth-profiles.json
```
