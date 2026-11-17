## Description:

LeSecure Local/On-Prem helps agents encrypt and decrypt plaintext, files, and folders with the local LE desktop tool using pin, password, MFA, time-lock, and location-lock options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spalgorithm](https://clawhub.ai/user/spalgorithm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and run local LE desktop encryption, decryption, file inspection, MFA, time-lock, and location-lock workflows without requiring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command construction can become unsafe if plaintext, paths, or duration values are interpolated directly.

Mitigation: Sanitize plaintext, avoid eval and backtick interpolation, pass dynamic duration values as argv, and use a resolved LE binary path.

Risk: Overwrite and delete-source flags can cause unintended data loss.

Mitigation: Confirm output destinations before encryption or decryption, preserve source files by default, and require explicit confirmation before using -c or -j.

Risk: GPS lookup and MFA flows may expose sensitive location, phone, or OTP data outside the expected local boundary.

Mitigation: Require user acknowledgment before LE -7 and avoid claiming MFA is fully local unless the LE provider documents phone and OTP handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spalgorithm/skills/lesecurelocal)
- [LE source code and documentation](https://github.com/SPAlgorithm/LE)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, LE lock flags, confirmation prompts for destructive operations, and consent prompts for GPS access.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
