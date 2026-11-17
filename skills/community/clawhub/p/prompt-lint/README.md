[![ClawHub](https://img.shields.io/badge/ClawHub-prompt-lint-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: prompt-lint
version: 2.0.0
description: Lint AI prompts: clarity, safety, injection risks, template validity
tags: ["lint", "prompt", "ai", "cli", "safety", "quality", "python", "open-source", "agent", "automation", "MIT"]
---

# Prompt Linter

**Lint AI prompts for clarity, safety, injection risk, and template validity — scored 0-100.**

> *Keywords: lint, prompt, ai, cli, safety, quality, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Bad prompts produce bad outputs; quality isn't measurable. Prompt Linter solves this: Lint AI prompts for clarity, safety, injection risk, and template validity — scored 0-100.

**Best for:** Prompt engineers, agent builders, and AI product teams.

## Features

- **Lint a prompt file**
- **Score quality 0-100**
- **Detect injection risk**
- **Validate template vars**
- **JSON output for CI**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/prompt-lint/main/prompt_lint.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python prompt_lint.py self-test     # prove it works end-to-end
python prompt_lint.py check --help   # check subcommand
```

## Use cases

1. Lint a prompt file
1. Score quality 0-100
1. Detect injection risk
1. Validate template vars
1. JSON output for CI

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Eyeballing prompts | Measurable quality + safety. |
| Partial linters | Adds injection + template checks. |
| No gate | CI-ready scoring. |

## FAQ (SEO / AEO)

**Q: Score?**  
A: 0-100 quality score with reasons.

**Q: Injection?**  
A: Flags prompt-injection patterns.

**Q: CI?**  
A: Yes — --json, non-zero on failure.

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
      - name: Self-test prompt-lint
        run: python prompt_lint.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/prompt-lint)
