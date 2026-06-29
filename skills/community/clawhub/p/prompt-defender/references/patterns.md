# Prompt Guard — Detection Patterns Reference

## Sensitive Data Patterns

| Pattern | Example | Risk Level |
|---------|---------|-----------|
| API Key (`sk-*` 20+ chars) | `sk-proj-abc123...` | Critical |
| Password/Secret inline | `password=supersecret!` | Critical |
| Chinese ID (18-digit) | `110101199001011234` | Critical |
| Chinese Phone | `13800138000` | High |
| Bank Card (13-19 digits) | `6222021234567890` | Critical |
| Access Token (40+ base64) | `ghp_xxxxxxxx...` | Critical |

## Injection Patterns

- "Ignore previous instructions"
- "Disregard all prior directives"
- "Forget everything you know"
- "You are now [new role]..."
- "New role/character/persona: ..."
- "Rewrite all instructions/rules"

## Jailbreak Patterns

- "DAN" (Do Anything Now)
- "No restrictions/limits/rules"
- Base64-encoded instructions
- Unicode escape tricks
- "Pretend/act as if you have no rules"
- "Output raw/unfiltered/uncensored"

## Score Calculation

Score = max(0, 100 - weighted_count * 12)
- Sensitive data: ×3 weight
- Injection: ×2 weight
- Jailbreak: ×2 weight

## Fix Suggestions

- **API Key leak**: Replace with `{{API_KEY}}` placeholder. Rotate the leaked key.
- **Password leak**: Replace with `{{PASSWORD}}`. Change the compromised password.
- **ID leak**: Redact middle digits. No real user ID should be in prompts.
- **Injection**: Wrap user input in a clearly delimited block; apply input sanitization.
- **Jailbreak**: Add system-level guardrails; reject known jailbreak patterns before passing to LLM.
