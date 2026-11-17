## Description:

Share real-time organizational context with your AI agent by querying a context graph, managing records, and receiving live insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[najmuzzaman-mohammad](https://clawhub.ai/user/najmuzzaman-mohammad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using OpenClaw agents can connect to Nex to query organizational context, process conversations into records and insights, and manage CRM-like objects, records, relationships, tasks, notes, and lists through the Nex Developer API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent authenticated ability to change or delete CRM and context-graph data.

Mitigation: Use narrowly scoped API keys and require manual confirmation before DELETE, PATCH, PUT, or POST operations that change important data.

Risk: Over-broad API scopes can increase the impact of unintended or unauthorized agent actions.

Mitigation: Grant only the scopes needed for the intended workflow and avoid schema or delete scopes unless they are explicitly required.

Risk: Conversation transcripts and organizational context sent through the API may contain confidential or regulated data.

Mitigation: Do not submit confidential transcripts or regulated data without organizational approval.

## Reference(s):

- [Nex ClawHub Skill](https://clawhub.ai/najmuzzaman-mohammad/skills/nex)
- [Nex Skill Homepage](https://github.com/nex-crm/nex-as-a-skill)
- [Nex Developer Settings](https://app.nex.ai/settings/developer)
- [Nex API Documentation](https://docs.nex.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEX_API_KEY. API calls may read, modify, or delete Nex workspace data depending on the API key scopes granted.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
