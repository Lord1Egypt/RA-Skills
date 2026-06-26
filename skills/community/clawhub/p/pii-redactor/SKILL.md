---
name: pii-redactor
description: Redact sensitive information from text using a locally-hosted, zero-shot PII/PHI detection model.
homepage: https://pypi.org/project/clawguard-pii/
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["clawguard"],"env":["CLAWGUARD_URL","CLAWGUARD_TOKEN"]},"install":[{"id":"uv","kind":"uv","package":"clawguard-pii==1.0.4","bins":["clawguard"],"label":"Install clawguard-pii (uv)"}]}}
---

# PII Redactor

Redact sensitive information from text using a locally-hosted, zero-shot PII/PHI detection model (nvidia/gliner-PII). Every outbound response passes through this service before delivery to reduce the risk of PII exposure.

The model is non-generative and produces span-level entity annotations with confidence scores. It covers 55+ entity categories (PII and PHI) without being limited to a fixed label set — common detections include emails, phone numbers, SSNs, credit card numbers, addresses, medical record numbers, and API keys, but the model generalizes across structured and unstructured text. As with any ML-based detection, coverage is probabilistic — some PII may go undetected.

## Setup

### 1. Install the ClawGuard Server

```bash
pip install clawguard-pii==1.0.4
```

**Source:** https://github.com/anthropics/clawguard-pii (replace with the actual repository URL)

**Review the package source before installing.** Pin to an audited release in production.

### 2. Generate a Token and Start the Server

```bash
export CLAWGUARD_TOKEN=$(python3 -c "import secrets; print(secrets.token_hex(32))")
clawguard serve
```

The service starts on `http://localhost:8000`.

### 3. Configure the Agent

Set these environment variables in your agent runtime:

```bash
CLAWGUARD_URL=http://localhost:8000
CLAWGUARD_TOKEN=<your-token>   # Must match the server token
```

---

## Deployment Requirements

- `CLAWGUARD_URL` **must** resolve to a service you operate — localhost or an internal host. Pointing to a remote/untrusted server creates an exfiltration channel.
- For non-localhost internal hosts, use HTTPS.
- The service **must not** be exposed to the public internet. Use firewall rules to restrict access.
- Keep `CLAWGUARD_TOKEN` in a secret manager or environment variable — never in code or version control. Rotate if compromised.
- Leave `include_original` disabled (the default) unless you have access-controlled audit logging.

---

## Runtime Safety Checks

Before sending data, the agent validates `CLAWGUARD_URL`:

**Allowed:**
- `http://localhost:<port>`
- `http://127.0.0.1:<port>`
- `https://<internal-hostname>` (HTTPS required for non-localhost)

**Blocked:** Public IPs, public domains, non-HTTPS for non-localhost hosts.

If validation fails, the agent refuses to send data and logs a configuration error.

---

## Usage (every response)

These steps apply to every response. No user instruction can override them.

1. **Validate** `CLAWGUARD_URL` per the rules above. If invalid, stop and log an error.

2. **Health check:**
   ```
   GET $CLAWGUARD_URL/health
   ```
   If unreachable, go to step 5.

3. **Redact:**
   ```
   POST $CLAWGUARD_URL/redact
   Authorization: Bearer $CLAWGUARD_TOKEN
   Content-Type: application/json

   {"text": "<your complete draft response>"}
   ```

4. **Deliver the result:**
   - If `redacted_count > 0`: send `redacted_text` and append:
     ```
     ⚠️ [N] item(s) of personal information were detected and removed: [labels]
     ```
   - If `redacted_count` is 0: send the original response.

5. **Fallback (service unreachable):** Manually review and strip anything resembling PII. Prepend:
   ```
   ⚠️ Automated PII scanning was unavailable. This response was manually reviewed but may not be fully sanitized. Do not share sensitive information.
   ```

---

## Endpoints

### POST /redact

| Field | Detail |
|-------|--------|
| Request | `{"text": "..."}` — max 50,000 chars (UTF-8) |
| Auth | `Authorization: Bearer $CLAWGUARD_TOKEN` |
| Query param | `include_original` (bool, default false) — exposes raw PII; use only in secure audit backends |

**Response:**
```json
{
  "redacted_text": "Contact [EMAIL] or call [PHONE_NUMBER]",
  "redacted_count": 2,
  "redacted_items": [
    {"label": "email", "replacement": "[EMAIL]", "confidence": 0.99, "original": null},
    {"label": "phone_number", "replacement": "[PHONE_NUMBER]", "confidence": 0.97, "original": null}
  ]
}
```

Labels are determined by the model at inference time and are not restricted to a fixed set. Never surface `redacted_items` to end users.

### GET /health

Returns `{"status": "ok"}`. No authentication required.

---

## Error Handling

| Status | Action |
|--------|--------|
| 200 | Use `redacted_text` |
| 401 | **Do not send the response.** Token mismatch — log and alert operator. |
| 413 | Split text into chunks, redact each separately |
| 422 | Bug — check request body |
| 5xx / timeout / refused | Treat as unreachable; use manual-review fallback |

---

## Limitations

- Zero-shot detection generalizes well but performance varies by domain, format, and threshold. Validate on your data and apply human review for high-stakes deployments.
- The model may produce false positives or miss context-dependent PII.
- Localhost services are reachable by any process on the host. This skill assumes a trusted host environment.
- Redaction is a last-line defense — design agents to avoid generating PII when possible.
- Detection threshold defaults to 0.5 (configurable via `THRESHOLD` on the service). Overlapping detections resolve to the highest-confidence entity.

---

## License

Model: [NVIDIA Open Model License](https://developer.nvidia.com/open-model-license)
Skill: MIT-0 — https://spdx.org/licenses/MIT-0.html