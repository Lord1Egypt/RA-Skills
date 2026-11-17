## Description:

NVEIL helps agents turn natural-language data processing and visualization requests into local CLI or Python workflows, using a remote planning service while executing on the user's machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pierrejacquet](https://clawhub.ai/user/pierrejacquet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to delegate structured data transformation, analysis, and visualization tasks to the NVEIL CLI or Python package instead of hand-writing pandas, NumPy, plotting, geospatial, or volume-rendering code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or regulated data workflows may send prompts, schema, and summary statistics to the NVEIL planning service.

Mitigation: Use the skill only after confirming that sharing dataset metadata is acceptable, and avoid autonomous use on confidential files unless this data flow has been approved.

Risk: The skill relies on unaudited external package behavior and remote planning.

Mitigation: Install a pinned NVEIL package version in an isolated virtual environment and review generated plans or outputs before using them in decisions.

Risk: Disabling TLS verification can weaken transport security.

Mitigation: Keep TLS verification enabled except for strictly local self-signed development servers.

Risk: Automatic MCP registration can modify local client configuration.

Mitigation: Prefer manual MCP registration or verify exactly what the installer changes before using auto-registration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pierrejacquet/skills/nveil)
- [Publisher profile](https://clawhub.ai/user/pierrejacquet)
- [NVEIL homepage](https://nveil.com)
- [NVEIL documentation](https://docs.nveil.com)
- [NVEIL API reference](https://docs.nveil.com/api-reference/)
- [NVEIL PyPI package](https://pypi.org/project/nveil/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to produce HTML, PNG, and .nveil files through the separate NVEIL package when invoked against user data.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
