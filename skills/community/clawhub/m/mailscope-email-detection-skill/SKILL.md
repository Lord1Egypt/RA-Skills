---
name: mailscope-email-detection
description: |
  Email security detection and analysis. Use this skill whenever the user wants to analyze, scan, or check the security of an email (.eml) file. This includes phishing detection, spoofing analysis, malicious attachment scanning, and general email threat assessment. Also use this skill when the user wants to configure their Mailscope API key (e.g. "set my api key", "configure the key", "here is my api key", "帮我配置 key"). Trigger when the user says things like "analyze this email", "check if this email is safe", "scan this .eml file", "is this phishing?", or provides a path to an .eml file and asks about its safety.
version: 0.0.1
author: ddgszc
tags: ["email", "security", "phishing", "malware", "detection"]
---

# Mailscope Email Detection

Use this skill when the user wants to perform security analysis on an email (.eml) file. The skill provides a comprehensive security assessment report by uploading the file to the Mailscope analysis platform.

## Language

Respond in the user's language. If they write in Chinese, reply in Chinese; if English, English. Keep technical tokens (paths, flags, field names) in English.

## Workflow

### Step 0: Configure API Key

When the user provides an API key (e.g., "我的 key 是 msk_xxx", "帮我配置 API Key", "set api key to msk_xxx", "这是key: msk_xxx"), write it into `config.json`:

1. Check if `config.json` exists in the skill root directory. If not, read `config.json.example` as a template and create `config.json` from it.
2. Read the current `config.json` and parse it as JSON.
3. Set the `api_key` field to the key the user provided.
4. Write the updated JSON back to `config.json` (use 2-space indentation for readability).
5. Confirm to the user: "API Key 已配置成功。"

The user gets their API key by applying at https://x.lizhisec.com. If they ask where to get one, point them there.

### Step 1: Check prerequisites

Before running the analysis, verify these conditions are met:

1. **Node.js 22+** is available. Check with `node --version`. If not available, tell the user to install Node.js 22+.
2. **config.json** exists with a valid `api_key`. If missing, guide the user through Step 0 above.

### Step 2: Run the analysis script

```bash
npx tsx scripts/analyze.ts <path/to/email.eml>
```

The script will:
1. Upload the .eml file to the analysis platform
2. Poll for results every 3 seconds until analysis completes
3. Display a formatted security analysis report

### Step 3: Interpret results for the user

The report output is self-contained and human-readable. Key elements to help the user understand:

- **风险等级 (Risk Tier)**: `risky` (dangerous), `clean` (safe), or other levels
- **置信度 (Confidence)**: AI confidence percentage
- **身份认证 (Authentication)**: SPF, DKIM, DMARC results
- **域名信息 (Domain Profile)**: Registration date, ICP record - recently registered domains are suspicious
- **AI 综合分析 (AI Analysis)**: Detailed threat assessment covering identity verification, behavioral patterns, intent recognition, and comprehensive judgment

If the email is flagged as `risky`, emphasize the recommended actions:
- Isolate the email immediately
- Block the sender domain
- Do NOT open attachments or enter passwords
- Preserve the .eml file for forensics

### Error handling

Common errors and how to address them:

| Error | Cause | Solution |
|-------|-------|----------|
| API key not configured | Missing or empty config.json | Guide user to set up config.json |
| Upload failed (HTTP 4xx) | Invalid API key | Re-apply at https://x.lizhisec.com |
| Analysis failed | Email could not be processed | Check if the .eml file is malformed |
| Analysis timeout | Platform overloaded | Wait and retry later |
| File not found | Path typo | Verify the .eml file path |

### What NOT to do

- Do NOT read raw JSON from the API response and present it directly to users
- Do NOT hardcode any API keys in responses visible to the user
- Do NOT modify `config.json` unless the user explicitly asked you to configure their API key (see Step 0)
- Do NOT expose the API_BASE_URL configuration to users (internal detail)
