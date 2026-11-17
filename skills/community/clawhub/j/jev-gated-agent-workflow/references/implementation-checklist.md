# Implementation checklist

Use this checklist when adding the gate to an agent host.

## Local router

- Keep the router in a separate local module so the host hook is small and auditable.
- Send the natural-language request and branch descriptions to TypeSafe JEV.
- Read the credential from the runtime environment or secret store; never hard-code it.
- Return a small JSON contract: `group_key`, `group_id`, `confidence`, `needs_confirmation`, `query`, and `decision_source`.
- Treat non-zero exit status, invalid JSON, timeout, and unavailable credentials as denial.

## Host hook

- Bind inbound natural language to the current session using host metadata.
- Intercept only the protected tools; leave unrelated tools unchanged.
- Resolve the final target from the local allowlist, not from the model or user.
- Reject a user/model target that differs from the routed target.
- Keep the permit short-lived and single-purpose.
- Log only branch names, confidence, tool names, and denial reasons; redact requests and all identifiers in public diagnostics.

## Token-efficiency checks

- Run the gate before history search, document retrieval, browser navigation, or large context assembly.
- Use the router's normalized query to constrain retrieval.
- Prefer one narrow read over broad search followed by filtering in the model.
- Summarize evidence once and avoid re-injecting the same raw history into later turns.
- Measure before/after retrieval volume and latency; do not claim token savings without a baseline.

## Verification matrix

Test with a fake tool adapter and a non-production allowlist:

| Case | Expected result |
| --- | --- |
| Clear request for an allowlisted branch | Permit and target injection |
| Missing natural-language request | Deny before the tool |
| JEV timeout or missing key | Deny before the tool |
| Low confidence or confirmation required | Deny or ask a user clarification, according to host policy |
| Out-of-allowlist choice or target mismatch | Deny |
| Expired or reused permit | Deny |

Before release, run the local skill validator and a secret scanner. Do not publish local policy files, real IDs, logs, or environment dumps.
