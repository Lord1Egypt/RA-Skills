## Description: <br>
Generate and verify hashes for strings and files using MD5, SHA variants, CRC32, HMAC, and BLAKE2 with streaming support and no external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compute hashes, verify file integrity, batch-hash files, and generate HMAC signatures during local checksum or integrity workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hashing files requires the agent to read the specified local files. <br>
Mitigation: Only provide paths for files that the agent is allowed to read and hash. <br>
Risk: HMAC generation can expose sensitive key material if long-lived secrets are supplied in prompts or command arguments. <br>
Mitigation: Use short-lived or test keys where possible, and avoid providing production secrets unless the workflow requires them. <br>
Risk: MD5, SHA1, and CRC32 are included for compatibility and checksums but are not appropriate for new security-sensitive cryptographic verification. <br>
Mitigation: Use SHA256, SHA512, or BLAKE2 for stronger integrity workflows unless a legacy format requires another algorithm. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/darbling/hash-utilities) <br>
- [Project Repository Linked by Artifact](https://github.com/darbling/clawhub-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with hash strings, verification results, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, selected hash algorithms, computed digests, and pass/fail verification results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
