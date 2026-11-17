## Description:

Helps review PMCF evaluation report drafts for missing measures-taken sections and annual-cycle information before filing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Medical-device regulatory teams and report authors use this skill to spot missing PMCF report sections or annual-cycle information in drafts before submission. Its guidance is decision support, not a substitute for review against applicable regulatory requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell, write and web access despite describing itself as a documentation-only, no-network checker.

Mitigation: Review the skill before installation; restrict those capabilities or ask the publisher to remove unused permissions.

Risk: Confidential medical-device reports may be exposed or altered if the requested capabilities are granted without clear privacy and write-scope rules.

Mitigation: Do not provide confidential reports until privacy handling and write scope are clear, and grant only necessary access.

Risk: The bundled files describe a CLI and status codes but contain no executable checker.

Mitigation: Verify the implementation and its results before relying on any purported automated completeness check.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/pmcf-evaluation-report-check)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [Text or structured JSON IR]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes status codes 0, 1 and 2 for report checks; the supplied artifact contains documentation but no executable checker.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release; bundled SKILL.md says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
