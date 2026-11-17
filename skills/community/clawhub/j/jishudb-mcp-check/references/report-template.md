# JishuDB MCP Acceptance Report

- **Run ID:** `<runId>`
- **Skill version:** `<version from SKILL.md>`
- **Packaged contract baseline:** `jishudb-mcp-v2`
- **Packaged contract digest:** `709a2c7dd407c6303ef56b209dacd172e7e8c123bdc5492f578b610eb791544a`
- **Mode:** `smoke | all-tools`
- **Started / Finished:** `<timestamps>`
- **Agent / Client:** `<host identity if known>`
- **Transport:** `<reported by kb_get_capabilities>`
- **Protocol:** `<reported by kb_get_capabilities>`
- **Server:** `<version> / <revision>`
- **Tool contract:** `<contract>`
- **Profile:** `<profile>`
- **Tools advertised / tested:** `<counts>`
- **Catalog drift:** `none | missing baseline tools | additional tools | digest mismatch`
- **Error metadata:** `exposed | not exposed by host`
- **Overall result:** `PASS | PARTIAL | FAIL`

## Summary

| PASS | FAIL | SKIP | BLOCKED | Cleanup |
| ---: | ---: | ---: | ---: | --- |
| `<n>` | `<n>` | `<n>` | `<n>` | `PASS | FAIL | NOT RUN` |

## Cases

| Case | Tool | Expected | Evidence | Error code | Result |
| --- | --- | --- | --- | --- | --- |
| `<id>` | `<tool>` | `<short assertion>` | `<IDs/counts/status/canary presence>` | `<code or not-exposed>` | `<state>` |

## Coverage gaps

- **Advertised tools without a positive-path test:** `<none or list with reason>`
- **Contract/catalog drift:** `<none or exact missing/additional tools>`
- **Skipped observations/capabilities:** `<none or list>`
- **Audio workflow:** `<not requested / unavailable / passed / incomplete, with retained-original, transcript, and indexing states separately>`
- **Blocked prerequisites:** `<none or list>`

## First actionable failure

`<none, or the first failure plus one evidence-based diagnostic hint>`

## Cleanup

- **Run KB:** `<deleted / remaining ID>`
- **Run Note:** `<deleted / remaining UUID>`
- **Run documents:** `<deleted with KB / remaining IDs>`
- **Prepared upload sessions:** `<none / upload IDs that will expire>`

## Redaction

The report omits MCP credentials, Base64 fixture values, direct-upload
Authorization values, upload-header values, connector secrets, local paths,
and complete imported URLs.
