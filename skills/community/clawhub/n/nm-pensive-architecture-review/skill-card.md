## Description:

Assesses architecture decisions, ADR compliance, and coupling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to review design changes, refactors, and new services for ADR compliance, coupling, and design principle issues before merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review examples may not fit the architecture task, and an existing `.review/findings.json` may affect a run.

Mitigation: Check the examples against the review scope and inspect the existing findings file before using the workflow.

Risk: Some referenced paths may be missing, leaving the review evidence incomplete.

Mitigation: Confirm referenced paths are available and treat findings as unverified when their supporting evidence cannot be checked.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-pensive-architecture-review)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)
- [FPF Framework](https://github.com/ailev/FPF)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, JSON]

**Output Format:** [Markdown review report and JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should include verified file locations and quoted anchors, or be labeled UNVERIFIED.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
