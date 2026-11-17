## Description:

Generate and edit images with OpenAI GPT Image 2.5 through the PopNow API, with a cost quote before generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyuminjo](https://clawhub.ai/user/kyuminjo)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and creative users use this skill to generate images from text or edit reference images through PopNow, reviewing an exact cost quote before creating each image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, text, and reference media URLs are sent to PopNow and the generation provider; command arguments may also remain in host logs.

Mitigation: Avoid sensitive prompts and reference images, and keep API keys in secret or environment settings rather than command arguments.

Risk: Image generation uses a prepaid API balance and can incur charges.

Mitigation: Use a dedicated key with spending and model restrictions, review the exact quote, and approve the quoted maximum cost before creating a task.

## Reference(s):

- [GPT Image 2.5 model page](https://popnow.ai/models/gpt-image-2-5-sunburst)
- [PopNow task API documentation](https://popnow.ai/docs/tasks)

## Skill Output:

**Output Type(s):** [Generated images, Image links, Usage guidance]

**Output Format:** [Generated image outputs are returned as links; guidance is provided in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-image generation and image editing, with output up to 4K as described in the skill.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
