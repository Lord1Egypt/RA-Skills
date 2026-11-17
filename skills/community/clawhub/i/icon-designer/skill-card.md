## Description:

Generates editable icon and poster-style image carousels through the Craftsman image_generator API using prompt, style, layout, and asset-size inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate icon, poster, and carousel image assets with configurable prompts, styles, asset sizes, and editable text/image layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference images, design configuration, and session details may be sent to the OneKey, DeepNLP, and Craftsman services.

Mitigation: Avoid confidential or proprietary inputs unless the service use is approved, and review applicable service terms before use.

Risk: The skill documents an unpinned npx onekey CLI path that uses an API key.

Mitigation: Prefer the documented curl/API path or a pinned and verified onekey CLI in a restricted environment, and protect the API key as a secret.

Risk: The referenced image-editing templates include watermark-removal behavior.

Mitigation: Use watermark-removal features only when the user has clear rights to modify the source image.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/icon-designer)
- [Craftsman Image Generator Console](https://craftsman-agent.aiagenta2z.com/app/image-generator)
- [DeepNLP OneKey Access Keys](https://deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with curl/npx command examples and JSON request/response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return share URLs, image URLs, editable layer data, and export options for generated visual assets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
