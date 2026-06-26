---
name: mind-security
description: >
  AI security toolkit — deepfake detection, prompt injection scanning,
  malware/phishing URL scanning, and AI text detection.
  Use when: (1) verifying if an image, video, or audio is a deepfake or AI-generated,
  (2) scanning user inputs for prompt injection attacks,
  (3) scanning URLs for malware, phishing, or domain reputation threats,
  (4) determining if text was written by an LLM.
metadata: {"openclaw": {"emoji": "🛡️", "primaryEnv": "BITMIND_API_KEY", "requires": {"bins": ["python3"], "anyBins": ["curl", "wget"], "env": ["BITMIND_API_KEY", "GPTZERO_API_KEY", "VIRUSTOTAL_API_KEY", "URLSCAN_API_KEY", "GOOGLE_SAFE_BROWSING_KEY"]}, "homepage": "https://github.com/mind-sec/mind-security"}}
---

# mind-security

AI security toolkit with four active modules.

## Quick Reference

| Task | Command | Docs |
|------|---------|------|
| Deepfake detection | `python3 scripts/check_deepfake.py <path_or_url>` | [deepfake-detection.md](references/deepfake-detection.md) |
| Prompt injection scan | `python3 scripts/check_prompt_injection.py "<text>"` | [prompt-injection.md](references/prompt-injection.md) |
| Malware/phishing scan | `python3 scripts/check_malware.py "https://..."` | [malware-scanning.md](references/malware-scanning.md) |
| AI text detection | `python3 scripts/check_ai_text.py "<text>"` | [ai-text-detection.md](references/ai-text-detection.md) |

## Modules

**Deepfake detection** — BitMind API (Bittensor Subnet 34) for images and videos. Supports YouTube, Twitter/X, TikTok URLs. EXIF/metadata fallback for local images. Set `BITMIND_API_KEY` ([get key](https://app.bitmind.ai/api/keys)).

**Prompt injection detection** — Multi-layer scanner: 50+ regex patterns (instant, zero-dep) + LLM Guard ML model (optional, `pip install llm-guard`). Identifies known injection signatures, role-override attempts, and instruction-bypass patterns.

**Malware/phishing scanning** — VirusTotal (70+ engines), URLScan.io (1500+ brands), Google Safe Browsing, plus local heuristics (typosquatting, suspicious TLDs, phishing patterns). Works with no keys via heuristics.

**AI text detection** — GPTZero API with per-sentence scoring and ~99% accuracy across GPT-4/5, Claude, Gemini, LLaMA. Requires `GPTZERO_API_KEY` ([get key](https://gptzero.me/dashboard)).

## API Keys

| Env Var | Used By | Required | Get It |
|---------|---------|----------|--------|
| `BITMIND_API_KEY` | Deepfake detection | For API mode | [app.bitmind.ai/api/keys](https://app.bitmind.ai/api/keys) |
| `GPTZERO_API_KEY` | AI text detection | **Yes** | [gptzero.me/dashboard](https://gptzero.me/dashboard) |
| `VIRUSTOTAL_API_KEY` | Malware scanner | Optional | [virustotal.com](https://virustotal.com) |
| `URLSCAN_API_KEY` | Malware scanner | Optional | [urlscan.io](https://urlscan.io) |
| `GOOGLE_SAFE_BROWSING_KEY` | Malware scanner | Optional | [console.cloud.google.com](https://console.cloud.google.com) |

## Script Conventions

- `python3 scripts/<script>.py --help`
- Core: zero pip dependencies (stdlib only)
- Optional ML: `pip install llm-guard` for prompt injection Layer 2
- JSON to stdout, errors to stderr
- Exit 0 success, exit 1 failure

## Security & Privacy

**External endpoints** — this skill sends user-provided data to the following third-party APIs for analysis. No data is stored or logged by the skill itself:

| API | Used By | Data Sent |
|-----|---------|----------|
| [BitMind](https://bitmind.ai) | Deepfake detection | Image/video files or URLs |
| [GPTZero](https://gptzero.me) | AI text detection | Text content |
| [VirusTotal](https://virustotal.com) | Malware scanner | URLs (not file contents) |
| [URLScan.io](https://urlscan.io) | Malware scanner | URLs |
| [Google Safe Browsing](https://safebrowsing.google.com) | Malware scanner | URLs |

**Trust statement** — All modules use Python stdlib only (no pip dependencies for core). API calls use `urllib.request` with explicit timeouts (10–120s). No telemetry, no analytics, no phone-home beyond the declared API calls above.
