## Description:

Bootstrap a multi-agent software project from idea to running CI/CD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckouder](https://clawhub.ai/user/ckouder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to plan a new multi-agent project, define agent roles, initialize task management, and set up GitHub CI/CD with Discord notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents to create GitHub repositories, change rulesets, configure webhooks, or alter CI/CD behavior.

Mitigation: Require explicit human approval before repository, branch protection, webhook, or CI/CD changes are executed.

Risk: Generated agent configurations may grant broad tool access.

Mitigation: Review generated agent profiles and reduce tool permissions to the least privilege needed for each role.

Risk: Discord notifications can expose task, commit, author, or project details.

Mitigation: Use private Discord channels and minimize notification payloads before enabling webhooks.

Risk: Unpinned third-party GitHub Actions can introduce supply-chain risk.

Mitigation: Pin third-party GitHub Actions to reviewed commit SHAs and require human approval on protected branches.

## Reference(s):

- [Project Bootstrap on ClawHub](https://clawhub.ai/ckouder/skills/project-bootstrap)
- [Taskboard CLI Setup](references/taskboard-setup.md)
- [CI/CD Templates](references/ci-cd-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, YAML, shell commands, and Python CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository, CI/CD, Discord, taskboard, and agent configuration changes for review before execution.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
