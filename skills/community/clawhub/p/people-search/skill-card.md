## Description:

Search, qualify, and enrich people and companies for professional discovery, recruiting, B2B lead generation, contact lookup, company research, and background web research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lessieai](https://clawhub.ai/user/lessieai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, recruiters, and business researchers use this skill to find and enrich professional contacts, source candidates, generate lead lists, and research companies. It guides agents through Lessie CLI or MCP workflows while prompting before credit-consuming actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send search terms, company data, social handles, and contact identifiers to Lessie.

Mitigation: Use it only with data that may be shared with Lessie under the account's privacy, security, and compliance requirements.

Risk: The setup flow asks agents to install unpinned npm packages and may persist CLI tokens or MCP configuration.

Mitigation: Prefer pinned or manually reviewed package installation, inspect MCP configuration before enabling it, and remove cached credentials when the skill is no longer needed.

Risk: Credit-consuming Lessie calls can incur cost and retrieve personal contact data.

Mitigation: Require explicit user confirmation before each credit-consuming action unless the user has waived prompts, and apply local laws and platform terms before using retrieved contact data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lessieai/skills/people-search)
- [CLI Tool Calling Reference](references/cli-reference.md)
- [Domain Resolution](references/domain-resolution.md)
- [Workflow Patterns](references/workflow-patterns.md)
- [Lessie pricing](https://lessie.ai/pricing)
- [Lessie privacy policy](https://lessie.ai/privacy)
- [Lessie terms of service](https://lessie.ai/terms-of-service)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Lessie CLI commands, MCP configuration snippets, search criteria, result triage, and credit usage summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata lists 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
