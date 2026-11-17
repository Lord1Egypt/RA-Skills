## Description:

Helps agents query Google Ads campaigns, ad groups, keywords, and performance metrics through a user-authorized connection, with optional approved changes and automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers, marketing teams, and developers use this skill to inspect Google Ads account performance and, with explicit approval, manage campaigns or set up related automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign changes can alter ad spend or published content.

Mitigation: Start with read-only queries and confirm the target account, exact change, and intended effect before any write.

Risk: Connecting an account grants access to Google Ads business data.

Mitigation: Obtain explicit approval for each connection, request only necessary access, and avoid exposing sensitive query results.

Risk: Trigger destinations can forward events persistently to external hosts.

Mitigation: Approve each destination separately and use only hosts the user explicitly trusts.

Risk: Raw API keys can leak through logs, shell history, or stored files.

Mitigation: Prefer the CLI OAuth flow and never print, persist, or include credentials in commands or output.

## Reference(s):

- [Google Ads skill release](https://clawhub.ai/byungkyu/skills/google-ads-api)
- [Google Ads API overview](https://developers.google.com/google-ads/api/docs/start)
- [Google Ads Query Language reference](https://developers.google.com/google-ads/api/docs/query/overview)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and query examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Google Ads query results and proposed changes; changes require user approval.]

## Skill Version(s):

1.2.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
