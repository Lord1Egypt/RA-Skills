## Description:

MacPowerTools provides local macOS maintenance, resource forecasting, backup, process-monitoring, LAN-discovery, and swarm-simulation commands for OpenClaw agents on Apple Silicon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aadipapp](https://clawhub.ai/user/aadipapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to run local Mac maintenance and agent-support commands on Apple Silicon systems. It is intended for local optimization workflows such as cleanup, backup support, process monitoring, resource forecasting, LAN discovery, and simulated swarm-coherence reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the package is a broken script and is not transparent enough for normal installation.

Mitigation: Do not install until the publisher ships valid Python and aligns the artifact with the advertised commands.

Risk: The security summary identifies intended local history storage despite claims of zero persistence.

Mitigation: Require clear documentation of local files and retention behavior before use.

Risk: The security summary identifies LAN discovery behavior.

Mitigation: Run only after the publisher documents the LAN-discovery behavior and after the user confirms it is acceptable for the target network.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aadipapp/skills/mac-power-tools)
- [Publisher profile](https://clawhub.ai/user/aadipapp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [CLI text, JSON-style command output, and Markdown install guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-focused output for local user-level workflows; no artifact-backed external API output is described.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter says 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
