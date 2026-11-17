## Description:

Connect to Meegle via MCP service, support OAuth authentication, and enable querying and managing work items, views, etc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wadxm](https://clawhub.ai/user/wadxm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate with Meegle and query, create, modify, or transfer Meegle work items through an MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credential material may be exposed to the agent during the remote OAuth flow.

Mitigation: Prefer browser OAuth, avoid pasting credential files into an agent conversation, and store credentials only at ~/.mcporter/credentials.json.

Risk: The npm tool is invoked without a pinned package version, so behavior can change after review.

Mitigation: Pin and verify the @lark-project/meego-mcporter package version before installation or execution.

Risk: Meegle access may allow querying or changing work items.

Mitigation: Grant only the Meegle permissions required for the intended task and confirm credential operations step by step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wadxm/skills/meegle-connector)
- [npm package: @lark-project/meego-mcporter](https://www.npmjs.com/package/@lark-project/meego-mcporter)
- [Meegle OAuth help center](https://meegle.com/b/helpcenter/product/5rifl7a7)
- [Meegle MCP server endpoint](https://meegle.com/mcp_server/v1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npx, OAuth confirmation, and credentials stored at ~/.mcporter/credentials.json.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
