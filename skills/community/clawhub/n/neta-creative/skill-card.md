## Description:

Neta Creative helps agents use the Neta CLI to generate and edit images, videos, songs, and music videos, query character settings, and deconstruct existing works for creative remixing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huxiuhan](https://clawhub.ai/user/huxiuhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative agents use this skill to compose Neta CLI commands and prompts for multimedia generation, character-based creation, background removal, and creative remix workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, lyrics, image references, and collection references to external Neta services.

Mitigation: Avoid submitting private, confidential, or rights-restricted media and review service terms before use.

Risk: The skill depends on a NETA_TOKEN credential for Neta CLI access.

Mitigation: Store NETA_TOKEN in a secure environment variable or secret store and avoid exposing it in logs, prompts, or generated files.

Risk: The install examples use a mutable global package reference with @latest.

Mitigation: Prefer a pinned Neta CLI package version for reviewed or repeatable deployments.

Risk: Some character tag and browsing examples are outside the stated creative-generation scope.

Mitigation: Use this skill for creation workflows and route browsing, feed exploration, or tag research to the appropriate companion skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huxiuhan/skills/neta-creative)
- [Best Practices for Image Generation](references/image-generation.md)
- [Best Practices for Video Generation](references/video-generation.md)
- [Best Practices for Song Generation](references/song-creation.md)
- [Best Practices for Song MVs](references/song-mv.md)
- [Best Practices for Character Search](references/character-search.md)
- [Best Practices for Creative Remix](references/collection-remix.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and prompt guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Neta CLI commands that call external Neta services using user-provided prompts, lyrics, images, and collection identifiers.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
