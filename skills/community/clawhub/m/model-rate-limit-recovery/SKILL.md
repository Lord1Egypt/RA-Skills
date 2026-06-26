---
name: model-rate-limit-recovery
description: Diagnose and recover from model rate limit errors (ChatGPT usage limits, 429 errors). Use when cron jobs or agent sessions fail with "Try again in ~9500 min" or similar rate limit messages. Covers API key rotation, model fallback, and manual recovery procedures.
---

# Model Rate Limit Recovery Skill

## When to Use
- Cron jobs fail with "⚠️ You have hit your ChatGPT usage limit (free plan). Try again in ~9500 min"
- Agent sessions fail with 429, rate_limit, quota, or resource exhausted errors
- Need to recover scheduled tasks after model provider limits are hit
- Setting up resilient agent workflows with automatic fallbacks

## Diagnosis Steps

### 1. Check Error Type
```bash
# Check cron job runs
openclaw cron runs --jobId <job_id>

# Look for error messages containing:
# - "usage limit"
# - "Try again in ~"
# - "429"
# - "rate_limit"
# - "quota"
# - "resource exhausted"
```

### 2. Verify Current Configuration
```bash
# Check current model configuration
openclaw status | grep -A5 "Model"

# Check environment for API keys
env | grep -i "OPENAI\|ANTHROPIC\|DEEPSEEK"
```

### 3. Identify Root Cause
**Common causes:**
- **Free plan limits**: ChatGPT free tier has usage caps
- **No API key rotation**: Single key exhausted
- **No fallback model**: Default model fails, no alternative
- **Cron jobs using default model**: Not specifying resilient model

## Recovery Procedures

### Immediate Recovery (Manual)
```bash
# 1. Run failed task manually with alternative model
openclaw sessions spawn \
  --task "Your task here" \
  --model "deepseek/deepseek-chat" \
  --label "Manual recovery"

# 2. Update cron job to specify model
openclaw cron update --jobId <job_id> --patch '{
  "payload": {
    "kind": "agentTurn",
    "message": "...",
    "model": "deepseek/deepseek-chat",
    "timeoutSeconds": 180
  }
}'
```

### API Key Rotation Setup
```bash
# Add multiple API keys for rotation
export OPENAI_API_KEYS="key1,key2,key3"
export OPENAI_API_KEY_1="sk-..."
export OPENAI_API_KEY_2="sk-..."
export OPENCLAW_LIVE_OPENAI_KEY="sk-..."  # Highest priority

# OpenClaw will automatically rotate through keys on rate limits
# 429, rate_limit, quota, resource exhausted → tries next key
# Other failures → fails immediately
```

### Model Fallback Configuration
```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai-codex/gpt-5.4",
        "fallback": "deepseek/deepseek-chat"
      },
      "models": {
        "openai-codex/gpt-5.4": {
          "params": {
            "maxRetries": 2,
            "retryOnRateLimit": true
          }
        }
      }
    }
  }
}
```

### Cron Job Best Practices
```json5
{
  "name": "Resilient Scheduled Task",
  "schedule": {
    "kind": "cron",
    "expr": "0 * * * *",
    "tz": "Africa/Johannesburg"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Task instructions...",
    "model": "deepseek/deepseek-chat",  // Specify model explicitly
    "timeoutSeconds": 300               // Set reasonable timeout
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce"
  }
}
```

## Prevention Strategies

### 1. Model Selection
- **Primary**: `openai-codex/gpt-5.4` (when available)
- **Fallback**: `deepseek/deepseek-chat` (no usage limits)
- **Backup**: `anthropic/claude-sonnet-4-6` (if available)

### 2. Cron Job Configuration
- Always specify `model` in payload
- Set reasonable `timeoutSeconds`
- Use `deleteAfterRun: true` for one-shot tasks
- Enable `delivery.mode: "announce"` for notifications

### 3. Monitoring
```bash
# Regular cron job health checks
openclaw cron list
openclaw cron runs --jobId <job_id> --limit 5

# Check for recent failures
grep -i "usage limit\|429\|rate_limit" /tmp/openclaw/openclaw-*.log
```

### 4. Skill Integration
```bash
# Create recovery script
cat > /root/.openclaw/workspace/scripts/recover-failed-cron.sh <<'EOF'
#!/bin/bash
JOB_ID="$1"
NEW_MODEL="${2:-deepseek/deepseek-chat}"

# Get failed runs
FAILED_RUNS=$(openclaw cron runs --jobId "$JOB_ID" | grep -c "status.*error")

if [ "$FAILED_RUNS" -gt 0 ]; then
  echo "Recovering $FAILED_RUNS failed runs for job $JOB_ID"
  openclaw cron update --jobId "$JOB_ID" --patch "{\"payload\":{\"model\":\"$NEW_MODEL\"}}"
  openclaw cron run --jobId "$JOB_ID"
fi
EOF
chmod +x /root/.openclaw/workspace/scripts/recover-failed-cron.sh
```

## Templates

### Resilient Cron Job Template
See `scripts/resilient-cron-template.json`

### Model Fallback Config
See `references/model-fallback-config.json`

### Recovery Script
See `scripts/recover-failed-cron.sh`

## Notes
- ChatGPT free plan has strict usage limits (~3 requests/hour)
- DeepSeek has no usage limits but may have different capabilities
- API key rotation only works for rate limits (429), not other errors
- Always verify recovery by checking created files/outputs
- Document failures and recoveries in memory/ for future reference

## References
- [OpenClaw Model Providers Docs](/concepts/model-providers)
- [API Key Rotation Documentation](/concepts/model-providers#api-key-rotation)
- [Cron Job Management](/tools/cron)