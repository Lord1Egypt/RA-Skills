## Description:

Monitors GitHub organization commit activity and reports team activity updates and current standings on a daily schedule or through the /team-status command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenkus47](https://clawhub.ai/user/tenkus47)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering managers use this skill to monitor recent GitHub commit activity for a configured organization and team, identify active and inactive members, and publish team status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses GitHub repository access and may require broad visibility into organization repositories.

Mitigation: Use a tightly scoped read-only GitHub token and confirm the token permissions before running the monitor.

Risk: The artifact targets a hard-coded GitHub organization and team.

Mitigation: Verify the configured organization and team are intended for the deployment before scheduling or invoking the skill.

Risk: The bundled sample_state.json contains private-repository and personnel activity data according to the security evidence.

Mitigation: Remove the bundled sample state and define retention controls for generated state and logs before use.

Risk: Scheduled execution can repeatedly collect and publish personnel activity data.

Mitigation: Do not enable the cron job until publication destination, state storage, and log retention are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenkus47/skills/github-tracker)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status report with setup and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports active and inactive members for a recent UTC commit window and updates local state.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
