## Description:

Generates poetic minimal zine-style poster prompts and matching raster images from a theme, sentence, object, mood, article idea, photo, or content brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chugenice](https://clawhub.ai/user/chugenice)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative practitioners use this skill to turn prompts or reference material into quiet Japanese/Korean zine-like editorial poster concepts, final image-generation prompts, and generated bitmap poster images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad creative triggers for poster and editorial-design prompts, so it may activate when a user only wanted design advice.

Mitigation: Review trigger behavior before deployment and ask the agent to confirm whether the user wants image generation when intent is ambiguous.

Risk: The skill calls ImageGen and image generation consumes credits.

Mitigation: Keep the existing user notice before ImageGen calls and allow prompt-only output when the user explicitly requests it.

## Reference(s):

- [Visual Rules - Minimal Zine Poster](references/visual-rules.md)
- [ClawHub skill page](https://clawhub.ai/chugenice/skills/minimalist-poster-prompt)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown containing a generated image reference, final image-generation prompt, and recipe summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ImageGen to produce a bitmap image after notifying the user that image generation consumes credits.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
