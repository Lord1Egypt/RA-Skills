## Description:

惠迈智能搜索 helps agents use Tavily search, extract, research, and usage APIs for web results, targeted page extraction, citation-oriented research, and usage checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, external users, and agents use this skill to gather current web evidence, extract focused content from URLs, create Tavily research tasks, and return cited JSON results for downstream answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, research prompts, request IDs, and extraction URLs are sent to Tavily using the configured Tavily API key.

Mitigation: Avoid submitting secrets, private or internal URLs, regulated data, or proprietary context unless organizational policy permits Tavily for that data.

Risk: A leaked Tavily API key could expose account quota or enable unauthorized requests.

Mitigation: Store TAVILY_API_KEY in the environment or a secrets manager, never paste it into chat logs, and rotate or revoke the key if exposure is suspected.

Risk: Full raw page extraction can increase context size and accidental data exposure.

Mitigation: Prefer search followed by targeted extract requests with a query and limited chunks per source.

Risk: Redirect behavior needs review before high-trust production use.

Mitigation: Keep requests constrained to the Tavily API host and harden redirect handling as part of production deployment review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-tavily-search)
- [Tavily API](https://api.tavily.com)
- [Tavily Documentation Index](https://docs.tavily.com/llms.txt)
- [Tavily Search](references/search.md)
- [Tavily Extract](references/extract.md)
- [Create Research Task](references/research.md)
- [Get Research Task Status](references/research-get.md)
- [Streaming](references/research-streaming.md)
- [Usage](references/usage.md)
- [Best Practices for Search](references/bp-search.md)
- [Best Practices for Extract](references/bp-extract.md)
- [Best Practices for Research](references/bp-research.md)
- [API Key Management](references/bp-api-key-management.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash or curl commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON responses may include result URLs, extracted content, request IDs, citation formats, and usage data.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
