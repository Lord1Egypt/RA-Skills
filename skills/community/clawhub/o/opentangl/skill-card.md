## Description:

OpenTangl helps configure an autonomous development loop for JavaScript and TypeScript projects, including project detection, configuration, vision documentation, LLM setup, and first-run commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[8co](https://clawhub.ai/user/8co)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to prepare OpenTangl for autonomous work on JavaScript and TypeScript projects. It guides project discovery, configuration file creation, product vision capture, LLM setup, and the first autopilot run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prepares an autonomous workflow that can create, review, and merge repository changes.

Mitigation: Use a limited GitHub token or account, test on non-critical repositories first, and confirm whether autopilot can merge without human approval before granting access to important projects.

Risk: The setup relies on mutable third-party install and runtime commands.

Mitigation: Pin the OpenTangl repository to a reviewed commit and prefer lockfile-based installs before running it.

## Reference(s):

- [OpenTangl homepage](https://github.com/8co/opentangl)
- [ClawHub skill page](https://clawhub.ai/8co/skills/opentangl)
- [Publisher profile](https://clawhub.ai/user/8co)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project configuration, product vision, and task queue files after gated user confirmation.]

## Skill Version(s):

0.1.10 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
