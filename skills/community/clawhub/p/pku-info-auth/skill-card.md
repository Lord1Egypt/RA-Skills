## Description:

PKU Info Auth helps agents and users authenticate with PKU services, manage stored credentials, and check session status without exposing passwords to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and agents working with PKU CLI tools use this skill to set up credential storage, check PKU service sessions, and trigger auto-login flows while keeping passwords out of agent-visible prompts and command arguments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored PKU credentials could be used for unintended service logins if an agent is allowed to proceed without user awareness.

Mitigation: Run initial credential storage manually, confirm which PKU service an agent is logging into, and clear stored credentials with info-auth clear when they are no longer needed.

## Reference(s):

- [PKU Info Auth ClawHub listing](https://clawhub.ai/wjsoj/skills/pku-info-auth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and credential-handling rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included in the skill artifact; guidance focuses on OS keyring storage, session checks, and user-controlled credential entry.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
