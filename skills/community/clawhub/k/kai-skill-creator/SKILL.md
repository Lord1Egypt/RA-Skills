---
name: kai-skill-creator
description: Create new OpenClaw skills that pass ClawHub validation on first attempt. Use when building a new skill for OpenClaw. Teaches the complete process from template to published skill.
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Kai Skill Creator

Create OpenClaw skills correctly. Learned from getting kai-minimax-tts and kai-skill-creator to pass ClawHub scan.

## Quick Start

### 1. Clone Template
```bash
cp -r /home/kai/.openclaw/workspace/skills/kai-minimax-tts /home/kai/.openclaw/workspace/skills/<NEW_SKILL>
```

### 2. Edit SKILL.md

**CORRECT FRONTMATTER:**
```yaml
---
name: skill-name
description: What this skill does and when to use it
metadata:
  openclaw:
    requires:
      bins:
        - binary1
        - curl
      env:
        - API_KEY
---

# My Skill

Brief description...

## Usage
Commands and examples...
```

### 3. Write Script
```bash
chmod +x /home/kai/.openclaw/workspace/skills/<NEW_SKILL>/scripts/<script>.sh
```

### 4. Validate
```bash
python3 /home/kai/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py /home/kai/.openclaw/workspace/skills/<NEW_SKILL>
```

### 5. Copy to Global
```bash
cp -r /home/kai/.openclaw/workspace/skills/<NEW_SKILL> /home/kai/.openclaw/skills/<NEW_SKILL>
```

### 6. Register in Config
Add to `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "<SKILL_NAME>": {
        "enabled": true
      }
    }
  }
}
```

### 7. Publish
```bash
cd ~/.openclaw/workspace
npx clawhub publish skills/<SKILL_NAME> --slug <SKILL_NAME> --version 1.0.0 --tags "tag1,tag2"
```

---

## ⚠️ CRITICAL: What NOT to Do

### ❌ NEVER Hardcode API Keys
```bash
# FLAGGED!
API_KEY="sk-api-xxxxx"
```

### ❌ NEVER Load .env in Script
```bash
# FLAGGED! Security risk
source ~/.env
```

### ❌ NEVER Use homepage Key
```yaml
# FLAGGED! Causes validation failure
homepage: https://example.com
```

### ❌ NEVER Mention External API URLs
```markdown
# FLAGGED! External endpoint reference
Get key from: https://api.example.com
```
Keep docs minimal. Scanner interprets URL mentions as potential data exfiltration.

### ❌ NEVER Leave Env Vars Undeclared
```yaml
# MISMATCH! Script uses $API_KEY but not declared
metadata:
  openclaw:
    requires: {}
```

### ❌ Script Syntax Errors
```bash
# Test your script before publishing!
bash script.sh --test
# If EOF error or syntax issues → FLAGGED
```

---

## ✅ The CORRECT Pattern

### Declaring Requirements
```yaml
metadata:
  openclaw:
    requires:
      env:
        - MINIMAX_API_KEY
        - CUSTOM_VAR
      bins:
        - curl
        - whisper
```

### Using Env Vars (Auto-Injected)
```bash
# Just use directly - OpenClaw injects these
API_KEY="$MINIMAX_API_KEY"
curl -H "Authorization: Bearer ${API_KEY}" ...
```

### Adding Secrets to Config
```json
{
  "skills": {
    "entries": {
      "my-skill": {
        "enabled": true,
        "env": {
          "API_KEY": "actual_key_here"
        }
      }
    }
  }
}
```

---

## Scanner Checks (What Gets Flagged)

The ClawHub scanner verifies:

1. **Coherence**: Declared requirements match actual code
2. **No surprise permissions**: Env vars/bins declared = actually used
3. **No data exfiltration**: External URLs in docs = red flag
4. **Valid syntax**: Scripts must parse without errors
5. **Purpose clarity**: Description matches what code actually does

**Green = purpose, permissions, and code all match.**

---

## Pre-Publish Checklist

- [ ] No API keys hardcoded anywhere
- [ ] No `.env` loading statements
- [ ] All env vars declared in `requires.env`
- [ ] All bins declared in `requires.bins`
- [ ] No `homepage` key
- [ ] No external API URLs in docs
- [ ] Script has valid syntax (test it!)
- [ ] Script produces expected output
- [ ] Version bumped (1.0.0 → 1.0.1 → etc)
- [ ] Validated with quick_validate.py

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "Omits required env" | Env var used but not declared | Add to `requires.env` |
| "Binary not found" | Wrong binary name | Use exact name, no path |
| "Unexpected permissions" | More bins declared than needed | Remove unused |
| "Purpose mismatch" | Docs say one thing, code does another | Align description |
| "External endpoint" | URL mentioned in docs | Remove URL references |
| EOF/syntax error | Script has bash errors | Fix syntax before publish |

---

## Testing Tips

Test script locally:
```bash
# With inline env var for testing
MINIMAX_API_KEY=test_key bash scripts/script.sh --speak "test" en

# Check syntax
bash -n scripts/script.sh
```

---

## File Locations

| Purpose | Path |
|---------|------|
| Workspace skills | `~/.openclaw/workspace/skills/` |
| Global skills | `~/.openclaw/skills/` |
| Config | `~/.openclaw/openclaw.json` |
| Validator | `/home/kai/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py` |
| Template | `~/.openclaw/workspace/skills/kai-minimax-tts/` |

---

*Updated 2026-03-20 - Full scan passage for kai-minimax-tts and kai-skill-creator*
