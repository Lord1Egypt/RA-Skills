## Description:

Hash Toolkit provides content hashing for deduplication with MD5, SHA256, and perceptual hashing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi)

### License/Terms of Use:


## Use Case:

Developers and agents use Hash Toolkit to generate content hashes for verification and deduplication, check known hash sets for duplicates, and run basic normalized-content similarity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The simplified perceptual hash can produce misleading similarity or deduplication results if used for robust image similarity, near-duplicate detection, or security-sensitive deduplication.

Mitigation: Use it only as a basic local hashing helper; replace the perceptual hash with a real perceptual hashing algorithm for strong similarity or security-sensitive workflows.

## Reference(s):

- [Hash Toolkit ClawHub Skill Page](https://clawhub.ai/raghulpasupathi/skills/hash-toolkit)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JavaScript utility functions returning hexadecimal hash strings and JSON-like duplicate-check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports MD5, SHA1, SHA256, and truncated SHA512 outputs; perceptual hashing is a simplified normalized-content hash.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
