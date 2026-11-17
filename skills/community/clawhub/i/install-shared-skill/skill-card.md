## Description:

Provides OpenClaw tools that install a named ClawHub skill by running the clawhub CLI in the current workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shifulegend](https://clawhub.ai/user/shifulegend)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to install a named skill from ClawHub into the active workspace through CLI-backed tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted skill name could run unintended shell commands.

Mitigation: Install only after the publisher fixes shell execution or restrict use to trusted, reviewed skill identifiers.

Risk: The stated shared or global install scope conflicts with the workspace-targeted command.

Mitigation: Confirm the install destination before use and do not rely on this skill for shared installation until the behavior and documentation agree.

Risk: The skill performs a high-impact install action.

Mitigation: Review and scan installed skills before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shifulegend/skills/install-shared-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Plain text terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns stdout and stderr from the clawhub install command; non-zero command exits are surfaced as tool failures.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
