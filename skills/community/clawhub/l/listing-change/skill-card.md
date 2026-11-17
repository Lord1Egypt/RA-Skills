## Description:

Uses saved Amazon product snapshots and deterministic diffs to summarize changes to listing fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and operators use this skill to review saved product listing snapshots, summarize field changes, and manage monitoring schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This version can consume analysis credits without per-request confirmation and change future spending settings beyond its advertised listing-alert scope.

Mitigation: Prefer a corrected package that enforces watch-only commands. Confirm recurring monitoring costs before enabling watches, and use pause or delete to stop them.

## Reference(s):

- [Watch workflow](references/watch-workflow.md)
- [Monitoring reference](references/reference.md)
- [ARI operations workspace](https://ari.funewa.com/zh/operations)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Listing-change watch summaries with structured digest data and watch-management commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot-based deterministic diffs; not real-time monitoring.]

## Skill Version(s):

1.5.3 (source: server release evidence, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
