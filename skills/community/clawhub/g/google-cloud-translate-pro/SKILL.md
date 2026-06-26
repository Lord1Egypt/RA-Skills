---
name: google-cloud-translate-pro
description: "Translate text across 195 languages using Google Cloud Translation API with zero-config setup. Use when: (1) translating text between any language pair, (2) detecting the language of unknown text, (3) bulk-translating multiple texts at once, (4) listing all supported languages, (5) building multilingual features into agent workflows. Powered by Google Cloud Translation — same engine behind Google Translate. Supports all 195 Google-supported languages including rare and low-resource languages. Drop-in replacement for Google Translate API at a fraction of the cost."
---

# Google Cloud Translate Pro

Translate text across **195 languages** powered by Google Cloud Translation — the same engine behind Google Translate.

## Quick Start

Get a free API key (500K credits, never expire):

```bash
curl -X POST https://api.socketsio.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpassword"}'
```

Set your key:

```bash
export SOCKETSIO_API_KEY=tr-your-key-here
```

## Capabilities

### Translate

Translate text to any of 195 languages. Auto-detects source language.

```bash
curl -X POST https://api.socketsio.com/v1/translate \
  -H "X-API-Key: $SOCKETSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello, how are you?", "target": "zh"}'
```

Response:

```json
{
  "data": {
    "translations": [{
      "translatedText": "你好，你好吗？",
      "detectedSourceLanguage": "en"
    }]
  }
}
```

### Detect Language

Identify the language of any text with confidence score.

```bash
curl -X POST https://api.socketsio.com/v1/detect \
  -H "X-API-Key: $SOCKETSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Bonjour le monde"}'
```

### Bulk Translate

Translate up to 128 texts in a single call.

```bash
curl -X POST https://api.socketsio.com/v1/translate \
  -H "X-API-Key: $SOCKETSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": ["Hello", "Goodbye", "Thank you"], "target": "es"}'
```

### List Languages

Get all 195 supported languages with display names.

```bash
curl https://api.socketsio.com/v1/languages \
  -H "X-API-Key: $SOCKETSIO_API_KEY"
```

## Agent Integration

For agent workflows, use the translate script directly:

```bash
python3 scripts/translate.py "Hello world" --target zh
python3 scripts/translate.py "Bonjour" --detect
python3 scripts/translate.py "Hello" "Goodbye" "Thanks" --target ja --bulk
```

The script reads `SOCKETSIO_API_KEY` from environment. See `scripts/translate.py --help` for all options.

## Google Translate v2 Compatible

The API is a drop-in replacement for Google Cloud Translation v2. If you have existing code using Google Translate, change only the base URL:

```python
# Before (Google, $20/M chars):
# url = "https://translation.googleapis.com/language/translate/v2"

# After (SocketsIO, $0.50/M chars):
url = "https://api.socketsio.com/v1/translate"
```

Same request format, same response format, 97% cheaper.

## Supported Languages

195 languages including: Afrikaans, Arabic, Bengali, Chinese (Simplified & Traditional), Czech, Danish, Dutch, English, Finnish, French, German, Greek, Gujarati, Hebrew, Hindi, Hungarian, Indonesian, Italian, Japanese, Kannada, Korean, Latvian, Lithuanian, Malay, Malayalam, Marathi, Norwegian, Persian, Polish, Portuguese, Punjabi, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tamil, Telugu, Thai, Turkish, Ukrainian, Urdu, Vietnamese, Welsh, and 147 more.

Full list: run `scripts/translate.py --languages` or call the `/v1/languages` endpoint.

## Pricing

| Tier | Price | Credits |
|------|-------|---------|
| Free Trial | $0 | 500K (never expire) |
| Starter | $5 | 2M |
| Growth | $20 | 10M |
| Scale | $100 | 50M |

For comparison: Google Translate API charges $20 per 1M characters. This skill uses the same Google engine at up to 97% less.

## Links

- API Docs: https://socketsio.com/docs
- Dashboard: https://socketsio.com/dashboard
- Pricing: https://socketsio.com/pricing
- Support: support@socketsio.com
