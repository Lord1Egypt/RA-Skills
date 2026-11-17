## Description:

Monitors user session idleness and automatically stops the OpenClaw Gateway after a configurable idle period to save resources and costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yu200512](https://clawhub.ai/user/yu200512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenClaw Gateway use this skill to install and configure an idle watcher that stops the Gateway after detected sessions remain idle beyond a configured threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persistent watcher can automatically stop OpenClaw Gateway and interrupt availability on shared, production, or business-critical systems.

Mitigation: Review before installation, test in the target environment, choose conservative idle thresholds, monitor the idle-shutdown log, and keep the documented systemd removal steps available.

Risk: Session-file filtering may miss active sessions and stop the Gateway while some users are still active.

Mitigation: Confirm that the configured session directory and filename patterns cover the active channels before enabling automatic shutdown.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yu200512/skills/idle-shutdown)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and systemd configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, configuration, and removal guidance for a persistent user-level idle shutdown watcher.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
