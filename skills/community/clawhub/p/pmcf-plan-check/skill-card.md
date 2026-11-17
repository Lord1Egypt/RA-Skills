## Description:

Checks a PMCF plan for missing or weak methods, endpoints, statistical considerations, and other core elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Medical-device regulatory teams use the checker to identify missing or weak elements in draft post-market clinical follow-up plans before human review and submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a mutable remote script into a persistent skills directory can give unreviewed code ongoing access.

Mitigation: Prefer the packaged script or a pinned revision; inspect the script before persistent installation.

Risk: The skill requests broader tool permissions than the local check requires.

Mitigation: Limit permissions to reading the PMCF input and running the local checker.

Risk: A complete checklist may be mistaken for regulatory approval or methodological adequacy.

Mitigation: Have a qualified reviewer assess the plan against current official requirements before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/pmcf-plan-check)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ten-element completeness score, missing or weak fields, suggested fixes, and exit status.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
