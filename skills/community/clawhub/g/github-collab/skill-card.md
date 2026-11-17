## Description:

Github Collab helps agents coordinate GitHub-oriented project work by creating projects, breaking down tasks, assigning work, tracking progress, managing configuration, and reporting status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wljmmx](https://clawhub.ai/user/wljmmx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multi-agent project execution across task planning, assignment, progress tracking, configuration management, and GitHub-related reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that some implementation paths can expose credentials.

Mitigation: Do not use real GitHub, database, or messaging credentials until saved and exported configuration redacts secrets and passwords are hashed and not returned.

Risk: The security scan reports shell command execution from project data.

Mitigation: Change command execution to argument-array APIs and add strict repository-name validation before running against real repositories.

Risk: Automatic subagent and scheduler behavior can act outside intended collaboration scope if not bounded.

Mitigation: Limit automatic behavior to approved repositories and notification channels before enabling queue processing or scheduler workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wljmmx/skills/github-collab)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw sessions_spawn API](https://docs.openclaw.ai/tasks/sessions_spawn)
- [OpenClaw subagents API](https://docs.openclaw.ai/tasks/subagents)
- [OpenClaw message API](https://docs.openclaw.ai/tasks/message)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands, configuration examples, code snippets, and generated status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local SQLite task, agent, project, configuration, log, and report files when its scripts are executed.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
