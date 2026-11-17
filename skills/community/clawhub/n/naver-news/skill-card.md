## Description:

Search Korean news articles using Naver Search API. Use when searching for Korean news, getting latest news updates, finding news about specific topics, or preparing daily news summaries. Supports relevance and date-based sorting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steamb23](https://clawhub.ai/user/steamb23)

### License/Terms of Use:


## Use Case:

External users, developers, and OpenClaw agents use this skill to search, filter, and collect Korean news from Naver for daily summaries, topic monitoring, breaking-news alerts, and custom news feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Naver API credentials are sent to Naver when the skill is used.

Mitigation: Use the skill only when Naver news search is intended, store credentials in the configured environment variables, and avoid submitting sensitive search terms.

Risk: Automated daily-summary workflows may run repeatedly and update local timestamp state.

Mitigation: Enable scheduled workflows deliberately, review their state-file behavior, and monitor runs for expected frequency and scope.

Risk: News results can include external article links and API-provided snippets that may be incomplete or stale.

Mitigation: Have agents cite source links, verify important claims against the underlying article, and apply editorial review before publishing summaries.

## Reference(s):

- [Naver News Search API Reference](references/api.md)
- [Naver Search API News Documentation](https://developers.naver.com/docs/serviceapi/search/news/news.md)
- [Naver Developers](https://developers.naver.com/)
- [ClawHub Skill Page](https://clawhub.ai/steamb23/skills/naver-news)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or JSON search results, with Markdown guidance and shell or Python examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Naver API credentials in NAVER_CLIENT_ID and NAVER_CLIENT_SECRET; supports relevance or date sorting, pagination, time filtering, and a documented 25,000-call daily API limit.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
