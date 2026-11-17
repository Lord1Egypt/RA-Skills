## Description:

Luma AI video-generation assistant for Dream Machine text-to-video, image-to-video, and prompt technique guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft Luma Dream Machine prompts, understand text-to-video and image-to-video workflows, and adapt the included API example for video-generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded images or references, authentication headers, and generated asset metadata may be sent to Luma's external service.

Mitigation: Use environment variables or a secret manager for API keys, avoid sensitive or regulated content unless approved, and review Luma's terms and privacy practices before use.

Risk: The skill includes an API example that could lead users to place credentials directly in code.

Mitigation: Replace placeholder tokens with secrets loaded from approved storage and review code snippets before execution.

## Reference(s):

- [Luma Dream Machine Generations API endpoint](https://api.lumalabs.ai/dream-machine/v1/generations)
- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/luma-ai)
- [Publisher profile](https://clawhub.ai/user/zhangifonly)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, API Calls]

**Output Format:** [Markdown with prompt examples, comparison tables, and Python API sample code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated prompts, camera-language guidance, best practices, and API request examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
