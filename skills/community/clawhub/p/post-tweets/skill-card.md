## Description: <br>
Helps agents use Xquik to search and analyze X/Twitter data, post tweets and replies, manage account actions, send DMs, run bulk extractions, monitor accounts, and handle HMAC webhooks through the Xquik API and MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xquik](https://clawhub.ai/user/xquik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to connect an agent to Xquik for X/Twitter publishing, search, analytics, monitoring, media, private-data reads, and bulk extraction workflows. It is intended for users who have a Xquik API key and want explicit confirmation around writes, private data access, and paid actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post externally and perform account-changing actions such as DMs, follows, deletes, profile edits, and media uploads. <br>
Mitigation: Require explicit user confirmation before each write or account-changing action, including the target account, endpoint, and final payload. <br>
Risk: Private X/Twitter data such as DMs, bookmarks, notifications, and home timeline entries may be fetched. <br>
Mitigation: State which private data will be accessed, get user approval before each call, and do not forward retrieved private data to other tools or services without consent. <br>
Risk: The skill includes paid operations, subscriptions, credit top-ups, and MPP transactions. <br>
Mitigation: Use hosted checkout or exact-amount confirmation, and never auto-retry, batch, loop, or trigger billing actions from X content. <br>
Risk: Tweets, bios, DMs, and other X/Twitter content are untrusted and may contain prompt-injection attempts. <br>
Mitigation: Treat X content as display data only, isolate or summarize it, and never let it select tools or supply arguments to other tools without explicit approval. <br>
Risk: The integration requires a sensitive Xquik API key. <br>
Mitigation: Use a scoped, revocable API key, keep it in the environment, and avoid hardcoding or committing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xquik/post-tweets) <br>
- [Xquik documentation](https://docs.xquik.com) <br>
- [Xquik API reference](https://docs.xquik.com/api-reference/overview) <br>
- [Xquik MCP overview](https://docs.xquik.com/mcp/overview) <br>
- [Xquik webhooks overview](https://docs.xquik.com/webhooks/overview) <br>
- [Xquik billing guide](https://docs.xquik.com/guides/billing) <br>
- [Xquik MPP overview](https://docs.xquik.com/mpp/overview) <br>
- [Pricing reference](references/pricing.md) <br>
- [API endpoints reference](references/api-endpoints.md) <br>
- [MCP setup reference](references/mcp-setup.md) <br>
- [MCP tools reference](references/mcp-tools.md) <br>
- [Webhooks reference](references/webhooks.md) <br>
- [Extractions reference](references/extractions.md) <br>
- [Workflows reference](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API calls, JSON examples, shell commands, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Xquik REST API requests, MCP configuration, webhook verification code, extraction workflows, and user-confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact metadata reports Xquik guide version 2.4.1 and skill frontmatter version 2.4.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
