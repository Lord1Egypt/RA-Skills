## Description:

Automated backup of agent state to trusted peers with encryption and versioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to back up agent configuration and state files to trusted remote peers, manage scheduled backup retention, and restore state when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill backs up sensitive agent state from $HOME/.pilot and sends archives to configured peers.

Mitigation: Review the files selected for backup and install only when the pilotctl transport and destination peers are trusted.

Risk: The restore workflow extracts a remote archive into live agent state.

Mitigation: Verify sender identity, signatures or hashes, and archive paths; extract into a temporary directory and require explicit approval before replacing live state.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-backup)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup, restore, and rotation command examples that depend on pilotctl, jq, and tar/gzip.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
