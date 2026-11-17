## Description:

Helps agents manage Google Apps Script projects, versions, deployments, and remote function execution through Maton-managed access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other authorized users can ask an agent to create or update Apps Script projects, manage versions and deployments, execute functions, and inspect execution status. Access requires a Maton account, network connectivity, and an authorized Google connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Google authorization could grant access beyond the task.

Mitigation: Review requested OAuth scopes and authorize only the access needed.

Risk: Writes, script execution, deployments, and triggers can change data or create persistent automation.

Mitigation: Default to read-only operations and obtain explicit user approval for each write, execution, deployment, or automation change.

Risk: API keys, destinations, and returned data may expose credentials or personal information.

Mitigation: Avoid sharing credentials or raw responses; verify destinations and limit displayed data to what the task needs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/google-apps-script)
- [Maton](https://maton.ai)
- [Google Apps Script API](https://developers.google.com/apps-script/api)
- [Google Apps Script API reference](https://developers.google.com/apps-script/api/reference/rest)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance for reviewing API responses and execution results.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
