[![ClawHub](https://img.shields.io/badge/ClawHub-json-tools-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: json-tools
version: 2.0.0
description: Validate, format, query, diff, filter, flatten, merge JSON files with dot-notation paths
tags: ["json", "tools", "validate", "query", "diff", "cli", "data", "python", "open-source", "agent", "automation", "MIT"]
---

# JSON Toolkit

**Validate, format, query, diff, filter, flatten, and merge JSON with dot-notation paths.**

> *Keywords: json, tools, validate, query, diff, cli, data, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

JSON wrangling across many small tasks needs many one-off tools. JSON Toolkit solves this: Validate, format, query, diff, filter, flatten, and merge JSON with dot-notation paths.

**Best for:** Developers, data engineers, and agents processing JSON.

## Features

- **Validate JSON**
- **Format/pretty-print**
- **Query by dot path**
- **Diff two files**
- **Flatten/merge**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/json-tools/main/json_tools.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python json_tools.py self-test     # prove it works end-to-end
python json_tools.py validate --help   # validate subcommand
python json_tools.py format --help   # format subcommand
python json_tools.py query --help   # query subcommand
python json_tools.py diff --help   # diff subcommand
python json_tools.py filter --help   # filter subcommand
python json_tools.py stats --help   # stats subcommand
python json_tools.py flatten --help   # flatten subcommand
python json_tools.py merge --help   # merge subcommand
```

## Use cases

1. Validate JSON
1. Format/pretty-print
1. Query by dot path
1. Diff two files
1. Flatten/merge

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| jq | Familiar dot-path query plus diff/flatten/merge. |
| Online JSON formatters | Local, no upload. |
| Multiple tools | One CLI for the whole lifecycle. |

## FAQ (SEO / AEO)

**Q: Query syntax?**  
A: Dot-notation paths (e.g. a.b.c).

**Q: Diff?**  
A: Semantic diff of two JSON files.

**Q: Merge?**  
A: Deep merge with conflict handling.

**Q: Offline?**  
A: Yes.

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
      - name: Self-test json-tools
        run: python json_tools.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/json-tools)
