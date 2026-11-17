## Description:

Openclaw Smart Search routes CLI search requests across Bailian MCP, Tavily, Serper, Exa, and Firecrawl, then merges the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdenny11gg](https://clawhub.ai/user/fdenny11gg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run command-line web searches that choose suitable search providers by language and intent, then merge and rank the returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential setup can persist the master key or provider credentials in local files or shell configuration.

Mitigation: Review setup steps before installing, avoid quick-config.sh, rotate any bundled or previously exposed provider credentials, and store OPENCLAW_MASTER_KEY in a restricted secret store or a 0600-only file.

Risk: Bailian setup configures an external mcporter/MCP tool that may persist beyond a single search run.

Mitigation: Review or pin the mcporter/MCP server version and configuration before enabling setup:bailian.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fdenny11gg/skills/openclaw-smart-search)
- [Publisher profile](https://clawhub.ai/user/fdenny11gg)
- [Node.js child process security guidance](https://nodejs.org/en/docs/guides/security/#child-processes)
- [OWASP injection prevention guidance](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)
- [Tavily](https://tavily.com/)
- [Serper](https://serper.dev/)
- [Exa](https://exa.ai/)
- [Firecrawl](https://www.firecrawl.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style CLI output with search results, setup guidance, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, mcporter for Bailian search, OPENCLAW_MASTER_KEY, and at least one configured provider API key.]

## Skill Version(s):

1.0.14 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
