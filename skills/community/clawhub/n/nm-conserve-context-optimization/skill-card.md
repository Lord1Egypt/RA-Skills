## Description:

Optimizes context window via MECW principles and memory tiering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to assess context pressure, select memory and compression strategies, and route complex work while preserving key task information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan labels the skill suspicious and reports a confirmed weakness in saved task state handling, alongside other concerns; overall confidence is medium.

Mitigation: Review the scan concerns before installing, and avoid using the skill with private task information until its saved-state behavior has been assessed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-context-optimization)
- [Publisher profile](https://clawhub.ai/user/athola)
- [Homepage listed in Clawdis metadata](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)
- [MECW principles](modules/mecw-principles.md)
- [MECW assessment](modules/mecw-assessment.md)
- [Context waiting strategies](modules/context-waiting.md)
- [Reversible compression](modules/reversible-compression.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Code]

**Output Format:** [Markdown guidance and findings, with optional code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No fixed output schema; detail depends on the task.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
