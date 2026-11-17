## Description:

Automates desktop GUI workflows through the computer use API with screenshots

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to automate GUI workflows, test applications visually, and interact with desktop software when a CLI or API is not suitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots can expose private information visible in open applications.

Mitigation: Close sensitive applications and keep credentials out of task prompts before starting.

Risk: GUI actions can change application state or cause real-world side effects.

Mitigation: Run in a sandbox and require human approval for actions with real-world consequences.

Risk: Security scan coverage is partial because several local references did not resolve.

Mitigation: Review the referenced material and dependencies before installation or use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-phantom-computer-control)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/phantom)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
