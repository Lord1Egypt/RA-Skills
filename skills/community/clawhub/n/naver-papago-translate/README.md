# naver-papago-translate

Simple CLI and Python API for Naver Papago NMT translation.

- Translates between Korean, English, Japanese, Chinese (zh-CN/zh-TW), Vietnamese, Indonesian, Thai, German, Russian, Spanish, Italian, and French via Papago NMT.
- No SDK required — uses HTTPS REST.
- Works headless; ideal for automation and AI agent skills.

## Quickstart

1) Get API credentials from Naver Developers (Papago 번역 NMT):
   - Create an app, then copy your Client ID and Client Secret.

2) Export environment variables:

```bash
export NAVER_CLIENT_ID="your-client-id"
export NAVER_CLIENT_SECRET="your-client-secret"
```

3) Install and run

```bash
pip install .
papago-translate --source ko --target en "안녕하세요, 만나서 반가워요!"
```

Output:
```
Hello, nice to meet you!
```

## CLI usage

```
papago-translate [OPTIONS] "text to translate"

Options:
  -s, --source TEXT   Source language code (e.g., ko, en, ja, zh-CN, zh-TW)
  -t, --target TEXT   Target language code (required)
  -f, --file PATH     Read input text from a file instead of argv
  --detect            Auto-detect source language (Papago detectLangs API)
  --json              Output JSON with metadata
  --timeout FLOAT     HTTP timeout seconds (default: 15)
  -v, --verbose       Print debug info to stderr
  -h, --help          Show help
```

Examples:
- Auto-detect source, translate to Korean:
  ```bash
  papago-translate --detect --target ko "See you tomorrow!"
  ```
- Translate file to English:
  ```bash
  papago-translate -s ko -t en -f notes.txt
  ```

## Python API

```python
from papago_translate import translate_text, detect_language

text = translate_text("ko", "en", "테스트 중입니다.")
lang = detect_language("Bonjour")
```

## Supported languages
According to the official docs, common codes include: ko, en, ja, zh-CN, zh-TW, vi, id, th, de, ru, es, it, fr. See Naver docs for full/updated list.

## Configuration
- NAVER_CLIENT_ID — required
- NAVER_CLIENT_SECRET — required

You can also configure via CLI flags `--client-id` and `--client-secret` (override env vars) if needed for sandboxing.

## License
MIT

## Security
- Credentials are read from environment variables or flags and never logged unless `--verbose` is set.
- HTTPS to `https://openapi.naver.com` with application/x-www-form-urlencoded per docs.

## References
- Papago NMT API: https://openapi.naver.com/v1/papago/n2mt
- Language detect: https://openapi.naver.com/v1/papago/detectLangs
- Docs: https://developers.naver.com/docs/papago/papago-nmt-api-reference.md
