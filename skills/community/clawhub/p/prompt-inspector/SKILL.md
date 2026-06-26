---
name: prompt-inspector
description: "Detect prompt injection attacks and adversarial inputs in user text before passing it to your LLM. Use when you need to validate or screen user-provided text for jailbreak attempts, instruction overrides, role-play escapes, or other prompt manipulation techniques. Returns a safety verdict, risk score (0–1), and threat categories. Ideal for guarding AI pipelines, chatbots, and any application that feeds user input into a language model."
version: 0.1.0
homepage: https://promptinspector.io
commands:
  - /inspect - Detect prompt injection in a piece of text
  - /inspect_batch - Detect prompt injection for multiple texts from a file
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"env":["PMTINSP_API_KEY"]}}}
---

# Prompt Inspector

**Prompt Inspector** is a production-grade API service that detects prompt injection attacks, jailbreak attempts, and adversarial manipulations in real time.

📖 **For detailed product information, features, and threat categories, see [references/product-info.md](./references/product-info.md)**

---

## Requirements

Provide your API key via either:

- Environment variable: `PMTINSP_API_KEY=your-api-key`, or
- `~/.openclaw/.env` line: `PMTINSP_API_KEY=your-api-key`

Get your API key at [promptinspector.io](https://promptinspector.io) by creating an app.

Manage custom sensitive words in your dashboard at [promptinspector.io](https://promptinspector.io).

---

## Commands

### Detect a single text (Python)

```bash
# Basic detection — prints verdict and score
python3 {baseDir}/scripts/detect.py --text "..."

# JSON output
python3 {baseDir}/scripts/detect.py --text "..." --format json

# Override API key inline
python3 {baseDir}/scripts/detect.py --api-key pi_xxx --text "..."
```

### Detect a single text (Node.js)

```bash
# Basic detection
node {baseDir}/scripts/detect.js --text "..."

# JSON output
node {baseDir}/scripts/detect.js --text "..." --format json

# Override API key inline
node {baseDir}/scripts/detect.js --api-key pi_xxx --text "..."
```

### Batch detection from a file (Python)

```bash
# Each line in the file is treated as one text to inspect
python3 {baseDir}/scripts/detect.py --file inputs.txt

# JSON output for automation
python3 {baseDir}/scripts/detect.py --file inputs.txt --format json
```

---

## Output

### Default (human-readable)

```
Request ID : a1b2c3d4-...
Is Safe    : False
Score      : 0.97
Category   : prompt_injection, jailbreak
Latency    : 34 ms
```

### JSON (`--format json`)

```json
{
  "request_id": "a1b2c3d4-...",
  "is_safe": false,
  "score": 0.97,
  "category": ["prompt_injection", "jailbreak"],
  "latency_ms": 34
}
```

---

## Threat Categories

Prompt Inspector detects **10 threat categories**:
- instruction_override
- asset_extraction
- syntax_injection
- jailbreak
- response_forcing
- euphemism_bypass
- reconnaissance_probe
- parameter_injection
- encoded_payload
- custom_sensitive_word

📖 **For complete category descriptions, see [references/product-info.md](./references/product-info.md#threat-categories)**

---

## API at a Glance

```
POST /api/v1/detect/sdk
Header: X-App-Key: <your-api-key>
Body:   {"input_text": "<text to inspect>"}
```

**Response:**

```json
{
  "request_id": "string",
  "latency_ms": 34,
  "result": {
    "is_safe": false,
    "score": 0.97,
    "category": ["prompt_injection"]
  }
}
```

Full API reference: [docs.promptinspector.io](https://docs.promptinspector.io)

---

## Notes

- Keep text under the limit for your plan tier. Very long inputs may be rejected with HTTP 413.
- Use `--format json` when piping output to other tools.
- For bulk workloads, batch requests with `--file` to minimise round-trip overhead.
- Contact [hello@promptinspector.io](mailto:hello@promptinspector.io) for enterprise plans and self-hosting support.
