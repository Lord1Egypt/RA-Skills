## Description:

Analyzes images, videos, and documents with the GLM-4.6V multimodal model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tridefender](https://clawhub.ai/user/tridefender)

### License/Terms of Use:

MIT

## Use Case:

Developers and end users use this skill to send authorized images, video URLs, and documents to GLM-4.6V for OCR, scene and object analysis, video summarization, keyframe analysis, and document parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool handler can turn user-supplied input into shell command execution.

Mitigation: Review before installing and avoid passing untrusted filenames, URLs, or prompts until the handler uses argument-array execution or equivalent escaping and validation.

Risk: The skill uploads local media and documents to an external Zhipu/GLM API.

Mitigation: Use only non-sensitive media or documents that the user is authorized to send to Zhipu/GLM.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tridefender/skills/multimodal)
- [Zhipu GLM chat completions API endpoint](https://open.bigmodel.cn/api/paas/v4/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text analysis returned by the GLM API, with optional streamed text output from the command-line script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one modality at a time and uses ZHIPU_API_KEY for API access.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
