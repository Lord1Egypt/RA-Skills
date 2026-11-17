# Quality Gates

## Contents

1. Gate order
2. Severity
3. Freshness
4. Stop rules

## Gate Order

Run gates in this order:

1. Source and version selection
2. Deterministic structural checks
3. Integrated artifact build
4. Freshness/hash check
5. Independent QA judgment
6. Final deterministic regression check

Never ask an agent to find an issue a deterministic test can prove.

## Severity

- **Blocker:** corrupt output, wrong source version, data loss, unsafe action, or deliverable cannot be used.
- **High:** factual error, behavioral regression, broken contract, wrong calculation, visible overflow, or unsupported external claim.
- **Medium:** meaningful clarity, consistency, or maintainability issue that does not block use.
- **Low:** preference or polish.

Only blockers and high findings automatically trigger rebuilds. Batch accepted medium issues into the same rebuild when cheap. Record low issues without extending the run.

## Freshness

Every QA pass binds to:

- `run_id`;
- `build_id`;
- absolute artifact path;
- SHA-256 hash;
- modification timestamp.

If any hash differs when the result returns, mark the review stale. Reuse the same reviewer with a refreshed capsule only when re-review is required.

## Stop Rules

Stop when:

- all required deterministic checks pass;
- no blocker or high finding remains;
- every agent is closed;
- every command session has an exit code;
- the newest user request is satisfied.

Do not start another broad QA wave because of low-severity polish. A second QA wave requires a documented blocker, new source material, or a materially changed build.
