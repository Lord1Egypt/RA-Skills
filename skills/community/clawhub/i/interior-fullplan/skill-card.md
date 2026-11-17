## Description:

Generates a Chinese-language Markdown interior design plan covering layout diagnosis, style direction, lighting, materials, budget allocation, design notes, and construction guidance from project inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[137984917-cyber](https://clawhub.ai/user/137984917-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Interior designers, design consultants, and agents use this skill to draft early-stage Chinese-language residential or commercial interior design proposals from basic client and project inputs.

### Deployment Geography for Use:

Global, with content tailored to Chinese-language interior design workflows and domestic residential or commercial design norms.

## Known Risks and Mitigations:

Risk: User-supplied project names can cause generated files to be written outside the intended Desktop location or overwrite writable files.

Mitigation: Use only trusted project names without slashes, backslashes, leading dots, or path-like text; prefer sanitizing the project name, constraining the resolved output path to Desktop, and avoiding silent overwrites before deployment.

Risk: Generated design, budget, and construction guidance may not reflect project-specific site conditions, client constraints, or applicable local requirements.

Mitigation: Have a qualified designer or project lead review the generated plan before using it in client materials, procurement, or construction decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/137984917-cyber/skills/interior-fullplan)
- [ClawHub publisher profile](https://clawhub.ai/user/137984917-cyber)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown design plan written to a local .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language content; output filename is based on the user-provided project name.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
