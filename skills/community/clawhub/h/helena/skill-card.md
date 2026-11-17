## Description:

Use Helena, Enrich Labs' AI marketing agent, to research, plan, create, schedule, publish, and analyze marketing for a connected brand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enrichlabs](https://clawhub.ai/user/enrichlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and agents use this skill to delegate connected-brand marketing research, planning, content creation, scheduling, publishing, and performance analysis to Helena through an Enrich Labs account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helena may operate on brand marketing data and connected marketing platforms.

Mitigation: Install and authorize the skill only for intended Enrich Labs accounts, review Helena's permissions, and avoid sharing unrelated secrets or private conversation history.

Risk: Ambiguous delegated requests could publish content, spend money, contact people, change campaigns, or delete data.

Mitigation: Clarify user intent before requesting live actions and preserve approval boundaries for planning, drafts, and analysis.

Risk: Credential handling could expose account secrets if handled in chat.

Mitigation: Use the OAuth browser flow or the documented safe code fallback and never ask users to paste passwords, OAuth codes, access tokens, or refresh tokens into chat.

## Reference(s):

- [Helena skill page](https://clawhub.ai/enrichlabs/skills/helena)
- [Enrich Labs MCP access](https://enrichlabs.ai/mcp)
- [Helena MCP endpoint](https://agent.enrichlabs.ai/api/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and delegated agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include returned links and image assets when Helena provides them]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
