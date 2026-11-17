## Description:

Photo Editor helps agents create and edit multi-page image carousels and poster-style image assets from text prompts, optional reference images, templates, and design configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call a remote image generation workflow that produces editable photo posters, social-media carousel pages, and related image assets from prompts, uploaded images, sizing options, and style settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts, uploaded reference images, and design configuration are sent to named external services.

Mitigation: Use only content that is acceptable to send to those services, and review provider terms and data handling before use.

Risk: Generated sessions, share URLs, and remote image links may remain accessible outside the local agent environment.

Mitigation: Avoid sensitive content, inspect sharing behavior before distribution, and remove or expire remote sessions when the service supports it.

Risk: The artifact documents unpinned npx CLI execution while an API key is exported in the environment.

Mitigation: Prefer a pinned and reviewed CLI version or direct API call, use a least-privilege key, and rotate credentials after testing.

## Reference(s):

- [Photo Editor on ClawHub](https://clawhub.ai/ai-hub-admin/skills/photo-editor)
- [Craftsman Image Generator Console](https://craftsman-agent.aiagenta2z.com/app/image-generator)
- [Craftsman Gallery](https://craftsman-agent.aiagenta2z.com/gallery)
- [Craftsman Workspace](https://craftsman-agent.aiagenta2z.com/workspace)
- [DeepNLP Workspace Keys](https://deepnlp.org/workspace/keys)
- [OneKey Agent Router](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash, curl, CLI examples, JSON request examples, generated image URLs, share links, and editable layer data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DeepNLP OneKey access key and sends user prompts, optional images, and design configuration to external services.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
