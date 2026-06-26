---
name: log-pii-redactor
description: Detect and redact personally identifiable information (PII) in application logs to comply with GDPR, CCPA, HIPAA, and PCI DSS. Knows the realistic 2026 PII surface — emails, phone numbers, SSNs, credit cards, IPv4/IPv6, JWT tokens, API keys, cloud secret patterns, addresses, names leaked via headers and stack traces. Picks the right strategy per field (irreversible mask vs deterministic tokenize vs salted hash vs drop) and ships a regex pack, a pre-prod scanner, and integration recipes for Fluent Bit, Logstash, Vector, and the OpenTelemetry Collector. Maps every redaction to the relevant compliance clause (GDPR Art 5/32, HIPAA Safe Harbor §164.514(b)(2), PCI DSS 3.4/3.5). Use when asked to scrub logs, build a redaction pipeline, audit a log stream for PII, design a tokenization scheme, prep for a SOC 2 or HIPAA audit, or stop sensitive data flowing into Datadog/Splunk/ELK/S3.
metadata:
  tags: ["pii", "logging", "redaction", "gdpr", "ccpa", "hipaa", "pci-dss", "compliance", "observability", "data-privacy"]
---

# Log PII Redactor

Find the PII bleeding into your logs, decide what to do with each kind, and put a deterministic redaction step in front of every sink that stores or indexes log data. The goal is not "no PII anywhere"; it is *no unredacted PII reaching a destination that retains it*. That distinction governs every design choice below.

## Usage

**Basic invocation:**
> Audit my JSON app logs for PII
> Build a Fluent Bit redaction filter
> Should I mask, tokenize, or hash user IDs?
> Write a pre-prod scanner that fails CI if PII is found
> Map our redaction rules to HIPAA Safe Harbor

**With context:**
> Rails app, JSON logs to Datadog, EU users, GDPR scope
> Fintech, PCI DSS Level 1, card data leaks suspected in payment service logs
> Healthcare SaaS, HIPAA, log pipeline is Vector → S3 → Athena
> Microservices, OTel Collector in front of Loki, names leaking via X-Forwarded-For and OAuth profile headers

The skill returns a regex pack, a per-field strategy table, integration config for the user's pipeline, a scanner script, and a compliance mapping table.

## The Three Real Questions

Most PII redaction projects fail because they conflate three different problems:

1. **Detection** — what counts as PII *in your data*? (Emails are easy; "names in stack traces" is not.)
2. **Strategy** — for each field, what action preserves the log's debugging value while removing the privacy harm?
3. **Placement** — at which point in the pipeline do you redact? (Source, agent, collector, or sink — only one of these is correct, and it depends on threat model.)

Solve them in that order. Skipping detection produces strategies for problems you don't have. Skipping strategy produces config that breaks debugging. Skipping placement produces redacted Splunk and unredacted S3 cold storage with five-year retention — the worst outcome.

## Step 1: Detection — The PII Surface

PII is broader than the obvious fields. The realistic surface in a 2026 web app:

### Direct identifiers (always PII)

| Type | Pattern shape | Notes |
|---|---|---|
| Email | RFC 5322-ish | The most common leak; appears in user objects, audit logs, error messages, OAuth callbacks |
| Phone | E.164 + national formats | `+12025551234`, `(202) 555-1234`, `+44 20 7946 0958` |
| SSN (US) | `\d{3}-\d{2}-\d{4}` | Plus the unhyphenated variant; never log raw |
| National IDs | Country-specific | UK NINO, Canadian SIN, German Steuer-ID, Indian Aadhaar — each has its own format |
| Credit card | 13–19 digits, Luhn-valid | PCI DSS scope; redaction is mandatory, not optional |
| IBAN | 2 letters + 2 digits + up to 30 alphanumeric | EU bank accounts |
| Passport / Driver's license | Country-specific | Often appears in KYC flows |
| Date of birth | Many formats | PII alone in HIPAA, quasi-identifier in GDPR |

### Network identifiers (PII under GDPR)

| Type | Pattern | GDPR status |
|---|---|---|
| IPv4 | `\b(?:\d{1,3}\.){3}\d{1,3}\b` | PII — Recital 30, confirmed *Breyer v. Germany* |
| IPv6 | RFC 4291 | PII; same rationale |
| MAC address | `([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}` | PII; device-level identifier |
| User-Agent | Free text | Quasi-identifier; combined with IP, fingerprintable |
| Session/cookie IDs | Opaque tokens | PII when stable across requests |

### Secrets (not PII per se, but leak-equivalents)

