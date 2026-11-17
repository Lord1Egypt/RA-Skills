## Description:

Grill The Plan helps an agent turn multi-step or risky work into a Chinese-language pre-flight checklist with explicit parameters, risks, dependencies, and user confirmation before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fbbyqsyea](https://clawhub.ai/user/fbbyqsyea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other agent users use this skill to slow down implementation until a plan has been decomposed, risk-checked, and explicitly confirmed. It is especially suited to multi-step work, architecture decisions, and operations where unclear parameters or irreversible actions would create downstream risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The stricter confirmation workflow can add friction before implementation.

Mitigation: Use the compact path for small, fully specified tasks and reserve the full checklist for multi-step, risky, architectural, or irreversible work.

Risk: Sensitive values could be exposed while plans are being reviewed.

Mitigation: Refer to credentials only by variable name and source, avoid echoing secret values, and treat tracked .env or credentials files as blocking risks.

## Reference(s):

- [Pre-Flight Checklist Example](references/example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown checklist, question prompts, and concise progress summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for explicit user confirmation before implementation and re-checks the plan when parameters, dependencies, or assumptions change.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
