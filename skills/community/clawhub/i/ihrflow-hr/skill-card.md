## Description:

iHRFlow HR assistant for recruiting. Use when searching candidates, managing positions, scheduling interviews, advancing pipeline, or viewing recruitment stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeling](https://clawhub.ai/user/mikeling)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams and recruiters use this skill to search candidates, review resumes, manage positions, schedule interviews, advance screening decisions, add notes, and summarize recruiting status from iHRFlow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses credentials and sessions to access live candidate and recruiting records.

Mitigation: Install only in a trusted OpenClaw environment for authorized HR users, use a fixed HTTPS MCP endpoint, avoid shared hosts, and protect credential environment variables.

Risk: The skill can change recruiting records, including candidate status, interview schedules, position state, and resume notes.

Mitigation: Require human confirmation before actions that modify candidate status, schedule or cancel interviews, publish or close positions, or write notes; verify record IDs before executing.

Risk: The security review notes session-file handling concerns for production use.

Mitigation: Review and fix session-file handling before production deployment, especially on shared systems.

## Reference(s):

- [iHRFlow MCP Tool & Resource Reference](references/api-reference.md)
- [iHRFlow HR Assistant README](README.md)
- [iHRFlow AI Recruiting Assistant User Guide](docs/用户手册.md)
- [iHRFlow Platform](https://ihrflow.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with tables and inline shell commands; MCP tool and resource calls return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, iHRFlow MCP endpoint configuration, and user credentials.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, CHANGELOG, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
