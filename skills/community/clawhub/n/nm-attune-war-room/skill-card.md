## Description:

Convenes a multi-LLM expert panel to pressure-test hard-to-reverse decisions

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Product and engineering teams use the skill to evaluate consequential decisions with competing approaches. It assesses reversibility, structures expert review and challenge, and produces a decision record with rationale and follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision summaries may be published to GitHub Discussions by default when available, potentially exposing sensitive information.

Mitigation: Review and redact the decision record before publication, and decline publishing when it contains information that should remain private.

Risk: Deliberation context may be shared with external model providers.

Mitigation: Remove confidential details and use external delegation only when it is permitted for the information involved.

Risk: The security assessment is partial because three referenced local paths were missing; their contents were not assessed.

Mitigation: Obtain and review the missing referenced files before relying on or installing the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-attune-war-room)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/attune)
- [Reversible and irreversible decisions](https://fs.blog/reversible-irreversible-decisions/)
- [One-way and two-way door decisions](https://tapandesai.com/one-way-two-way-doors-decision-making/)
- [Type 1 and Type 2 decision framework](https://ashikuzzaman.com/2025/03/03/amazons-type-1-vs-type-2-decisions-a-framework-for-effective-decision-making/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown decision report with assessment tables and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a reversibility assessment, alternatives, rationale, action items, watch points, and dissenting views; content may be shared with external model providers or published to GitHub Discussions.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
