---
name: Social Suite
description: Unified social media content pipeline. One command runs the full flywheel — pulls relevant content atoms from your library, audits AI signature (LinkedIn 360Brew detection), pre-flight checks platform-specific invisible rules, and outputs a combined PASS/FAIL verdict with specific fixes. Chains phy-content-compound + phy-content-humanizer-audit + phy-platform-rules-engine into a single pre-publish gate. Supports LinkedIn, Reddit, Twitter/X, HackerNews. Zero external dependencies.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - social-media
  - content
  - pipeline
  - linkedin
  - reddit
  - twitter
  - pre-publish
---

# phy-social-suite — One Command, Full Content Pipeline

Run the entire social media flywheel in one command:

```bash
# Full pipeline: atoms + AI audit + platform rules
python3 ~/.claude/skills/phy-social-suite/scripts/social_suite.py \
  --file draft.txt --platform linkedin \
  --library ~/Desktop/content-ideas/ --topic "developer tools"

# Quick check (no library)
echo "My post" | python3 ~/.claude/skills/phy-social-suite/scripts/social_suite.py --platform reddit
```

## What It Runs

| Stage | Skill | What It Does |
|-------|-------|-------------|
| 1 | `phy-content-compound` | Finds relevant atoms from your past content |
| 2 | `phy-content-humanizer-audit` | Checks AI signature (8 dimensions) |
| 3 | `phy-platform-rules-engine` | Pre-flight platform rules (28 rules) |
| Verdict | Combined | PASS/WARN/FAIL with specific fixes |

## Requirements

Install the 3 component skills first:
- `phy-content-compound`
- `phy-content-humanizer-audit`
- `phy-platform-rules-engine`

If any are missing, the suite skips that stage and notes it in the output.

## Companion Skills

| Skill | Role in Pipeline |
|-------|-----------------|
| `phy-post-forensics` | Run AFTER posting to analyze what worked |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
