## Description:

Use Qwen through an OOMOL-connected account for document analysis, image text extraction and translation, image generation, speech tasks, custom voice management, and text translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an OOMOL-connected Qwen account can use the skill to analyze documents, extract text from images, translate text or images, handle speech tasks, generate images, and manage custom voices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run a remotely downloaded installer, and the security scan could not determine what it does.

Mitigation: Review the install script and confirm its source is trusted before running it.

Risk: Prompts or other content sent to Qwen may include sensitive information handled by an external service.

Mitigation: Avoid sending sensitive content unless it is approved for use with the connected Qwen service.

Risk: Some actions create or delete Qwen data, including custom voices and asynchronous tasks.

Mitigation: Confirm the exact action, payload, and target before running write or destructive actions.

Risk: The security scan was partial because two local references could not be resolved, so its evidence is incomplete.

Mitigation: Resolve and review the missing references, then repeat the security review before relying on the assessment.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Qwen](https://qwen.ai/)
- [Qwen API documentation](https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api)

## Skill Output:

**Output Type(s):** [Text, Structured data, Images, Audio]

**Output Format:** [Qwen action results in text, JSON, image, or audio form, depending on the action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action; some operations submit asynchronous tasks or change Qwen data.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
