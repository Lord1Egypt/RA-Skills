# Environment Contract

Use this reference when the user supplies a runtime environment or asks to execute the generated automated API suite.

## Minimum runtime fields

Capture or infer these fields before execution:

- `environment_name`: dev/test/sit/uat/prod-like label
- `base_url`: root host for requests
- `runner`: `postman`, `newman`, `pytest`, or user-specified runner
- `auth_type`: bearer/basic/api-key/cookie/custom/signature/none
- `auth_source`: env var, secret file, login API, static token, or manual input
- `default_headers`: shared headers for all calls
- `variables`: environment-scoped values such as tenant id, app id, locale, or seed data
- `timeout_ms`: request timeout
- `report_dir`: where execution artifacts and final reports should be written

## Preferred normalization shape

Represent the execution environment in a single JSON or YAML object similar to:

```json
{
  "environment_name": "sit",
  "runner": "postman",
  "base_url": "https://sit.example.com",
  "auth_type": "bearer",
  "auth_source": {
    "mode": "env",
    "token_env": "API_TOKEN"
  },
  "default_headers": {
    "X-App-Id": "demo"
  },
  "variables": {
    "tenant_id": "t-001"
  },
  "timeout_ms": 10000,
  "report_dir": "./reports"
}
```

## Runner decision guide

- Choose `postman/newman` when JavaScript test scripts, collection exports, or pre-request/post-response event scripts are the natural fit.
- Choose `pytest` when the project or environment already uses Python, virtual environments, or CI jobs driven by `pytest`.
- If the user specifies a runner, treat that as authoritative.

## Execution expectations

Before running:

1. Verify the requested runtime exists locally.
2. Verify secrets are supplied safely.
3. Verify the target environment is intentional.
4. Write the normalized environment file into the generated workspace.
5. Preserve raw execution artifacts for report generation.

## Safety note

If the provided environment looks production-like and the user has not clearly asked for live execution, pause and confirm before sending mutating requests.
