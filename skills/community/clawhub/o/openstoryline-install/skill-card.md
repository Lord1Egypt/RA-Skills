## Description:

Install, configure, and start FireRed-OpenStoryline from source on a local machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anlittledy](https://clawhub.ai/user/anlittledy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install or repair a local FireRed-OpenStoryline source checkout, configure model settings and API keys, download required resources, verify the setup, and start the MCP and web services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running upstream installation scripts and dependency files can execute behavior that changes after this skill release.

Mitigation: Review requirements.txt and download.sh before execution, install only from a trusted upstream state, and consider pinning a known commit.

Risk: API keys entered directly in shell commands or config.toml can be exposed through shell history, file permissions, or version control.

Mitigation: Avoid putting real API keys directly in shell commands when possible; clean shell history if used, restrict config.toml permissions, and keep config.toml out of version control.

## Reference(s):

- [FireRed-OpenStoryline GitHub Repository](https://github.com/FireRedTeam/FireRed-OpenStoryline.git)
- [OpenStoryline Install on ClawHub](https://clawhub.ai/anlittledy/skills/openstoryline-install)
- [Publisher Profile](https://clawhub.ai/user/anlittledy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status reporting for installed components, downloads, missing configuration, and local service addresses.]

## Skill Version(s):

0.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
