## Description:

Prompt-ZS helps agents generate Chinese-first prompts for AI image and video creation, including bilingual JSON prompt objects, tagged image prompts, concise video prompts, and direct translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn image, video, and translation requests into structured prompts for tools such as Midjourney, Stable Diffusion, Runway, and Pika. It is especially suited to Chinese-first workflows that may also need English prompt fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the skill to trigger for general image or video generation requests where users expect a different workflow.

Mitigation: Confirm that the request is for prompt generation, prompt optimization, image prompt writing, video prompt writing, or direct translation before applying the skill.

Risk: The skill commonly emits Chinese-first output with English fields, which may not match users who require strict single-language output.

Mitigation: Ask for or honor explicit language requirements when a user needs only Chinese, only English, or another locale-specific format.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/prompt-zs)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)
- [Text-to-video example](artifact/examples/video-text-example.md)
- [Image-to-video example](artifact/examples/video-image-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Chinese-first plain text, Markdown examples, and JSON prompt objects with cn, en, cn-tag, and en-tag fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video prompts are intended to be concise single paragraphs under 500 Chinese characters; JSON outputs should omit surrounding Markdown code fences.]

## Skill Version(s):

1.0.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
