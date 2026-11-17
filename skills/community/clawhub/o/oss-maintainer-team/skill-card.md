## Description:

Manages open source repositories by triaging issues, reviewing code, testing, releasing updates, auditing security, and maintaining documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3ratech](https://clawhub.ai/user/t3ratech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to coordinate routine open-source repository maintenance, including issue triage, pull request review, testing, release preparation, security review, and documentation updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to read repository files, write maintainer-facing materials, and run shell commands.

Mitigation: Use it only in repositories where that access is acceptable, and review proposed file writes and shell commands before applying them.

Risk: The skill uses memory for maintainer context, which may retain repository or workflow details.

Mitigation: Avoid using it with sensitive projects unless the memory behavior is acceptable for that environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/t3ratech/skills/oss-maintainer-team)
- [Publisher profile](https://clawhub.ai/user/t3ratech)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository file changes, tests, release notes, and documentation updates for maintainer review.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
