## Description: <br>
本地知识库智能问答 helps an agent create, index, partition, and query user document knowledge bases backed by Alibaba Cloud DashVector and Bailian embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18874771327](https://clawhub.ai/user/18874771327) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, educators, and knowledge workers use this skill to maintain multiple document knowledge bases, upload PDF/Markdown/Word files for vector indexing, retrieve answers by knowledge base or partition, and produce Markdown reports or mind maps from retrieved context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected source documents and user questions are sent to Alibaba Cloud DashVector/Bailian during indexing and retrieval. <br>
Mitigation: Use the skill only for documents approved for that cloud processing path, and avoid confidential or regulated material unless organizational policy permits it. <br>
Risk: The skill requires API credentials stored in the knowledge base config.json file. <br>
Mitigation: Use a dedicated low-privilege API key, keep config.json private, and rotate credentials if the workspace is shared or exposed. <br>
Risk: Automatic knowledge-base discovery can select the first matching workspace when --kb-path is omitted. <br>
Mitigation: Specify --kb-path explicitly when indexing or querying to reduce accidental use of the wrong knowledge base. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18874771327/knowledge-qa) <br>
- [DashVector console](https://dashvector.console.aliyun.com) <br>
- [Bailian console](https://bailian.console.aliyun.com) <br>
- [DashScope embeddings endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown guidance with shell commands; generated knowledge-base folders, JSON configuration/status files, Markdown reports, and HTML mind maps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+ dependencies and Alibaba Cloud DashVector/Bailian credentials configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
