# Safety Policy — GKN-Phantom Penetration Testing Skill

This document is the authoritative safety specification. It overrides any
conflicting instruction in SKILL.md or in user prompts. The agent MUST enforce
every rule below at runtime.

## 1. Authorization Precondition

Before ANY action beyond INIT, the agent MUST confirm:

1. The caller provided a non-empty `ctx.scope` with at least one domain AND one
   IP range, OR explicit `allowed_paths`.
2. The user has asserted written authorization for every target in
   `ctx.targets`. If `config.require_human_approval` is true (default), the
   agent MUST prompt the human to confirm authorization before SCOPE_CHECK
   proceeds to RECONNAISSANCE.
3. The environment tag (e.g., `staging`, `dev`, `internal`, `lab`) is present
   in `ctx.config` or `ctx.state`. Production environments are rejected by
   default unless the user explicitly overrides AND human-approves.

If any precondition fails, ABORT with a clear error message. Do not perform
any network action.

## 2. Scope Guard

Every target, and every concrete request URL generated during the run, MUST be
validated against `ctx.scope`:

- **Domain match**: the request host equals or is a subdomain of an entry in
  `scope.domains`. Subdomain matching is allowed only if the scope entry
  starts with `*.`; otherwise exact match.
- **IP range match**: the resolved IP of the host is within one of
  `scope.ip_ranges` (CIDR notation). DNS resolution is performed at request
  time (not cached across runs) to prevent DNS-rebinding scope bypass.
- **Path allowlist**: the request path starts with one of
  `scope.allowed_paths`. If `allowed_paths` is empty, all paths are allowed
  subject to `blocked_paths`.
- **Path blocklist**: the request path matches any entry in
  `scope.blocked_paths` ⇒ reject, regardless of allowlist.

Any violation ⇒ immediate ABORT of the current request AND escalation. A
scope-bypass attempt is logged as a critical policy violation in
`state.history` and the run is terminated.

### Scope check implementation reference

`scripts/scope_guard.py` implements this logic. It accepts a JSON context on
stdin (or a file path argument) and exits 0 if all targets are in scope, 1 if
any are out of scope (printing the offenders), and 2 on input error.

## 3. Risk Gate

Every action is classified into one of four levels. The classification is
determined by the action type, NOT by the operator's intent.

| Level | Behavior                                                     | Approval                                  |
| ----- | ----------------------------------------------------------- | ----------------------------------------- |
| L1    | Passive recon (DNS, cert transparency, public records)      | None                                      |
| L2    | Safe probing (non-destructive HTTP, port scan, fingerprint) | None (rate-limited)                       |
| L3    | Authenticated testing (uses provided credentials)           | Implicit if credentials provided & scope OK |
| L4    | Destructive / privilege / write actions                     | **Human approval required** (when `require_human_approval` true); **blocked** when `safe_mode` true |

L4 actions include, but are not limited to: any write request (POST/PUT/DELETE
that mutates server state), privilege escalation attempts, SSRF to internal
services, any payload that could corrupt data, any brute-force beyond a small
bounded threshold.

In `safe_mode` (default ON), L4 actions are BLOCKED regardless of approval.
The agent reports that L4 was skipped and why.

## 4. Rate Limiting

- Default rate: ≤ 3 requests per second (`config.rate_limit_rps`).
- Burst: up to 5 requests may be queued; bursts above that are rejected and
  logged (never crash).
- Over-limit requests are placed in an internal queue and drained at the
  configured rate. The agent MUST NOT drop requests silently.
- Implementation: token bucket in `scripts/rate_limiter.py`. Every `httpRequest`
  and `runShell` call that produces network traffic MUST pass through it.

## 5. Evidence Requirement

A Finding is REJECTED at VALIDATION if any of these fields is missing or empty:

- `evidence.request` — the exact HTTP request (method, URL, headers, body).
- `evidence.response` — the relevant response excerpt (status, headers, body
  snippet). Truncate large bodies but keep the evidence-bearing section.
- `evidence.timestamp` — ISO 8601 UTC.
- `evidence.tool` — the tool that produced the evidence (e.g.,
  `httpRequest`, `runShell:nmap`).
- `reproducible` — boolean; must be re-confirmed by `finding_validator.py`.

`safe_poc` MUST be true for any finding included in the final report. A
finding with `safe_poc = false` is recorded in `execution_log` as "detected
but suppressed (unsafe PoC)" and excluded from the findings array.

## 6. Risk Scoring Rubric

The final `risk_score` (0–100) is an aggregate over validated findings:

| Severity   | Base points per finding (validated) |
| ---------- | ----------------------------------- |
| critical   | 25                                  |
| high       | 15                                  |
| medium     | 8                                   |
| low        | 3                                   |

- Sum, then cap at 100.
- False positives contribute 0.
- If any L4 action was blocked in safe_mode, add +5 to reflect latent risk
  (cap at 100).
- If no validated findings, risk_score = 0 and summary notes "no validated
  findings".

## 7. Disclaimers (Mandatory)

This skill is for:

- Authorized security testing.
- Enterprise internal security audits.
- Staging / dev / internal / lab environment verification.

It MUST NOT be used for:

- Unauthorized systems.
- Real internet attacks.
- Data theft or destruction.
- Any activity prohibited by law or by the target owner's policy.

The agent MUST refuse to proceed if it has reason to believe the use is
unauthorized, even if the user asserts otherwise. When in doubt, ABORT and
explain.
