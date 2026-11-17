## Description:

Check if referenced bioinformatics software/code licenses allow commercial use, including GPL and MIT-style cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to triage whether referenced bioinformatics tools and Python requirements appear compatible with commercial use. It helps surface copyleft warnings and compliance follow-up items before a final legal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: License results may be incomplete or stale because the skill uses a bounded license database.

Mitigation: Verify licenses against upstream project sources before relying on commercial-use decisions.

Risk: Copyleft obligations can depend on integration, distribution, and network-use context.

Mitigation: Confirm GPL, LGPL, and AGPL obligations with appropriate counsel before commercial release.

Risk: Results are preliminary triage rather than legal advice.

Mitigation: Treat the report as an input to compliance review, not as the final licensing decision.

## Reference(s):

- [Open Source License Check on ClawHub](https://clawhub.ai/aipoch-ai/skills/open-source-license-check)
- [Audit Reference](references/audit-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text license compatibility report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commercial-use status, copyleft warnings, assumptions, and compliance recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
