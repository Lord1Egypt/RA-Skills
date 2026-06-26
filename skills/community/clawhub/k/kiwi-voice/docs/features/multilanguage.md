# Multi-Language Support

Kiwi ships with **15 languages** out of the box. All user-facing strings, voice commands, wake word variants, hallucination filters, and security patterns are fully localized.

## Available Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| `en` | English | `tr` | Turkish |
| `ru` | Russian | `pl` | Polish |
| `es` | Spanish | `zh` | Chinese |
| `pt` | Portuguese | `ja` | Japanese |
| `fr` | French | `ko` | Korean |
| `it` | Italian | `hi` | Hindi |
| `de` | German | `ar` | Arabic |
| `id` | Indonesian | | |

## Switching Language

### Via config.yaml

```yaml
language: "en"
```

### Via environment variable

```bash
KIWI_LANGUAGE=es python -m kiwi
```

### Via REST API (runtime)

```bash
curl -X POST http://localhost:7789/api/language \
  -H "Content-Type: application/json" \
  -d '{"language": "fr"}'
```

### Via Dashboard

Use the Language panel dropdown and click Apply.

## What Gets Localized

Each locale YAML file (`kiwi/locales/{code}.yaml`) contains 19 sections:

| Section | Content |
|---------|---------|
| `system` | Voice system prompt for the LLM |
| `responses` | ~37 spoken user-facing strings |
| `status` | Long-task status announcements |
| `security` | Warning messages, Telegram button labels |
| `speakers` | Speaker identification responses |
| `speaker_access` | Access control messages |
| `wake_word` | Keyword, typos, fuzzy blacklist |
| `hallucinations` | Whisper hallucination phrases/patterns |
| `text_processing` | Abbreviations, incomplete/complete patterns, emotion keywords |
| `security_patterns` | Dangerous command regexes |
| `dangerous_commands` | Example dangerous commands |
| `owner_commands` | Voice control command phrases |
| `owner_control_patterns` | Owner command regexes |
| `name_patterns` | Name extraction regexes and filter words |
| `commands` | Command keywords (stop, calibrate, approval, etc.) |
| `cli_errors` | CLI error messages |
| `ws_errors` | WebSocket error messages |
| `tool_activity` | Tool status descriptions |
| `tool_errors` | Tool error messages |

## Adding a New Language

1. Copy the English locale as a template:

    ```bash
    cp kiwi/locales/en.yaml kiwi/locales/sv.yaml
    ```

2. Translate all string values. Preserve keys and `{placeholder}` tokens:

    ```yaml
    responses:
      greeting: "Hej! Jag är Kiwi..."
      heard: "Hörde: {command}"
    ```

3. Adapt language-specific sections that require linguistic knowledge:
    - `wake_word.typos` — phonetic variants in the target language
    - `hallucinations.phrases` — common Whisper hallucinations for that language
    - `text_processing` — abbreviations and patterns
    - `security_patterns` — dangerous command regexes in the target language

4. Set the language:

    ```yaml
    language: "sv"
    ```

## i18n API

Internally, Kiwi uses the `t()` function from `kiwi/i18n.py`:

```python
from kiwi.i18n import setup, t

setup("en", fallback="ru")       # Initialize
t("responses.greeting")           # → "Hello! I'm Kiwi..."
t("responses.heard", command=cmd) # → "Heard: {command}" with placeholder
t("hallucinations.phrases")       # → returns a list
```

- Dot-notation key resolution
- Automatic fallback to the fallback locale if a key is missing
- Returns lists and dicts as-is for non-string values
