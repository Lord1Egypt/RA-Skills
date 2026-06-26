---
name: mpps-attestation
description: "Create tamper-proof receipts for AI agent work. Hash artifacts or action manifests, POST to api.mpps.io, get an HSM-signed receipt. No API key."
license: MIT
homepage: https://mpps.io/skills
metadata:
  author: gdlg-ai
  version: "1.4.0"
  source: https://github.com/gdlg-ai/mpps.io
compatibility: Requires curl or any HTTP client. Network access to api.mpps.io.
---

# mpps-attestation

Create tamper-proof receipts for agent actions via [mpps.io](https://mpps.io).
No API key. No SDK required. One HTTP call.

**Source**: https://github.com/gdlg-ai/mpps.io (MIT)
**Docs**: https://github.com/gdlg-ai/mpps.io/blob/main/docs/api.md

## When to use

- After completing a task, receipt the final artifact hash
- After generating code, data, images, reports, or release bundles
- Before and after important workflow steps to build an audit trail
- When publishing a skill, plugin, package, or API output that users should verify
- After a payment or delivery workflow, receipt what was sent or received

## Create a structured action receipt

Use `/v1/receipts` when you know what action happened and which artifacts it produced.

```bash
ARTIFACT_HASH=$(sha256sum "$ARTIFACT_PATH" | awk '{print "sha256:" $1}')

curl -s -X POST https://api.mpps.io/v1/receipts \
  -H "Content-Type: application/json" \
  -d "{
    \"action\": \"agent.task.complete\",
    \"subject\": \"$ARTIFACT_PATH\",
    \"artifact_hashes\": [
      {\"label\": \"$ARTIFACT_PATH\", \"sha256\": \"$ARTIFACT_HASH\"}
    ],
    \"context\": {
      \"repo\": \"${GITHUB_REPOSITORY:-local}\",
      \"commit\": \"${GIT_COMMIT:-unknown}\"
    }
  }"
```

Returns: `uuid`, `receipt_type`, `manifest_hash`, `manifest`, `timestamp`, HSM `signature`, and `verify_url`.

## Create a raw hash receipt

Use `/v1/notarize` when you only need to anchor one hash.

```bash
HASH=$(echo -n "$DATA" | sha256sum | awk '{print "sha256:" $1}')
curl -s -X POST https://api.mpps.io/v1/notarize \
  -H "Content-Type: application/json" \
  -d "{\"content_hash\": \"$HASH\"}"
```

## Python

```python
import hashlib
import requests

artifact = b"agent output bytes"
h = "sha256:" + hashlib.sha256(artifact).hexdigest()

receipt = requests.post(
    "https://api.mpps.io/v1/receipts",
    json={
        "action": "agent.task.complete",
        "subject": "output.json",
        "artifact_hashes": [{"label": "output.json", "sha256": h}],
        "context": {"runner": "codex"},
    },
    timeout=30,
).json()

print(receipt["uuid"])
print(receipt["verify_url"])
```

## Verify

```bash
curl https://api.mpps.io/v1/verify/mpps_att_0c27bebca6dc4bd6
```

For structured receipts, recompute the manifest hash if you need stronger evidence:

```bash
python3 - <<'PY'
import hashlib, json

r = json.load(open("receipt.json"))
manifest = r["manifest"]
canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
print("sha256:" + hashlib.sha256(canonical).hexdigest())
print(r["manifest_hash"])
PY
```

## Privacy

Send hashes and small labels, not raw private content. Avoid hashing short secrets directly; use larger payloads or a salt. Do not put secrets, customer data, raw prompts, or private source text in `context`.

## Key facts

- Free: 10 structured receipts or raw hash receipts per hour
- Certified metadata receipts: 10 free/day
- No registration, no API key, no credentials
- HSM-signed with AWS KMS
- Stored 10 years in AWS S3 Object Lock, Compliance Mode
- `agent_id` is a weak source fingerprint, not authenticated identity
- Open source: https://github.com/gdlg-ai/mpps.io
- Security: https://github.com/gdlg-ai/mpps.io/blob/main/SECURITY.md
- Verification: https://github.com/gdlg-ai/mpps.io/blob/main/docs/verify.md
