## Description:

Large file transfer with automatic chunking, resume capability, and integrity verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to transfer large files over Pilot Protocol by chunking files, tracking progress, and resuming interrupted transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming transfer metadata may write or delete files outside the intended receive folder.

Mitigation: Validate filenames, confine receives to a private temporary directory, and reject path traversal before creating, concatenating, or deleting paths.

Risk: The documented integrity verification is incomplete.

Mitigation: Implement checksum validation and resume-state checks before accepting chunks or reassembling a transferred file.

Risk: The skill should not be used as written with untrusted senders or important local files.

Mitigation: Review commands before execution and use only with trusted senders until the receive path handling and verification behavior are corrected.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-chunk-transfer)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot daemon, jq, dd, md5sum, and bc.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
