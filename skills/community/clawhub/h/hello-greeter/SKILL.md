---
name: hello-greeter
description: Generate personalized greeting messages in multiple languages and formats. Use when the user asks to create a greeting, welcome message, or salutation in a specific language or tone, or when building onboarding/welcome content that needs multilingual support.
---

# Hello Greeter

Generate personalized greetings in various languages and tones.

## Quick Start

Run the greeting script:

```bash
python3 scripts/greet.py --name "Alice" --lang en --tone formal
```

## Options

| Flag | Values | Default |
|------|--------|---------|
| `--name` | Any string | World |
| `--lang` | en, zh, ja, es, fr | en |
| `--tone` | formal, casual, playful | casual |

## Examples

```bash
python3 scripts/greet.py --name "小明" --lang zh --tone playful
python3 scripts/greet.py --name "Yuki" --lang ja --tone formal
```