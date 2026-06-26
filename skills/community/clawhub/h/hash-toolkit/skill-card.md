## Description: <br>
Content hashing for deduplication with MD5, SHA256, and perceptual hashing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate content hashes, compare known hashes for duplicate detection, and produce simplified perceptual hashes for similarity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MD5 and SHA1 hashes may be inappropriate for security or integrity decisions. <br>
Mitigation: Use SHA-256 or stronger algorithms for integrity checks and avoid MD5 or SHA-1 for trust decisions. <br>
Risk: The perceptual hash implementation is simplified and may give misleading similarity results. <br>
Mitigation: Use it only as a lightweight heuristic and do not rely on it for image similarity, near-duplicate detection, or trust decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration] <br>
**Output Format:** [JavaScript functions returning hash strings and JSON-like duplicate-check results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports MD5, SHA1, SHA256, truncated SHA512, and simplified perceptual hash outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
