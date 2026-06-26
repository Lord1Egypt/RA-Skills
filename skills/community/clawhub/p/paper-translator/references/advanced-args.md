# pdf2zh-next Parameter Reference

## Basic

```bash
pdf2zh_next <input.pdf> [args]
```

## Common

| Arg | Value/Example |
|-----|---------------|
| `--lang-in` / `--lang-out` | Source/Target language (e.g. `en`→`zh`) |
| `--qps 10` | Requests per second |
| `--pool-max-workers 100` | Concurrency (≈qps×10) |
| `--output /path` | Output directory |
| `--pages 1-5` | Page range |
| `--ignore-cache` | Ignore cache |
| `--no-dual` | No bilingual output |
| `--no-mono` | No monolingual output |
| `--no-auto-extract-glossary` | Skip glossary extraction |

## Compatibility

| Arg | Purpose |
|-----|---------|
| `--disable-rich-text-translate` | For complex PDFs |
| `--skip-clean` | Skip cleanup (faster, slightly lower quality) |
| `--enhance-compatibility` | Enable all compatibility modes |

## Performance

| Arg | Description |
|-----|-------------|
| `--max-pages-per-part 50` | Split large files (prevents OOM) |
| `--primary-font-family serif\|sans-serif` | Font selection |
| `--report-interval 5` | Report progress every 5 seconds |

## Full Documentation

https://pdf2zh-next.com/advanced/advanced.html