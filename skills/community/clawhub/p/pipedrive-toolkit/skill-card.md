## Description:

Pipedrive API工具 helps agents manage Pipedrive deals, contacts, organizations, and activities through managed OAuth and configurable API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent builders, and business automation teams use this skill to automate Pipedrive CRM operations such as querying and managing deals, contacts, organizations, and activities. It is intended for workflow automation where API credentials and live CRM effects can be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect live CRM records through Pipedrive or Maton API operations.

Mitigation: Use least-privileged or test credentials and require explicit confirmation before create, update, delete, or webhook operations.

Risk: API keys or OAuth credentials could be exposed in logs or shared transcripts.

Mitigation: Store credentials in environment variables and avoid printing or pasting API keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pipedrive-toolkit)
- [Maton Pipedrive deals API endpoint](https://api.maton.ai/pipedrive/api/v1/deals)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline shell or Python commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external Pipedrive or Maton APIs when the user executes generated commands with configured credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
