## Description:

Celigo (celigo.com). Use this skill for ANY Celigo request — searching and reading data. Whenever a task involves Celigo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and operators use this skill to read Celigo connections, exports, flows, imports, and token metadata through an OOMOL-connected account. It guides agents to check each action's schema before sending a request and explains how to handle connection setup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup instructions direct the agent to execute downloaded CLI installation code without clear user approval.

Mitigation: Review and install the CLI separately from a verified release, and require approval before making installation changes.

Risk: Celigo access uses the permissions and data available to the connected account.

Mitigation: Consider the connected account's permissions and the sensitivity of its data before using the skill.

## Reference(s):

- [Celigo skill release](https://clawhub.ai/oomol/skills/oo-celigo)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Celigo](https://www.celigo.com)
- [Celigo standard REST API documentation](https://docs.celigo.com/hc/en-us/articles/360042281231-Getting-started-with-standard-REST-API)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