| Type | Pattern hint |
|---|---|
| JWT | `eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` |
| AWS access key | `AKIA[0-9A-Z]{16}` |
| AWS secret | 40-char base64 in `aws_secret_access_key` context |
| GitHub PAT | `ghp_[0-9A-Za-z]{36}` |
| Slack token | `xox[baprs]-[0-9A-Za-z-]+` |
| Stripe key | `sk_live_[0-9A-Za-z]{24,}` |
| Generic bearer | `Bearer [A-Za-z0-9._-]+` in Authorization header |
| Private key | `-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----` |

### Indirect identifiers (the hard ones)

These are why naive regex packs fail:

- **Names** in `X-Forwarded-For`, `User-Agent` extensions, OAuth profile dumps, CRM webhook bodies, exception messages (`User Petro Pankov not found`)
- **Addresses** in delivery webhooks, geocoder responses, error contexts
- **Free-text fields** that customers stuff with PII (support ticket bodies, search queries)
- **URLs** with PII in query strings (`?email=alice@example.com&token=...`)
- **Stack traces** that include serialized object dumps with user data
- **GraphQL/SQL parameters** logged on slow-query traces

Indirect identifiers can rarely be regex-matched cleanly. Strategy: redact at the *structured field* level by name (key allowlist/denylist), not by content scanning.

## Step 2: Strategy — Mask, Tokenize, Hash, or Drop

Every PII field gets one of four treatments. The choice depends on whether you need to *correlate* logs after redaction.

### Mask (irreversible, character-level)

- `alice@example.com` → `a****@e******.com` or `***REDACTED***`
- Use when: humans read the log, no need to correlate across entries
- Pros: simple; safe
- Cons: cannot pivot ("show all errors for this user")

### Tokenize (deterministic, reversible with vault)

- `alice@example.com` → `tok_a8f3c2...` (token in log; mapping in a separate vault)
- Use when: you need to correlate across logs but never reverse without authorization
- Pros: full debugging capability via vault lookup
- Cons: requires vault infrastructure (usually a small Postgres + KMS-encrypted lookup service)

### Hash (deterministic, irreversible, salted)

- `alice@example.com` → `HMAC-SHA256(salt, value)` truncated to 16 chars
- Use when: correlation needed, reversal forbidden (HIPAA Safe Harbor compliant)
- Pros: no vault; deterministic across services if salt is shared
- Cons: rainbow-table attack on small spaces (e.g., phone numbers) — rotate salt quarterly; truncate output to discourage offline attack
- Critical: salt must be in KMS, never in the redaction config file

### Drop (the field never enters the log)

- The field is removed entirely or replaced with a fixed sentinel (`"<dropped>"`)
- Use when: the field has no debugging value (raw card numbers, passwords, private keys)
- Always-drop list (no exceptions): passwords, raw card PANs, CVVs, private keys, full session cookies, OAuth refresh tokens

### Decision matrix

| Field | Default strategy | Why |
|---|---|---|
| Password | Drop | Zero debug value; PCI/SOX/PII in one |
| Credit card PAN | Drop or mask last 4 (`****-****-****-1234`) | PCI DSS 3.4 |
| CVV | Drop | PCI DSS 3.2 — must never be stored |
| Email | Hash (HMAC) | Correlation valuable; reversal not needed |
| Phone | Hash | Same |
| SSN/National ID | Drop | No debug value justifies retention |
| User ID (internal) | Pass through | Already a pseudonym if generated server-side |
| IP address | Truncate (`/24` v4, `/64` v6) or hash | GDPR-acceptable; preserves geo signal |
| JWT | Drop body, keep header for debugging | Body has user claims |
| API key | Drop | No debug case justifies retention |
| Names in free text | Tokenize via NER pre-pass | Or drop the whole field if low-value |
| URL query params | Allowlist params; drop unknowns | `?token=` always drops |
| User-Agent | Pass through | Quasi-identifier; usually acceptable |
| Stack trace | Scan + scrub | Apply field-level redaction inside |

## Step 3: The Regex Pack

A practical pack for log-stream filters. Keep these in one config and reuse across all your tools (Vector, Fluent Bit, OTel all accept these).

