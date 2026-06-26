# Prompt Inspector — Usage Guide

## Overview

Prompt Inspector protects your LLM-based applications by detecting adversarial user inputs before they reach your language model. This guide covers common integration patterns and usage scenarios.

---

## Authentication

All API requests require an API key sent in the `X-App-Key` HTTP header.

**Obtain your key:** Sign up at [promptinspector.io](https://promptinspector.io).

The helper scripts resolve the key in this order:

| Priority | Source                              |
| -------- | ----------------------------------- |
| 1        | `--api-key` CLI argument            |
| 2        | `PMTINSP_API_KEY` environment variable |
| 3        | `~/.openclaw/.env` → `PMTINSP_API_KEY=...` |

---

## Quick Start

### Python

```bash
# Set your key once
export PMTINSP_API_KEY=your-api-key

# Inspect a single text
python3 {baseDir}/scripts/detect.py --text "User input content."
```

**Output:**
```
Request ID : a1b2c3d4-e5f6-...
Is Safe    : False
Score      : 0.97
Category   : prompt_injection
Latency    : 28 ms
```

### Node.js

```bash
export PMTINSP_API_KEY=your-api-key

node {baseDir}/scripts/detect.js --text "User input content."
```

---

## Output Formats

### Human-readable (default)

Suitable for interactive use and debugging.

```bash
python3 {baseDir}/scripts/detect.py --text "..." --format human
```

```
Request ID : a1b2c3d4-...
Is Safe    : False
Score      : 0.97
Category   : prompt_injection, jailbreak
Latency    : 34 ms
```

### JSON

Suitable for scripting, piping, and programmatic use.

```bash
python3 {baseDir}/scripts/detect.py --text "..." --format json
```

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

## Batch Detection

Inspect multiple texts from a file — one text per line:

```bash
# Create a test file
cat > inputs.txt <<EOF
Hello, how are you?
What is the capital of France?
EOF

# Run batch detection
python3 {baseDir}/scripts/detect.py --file inputs.txt

# JSON output for downstream processing
python3 {baseDir}/scripts/detect.py --file inputs.txt --format json > results.json
```

Node.js equivalent:

```bash
node {baseDir}/scripts/detect.js --file inputs.txt --format json > results.json
```

---

## Self-Hosted / Custom Endpoint

If you run Prompt Inspector on your own infrastructure:

```bash
python3 {baseDir}/scripts/detect.py \
  --base-url https://your-server.com \
  --text "..."
```

```bash
node {baseDir}/scripts/detect.js \
  --base-url https://your-server.com \
  --text "..."
```

---

## Understanding the Response

| Field        | Type            | Description                                                    |
| ------------ | --------------- | -------------------------------------------------------------- |
| `request_id` | string          | Unique ID for this detection request (useful for logging)      |
| `is_safe`    | boolean         | `true` = input appears safe; `false` = threat detected         |
| `score`      | float or null   | Risk score 0–1. Higher = more likely adversarial. `null` if safe |
| `category`   | array of string | Detected threat categories (empty array if safe)               |
| `latency_ms` | integer         | Server-side processing time in milliseconds                    |

### Threat Categories

| Category               | Description                                              |
| ---------------------- | -------------------------------------------------------- |
| `prompt_injection`     | Classic instruction override / prompt hijacking          |
| `jailbreak`            | Attempts to bypass safety guidelines or restrictions     |
| `instruction_override` | Commands to ignore system prompts or previous context    |
| `role_play_escape`     | Persona-switching attacks (e.g., "pretend you are DAN")  |
| `data_exfiltration`    | Attempts to extract system prompts or sensitive data     |

---

## Integration Patterns

### Pattern 1 — Hard block

Reject any input where `is_safe` is `false`:

```python
result = client.detect(user_input)
if not result.is_safe:
    return "Your input was flagged as potentially unsafe."
# Forward to LLM
```

### Pattern 2 — Score threshold

Tune sensitivity with a custom threshold:

```python
result = client.detect(user_input)
THRESHOLD = 0.8
if result.score is not None and result.score >= THRESHOLD:
    return "High-risk input detected."
```

### Pattern 3 — Category-based routing

Allow some categories while blocking others:

```python
result = client.detect(user_input)
BLOCKED = {"prompt_injection", "jailbreak", "data_exfiltration"}
if set(result.category) & BLOCKED:
    return "This type of input is not allowed."
```

---

## Rate Limits & Plan Tiers

| Plan       | Requests / month | Max text length |
| ---------- | ---------------- | --------------- |
| Free       | 1,000            | 2,000 chars     |
| Starter    | 50,000           | 10,000 chars    |
| Pro        | Unlimited        | 50,000 chars    |
| Enterprise | Custom           | Custom          |

Upgrade or check usage at [promptinspector.io](https://promptinspector.io).

---

## Further Resources

- **API Reference:** [docs.promptinspector.io](https://docs.promptinspector.io)
- **Python SDK:** `pip install prompt-inspector`
- **Node.js SDK:** `npm install prompt-inspector`
- **Open Source:** [github.com/aunicall/prompt-inspector](https://github.com/aunicall/prompt-inspector)
- **Support:** [hello@promptinspector.io](mailto:hello@promptinspector.io)
