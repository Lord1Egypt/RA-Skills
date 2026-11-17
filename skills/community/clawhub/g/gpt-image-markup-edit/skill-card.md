## Description:

Markup-guided image edits with GPT Image 2.6 on varg: draw circles, boxes, arrows and short notes on a transparent PNG the same size as the source (scripts/markup.py turns a JSON list of shapes into that PNG, a preview and the prompt lines), upload it, then edit with provider_options.fal.markup_image_url and a prompt written per colour ("Red circle: … Blue circle: … Change nothing outside the marks."). Includes the measured example (two changes, the rest of the frame kept), how to check what changed, and when to use a black-and-white mask_url instead. Use when someone wants to change one or several specific spots in an image, says "circle it", "only change this part", "fix this word", "add a hat here", or an edit keeps changing things it should not. Not for whole-image restyles (gpt-image-2-6 recipes), animation (gpt-image-gif) or video edits (varg-ai).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to guide targeted edits to specific regions of an image with colored markup, then review the result and compare it with the original.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and prompts are sent to external services as part of an edit.

Mitigation: Review the provider and its data terms before uploading sensitive content; use non-sensitive images when unsure.

Risk: The documented installer is not pinned to a specific version.

Mitigation: Review the installation source and use a trusted, pinned release where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vargai/skills/gpt-image-markup-edit)
- [varg how-to](https://varg.ai/how-to)
- [OpenAI image generation guide](https://developers.openai.com/api/docs/guides/image-generation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Image files]

**Output Format:** [Markdown instructions with JSON examples, API call examples, and generated PNG markup, preview, or mask files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image outputs match the source dimensions; markup PNGs use a transparent background.]

## Skill Version(s):

1.0.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
