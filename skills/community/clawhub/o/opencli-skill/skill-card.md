## Description:

Use opencli CLI to interact with social and content websites such as Bilibili, Zhihu, Twitter/X, YouTube, Weibo, Xiaohongshu, V2EX, Reddit, HackerNews, Xueqiu, and BOSS Zhipin through the user's existing Chrome login session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronwang1980](https://clawhub.ai/user/aaronwang1980)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to browse, search, summarize, and perform selected account actions on supported social, news, job, and finance websites through opencli or browser automation backed by an already logged-in Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate websites using an already logged-in Chrome profile, exposing personal account state and private data to agent actions.

Mitigation: Use a separate Chrome profile or low-risk accounts, and review each requested site action before allowing the agent to proceed.

Risk: Write operations such as posts, replies, likes, deletes, direct messages, and check-ins can affect public or account-visible state.

Mitigation: Require explicit user confirmation with the exact target and content before any write operation is executed.

Risk: Mutable install commands such as npx or @latest can change behavior over time.

Mitigation: Prefer pinned package versions or a reviewed local installation before using the skill in higher-trust workflows.

## Reference(s):

- [opencli command reference](references/commands.md)
- [opencli upstream project](https://github.com/jackwener/opencli)
- [Playwright MCP Bridge extension](https://chromewebstore.google.com/detail/playwright-mcp-bridge/kldoghpdblpjbjeechcaoibpfbgfomkn)
- [ClawHub skill page](https://clawhub.ai/aaronwang1980/skills/opencli-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, command snippets, configuration guidance, and structured command-output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON, YAML, CSV, Markdown, or table-formatted data emitted by opencli commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
