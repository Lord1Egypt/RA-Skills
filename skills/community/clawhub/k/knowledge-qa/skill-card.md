## Description:

Helps an agent create, index, query, and manage document knowledge bases using PDF, Markdown, and Word files with Alibaba Cloud DashVector retrieval and Bailian embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18874771327](https://clawhub.ai/user/18874771327)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to initialize local document knowledge bases, upload and index source documents, query one or more partitions, and generate Markdown reports or mind maps from retrieved content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents, user questions, and generated embeddings can be sent to Alibaba Cloud services through configurable DashVector and Bailian endpoints.

Mitigation: Use a dedicated low-privilege DashVector/Bailian key, verify the DashVector endpoint before each knowledge base is used, and avoid confidential or regulated documents unless approved.

Risk: API keys and query results are stored in local configuration and output files.

Mitigation: Inspect and clear generated config.json and scripts/query_result.json files after use, and rotate credentials if they may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18874771327/skills/knowledge-qa)
- [DashVector console](https://dashvector.console.aliyun.com)
- [DashVector API key page](https://dashvector.console.aliyun.com/api-key)
- [Bailian console](https://bailian.console.aliyun.com)
- [Bailian API key page](https://bailian.console.aliyun.com/api-key)
- [DashScope embeddings endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, generated report files, and HTML mind map files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update knowledge-base folders, config.json, indexed_files.json, reports, mind maps, and query_result.json in the user's workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
