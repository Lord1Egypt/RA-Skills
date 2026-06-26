## Description: <br>
Hash files and strings, verify checksums, and run integrity checks fast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Hashgen to generate MD5, SHA1, SHA256, and SHA512 hashes for text or files, compare digest values, and verify checksums during integrity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive text passed on the command line can appear in shell history, terminal scrollback, logs, or process-related records. <br>
Mitigation: Avoid hashing passwords, API keys, tokens, and other secrets as command-line text; use non-sensitive inputs or file-based workflows where appropriate. <br>
Risk: MD5 and SHA1 are weak for security-sensitive integrity decisions. <br>
Mitigation: Prefer SHA256 or SHA512 for integrity checks; use MD5 and SHA1 only when compatibility with existing checksums requires them. <br>


## Reference(s): <br>
- [Hashgen on ClawHub](https://clawhub.ai/bytesagain3/hashgen) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text command output and concise Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local hash values, comparison results, file metadata, and checksum verification status.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
