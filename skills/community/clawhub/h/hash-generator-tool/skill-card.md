## Description:

Multi-purpose hash tool: MD5, SHA-1, SHA-256, SHA-512, BLAKE2b, Base64 encode/decode, UUID generation, HMAC signing. Pure Python standard library, no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill for offline hashing, checksum generation, Base64 encoding and decoding, UUID generation, and HMAC signing from a local Python command-line utility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HMAC secrets passed directly on the command line may be retained in shell history or process metadata.

Mitigation: Avoid production HMAC keys in the documented command-line form; clear affected shell history and rotate exposed keys if used.

Risk: MD5 and SHA-1 are available but are not appropriate for security-sensitive collision-resistant hashing.

Mitigation: Use SHA-256, SHA-512, BLAKE2b, or HMAC with a supported modern digest for security-sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/hash-generator-tool)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with the Python standard library and no external API key.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
