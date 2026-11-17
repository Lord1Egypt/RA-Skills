## Description:

Helps developers verify fail-closed guardrails with hostile fixtures and mutation tests that guard against stale Python bytecode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check that agent gates refuse hostile or uncertain inputs and that their tests detect removed guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running a chosen test command can execute code from the tested project.

Mitigation: Use trusted repositories and test commands, and start with a clean or sanitized environment if the shell contains sensitive tokens.

## Reference(s):

- [Guardrail Testing on ClawHub](https://clawhub.ai/alexbloch-ia/skills/guardrail-testing)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Markdown]

**Output Format:** [Markdown with test instructions, code snippets, and a guardrail-proof summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports mutation survivors and a PROVEN, NOT PROVEN, or INDETERMINATE verdict.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
