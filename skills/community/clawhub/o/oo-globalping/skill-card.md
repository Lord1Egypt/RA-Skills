## Description:

Globalping (globalping.io). Use this skill for ANY Globalping request — reading, creating, and updating data. Whenever a task involves Globalping, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Globalping probes and account limits, retrieve measurement results, and create measurements through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path runs remote CLI installers whose complete effects are unverified.

Mitigation: Review the installer and use a verified, pinned CLI release before installation.

Risk: CLI startup may synchronize skill files and change local agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI when startup synchronization is not needed.

Risk: Creating a measurement changes Globalping state.

Mitigation: Confirm the exact measurement target and payload before running create_measurement.

## Reference(s):

- [Globalping](https://globalping.io)
- [Globalping API documentation](https://globalping.io/docs/api.globalping.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON payloads and connector results, with oo CLI commands for invoking actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
