---
name: liveos-community
description: Work with the open LiveOS Community repo for public-screen live-commerce monitoring demos, without touching commercial Feishu, Buyin, OpenClaw anchor, or customer-secret workflows.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python
    emoji: "📺"
    homepage: https://github.com/zhujiushequn/liveos-community
---

# LiveOS Community

Use this skill when the user wants to understand, run, or extend the public
LiveOS Community repository.

## Boundary

This skill is only for the open community edition:

- public-screen event parsing
- local sample-data demos
- local Markdown report generation
- integration interface discussion

Do not claim the community edition includes:

- Feishu robot auto-creation or permissions
- OpenClaw production `anchor` routing
- private-chat `JOB_STARTED` acceptance
- DeepSeek production prompts or keys
- Buyin/Juliang Baiying login, account switching, same-source KPI, or replay automation
- customer logs, browser cookies, or generated commercial reports

## Quick Commands

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m liveos_community.cli demo --minutes 5
```

## Agent Guidance

If asked to add features, keep the open-core boundary intact. Add interfaces,
examples, docs, tests, or local demo behavior. Do not copy closed commercial
logic from private LiveOS installs into this repository.

