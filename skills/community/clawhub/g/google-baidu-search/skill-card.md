## Description:

Automatically chooses Google or Baidu for web search based on query language and returns unified search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run web searches through Google Custom Search, Baidu Search, or an automatic engine selector for Chinese and international queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to external Google or Baidu services.

Mitigation: Avoid using this skill for secrets, regulated data, or sensitive business queries unless external disclosure is acceptable.

Risk: API keys may be exposed in error output.

Mitigation: Use restricted, low-quota API keys and review or fix error handling so credential-bearing URLs are not printed.

Risk: The skill requires provider API credentials and is subject to provider quotas and rate limits.

Mitigation: Configure only the required providers, monitor quota usage, and keep credentials in environment variables or a local .env file excluded from sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leohuang8688/skills/google-baidu-search)
- [Publisher profile](https://clawhub.ai/user/leohuang8688)
- [Google Custom Search documentation](https://cloud.google.com/custom-search/docs)
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
- [Baidu AI documentation](https://ai.baidu.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Formatted text or Markdown search results, plus Python and CLI usage examples in documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include title, URL, snippet, source, and engine fields when provider responses contain them.]

## Skill Version(s):

1.5.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
