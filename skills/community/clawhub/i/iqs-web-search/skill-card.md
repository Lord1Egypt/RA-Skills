## Description:

Provides real-time web search through Alibaba Cloud IQS for agents that need current web results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mickemin](https://clawhub.ai/user/mickemin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to retrieve current web search results, news, documents, and page summaries through Alibaba Cloud IQS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and returned content are sent to and received from Alibaba Cloud IQS.

Mitigation: Avoid submitting secrets, personal data, or confidential business text in search queries.

Risk: The skill requires an Alibaba Cloud API key in the TONGXIAO_API_KEY environment variable.

Mitigation: Use a credential manager or temporary environment variable instead of storing the API key in shell startup files.

Risk: Web search output may include incomplete, outdated, or misleading third-party content.

Mitigation: Review and corroborate search results before using them in decisions or generated artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mickemin/skills/iqs-web-search)
- [Alibaba Cloud IQS API Key Console](https://ipaas.console.aliyun.com/api-key)
- [Alibaba Cloud IQS HTTP Search API](https://help.aliyun.com/zh/document_detail/2871439.html)
- [Alibaba Cloud IQS Credentials Documentation](https://help.aliyun.com/zh/document_detail/2872258.html)
- [Alibaba Cloud IQS Latency and Quota Documentation](https://help.aliyun.com/zh/document_detail/2870259.html)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text search results with titles, links, summaries, and page text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, network access to Alibaba Cloud IQS, and TONGXIAO_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