```yaml
# pii-patterns.yaml — share across all log agents
patterns:
  email: '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
  phone_e164: '\+[1-9]\d{1,14}\b'
  phone_us: '\b\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
  ssn_us: '\b\d{3}-\d{2}-\d{4}\b'
  ssn_us_unhyphenated: '\b(?!000|666|9\d{2})\d{9}\b'  # context-checked
  credit_card: '\b(?:\d[ -]*?){13,19}\b'  # validate Luhn after match
  ipv4: '\b(?:\d{1,3}\.){3}\d{1,3}\b'
  ipv6: '\b(?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b'
  jwt: '\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b'
  aws_access_key: '\bAKIA[0-9A-Z]{16}\b'
  github_pat: '\bghp_[0-9A-Za-z]{36}\b'
  stripe_live_key: '\bsk_live_[0-9A-Za-z]{24,}\b'
  slack_token: '\bxox[baprs]-[0-9A-Za-z-]{10,}\b'
  bearer_token: '(?i)\bBearer\s+[A-Za-z0-9._-]+'
  private_key_block: '-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----'
  iban: '\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b'
```

Critical caveats:

- **Credit card regex must be Luhn-validated post-match** or you'll redact every order ID
- **SSN unhyphenated requires context** (preceding `ssn`/`social`) or it false-positives on every 9-digit number
- **IPv4 regex matches version strings** (`192.168.0.1` and `4.5.6.7` and `5.0.0.1`); allowlist private ranges if you want
- **Email regex over-matches** on things like `path/to/file@domain` — acceptable cost

## Step 4: The Pre-Production Scanner

Run this in CI against a sample of staging logs *before* production rollout. It's the cheapest way to catch what your redaction rules miss.

```python
#!/usr/bin/env python3
# pii_scan.py — fail CI if PII patterns appear in a log file
import re, sys, json, hashlib, yaml
from pathlib import Path

PATTERNS = yaml.safe_load(Path("pii-patterns.yaml").read_text())["patterns"]
COMPILED = {name: re.compile(p) for name, p in PATTERNS.items()}

def luhn_ok(num):
    digits = [int(c) for c in num if c.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def scan_line(line, lineno):
    findings = []
    for name, rx in COMPILED.items():
        for m in rx.finditer(line):
            val = m.group(0)
            if name == "credit_card" and not luhn_ok(val):
                continue
            # Truncate finding for the report; never log full match
            sample = hashlib.sha256(val.encode()).hexdigest()[:8]
            findings.append((lineno, name, sample))
    return findings

def main(path, threshold=0):
    findings = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            findings.extend(scan_line(line, i))
    by_type = {}
    for _, name, _ in findings:
        by_type[name] = by_type.get(name, 0) + 1
    print(json.dumps({"total": len(findings), "by_type": by_type}, indent=2))
    sys.exit(1 if len(findings) > threshold else 0)

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0)
```

Run as a CI gate against any sample of pre-prod logs. Hashed samples in the report let engineers triage without re-leaking.

## Step 5: Pipeline Integration Recipes

### Fluent Bit

```ini
[FILTER]
    Name         modify
    Match        app.*
    Remove       password
    Remove       authorization
    Remove       cvv

[FILTER]
    Name         lua
    Match        app.*
    script       /fluent-bit/scripts/redact.lua
    call         redact

# redact.lua — apply regex pack to every string value
function redact(tag, ts, record)
    for k, v in pairs(record) do
        if type(v) == "string" then
            v = string.gsub(v, "[%w._%%+-]+@[%w.-]+%.%a%a+", "<EMAIL>")
            v = string.gsub(v, "%+%d[%d ]+", "<PHONE>")
            v = string.gsub(v, "Bearer [%w._-]+", "Bearer <REDACTED>")
            record[k] = v
        end
    end
    return 1, ts, record
end
```

### Vector (the cleanest option for new pipelines)

```toml
[transforms.redact_pii]
type = "remap"
inputs = ["app_logs"]
source = '''
. = redact(., redactor: "full", filters: ["pattern", "us_social_security_number"])
.email = if exists(.email) { hmac(.email, key: get_env_var!("PII_HMAC_KEY"), algorithm: "SHA-256") } else { null }
.phone = if exists(.phone) { hmac(.phone, key: get_env_var!("PII_HMAC_KEY"), algorithm: "SHA-256") } else { null }
del(.password)
del(.cvv)
del(.authorization)
.client_ip = if exists(.client_ip) { ip_subnet!(.client_ip, "/24") } else { null }
'''
```

Vector's built-in `redact` function already covers many patterns; the example above adds field-level HMAC for correlation.

### Logstash

```ruby
filter {
  mutate {
    remove_field => [ "password", "cvv", "[headers][authorization]" ]
  }
  ruby {
    code => '
      h = event.to_hash
      h.each do |k, v|
        next unless v.is_a?(String)
        v = v.gsub(/[\w.+-]+@[\w.-]+\.\w+/, "<EMAIL>")
        v = v.gsub(/Bearer\s+[\w.-]+/, "Bearer <REDACTED>")
        v = v.gsub(/eyJ[\w-]+\.[\w-]+\.[\w-]+/, "<JWT>")
        event.set(k, v)
      end
    '
  }
}
```

