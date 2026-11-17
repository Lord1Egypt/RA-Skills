## Description:

LiblibAI helps agents generate AI images through the LiblibAI API, with documented support for text-to-image, image-to-image, Ultra models, ComfyUI workflows, and file uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shishugen](https://clawhub.ai/user/shishugen)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and content creators use this skill to configure LiblibAI API credentials and run image generation, image transformation, file upload, and task-status workflows from an agent environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and user prompts or images can be sent to a custom API endpoint.

Mitigation: Use the official LiblibAI endpoint unless the alternative endpoint is trusted and controlled; rotate LiblibAI keys if they were used with an unknown mirror.

Risk: Uploaded images or prompts may contain sensitive or confidential content.

Mitigation: Avoid uploading sensitive images or confidential prompts and review content before submission.

Risk: The security verdict is suspicious because the skill can send credentials and content to an unvalidated custom endpoint.

Mitigation: Review the skill before installing and confirm endpoint configuration in the execution environment.

## Reference(s):

- [LiblibAI Website](https://liblibai.com)
- [LiblibAI API Documentation](https://liblibai.feishu.cn/wiki/UAMVw67NcifQHukf8fpccgS5n6d)
- [liblibai npm Package](https://www.npmjs.com/package/liblibai)
- [ClawHub Skill Page](https://clawhub.ai/shishugen/skills/liblibai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and CLI text output with image URLs, UUIDs, status, progress, and balance fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LiblibAI API credentials; may upload local files and send prompts or images to the configured API endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
