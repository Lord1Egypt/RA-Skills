## Description:

Fetches Chinese news channel lists and channel-specific news items from JisuAPI for topics such as headlines, finance, sports, entertainment, and technology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Chinese news channels and channel-specific article lists, then summarize titles, timestamps, sources, and links for news aggregation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News requests and the JISU_API_KEY are sent to JisuAPI.

Mitigation: Use only a JisuAPI app key intended for this third-party service and manage it as a revocable credential.

Risk: Returned news content comes from internet publishers and may have copyright or authorization requirements.

Mitigation: Review source links and obtain publisher authorization before redistributing full article content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-news)
- [JisuAPI News API documentation](https://www.jisuapi.com/api/news/)
- [JisuAPI provider website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses from a Python CLI, typically summarized by the agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the JISU_API_KEY environment variable, and network access to JisuAPI.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
