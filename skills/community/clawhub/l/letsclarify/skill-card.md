## Description:

Collect structured human input such as approvals, decisions, reviews, and data through web forms, with JSON-schema form creation, unique human URLs, and result polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heisee](https://clawhub.ai/user/heisee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when a workflow needs structured human input before proceeding, such as approvals, reviews, decisions, or data collection. The skill supports creating forms, distributing recipient links, polling or receiving results, and cleaning up retained data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Form content, responses, uploaded files, and recipient metadata are sent to letsclarify.ai and may also be sent to configured webhook URLs.

Mitigation: Confirm the data sharing posture before use, avoid unnecessary sensitive content, and only configure webhook endpoints you control and trust.

Risk: API keys and delete tokens can grant access to forms, results, or destructive deletion actions.

Mitigation: Store credentials securely, avoid exposing tokens in logs or shared prompts, and confirm before deleting forms.

Risk: Recurring polling can continue to fetch form status and results after the original workflow decision point.

Mitigation: Approve cron polling intentionally and remove polling jobs once responses are complete or the form expires.

Risk: Deleting a form permanently removes collected submissions and files.

Mitigation: Export or summarize required results before deletion and require explicit confirmation for destructive cleanup.

## Reference(s):

- [Let's Clarify homepage](https://letsclarify.ai)
- [Let's Clarify MCP endpoint](https://letsclarify.ai/mcp)
- [Extended Reference](artifact/REFERENCE.md)
- [ClawHub skill page](https://clawhub.ai/heisee/skills/letsclarify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, bash, and HTML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API or MCP request examples, form schema JSON, polling guidance, and result summaries.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
