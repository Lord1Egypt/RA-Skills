## Description:

Provides OECD statistical dataset discovery, metadata lookup, indicator search, data querying, and Data Explorer URL generation for agents and chatbots through an SDMX-oriented MCP-style service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent builders use this skill to search OECD datasets, inspect dataset structures, retrieve bounded statistical observations, and provide OECD Data Explorer links in assistant responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes OECD-style queries and the user's XiaoBenYang API key through a private XiaoBenYang service.

Mitigation: Use a narrowly scoped, revocable XiaoBenYang API key and assume query contents and the key are visible to that service.

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Avoid installing it where plaintext .env credentials could be indexed, backed up, committed, or shared.

Risk: The security verdict is suspicious because the skill presents as an OECD data helper while relying on a private proxy service.

Mitigation: Review the skill before installing and prefer a version that directly uses official OECD endpoints or clearly documents proxy, retention, and credential storage behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/oecd-search)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Configuration guidance]

**Output Format:** [Markdown summaries of JSON API results, dataset metadata, statistical observations, status messages, and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query data defaults to bounded observation output and should use filters, time periods, or observation limits for large datasets.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
