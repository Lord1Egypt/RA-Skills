---
name: personal-insight-engine
description: Personal Insight Engine (PIE) - A strategic analysis tool that scans local session logs (memory/*.md) and extracts 3 strategic insights using LLMs.
version: 1.0.4
metadata:
  {
    "openclaw":
      {
        "requires": { 
          "bins": ["python3"], 
          "env": ["ZHIPU_API_KEY", "GEMINI_API_KEY"],
          "python_packages": ["httpx", "python-dotenv"] 
        },
      },
  }
---

# PIE (Personal Insight Engine)

Analyze your startup journey by distilling strategic patterns from your memory logs.

## Setup

**1. Configure API Keys:**
PIE requires at least **one** of the following environment variables. If both are provided, Gemini is used by default.
- `GEMINI_API_KEY`: For Google Gemini 2.0 Flash (Recommended).
- `ZHIPU_API_KEY`: For Zhipu AI GLM-4.

**2. Dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Run Weekly Review
By default, scans the last 7 days and auto-detects the provider:

```bash
python3 scripts/pie.py
```

### Force a Provider
If you want to use a specific LLM regardless of your environment defaults:

```bash
python3 scripts/pie.py --provider zhipu
python3 scripts/pie.py --provider gemini
```

### Custom Lookback
Scan a specific number of days (e.g., last 30 days):

```bash
python3 scripts/pie.py --days 30
```

## Privacy & Safety (Hardened)

PIE is built for high-stakes startup analysis where privacy is non-negotiable:
- **Zero-Exposure Redaction**: Before transmission, all content is scrubbed for:
  - API Keys, Tokens, and Passwords (regex-hardened).
  - Email addresses and IP addresses.
  - Local file system paths (home/user directories).
- **Standardized Pathing**: Only scans the `memory/` folder within the official `OPENCLAW_WORKSPACE`.
- **Content Distillation**: Strips out JSON metadata and system headers to ensure the LLM only sees the semantic dialogue.

## How it works

1. **Discovery**: Standardized scan of `memory/` via `OPENCLAW_WORKSPACE`.
2. **Sanitization**: Multi-stage PII redaction (IPs, Emails, Keys, Paths).
3. **Synthesis**: Pattern recognition across logs for strategic pivots and pain points.
4. **Output**: Formatted Markdown report for the startup founder.

---
*Developed by Leo & Neo (Startup Partners)*
