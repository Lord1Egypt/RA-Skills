---
name: claw0x-humanizer
description: >
  Remove signs of AI-generated writing from text via the Claw0x API. Use when the
  user asks to humanize text, make AI writing sound natural, remove AI patterns,
  rewrite to avoid AI detection, or clean up robotic-sounding content. Based on
  Wikipedia's 24 "Signs of AI writing" patterns. LLM-powered with regex fallback.
metadata:
  requires:
    env:
      - CLAW0X_API_KEY
---

# AI Text Humanizer

Rewrite AI-generated text to remove robotic patterns and make it sound naturally human. Targets 24 known AI writing signatures including filler phrases, AI vocabulary, sycophantic tone, and formulaic structure.

## How It Works — Under the Hood

This skill uses a two-layer architecture to transform AI-generated text into human-sounding prose:

### Layer 1: LLM Rewriting (Primary)

The primary path sends your text to a large language model (Gemini) with a carefully engineered system prompt derived from Wikipedia's WikiProject AI Cleanup guide. The LLM API key (`GEMINI_API_KEY`) is managed server-side by the Claw0x platform — callers do not need to provide or configure it. You only need a `CLAW0X_API_KEY` to authenticate through the Gateway. The system prompt instructs the model to:

1. Scan the input for all 24 known AI writing patterns
2. Rewrite the text to eliminate those patterns while preserving meaning
3. Audit the rewritten output for any lingering AI-isms
4. Revise a second time to catch patterns that survived the first pass

The LLM is also given personality rules: have opinions, vary sentence rhythm, acknowledge complexity, use "I" when natural, and let some structural imperfection through.

### Layer 2: Regex Fallback (Deterministic)

If the LLM is unavailable (rate limit, timeout), the skill falls back to a deterministic regex engine that applies pattern-matched replacements across six categories:

- Chatbot artifacts — removes "I hope this helps!", "Let me know if..."
- Filler phrases — "in order to" → "to", "due to the fact that" → "because"
- Significance inflation — "marking a pivotal moment" → removed
- Copula avoidance — "serves as" → "is"
- AI vocabulary — 40+ word substitutions (e.g. "leverage" → "use")
- Emoji removal and em-dash normalization

The regex path is lower quality but instant, deterministic, and zero-cost.

## Prerequisites

This skill requires a Claw0x API key:

1. Sign up at [claw0x.com](https://claw0x.com)
2. Go to Dashboard → API Keys → Create Key
3. Store the key securely using one of these methods:
   - Add `CLAW0X_API_KEY` to your agent's secure environment variables
   - Use your platform's secret manager (e.g. GitHub Secrets, Vercel env vars)
   - Use a `.env` file excluded from version control via `.gitignore`

> Security note: Never embed API keys in prompts, source code, or version-controlled files.

## When to Use

- User says "humanize this", "make this sound more natural", "remove AI patterns"
- User wants text to pass AI detection tools (GPTZero, Originality.ai, etc.)
- Agent pipeline produces text that needs to sound human-written
- Content teams need to clean up AI-drafted blog posts, emails, or documentation

## API Call

```bash
curl -s -X POST https://claw0x.com/v1/call \
  -H "Authorization: Bearer $CLAW0X_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "humanizer",
    "input": {
      "text": "Your AI-generated text here..."
    }
  }'
```

## Input

The `input` field accepts an object with one of these keys:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input.text` | string | yes (one of) | Text to humanize |
| `input.content` | string | yes (one of) | Alternative key for the text |
| `input.body` | string | yes (one of) | Alternative key for the text |

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `humanized_text` | string | The rewritten text with AI patterns removed |
| `original_length` | number | Character count of original text |
| `humanized_length` | number | Character count of humanized text |
| `method` | string | `"llm"` (AI rewrite) or `"regex"` (deterministic fallback) |

## Example

**Input:**
```json
{
  "skill": "humanizer",
  "input": {
    "text": "Additionally, it is worth noting that this groundbreaking solution serves as a testament to the transformative power of innovation. The future looks bright for this pivotal technology. I hope this helps!"
  }
}
```

**Output:**
```json
{
  "humanized_text": "This solution shows what good engineering looks like in practice. The technology has real potential, though how it plays out depends on adoption.",
  "original_length": 204,
  "humanized_length": 138,
  "method": "llm"
}
```

## Error Codes

- `400` — Missing or empty text input
- `500` — Processing failed (not billed)

## Pricing

Pay-per-successful-call only. Failed calls and 5xx errors are never charged.
