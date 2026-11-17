---
name: md-linter
version: 2.0.0
description: Lint and auto-format Markdown: trailing whitespace, frontmatter validation, TOC generation
tags: ["markdown", "lint", "format", "toc", "cli", "docs", "python", "open-source", "agent", "automation", "MIT"]
---

# Markdown Linter & Formatter

**Lint and auto-format Markdown: trailing whitespace, frontmatter validation, TOC generation, external link checks.**

> *Keywords: markdown, lint, format, toc, cli, docs, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Markdown drift (broken links, missing TOC, bad frontmatter) hurts docs and SEO. Markdown Linter & Formatter solves this: Lint and auto-format Markdown: trailing whitespace, frontmatter validation, TOC generation, external link checks.

**Best for:** Docs owners, open-source maintainers, and agents generating Markdown.

## Features

- **Lint a Markdown file**
- **Auto-format/normalize**
- **Validate frontmatter**
- **Generate a TOC**
- **Check external links**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/md-linter/main/md_linter.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python md_linter.py self-test     # prove it works end-to-end
python md_linter.py check --help   # check subcommand
python md_linter.py toc --help   # toc subcommand
python md_linter.py links --help   # links subcommand
python md_linter.py frontmatter --help   # frontmatter subcommand
python md_linter.py format --help   # format subcommand
```

## Use cases

1. Lint a Markdown file
1. Auto-format/normalize
1. Validate frontmatter
1. Generate a TOC
1. Check external links

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| markdownlint | Adds TOC generation + frontmatter validation. |
| Manual TOC | One command. |
| Broken links | External-link checker. |

## FAQ (SEO / AEO)

**Q: TOC?**  
A: Yes — generate/insert a table of contents.

**Q: External links?**  
A: --check-external validates them.

**Q: Write?**  
A: --write reformats in place.

**Q: Offline?**  
A: External-link check needs network; linting is offline.

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
      - name: Self-test md-linter
        run: python md_linter.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/md-linter)
