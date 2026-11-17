## Description:

Helps agents generate and check local SHA-256 file manifests to compare directory contents before and after transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can ask an agent to generate a local directory checksum manifest or check existing files against one after downloads, transfers, or backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A check can report PASS even when new untrusted files have been added.

Mitigation: Review added-file results and treat additions as failures unless explicitly allowed; do not use this as a strict tamper gate without that safeguard.

Risk: Hashing sensitive directories creates a manifest of filenames and hashes.

Mitigation: Limit use to intended directories and protect or avoid retaining sensitive manifests.

Risk: The declared permissions omit file and process access needed for local hashing.

Mitigation: Review the skill and its local access requirements before installation or execution.

## Reference(s):

- [hash-check release on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/hash-check)
- [Publisher profile on ClawHub](https://clawhub.ai/user/zhaoxinghua09-cell)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Files]

**Output Format:** [Local SHA-256 manifest and command-line text or JSON check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Check results list missing, added, and changed files; added files alone do not cause a failure exit status.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
