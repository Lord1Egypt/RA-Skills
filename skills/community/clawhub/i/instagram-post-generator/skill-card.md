## Description:

AI Instagram Post Generator generates editable, Instagram-ready posts and slides with AI-created content, captions, images, text blocks, storylines, and backgrounds, including knowledge cards, posters, movie introductions, and other export-ready layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to generate editable social media carousel posts, captions, images, and design layers through the OneKey Agent Gateway. It is suited for Instagram-ready knowledge cards, posters, and similar visual post formats that can be exported or shared from a generated workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded images, and design configuration are sent to external services.

Mitigation: Use the skill only with data approved for those services, and avoid sensitive or confidential inputs unless the service terms and controls meet your requirements.

Risk: One documented CLI path runs an unpinned npm package while using an API key.

Mitigation: Prefer the documented HTTPS API call, or pin and verify the CLI package before use; use a limited or disposable OneKey access key where possible.

Risk: Generated outputs can include shareable workspace and image URLs.

Mitigation: Review generated assets and links before distribution, and manage access or rotate generated links according to the hosting service controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/instagram-post-generator)
- [Craftsman Social Media Posts Generator](https://craftsman-agent.aiagenta2z.com/app/social-media-posts)
- [Craftsman Gallery](https://craftsman-agent.aiagenta2z.com/gallery)
- [OneKey Gateway Keys](https://deepnlp.org/workspace/keys)
- [OneKey Router API Endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration, JSON]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described service returns generated post metadata, editable layer data, image URLs, and shareable workspace URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
