## Description:

Historical debug review: read dated memory first, then narrow raw session evidence only where memory leaves a causal gap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to answer historical debugging questions by starting from dated memory, filling specific evidence gaps from raw session logs, and separating verified causes from likely causes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Historical memory and raw session logs can contain sensitive or unrelated prior-session content.

Mitigation: Install only where the agent is authorized to review the relevant records, limit access to the current user's permitted data, and redact secrets or unrelated content before quoting evidence.

Risk: Broad or noisy raw-log searches can miss relevant evidence or produce misleading matches.

Mitigation: Start from dated memory, narrow lookups by date, session id, or exact phrase, and cite independent supporting artifacts before concluding disputed claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/memory-first-historical-evidence-review)

## Skill Output:

**Output Type(s):** [analysis, guidance, shell commands, markdown]

**Output Format:** [Markdown with cited evidence and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish verified causes from likely causes and cite supporting artifacts for disputed claims.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
