---
name: naver-papago-translate
description: Translate text between Korean, English, Japanese, Chinese, and 10+ other languages using Naver Papago NMT. Ideal for Korean-centric workflows, i18n tasks, and automation pipelines.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - NAVER_CLIENT_ID
        - NAVER_CLIENT_SECRET
      bins:
        - python3
    primaryEnv: NAVER_CLIENT_ID
    homepage: https://github.com/ChloePark85/naver-papago-translate
    install:
      - kind: uv
        package: naver-papago-translate
        bins: [papago-translate]
---

# naver-papago-translate

Translate text through Naver's Papago NMT API from the CLI or Python. Supports 13+ language pairs (ko/en/ja/zh-CN/zh-TW/vi/id/th/de/ru/es/it/fr) with optional auto-detect.

## When to use

- You need high-quality Korean↔X translation (Papago is tuned for Korean).
- You want a headless, dependency-light translator for agent pipelines.
- You prefer official Naver Developer credentials over scraping.

## Prerequisites

1. Get credentials from [Naver Developers](https://developers.naver.com/) → create a Papago NMT app.
2. Export environment variables:

```bash
export NAVER_CLIENT_ID="your-client-id"
export NAVER_CLIENT_SECRET="your-client-secret"
```

3. Install:

```bash
pip install naver-papago-translate
# or from source
pip install git+https://github.com/ChloePark85/naver-papago-translate
```

## CLI

```bash
papago-translate --source ko --target en "안녕하세요, 만나서 반가워요!"
# → Hello, nice to meet you!

# Auto-detect source
papago-translate --detect --target ko "See you tomorrow!"

# Read from file, JSON output
papago-translate -s ko -t en -f notes.txt --json
```

Options: `-s/--source`, `-t/--target` (required), `-f/--file`, `--detect`, `--json`, `--timeout`, `-v/--verbose`.

## Python API

```python
from papago_translate import translate_text, detect_language

out = translate_text("ko", "en", "테스트 중입니다.")
lang = detect_language("Bonjour")
```

## Supported languages

`ko, en, ja, zh-CN, zh-TW, vi, id, th, de, ru, es, it, fr` — see [Naver docs](https://developers.naver.com/docs/papago/papago-nmt-api-reference.md) for the current list.

## Security

- Credentials read only from env or flags; never logged unless `--verbose`.
- HTTPS to `openapi.naver.com`.

## References

- Papago NMT: https://openapi.naver.com/v1/papago/n2mt
- Detect language: https://openapi.naver.com/v1/papago/detectLangs
- Source: https://github.com/ChloePark85/naver-papago-translate
