## Description:

Give ClawBot access to your team's entire coding history. Muse connects your past sessions, team knowledge, and project context so ClawBot can help design features, mediate team discussions, and work autonomously across your codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexander-morris](https://clawhub.ai/user/alexander-morris)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use Muse to search AI coding sessions, manage project knowledge, inspect session artifacts, and coordinate Tribe/Muse autonomous-agent workflows through the tribe CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party CLI that may access sensitive coding history, telemetry, knowledge-base data, and autonomous-agent workflows.

Mitigation: Use only with repositories and team history you are authorized to expose to Tribe/Muse, and review Tribe/Muse data handling before installation.

Risk: Authentication and sync behavior can broaden access to local or team development data.

Mitigation: Use a least-privilege account, confirm telemetry and sync settings, and avoid auto or force-sync modes in sensitive workspaces.

Risk: The npm package @_xtribe/cli is installed and trusted before running skill workflows.

Mitigation: Pin or otherwise verify the package before installation and review the skill before deployment.

## Reference(s):

- [Muse Skill Page](https://clawhub.ai/alexander-morris/skills/muse)
- [TribeClaw Deployment Site](https://tribeclaw.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional JSON-formatted CLI outputs when users run tribe commands with --format json.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
