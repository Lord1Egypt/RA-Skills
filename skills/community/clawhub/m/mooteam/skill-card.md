## Description:

MooTeam CRM gives an OpenClaw agent CLI access to MooTeam API v1 for projects, teams, tasks, drafts, comments, workflows, statuses, labels, timers, time logs, and activity logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antokhin-digital](https://clawhub.ai/user/antokhin-digital)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operational teams use this skill to let an OpenClaw agent inspect and manage MooTeam CRM and project-management data through authenticated CLI/API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete MooTeam company project data when run with an authorized token.

Mitigation: Use a least-privileged MooTeam token and review create, update, timer, and delete commands before execution.

Risk: Project deletion is documented with a --force safeguard, but the security summary says that safeguard is not actually enforced.

Mitigation: Treat project deletion as unsafe until the --force check or a stronger confirmation is enforced.

## Reference(s):

- [MooTeam API Usage Guide](artifact/references/api_docs.md)
- [MooTeam API endpoint](https://api.moo.team/api)
- [ClawHub skill page](https://clawhub.ai/antokhin-digital/skills/mooteam)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI invocations return JSON or terminal tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOOTEAM_API_TOKEN and MOOTEAM_COMPANY_ALIAS; commands can modify or delete MooTeam business data.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
