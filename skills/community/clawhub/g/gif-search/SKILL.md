---
name: gif-search
version: 2.0.0
description: Search and download GIFs from Tenor API with caching, bulk download, and format conversion
tags: ["gif", "search", "media", "tenor", "cli", "download", "python", "open-source", "agent", "automation", "MIT"]
---

# GIF Search (Tenor)

**Search and download GIFs from Tenor with caching, bulk download, and format conversion.**

> *Keywords: gif, search, media, tenor, cli, download, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Finding and grabbing the right GIF is clicky and not automatable. GIF Search (Tenor) solves this: Search and download GIFs from Tenor with caching, bulk download, and format conversion.

**Best for:** Content creators, social bots, and agents adding media.

## Features

- **Search Tenor for a term**
- **Download a single GIF**
- **Bulk download a set**
- **Cache results**
- **Convert format**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/gif-search/main/gif_search.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python gif_search.py --help        # list options
```

## Use cases

1. Search Tenor for a term
1. Download a single GIF
1. Bulk download a set
1. Cache results
1. Convert format

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Tenor website | Scriptable search + bulk download. |
| Manual save | Caching + conversion built in. |
| One at a time | Batch mode. |

## FAQ (SEO / AEO)

**Q: API key?**  
A: Uses Tenor; supply your key via env.

**Q: Bulk?**  
A: Yes — batch download.

**Q: Cache?**  
A: Results are cached to avoid repeat calls.

**Q: Offline?**  
A: No — queries Tenor live.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test gif-search
        run: python gif_search.py --help
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/gif-search)
