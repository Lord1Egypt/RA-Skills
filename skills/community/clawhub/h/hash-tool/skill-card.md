## Description:

Compute cryptographic hash values of files and text. Use for verifying file integrity, checksums, and data validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to compute and verify checksums for files or text during integrity checks, checksum comparison, and data validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes MD5 and SHA-1 outputs, which are legacy checksum algorithms and should not be treated as strong security validation.

Mitigation: Use SHA-256, SHA-512, or BLAKE2 for security-sensitive integrity checks, and reserve MD5 or SHA-1 for legacy checksum comparison only.

Risk: The tool reads user-selected files or text to compute hashes.

Mitigation: Run it only on files and input text the user intends to read and process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/hash-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and checksum text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic hash strings for selected algorithms; MD5 and SHA-1 are legacy checksum options, not strong security validation choices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
