## Description:

Provides guidance for integrating Zhipu GLM-4.6V multimodal vision APIs for image understanding, document parsing, video understanding, and tool calling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isabellazhangym](https://clawhub.ai/user/isabellazhangym)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to connect agents to Zhipu GLM-4.6V for OCR, image understanding, long document analysis, and vision-related tool calling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, documents, or screenshots submitted through the skill may contain sensitive information and are sent to the Zhipu AI service.

Mitigation: Use the service only when acceptable for the data involved, and redact sensitive content before model submission.

Risk: The integration depends on a private API key for the Zhipu AI open platform.

Mitigation: Keep ZHIPUAI_API_KEY scoped and private, provide it only through the environment, and avoid hardcoding credentials.

Risk: Unpinned SDK installation can change behavior when zhipuai releases new versions.

Mitigation: Use a virtual environment and pin zhipuai to a reviewed version for production or controlled deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/isabellazhangym/skills/image-understanding)
- [BigModel open platform documentation](https://open.bigmodel.cn/)
- [BigModel vision MCP server documentation](https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ZHIPUAI_API_KEY environment variable and the zhipuai Python SDK.]

## Skill Version(s):

0.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
