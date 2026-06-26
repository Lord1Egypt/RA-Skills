# OpenClaw Secrets Hygiene Skill

## Description
OpenClaw-specific secrets management and credential hygiene based on real implementation experience. Handles OpenClaw's unique patterns: gateway coordination, SecretRef format nuances, auth-profiles.json vs models.json differences, and sequential execution to avoid gateway conflicts.

## When to Use
- Auditing OpenClaw deployments for plaintext credentials
- Migrating plaintext secrets to OpenClaw secrets management
- Troubleshooting unresolved SecretRef objects
- Coordinating gateway operations during secrets integration
- Developing security policies for OpenClaw deployments

## Inputs
- Optional: Path to OpenClaw configuration directory (default: `~/.openclaw`)
- Optional: Agent IDs to audit (default: all agents)
- Optional: Skip gateway operations flag (for analysis-only mode)

## Outputs
1. **Audit report:** Plaintext findings categorized by risk level
2. **Migration plan:** Step-by-step migration instructions
3. **Configuration templates:** Updated files with secret references
4. **Testing checklist:** Validation steps for secrets integration
5. **Troubleshooting guide:** Common issues and solutions

## Key Learnings from Implementation
### 1. Gateway Coordination is Critical
- **Problem:** Parallel gateway restarts cause connection loss (`gateway closed (1012): service restart`)
- **Solution:** Sequential execution with only one subagent authorized for gateway operations
- **Pattern:** Analysis → Preparation → Application → Testing (single gateway restart)

### 2. OpenClaw SecretRef Format Nuances
- **JSON Pointer format:** References use `/secret-name` (JSON Pointer with leading slash)
- **secrets.json keys:** Use `"secret-name"` (NO leading slash in key names)
- **Correct pattern:** Reference `"/secret-name"` → Key `"secret-name"` in secrets.json
- **Provider reference:** Must match `filemain` provider name in openclaw.json

### 3. Different File Types, Different Approaches
- **openclaw.json:** Gateway token, external API keys - use SecretRef objects
- **auth-profiles.json:** Authentication profiles - migrate to SecretRef objects
- **models.json:** Model provider API keys - use placeholder `"secretref-managed"` string (OpenClaw resolves to secrets)

### 4. Testing Patterns
- **Gateway health:** `curl http://127.0.0.1:18789/health`
- **Secrets audit:** `openclaw secrets audit`
- **Secrets reload:** `openclaw secrets reload` (may need OPENCLAW_GATEWAY_TOKEN env var)
- **Validation:** Plaintext count reduction, unresolved reference resolution

## Implementation Workflow

### Phase 1: Audit & Analysis
```bash
# 1. Initial audit
openclaw secrets audit

# 2. Categorize findings
# - openclaw.json: Gateway token, external API keys
# - auth-profiles.json: Authentication profiles  
# - models.json: Model provider API keys

# 3. Risk assessment
# High: Gateway token, external API keys
# Medium: Authentication profiles
# Low: Model provider keys (agent-directory protected)
```

### Phase 2: Preparation
```bash
# 1. Create centralized secrets file
mkdir -p ~/.openclaw
cat > ~/.openclaw/secrets.json << 'EOF'
{
  "gateway-token": "REPLACE_WITH_TOKEN",
  "brave-api-key": "REPLACE_WITH_KEY",
  "openai-api-key": "REPLACE_WITH_KEY",
  "agent-openrouter-key": "REPLACE_WITH_KEY"
}
EOF
chmod 600 ~/.openclaw/secrets.json

# 2. Update openclaw.json with secret references
# Change plaintext values to:
# {
#   "source": "file",
#   "provider": "filemain",
#   "id": "/secret-name"
# }
```

### Phase 3: Agent Configuration Updates
```bash
# 1. Update auth-profiles.json files
# Change "key": "plaintext" to:
# "key": {
#   "source": "file",
#   "provider": "filemain",
#   "id": "/secret-name"
# }

# 2. Handle models.json API keys
# Use placeholder string (OpenClaw will resolve from secrets):
# "apiKey": "secretref-managed"
# NOT SecretRef objects (causes unresolved references)
# OpenClaw replaces placeholder with actual secret at runtime
```

### Phase 4: Testing & Validation
```bash
# 1. Set gateway token for CLI operations
export OPENCLAW_GATEWAY_TOKEN="your-token"

# 2. Reload secrets
openclaw secrets reload

# 3. Verify audit improvement
openclaw secrets audit

# 4. Test gateway functionality
curl http://127.0.0.1:18789/health

# 5. Test external integrations (if applicable)
# Brave search, model API calls, etc.
```

## Common Issues & Solutions

### Issue 1: "JSON pointer segment does not exist"
**Cause:** Secret reference format mismatch
**Solution:** Ensure secrets.json has key `secret-name` (no slash) for reference `/secret-name`

### Issue 2: "gateway closed (1012): service restart"
**Cause:** Parallel gateway operations
**Solution:** Sequential execution, single gateway restart point

### Issue 3: "unresolved SecretRef object; regenerate models.json"
**Cause:** models.json contains SecretRef objects instead of placeholder strings
**Solution:** Replace SecretRef objects with `"secretref-managed"` placeholder string
**Emergency fix:** Use Python/script to convert `{"source": "file", ...}` → `"secretref-managed"`

```python
import json

with open('models.json', 'r') as f:
    data = json.load(f)

if 'providers' in data:
    for provider in data['providers']:
        if 'apiKey' in data['providers'][provider]:
            if isinstance(data['providers'][provider]['apiKey'], dict):
                data['providers'][provider]['apiKey'] = 'secretref-managed'

with open('models.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Issue 4: "requires interactive TTY"
**Cause:** `openclaw secrets configure` needs terminal
**Solution:** Manual configuration or environment variable workaround

## Security Considerations

### Risk Levels
- **High:** Gateway token, external API keys (Brave, etc.)
- **Medium:** Authentication profiles
- **Low:** Model provider keys (protected in agent directories)

### Acceptable Deferred Items
- models.json API keys may remain plaintext if:
  - Files are in protected agent directories (`~/.openclaw/agents/*/agent/`)
  - No world-readable permissions
  - Documented as technical debt

### Documentation Requirements
- Migration plan with timestamps
- Policy framework for ongoing management
- Regular audit schedule (weekly recommended)

## Templates & Examples

### secrets.json Template
```json
{
  "gateway-token": "REPLACE",
  "brave-api-key": "REPLACE",
  "openai-api-key": "REPLACE",
  "agent-openrouter-key": "REPLACE"
}
```

### auth-profiles.json Update Template
```json
{
  "version": 1,
  "profiles": {
    "provider:profile": {
      "type": "api_key",
      "provider": "provider",
      "key": {
        "source": "file",
        "provider": "filemain",
        "id": "/secret-name"
      }
    }
  }
}
```

## Success Metrics
- Plaintext findings reduced by 70%+
- Gateway operational with secret token
- External integrations working with secret keys
- Documentation complete (migration plan, policies)
- Regular audit schedule established

---

**Skill Author:** Based on real OpenClaw security remediation experience by jlab1201 (2026-04-11)
**Lessons Incorporated:** Gateway coordination, OpenClaw SecretRef patterns, emergency resolution techniques
