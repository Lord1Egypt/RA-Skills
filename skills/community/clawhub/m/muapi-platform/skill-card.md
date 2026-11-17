## Description:

Setup and utility scripts for muapi.ai to configure API keys, test connectivity, and poll for async generation results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anil-matcha](https://clawhub.ai/user/anil-matcha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure MuAPI credentials, verify access through the muapi CLI, and retrieve asynchronous prediction results by request ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented setup path can expose a MuAPI API key in shell history or process arguments.

Mitigation: Prefer the interactive setup form, avoid passing the API key directly as a command argument, confirm where the muapi CLI stores credentials, and rotate any key previously entered through the command-line example.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local shell scripts that call the muapi CLI and can return status text or JSON output from result polling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
