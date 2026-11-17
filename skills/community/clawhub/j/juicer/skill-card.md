## Description:

Connect Juicer to OpenClaw to gather public social posts, manage feeds and event walls, and track brand mentions, topics, and competitors across social networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juicer](https://clawhub.ai/user/juicer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media teams use Juicer to find public posts across supported networks, create embeddable feeds and event walls, and monitor brands, topics, and competitors. Before lookups, they can check account limits and credit costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email authorization shares the user's address with Juicer and may create an account and send confirmation email.

Mitigation: Choose the connection method deliberately and explain the email flow before requesting the user's address.

Risk: The connection can access the user's Juicer account, and API keys can expose that access if mishandled.

Mitigation: Review account permissions, store API keys in secrets, never print them or write them into files, and get explicit approval before destructive actions.

## Reference(s):

- [Juicer MCP server setup](https://developers.juicer.io/mcp-server)
- [Juicer developer documentation](https://developers.juicer.io)
- [Juicer developer portal](https://www.juicer.io/developer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with setup instructions, API examples, and social data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on connected account permissions, supported network search types, and available credits.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
