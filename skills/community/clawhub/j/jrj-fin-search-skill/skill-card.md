## Description:

Searches Chinese A-share financial news and research-report summaries by keyword, source, and time range so agents can retrieve current market, company, and industry information.

This skill is for research and development only.

## Publisher:

[haomanjia](https://clawhub.ai/user/haomanjia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search JRJ-backed A-share news and research-report summaries before answering finance, stock, market-event, or industry-research questions. It supports company tracking, industry monitoring, event review, source checking, and finance recap workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has an undocumented endpoint override that can send the API key and search terms to an arbitrary or unencrypted server.

Mitigation: Keep JRJ_API_URL unset unless the endpoint is fully controlled, require HTTPS, store JRJ_API_KEY as a secret, and rotate the key if it was used with an untrusted or plaintext endpoint.

Risk: Financial news and research-report summaries may be incomplete, time-sensitive, or unsuitable as investment advice.

Mitigation: Treat outputs as informational, verify cited source links and dates, and require independent judgment before financial decisions.

## Reference(s):

- [API 接口参考](references/api-reference.md)
- [JRJ Claw homepage](https://ai.jrj.com.cn/claw)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration instructions, API Calls]

**Output Format:** [JSON or Markdown search results from a Node.js command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JRJ_API_KEY. Results may be truncated and can include titles, dates, sources, links, summaries, organizations, and abstracts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
