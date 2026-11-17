## Description:

Calculate, verify, and compare file hashes using MD5, SHA-1, SHA-256, SHA-512, and BLAKE2b.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to calculate checksums, verify downloaded file hashes, compare files for equality, and hash text strings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MD5 and SHA-1 are weak choices for security-sensitive verification.

Mitigation: Use SHA-256, SHA-512, or BLAKE2b for security-sensitive checks; reserve MD5 and SHA-1 for compatibility with older published checksums.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogue-agent1/skills/hashcheck)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional JSON hash results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports file hashes, text hashes, verification, comparison, and multi-algorithm display.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
