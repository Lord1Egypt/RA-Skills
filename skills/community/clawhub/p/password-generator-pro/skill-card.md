## Description:

Generate secure random passwords using Python's secrets module with customizable length and character set options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate one or more random passwords with configurable length and optional number or symbol inclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated passwords are printed in the terminal, where they may remain visible in scrollback, logs, or shared sessions.

Mitigation: Run the generator in a private terminal session, clear terminal history where appropriate, and store generated passwords in a password manager.

Risk: Reusing generated passwords across accounts can increase account compromise impact.

Mitigation: Generate unique passwords per account or service and avoid reuse across important accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/password-generator-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text password strings with optional Markdown command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated passwords are printed to the terminal and can be customized by length, count, and character set options.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
