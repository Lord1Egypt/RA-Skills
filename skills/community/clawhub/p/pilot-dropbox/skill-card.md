## Description:

Shared folder that automatically synchronizes between peers using Pilot Protocol pub/sub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to set up a persistent peer-to-peer shared folder with automatic synchronization and eventual consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Peer-provided filenames may cause deletion or disclosure of files outside the intended shared folder.

Mitigation: Add strict basename validation and canonical path containment checks before reading, sending, or deleting any file.

Risk: Untrusted peers or topics may trigger unsafe synchronization behavior.

Mitigation: Run the daemon only with trusted peers and topics under a dedicated low-privilege account or sandbox, and require confirmation or quarantine for deletes.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [Pilot Dropbox ClawHub listing](https://clawhub.ai/teoslayer/skills/pilot-dropbox)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for subscribing to a topic, publishing file changes, removing files, and running a shared-folder daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
