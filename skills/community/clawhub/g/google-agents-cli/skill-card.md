## Description:

Bootstraps the Google agents-cli experience for Google Agent Development Kit agent development, including setup for specialized skills covering scaffold, build, evaluate, deploy, publish, and observe workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eliasecchig](https://clawhub.ai/user/eliasecchig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and hand off to the Google agents-cli toolchain when building, evaluating, deploying, publishing, or observing ADK-based agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup command is unpinned and installs multiple additional agent skills that were not included in this review.

Mitigation: Review the package and installed skills before use, prefer a pinned verified package version, and run setup in an isolated environment without unnecessary credentials or sensitive project access.

## Reference(s):

- [agents-cli GitHub repository](https://github.com/google/agents-cli)
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/index.md)
- [ClawHub skill page](https://clawhub.ai/eliasecchig/skills/google-agents-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires agents-cli and uv; setup installs additional specialized skills into the coding-agent environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
