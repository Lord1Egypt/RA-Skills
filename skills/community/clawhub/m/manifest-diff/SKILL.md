---
name: manifest-diff
version: 2.0.0
description: Diff agent/skill manifests: capabilities, permissions, versions
tags: ["diff", "manifest", "agent", "cli", "audit", "security", "python", "open-source", "automation", "MIT"]
---

# Manifest Diff

**Diff two agent/skill manifests and report capability, permission, and version changes.**

> *Keywords: diff, manifest, agent, cli, audit, security, python, open-source, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Spotting what changed between two agent manifests by eye is error-prone. Manifest Diff solves this: Diff two agent/skill manifests and report capability, permission, and version changes.

**Best for:** Agent reviewers and platform teams managing versions.

## Features

- **Diff two manifests**
- **See capability changes**
- **Flag permission deltas**
- **Catch version downgrades**
- **JSON output for CI**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/manifest-diff/main/manifest_diff.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python manifest_diff.py self-test     # prove it works end-to-end
python manifest_diff.py diff --help   # diff subcommand
```

## Use cases

1. Diff two manifests
1. See capability changes
1. Flag permission deltas
1. Catch version downgrades
1. JSON output for CI

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Reading both files | Automatic delta report. |
| diff on raw JSON | Semantic, not textual. |
| Guessing risk | Permission deltas surfaced explicitly. |

## FAQ (SEO / AEO)

**Q: Input?**  
A: Two manifest files (a/b).

**Q: What changes?**  
A: Capabilities, permissions, versions.

**Q: CI?**  
A: Yes — --json.

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
      - name: Self-test manifest-diff
        run: python manifest_diff.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/manifest-diff)
