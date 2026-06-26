# Sandbox Testing Procedure

## Sub-Agent Spawn Template

```javascript
sessions_spawn({
    runtime: "subagent",
    mode: "run",
    cleanup: "delete",
    timeoutSeconds: 120,
    task: `Security testing agent in isolated sandbox.

SKILL TO TEST: {skill-name}

COMMANDS:
1. openclaw skill install {skill-name}
2. SKILL_PATH=~/.openclaw/workspace/skills/{skill-name}
3. ls -laR $SKILL_PATH
4. find $SKILL_PATH -type f \( -name "*.sh" -o -name "*.py" -o -name "*.js" -o -perm -111 \)
5. grep -rE "curl.*sh|wget.*sh|eval|exec|rm -rf|sudo|~/.ssh|~/.aws|base64.*decode|nc -l|chmod +x|crontab" $SKILL_PATH
6. grep -rE "https?://|wss?://" $SKILL_PATH
7. head -50 $SKILL_PATH/SKILL.md

OUTPUT JSON between <<<JSON>>> and <<<END>>>:
<<<JSON>>>
{
  "skill_name": "{skill-name}",
  "installed": true/false,
  "file_count": number,
  "executables": ["list"],
  "suspicious_patterns": [{"pattern": "name", "file": "path", "line": "content"}],
  "network_calls": ["urls"],
  "red_flags_count": number,
  "risk_level": "SAFE|REVIEW|REJECT",
  "recommendation": "brief text"
}
<<<END>>>`
})
```

## Parsing Response

1. Extract JSON between `<<<JSON>>>` and `<<<END>>>`
2. Fallback: try markdown code blocks
3. Validate required fields
4. Handle parse errors gracefully

## Risk Assessment

- 0 red flags → ✅ PASSED
- 1-2 red flags → ⚠️ REVIEW REQUIRED
- 3+ red flags → ❌ FAILED
