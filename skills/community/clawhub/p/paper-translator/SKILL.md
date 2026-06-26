# Paper Translator

Translates academic PDFs (EN→ZH), preserving formulas and layout. Generates bilingual version + Chinese-only version + glossary.

## One-liner

```bash
bash <this-skill>/scripts/translate_paper.sh <paper.pdf>
```

Outputs (same directory):
- `xxx.zh.dual.pdf` — Bilingual (EN+ZH)
- `xxx.zh.mono.pdf` — Chinese only
- `xxx.zh.glossary.csv` — Glossary

## Arguments

Add after the script:

| Arg | Example | Description |
|-----|---------|-------------|
| `--lang-out` | `zh-CN` | Target language |
| `--pages` | `1-10` | Translate first 10 pages only |
| `--no-dual` | | Generate monolingual only |
| `--ignore-cache` | | Re-translate ignoring cache |
| `--output` | `/out` | Output directory |

## Auto-installed dependencies

Checks for `uv` and `pdf2zh-next` on first run; installs automatically if missing.

## Full arguments

See [references/advanced-args.md](references/advanced-args.md)

## References

- [pdf2zh-next](https://pdf2zh-next.com/)
- [PDFMathTranslate-next](https://github.com/PDFMathTranslate-next/PDFMathTranslate-next)

## QQBot Send

```bash
cp *.pdf ~/.openclaw/media/qqbot/uploads/
```

Then send using `<qqmedia>/path/to/file.pdf</qqmedia>`. Max 10MB per file.