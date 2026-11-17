## Description:

AI agent self-portrait generator that creates avatars, profile pictures, and visual identity assets using SkillBoss API Hub image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate personality-driven visual identity assets for AI agents, including avatars, banners, and full-body profile images. It supports mood, seasonal theme, and batch generation workflows for profile refreshes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance for updating public avatars and storing profile asset history.

Mitigation: Use the generator manually unless each avatar update is explicitly approved, and review generated images before publishing them to connected accounts.

Risk: Personality prompts and generated gallery captions may contain sensitive identity details or untrusted input.

Mitigation: Avoid secrets or sensitive identity data in personality prompts, and treat generated local gallery files as untrusted when personality input can come from others.

Risk: Installation and generation depend on an API key and an external image generation service.

Mitigation: Use pinned or verified install commands and provide SKILLBOSS_API_KEY only through the runtime environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/skills/modesty-agent-selfie)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance and CLI text; runtime output includes PNG image files and an optional HTML gallery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; supports avatar, banner, and full image formats with mood and theme presets.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
