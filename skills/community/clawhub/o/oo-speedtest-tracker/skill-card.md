## Description:

Use this skill for Speedtest Tracker requests, including reading, creating, and updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to inspect Speedtest Tracker results and statistics, find servers, check service health, and queue speed tests through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the oo CLI may run a downloaded installer and enable automatic agent-skill synchronization.

Mitigation: Review the CLI and installer before use, and decide whether to allow skill synchronization.

Risk: Speedtest Tracker requests pass through OOMOL, and connector behavior and remote installers were not fully verified.

Mitigation: Connect only the permissions needed for the task and review provider or connector errors before proceeding.

## Reference(s):

- [Speedtest Tracker](https://speedtest-tracker.dev/)
- [Speedtest Tracker API documentation](https://docs.speedtest-tracker.dev/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Speedtest Tracker skill release](https://clawhub.ai/oomol/skills/oo-speedtest-tracker)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON connector results summarized as natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Speedtest Tracker instance and granted permissions.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
