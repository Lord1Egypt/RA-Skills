# Attack Registry — what to record when an agent is attacked

Keelwright logs every detected attack to a JSONL file so the operator builds a real picture
of who is targeting them, how, and whether the defense held. This is not optional telemetry
pollution — it is the evidence trail that turns "I think I'm safe" into "here is the log".

## Location

Default: `~/.keelwright/keelwright/attack_registry.jsonl` (one line per event, append-only).
Override with `--path` or `KEELWRIGHT_ATTACK_REGISTRY_PATH`.
Override with `--path`. The file is local scratch memory — add to `.gitignore` if inside a repo.

## Retention & Redaction

- **Retention:** entries older than 30 days are automatically purged on cleanup
  (`python scripts/attack_registry.py --cleanup`). The registry does not grow indefinitely.
- **Redaction:** query parameters and fragments are stripped from `source_url` before logging
  (no tokens, secrets, or PII in logs).
- **Opt-in:** logging only happens if `KEELWRIGHT_ATTACK_REGISTRY=1` is set in the environment
  or explicit `--force-add` is used.

## Schema (one JSON object per line)

| field | type | meaning |
|---|---|---|
| `timestamp` | string (ISO-8601) | when detected |
| `channel` | string | web_search / web_extract / browser / fetch_url / vision_analyze / memory_write / unknown |
| `source_url` | string | the URL or domain the content came from (empty if N/A). Query params stripped. |
| `attack_type` | string | OWASP ASI class: ASI01 goal-hijack, ASI02 tool-misuse, ASI06 memory-poisoning, ASI08 cascading, ASI09 trust-exploit, ASI10 rogue-agent; or `indirect-prompt-injection`, `cloaking`, `data-exfil` |
| `severity` | string | CRITICAL / HIGH / MEDIUM / LOW |
| `detected_by` | string | injection-guard / agent-defense / keelwright-heuristic / manual |
| `action_taken` | string | blocked / sanitized / flagged / allowed-in-contamination-window |
| `outcome` | string | blocked-success / leaked / escalated-to-human |
| `model_provider` | string | provider/model that produced or consumed the content (for reproducibility) |
| `notes` | string | what exactly happened, what the skill blocked |

## Helper

`scripts/attack_registry.py` appends and reads:

```bash
# record
python scripts/attack_registry.py --add \
  --channel web_extract --source-url "https://evil.example/scan" \
  --attack-type indirect-prompt-injection --severity HIGH \
  --detected-by injection-guard --action-taken blocked --outcome blocked-success \
  --model-provider "nous/tencent-hy3" --notes "Page told model to exfiltrate .env"

# read last 20
python scripts/attack_registry.py --tail 20

# count by type
python scripts/attack_registry.py --stats

# cleanup entries older than 30 days
python scripts/attack_registry.py --cleanup
```

## What else belongs in the registry (operator guidance)

Beyond the schema above, keep a weekly human-readable rollup (`attack_registry.md` summary):
- **Top attacker domains** — repeat offenders to block at the network layer.
- **Peak windows** — times of day attacks cluster (bot campaigns run on schedules).
- **Bypass attempts** — cases where injection-guard passed but agent-defense caught (defense-in-depth proof).
- **False positives** — legit content flagged, so the threshold can be tuned without weakening safety.
- **Model correlation** — which models get targeted more (weak models are poisoned more often).

The registry is evidence. If an attack leaks (outcome=leaked), escalate immediately and treat
it as an incident, not a log line.