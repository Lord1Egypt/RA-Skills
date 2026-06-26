## Description: <br>
Compute MD5 cryptographic hash values for files and text. Use for file integrity verification and checksum validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate MD5 checksums for local files or text when checking basic file integrity or validating expected checksum values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MD5 is not appropriate for security-sensitive integrity checks or tamper resistance when adversarial modification is a concern. <br>
Mitigation: Use SHA-256 or a stronger hash for security-sensitive workflows, and limit this skill to basic local checksum generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/md5-tool) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text checksum output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local file or standard input and prints a single MD5 hexadecimal digest.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
