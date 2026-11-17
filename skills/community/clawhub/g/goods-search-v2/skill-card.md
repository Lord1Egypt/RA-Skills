## Description:

Goods Search V2 helps agents handle shopping requests by choosing between Volcengine Viking AISearch chat search and direct product search, then formatting returned product results without inventing missing fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyantong429-coder](https://clawhub.ai/user/chenyantong429-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to support shopping search workflows, including product retrieval, conversational product search, product card generation, and structured product list summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API credentials and user query data to a configured remote host.

Mitigation: Use only trusted Volcengine HTTPS endpoints, restrict environment configuration changes, and review the configured API base before deployment.

Risk: Shopping requests may transmit user, session, location, image, or preference data to the remote search service.

Mitigation: Send only data approved for remote processing and avoid sensitive personal information unless that transmission is acceptable.

Risk: API keys may be exposed if supplied through command-line arguments or unmanaged local configuration.

Mitigation: Provide credentials through protected environment variables or secret management, and avoid passing API keys directly on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenyantong429-coder/skills/goods-search-v2)
- [ChatSearch API reference](references/chat_search_api.md)
- [Search API reference](references/search_api.md)
- [Volcengine ChatSearch API documentation](https://www.volcengine.com/docs/85296/1873492?lang=zh)
- [Volcengine Search API documentation](https://www.volcengine.com/docs/85296/1544974?lang=zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown product summaries, JSON API responses, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include returned product fields, request identifiers, citations, total item counts, spelling corrections, and omitted fields when source data is absent.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
