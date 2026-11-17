## Description:

Generate, edit, and orchestrate LitMedia videos, images, talking avatars, character replacement, and audio from natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litmedia-ai](https://clawhub.ai/user/litmedia-ai)

### License/Terms of Use:

Apache 2.0

## Use Case:

External creators, marketers, educators, and developers use this skill to ask an agent to create or edit LitMedia media assets, including images, videos, talking avatars, character replacement, narration, and batch creative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account credentials and stores local LitMedia credentials.

Mitigation: Review before installation, avoid authentication in logged or shared consoles, and treat the local credentials file as sensitive.

Risk: Media generation workflows may upload identity media such as faces or voices to LitMedia.

Mitigation: Use only media the user is authorized to upload and generate from, especially for face and voice inputs.

Risk: Generation requests can consume paid LitMedia credits.

Mitigation: Confirm task parameters and expected cost before submitting generation tasks, and check credit balance when needed.

Risk: Server security review describes unsafe logging and overreaching agent instructions that need review.

Mitigation: Review and scan the skill before deployment, with specific attention to authentication output and user-facing instruction scope.

## Reference(s):

- [LitMedia AI Website](https://www.litmedia.ai)
- [ClawHub Skill Page](https://clawhub.ai/litmedia-ai/skills/litmedia)
- [AI Image Module](artifact/references/ai_image.md)
- [Auth Module](artifact/references/auth.md)
- [Avatar4 Module](artifact/references/avatar4.md)
- [Error Handling Guide](artifact/references/error_handling.md)
- [User Module](artifact/references/user.md)
- [Video Generation Module](artifact/references/video_gen.md)
- [Character Replace Module](artifact/references/video_mimic.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown replies with generated media links, files, or concise next-step guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation can upload local media inputs, consume LitMedia credits, and return image, video, audio, or avatar outputs.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
