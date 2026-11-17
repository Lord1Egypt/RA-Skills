## Description:

Install and authenticate OB1 (OpenBlock One), a multi-model terminal coding agent. Use when asked to install OB1, set up ob1, or when ob1 authentication/login is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[txc-z](https://clawhub.ai/user/txc-z)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install OB1 on macOS or Linux, complete device-code authentication, verify the installation, and run OB1 in interactive or non-interactive workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step executes a mutable remote script directly in the shell without verification.

Mitigation: Run the installer only when OpenBlock Labs and the installer endpoint are trusted; prefer a version-pinned, checksum-verified, inspectable installer or signed package before granting access to user files or OB1 authentication state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/txc-z/skills/ob1-install)
- [Publisher profile](https://clawhub.ai/user/txc-z)
- [OB1 installer endpoint](https://dashboard.openblocklabs.com/install)
- [OB1 device authentication](https://auth.openblocklabs.com/device)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
