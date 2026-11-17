## Description:

Converts REST APIs into OpenClaw skills by generating SKILL.md documentation, claw.json metadata, and Python API client scripts from OpenAPI specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT

## Use Case:

Developers and API providers use this skill to turn OpenAPI-described REST APIs into reusable OpenClaw skills with generated documentation, package metadata, and API client code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted OpenAPI specifications can influence generated files and code.

Mitigation: Use trusted local specs or known public HTTPS hosts, then review generated SKILL.md and scripts/api.py before installing or running the generated skill.

Risk: The generator writes files to an output directory and may create unintended artifacts if inputs are not controlled.

Mitigation: Provide a safe skill name and a controlled output directory when generating a wrapper.

Risk: Generated API clients may handle credentials or call live network APIs.

Mitigation: Use sandbox or read-only API credentials rather than production tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-api-wrapper)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown documentation, JSON configuration, and Python code files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated skills and scripts should be reviewed and scanned before installation or execution.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
