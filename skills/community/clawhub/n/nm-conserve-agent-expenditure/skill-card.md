## Description:

Tracks per-agent token usage and flags waste in parallel dispatch

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after parallel agent runs to review token expenditure, check for duplicated or low-value work, and decide whether to adjust agent counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Waste classifications depend on usage, findings, file-access, and historical-baseline data that may be incomplete.

Mitigation: Check that the required records and comparison baselines are available; identify missing evidence before making a classification or recommendation.

Risk: The security review notes that one external link was out of scope.

Mitigation: Review the linked source and confirm it is trusted before installing the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conserve-agent-expenditure)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post-dispatch checklist, waste-signal assessment, and agent-count recommendation.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
