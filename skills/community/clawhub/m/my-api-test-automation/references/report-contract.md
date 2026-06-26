# Report Contract

Use this reference when building the final output after generating or executing API automated tests.

## Required report sections

1. Executive summary
2. Source artifacts
3. Runtime environment
4. Generated suite summary
5. Execution results
6. Failure diagnostics
7. Coverage and gaps
8. Assumptions and blockers
9. Recommended next actions

## Expected result file shape

`scripts/build_test_report.py` accepts one or more JSON files from `results-dir`. Each file may contain a top-level object with these optional fields:

```json
{
  "summary": {
    "total": 10,
    "passed": 8,
    "failed": 2,
    "skipped": 0,
    "duration_seconds": 12.4
  },
  "environment": {
    "name": "sit",
    "base_url": "https://sit.example.com",
    "runner": "postman"
  },
  "results": [
    {
      "case_id": "login-happy-path",
      "name": "Login returns token",
      "endpoint": "POST /auth/login",
      "status": "passed",
      "status_code": 200,
      "duration_ms": 320,
      "message": "ok"
    }
  ],
  "artifacts": [
    "newman-result.json"
  ]
}
```

## Normalization rules

- Merge all `results` arrays.
- Prefer explicit summary counts from the files; otherwise compute counts from normalized results.
- Treat unknown statuses as `failed` unless there is a strong reason not to.
- Preserve `message`, `details`, and `artifact` fields for debugging.

## Coverage expectations

If `case-manifest.json` exists, compare executed `case_id` values with manifest entries and call out:

- unexecuted cases
- undocumented cases generated ad hoc
- endpoints without negative tests or dependency tests when that absence is obvious
