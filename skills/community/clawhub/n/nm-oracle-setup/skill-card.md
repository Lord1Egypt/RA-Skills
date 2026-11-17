## Description:

Provisions the oracle ML inference daemon with onnxruntime via uv

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers setting up the Oracle inference environment use this skill to provision the local ONNX Runtime daemon dependencies for skill quality evaluation. It provisions the environment; it does not perform the quality evaluation itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security analysis has partial coverage because a local Markdown reference could not be resolved.

Mitigation: Resolve and review the referenced material, then review the skill before installation.

Risk: Provisioning installs onnxruntime and pyyaml and requires an initial internet download.

Mitigation: Run provisioning in the intended project virtual environment and follow the environment's dependency and package source policies.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-oracle-setup)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/oracle)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown instructions with inline shell commands and a provisioning result message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and an internet connection for the initial dependency download.]

## Skill Version(s):

1.10.3 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
