## Description:

Java Switch helps agents install and switch Java versions on macOS using Homebrew and /usr/libexec/java_home while configuring JAVA_HOME and PATH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longfer](https://clawhub.ai/user/longfer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent to switch to a requested Java version, install it with Homebrew when needed, and update macOS shell environment settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install Homebrew or OpenJDK packages on the user's machine.

Mitigation: Review the commands before execution and run installation steps only after explicit user approval.

Risk: The skill can persistently modify ~/.zshrc and change JAVA_HOME/PATH behavior for future shells.

Mitigation: Back up shell configuration, inspect the planned changes, and prefer simple numeric Java versions before applying persistent updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/longfer/skills/java-switch)
- [Publisher Profile](https://clawhub.ai/user/longfer)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install OpenJDK with Homebrew and persist JAVA_HOME/PATH updates in ~/.zshrc.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
