## Description:

Analyzes portrait photos to recommend flattering hairstyles based on face shape, facial features, hair texture, current hair, and personal style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nellyxiaolong-cmyk](https://clawhub.ai/user/nellyxiaolong-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get personalized haircut and hairstyle recommendations from uploaded portrait or headshot photos, including practical instructions they can share with a stylist. The skill can also provide copy-ready prompts for generating hairstyle preview images when direct image generation is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded portraits and likeness-based hairstyle previews can expose sensitive personal image data.

Mitigation: Ask for user consent before generating or exporting preview prompts, disclose where images or prompts may be sent, and offer a recommendation-only path.

Risk: Face-shape, gender, age, or appearance analysis may be uncertain or feel overly personal.

Mitigation: State uncertainty when photo quality or visible features are insufficient and keep recommendations respectful, practical, and focused on styling outcomes.

## Reference(s):

- [Hairstyle Knowledge Reference](references/hairstyles.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown recommendation report with hairstyle rationale, stylist instructions, alternatives, and image-generation prompt blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return or request generation of hairstyle preview imagery when an image generation tool is available.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
