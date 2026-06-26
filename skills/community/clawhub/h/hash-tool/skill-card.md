## Description: <br>
Compute cryptographic hash values of files and text for file integrity checks, checksum verification, and data validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate and compare hashes for local files or text when validating checksums and confirming file integrity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MD5 and SHA-1 are legacy algorithms and are weak choices for tamper-resistant integrity claims. <br>
Mitigation: Prefer SHA-256, SHA-512, or BLAKE2 for integrity checks; reserve MD5 and SHA-1 for legacy compatibility. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text hash values and verification status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports file and string inputs, hex or base64 encoding, and single-algorithm or all-algorithm output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
