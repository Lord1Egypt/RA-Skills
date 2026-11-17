## Description:

Operate the Neonous AI agent platform to create agents, chat, manage tools, and run workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesterchou](https://clawhub.ai/user/chesterchou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer Neonous agents, chats, MCP servers, workflows, artifacts, notifications, Telegram integrations, working memory, and account usage from an agent-assisted interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can administer a Neonous account broadly, including operations that expose credentials, publish or delete data, change integrations, or affect billing-related workflows.

Mitigation: Install only when broad Neonous account administration is intended; use a scoped and revocable API key when available, prefer the web UI for secrets and billing, and require explicit confirmation before sharing, deleting, emptying trash, resetting memory, or adding MCP or Telegram integrations.

Risk: Commands depend on a caller-provided Neonous base URL and API key.

Mitigation: Verify NEONOUS_URL is the official trusted HTTPS Neonous endpoint before running commands and keep NEONOUS_API_KEY out of logs, transcripts, and shared files.

## Reference(s):

- [Neonous homepage](https://neonous-ai.com)
- [ClawHub Neonous skill page](https://clawhub.ai/chesterchou/skills/neonous)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEONOUS_API_KEY, NEONOUS_URL, curl, and jq.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
