## Description: <br>
Calls Alibaba Cloud IQS over HTTP to retrieve current web search results for agents that need online information retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mickemin](https://clawhub.ai/user/mickemin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent run Alibaba Cloud IQS web searches and summarize current search results, news, and technical information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and returned content are transmitted through Alibaba Cloud IQS. <br>
Mitigation: Avoid sending secrets, internal text, or private data in search queries. <br>
Risk: The skill requires an Alibaba Cloud IQS API key. <br>
Mitigation: Use a dedicated key with limited quota where possible and avoid storing it in shell profile files on shared machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mickemin/iqs-web-search) <br>
- [Aliyun IQS API key console](https://ipaas.console.aliyun.com/api-key) <br>
- [Aliyun search HTTP API documentation](https://help.aliyun.com/zh/document_detail/2871439.html) <br>
- [Aliyun credential documentation](https://help.aliyun.com/zh/document_detail/2872258.html) <br>
- [Aliyun response time and quota documentation](https://help.aliyun.com/zh/document_detail/2870259.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like search result text emitted by a shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and TONGXIAO_API_KEY; sends search queries to Alibaba Cloud IQS.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
