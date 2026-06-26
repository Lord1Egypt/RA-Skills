# Prompt Inspector — Frequently Asked Questions

## General

### What is Prompt Inspector?

Prompt Inspector is a real-time API service that detects prompt injection attacks, jailbreak attempts, and adversarial manipulations in text before it reaches your language model. It acts as a security layer for any LLM-based application.

### What types of attacks does it detect?

**Category**
+ `prompt_injection`
+ `jailbreak`
+ `instruction_override`
+ `role_play_escape`
+ `data_exfiltration`


### Is Prompt Inspector open source?

The core engine is open source at [github.com/aunicall/prompt-inspector](https://github.com/aunicall/prompt-inspector). The hosted API at [promptinspector.io](https://promptinspector.io) provides a fully managed, production-ready deployment.

---

## Authentication & API Keys

### Where do I get an API key?

Sign up at [promptinspector.io](https://promptinspector.io) and generate a key from your dashboard.

### How do I set my API key for the helper scripts?

The scripts check three locations in order:

1. `--api-key pi_xxx` (CLI argument)
2. `export PMTINSP_API_KEY=pi_xxx` (environment variable)
3. `~/.openclaw/.env` file with the line `PMTINSP_API_KEY=pi_xxx`

The environment variable approach is recommended for day-to-day use:

```bash
export PMTINSP_API_KEY=your-api-key
```

### I'm getting `Authentication failed`. What should I check?

- Ensure you copied the full key without leading/trailing spaces.
- Verify the key is active in your dashboard at [promptinspector.io](https://promptinspector.io).
- If you rotated your key, make sure the old key is not still being used.

---

## API Usage

### What is the API endpoint?

```
POST https://promptinspector.io/api/v1/detect/sdk
```

### What does a minimal API request look like?

```bash
curl -X POST https://promptinspector.io/api/v1/detect/sdk \
  -H "X-App-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"input_text": "..."}'
```

### What does the response look like?

```json
{
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "latency_ms": 28,
  "result": {
    "is_safe": false,
    "score": 0.97,
    "category": ["prompt_injection"]
  }
}
```

### What does `score: null` mean?

When `is_safe` is `true` and no threat is detected, the score is returned as `null` (not applicable). Your code should handle this case — treat `null` the same as a score of `0`.

### What is the maximum text length?

This depends on your plan tier:

| Plan       | Max text length |
| ---------- | --------------- |
| Free       | 2,000 chars     |
| Starter    | 10,000 chars    |
| Pro        | 50,000 chars    |
| Enterprise | Custom          |

Exceeding the limit returns HTTP 413. Upgrade your plan at [promptinspector.io](https://promptinspector.io).

---

## Helper Scripts

### Do the scripts require installing any packages?

No. Both `detect.py` (Python 3.8+) and `detect.js` (Node.js 14+) use only standard library modules. No `pip install` or `npm install` needed.

### How do I inspect multiple texts at once?

Use the `--file` option. Put each text on its own line in a plain text file:

```bash
python3 detect.py --file my_inputs.txt --format json > results.json
```

```bash
node detect.js --file my_inputs.txt --format json > results.json
```

### How do I use a self-hosted Prompt Inspector instance?

Pass the `--base-url` option:

```bash
python3 detect.py --base-url https://your-server.com --text "..."
node detect.js  --base-url https://your-server.com --text "..."
```

### The script prints to stderr while running in batch mode — is that intentional?

Yes. Progress messages (e.g., `[1/10] Inspecting: ...`) are written to **stderr** so they don't pollute the **stdout** JSON output when piping with `--format json`.

---

## Errors & Troubleshooting

### HTTP 401 / 403 — Authentication failed

Your API key is missing, incorrect, or expired. See [Authentication & API Keys](#authentication--api-keys) above.

### HTTP 413 — Input too long

Your text exceeds the maximum length for your plan. Truncate the input or upgrade your plan.

### HTTP 422 — Invalid request

The request body is malformed. Ensure `input_text` is a non-empty string.

### HTTP 429 — Rate limit exceeded

You have exceeded the request rate for your plan. Slow down your requests or upgrade to a higher-tier plan.

### Connection timeout

- Check your network connection and firewall settings.
- Verify the `--base-url` is correct.
- Try increasing the timeout: `--timeout 60`.

---

## Plans & Pricing

### Is there a free tier?

Yes. The Free plan includes 1,000 requests per month with up to 2,000 characters per text.

### How do I upgrade?

Visit [promptinspector.io](https://promptinspector.io) and go to your billing dashboard.

### Do you offer enterprise or self-hosted plans?

Yes. Contact [hello@promptinspector.io](mailto:hello@promptinspector.io) for enterprise pricing and self-hosting options.

---

## Further Help

- **Docs:** [docs.promptinspector.io](https://docs.promptinspector.io)
- **Email:** [hello@promptinspector.io](mailto:hello@promptinspector.io)
- **GitHub:** [github.com/aunicall/prompt-inspector](https://github.com/aunicall/prompt-inspector)
