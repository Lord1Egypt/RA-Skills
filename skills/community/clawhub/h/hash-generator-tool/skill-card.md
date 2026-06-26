## Description: <br>
Multi-purpose hash tool for MD5, SHA-1, SHA-256, SHA-512, BLAKE2b, Base64 encode/decode, UUID generation, and HMAC signing using the Python standard library with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate hashes, Base64 encodings or decodings, random UUIDs, and HMAC signatures from local command-line inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HMAC secrets, messages, and JSON output can appear in terminal history, process arguments, command output, or agent logs. <br>
Mitigation: Avoid real long-lived HMAC keys or sensitive payloads in command-line arguments or JSON output, especially in logged environments. <br>
Risk: MD5 and SHA-1 are available but are not appropriate for security-sensitive hashing. <br>
Mitigation: Use SHA-256, SHA-512, or BLAKE2b for security-sensitive use cases and reserve MD5 or SHA-1 for non-security compatibility checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/hash-generator-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON command output, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with the Python standard library and no external API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, target metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
