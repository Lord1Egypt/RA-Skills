---
name: polyglot
description: Translate text to any language with formality control and cultural notes. Target language defaults to English.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "🌐"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Polyglot

Translate text between any languages with formality control and cultural context. Detects source language automatically and provides notes on idioms, formality, and cultural considerations. Target language defaults to English if not specified.

## When to Use

- Translating documents or messages
- Understanding foreign language content
- Localizing content with cultural awareness
- Controlling tone with formal or informal register
- Learning about linguistic nuances

## Usage Flow

1. Provide text to translate
2. Optionally specify `target_language` (defaults to English)
3. Optionally set `formality`: `formal`, `informal`, or `neutral` (default)
4. AIProx routes to the polyglot agent
5. Returns translated text, detected source language, target language used, cultural notes, and formality level

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "text": "The early bird catches the worm",
    "target_language": "Japanese",
    "formality": "formal",
    "task": "translate"
  }'
```

### Response

```json
{
  "translated": "早起きは三文の徳",
  "language": "English",
  "target_language": "Japanese",
  "notes": "Used the equivalent Japanese proverb '早起きは三文の徳' (hayaoki wa sanmon no toku) meaning 'waking early brings three mon of virtue.' Both emphasize benefits of rising early; the Japanese version focuses on small but certain gains.",
  "formality": "formal"
}
```

## Trust Statement

Polyglot processes text for translation only. Content is not stored or logged beyond the transaction. Translation is performed by Claude via LightningProx. Your spend token is used for payment only.
