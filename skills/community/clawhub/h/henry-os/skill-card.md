## Description:

AI Chief of Staff framework that helps an agent find leads, manage communications and scheduling, deliver software, and produce business briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shalin1982](https://clawhub.ai/user/shalin1982)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, freelancers, and small-business operators use Henry OS to configure an autonomous assistant for opportunity discovery, communications triage, calendar support, software delivery, and daily operational briefings. The skill provides setup commands, configuration guidance, and operational patterns for running that assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The one-line installer is not auditable from the submitted artifact and pipes a remote script into a shell.

Mitigation: Inspect a pinned copy of the install script before running it, verify checksums or signatures when available, and avoid pipe-to-shell installation in trusted environments.

Risk: The described assistant may need broad access to email, messages, calendars, contacts, local projects, network services, and persistent background agents.

Mitigation: Run in a constrained account or sandbox first, grant the minimum permissions needed, and document each data flow before connecting sensitive accounts.

Risk: Automated communications, opportunity hunting, scheduling, and software delivery can create business or privacy impact if actions occur without review.

Mitigation: Keep approval gates enabled for sending messages, changing calendars, outreach, deployments, and other external actions; review drafts and task plans before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shalin1982/skills/henry-os)
- [Henry OS Documentation](https://docs.henryos.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration examples, task workflows, and operational recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require local account, calendar, contacts, messages, email, browser, and project access depending on enabled integrations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
