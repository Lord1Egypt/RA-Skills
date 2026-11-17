## Description:

Hash files and strings, verify checksums, and run integrity checks fast. Use when generating SHA hashes, verifying files, or comparing digest values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Hashgen to generate MD5 and SHA-family digests for strings and files, compare hash values, and verify text against an expected checksum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text passed as command-line input may appear in terminal output, shell history, logs, or process listings.

Mitigation: Do not pass passwords, API keys, tokens, or other secrets as command-line text; use non-sensitive sample inputs or files whose contents are appropriate to hash locally.

## Reference(s):

- [Hashgen on ClawHub](https://clawhub.ai/bytesagain3/skills/hashgen)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include digest values, file metadata, comparison results, and verification results from local hashgen commands.]

## Skill Version(s):

3.0.0 (source: release evidence, artifact frontmatter, script constant)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
