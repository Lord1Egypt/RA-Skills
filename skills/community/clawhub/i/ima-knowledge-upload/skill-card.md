## Description:

上传Markdown文件到IMA知识库的标准流程，支持通过笔记导入添加Markdown内容，也支持通过媒体上传添加PDF、Word等文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to upload Markdown reports, notes, and other files to IMA knowledge bases while following the required title, file name, and knowledge-base ID rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Method B may expose cloud credentials if real COS secrets are pasted into command lines or shared agent transcripts.

Mitigation: Use short-lived, least-privilege credentials through environment variables or a protected credential provider.

Risk: Files can be uploaded to the wrong IMA knowledge base if the knowledge-base ID is incorrect.

Mitigation: Verify the target knowledge-base ID before uploading and stop the workflow if upload or preflight checks fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meta-evo-creator/skills/ima-knowledge-upload)
- [Publisher profile](https://clawhub.ai/user/meta-evo-creator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY environment variables for IMA API access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