### OpenTelemetry Collector

```yaml
processors:
  redaction:
    allow_all_keys: true
    blocked_values:
      - '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
      - 'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'
      - '\b(?:\d[ -]*?){13,19}\b'
    summary: debug

  attributes:
    actions:
      - key: http.request.header.authorization
        action: delete
      - key: http.request.body.password
        action: delete
      - key: enduser.id
        action: hash
```

The OTel `redaction` processor handles regex-style scrubbing; `attributes` handles field-level deletion and hashing.

## Step 6: Placement Decision

| Where you redact | Pros | Cons | Use when |
|---|---|---|---|
| In application code | Most precise | Every team must implement; drift over time | Highly regulated (HIPAA), small surface |
| Sidecar agent (Fluent Bit on pod) | Centralized config; near source | Pod resource cost | Kubernetes; multi-language services |
| Collector (Vector / OTel) | Single chokepoint; easy to audit | All raw PII still on the wire to collector | Most teams; default choice |
| Sink-side (Datadog redaction rules) | Easy; vendor-managed | Raw PII already left your network; data leaves your control | Never as the only layer |

**Default architecture:** redact in the collector (Vector or OTel) on the same VPC as the apps; treat sink-side rules as a defense-in-depth backup, never the primary control.

## Compliance Mapping

| Regulation | Clause | What it requires | How redaction satisfies |
|---|---|---|---|
| GDPR | Art 5(1)(c) data minimization | Only personal data necessary may be processed | Drop unused PII fields; hash IDs |
| GDPR | Art 5(1)(f) integrity & confidentiality | Personal data secured against unauthorized access | Mask/hash before logs reach indexed sinks |
| GDPR | Art 32 security of processing | Pseudonymization listed as exemplar safeguard | HMAC-with-KMS-salt = pseudonymization |
| CCPA | §1798.140(o) | "Personal information" includes IP, device IDs | Truncate or hash IPs |
| HIPAA | §164.514(b)(2) Safe Harbor | 18 identifiers must be removed | Drop names, SSNs, MRNs, full DOB, full ZIP, dates more granular than year, IPs, biometrics |
| HIPAA | §164.312(a)(1) access control | Logs containing PHI must enforce same controls as the source | If logs aren't redacted, log store inherits PHI scope; redaction shrinks scope |
| PCI DSS | 3.4 | PAN must be unreadable wherever stored | Mask to last-4 or drop |
| PCI DSS | 3.5 | Cryptographic key management | HMAC salt in KMS, rotated |
| PCI DSS | 10.5 | Audit trails secured | Redaction must not impair the audit trail's integrity (keep transaction IDs) |
| SOC 2 | CC6.7 | Restrict transmission of PII | Redact before egress to third-party SaaS observability |

## Common Pitfalls

- **Redacting after sink ingestion** — the data is already on someone else's disk, possibly in cold-tier backup. Redact *before* the sink.
- **Hashing without a salt** — rainbow-table attack on small spaces (phones, ZIPs) reverses your hashes in minutes.
- **Salt in the config file** — anyone with config access can reverse the hash. Salt belongs in KMS / Vault.
- **Forgetting backups** — log archives in S3/Glacier are long-retention. Redaction must run *before* archive write.
- **Redacting the request ID** — kills your ability to correlate. Request IDs should be server-generated UUIDs and pass through.
- **Trusting the application to never log PII** — it will. The redaction layer is your second line; treat the application's hygiene as best-effort, not a control.
- **Skipping URLs and stack traces** — the highest-leak surfaces. Always scan query strings and exception messages.
- **Indexing before redacting** — Elasticsearch keeps tokenized PII even after the source doc is overwritten. Redact upstream of the indexer.

## Output Format

The skill returns:

1. **PII surface report** — every field/pattern that needs redaction in the user's data
2. **Strategy table** — per-field decision (mask/tokenize/hash/drop) with rationale
3. **Regex pack** — yaml file ready for Vector, Fluent Bit, OTel, Logstash
4. **Pipeline config** — full integration recipe for the user's specific stack
5. **Pre-prod scanner** — Python script wired into CI to fail builds on PII leaks
6. **Compliance mapping** — which clause each redaction satisfies
7. **Placement diagram** — where in the architecture redaction runs
8. **Rollout plan** — staging validation, sampled prod canary, full enable, audit log retention
