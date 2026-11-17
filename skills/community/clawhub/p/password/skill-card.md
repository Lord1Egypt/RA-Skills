## Description:

Manage passwords with generation, strength checks, and storage. Use when creating credentials, auditing strength, rotating secrets, checking breaches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to generate passwords and PINs, produce diceware-style passphrases, and analyze password strength or entropy. It can also check candidate passwords against breach data when network access and curl are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real passwords supplied as command-line arguments can be exposed through shell history, process listings, or logs.

Mitigation: Use generated test values only unless the tool is changed to read secrets through a hidden prompt or standard input.

Risk: Breach checking performs an external network request to Have I Been Pwned.

Mitigation: Treat breach checks as network operations and review whether that external service is acceptable for the deployment environment.

Risk: The release advertises storage and rotation behavior that is not implemented in the inspected artifact.

Mitigation: Do not rely on password storage or rotation unless those features are implemented and reviewed in a later artifact.

## Reference(s):

- [ClawHub Password Skill](https://clawhub.ai/bytesagain3/skills/password)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated passwords, strength ratings, entropy estimates, breach-check status, diceware-style passphrases, and PINs.]

## Skill Version(s):

3.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
