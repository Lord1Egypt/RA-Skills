## Description:

Front door for Pipaclaw public skills. Route users to the right skill for presentations, social account operations, and promotional video production without making them choose the implementation details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xexojay](https://clawhub.ai/user/xexojay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this hub to route requests into the appropriate public Pipaclaw skill for presentation creation, social account operations, or promotional video production. It helps users start from the desired outcome rather than choosing implementation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The promo-video workflow may create cloud project state, generate workspace links, and store a reusable API key on disk.

Mitigation: Review the promo-video workflow before installation and use it only where persistent cloud project state and local credential storage are acceptable.

Risk: A configurable Maliang/Nano API base URL could send credentials or requests to an untrusted origin if environment variables are controlled by an untrusted shell or wrapper.

Mitigation: Use trusted environment settings for PROMO_VIDEO_MAKER_BASE_URL and MALIANG_HUB_BASE_URL, and avoid running helper scripts in environments that can override those values unexpectedly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xexojay/skills/pipaclaw-skills-hub)
- [Routing Map](references/routing-map.md)
- [PPT Maker workflow](ppt-maker/SKILL.md)
- [Promo Video Maker workflow](promo-video-maker/SKILL.md)
- [Social Account Ops workflow](social-account-ops/SKILL.md)
- [Promo Video Maker project access reference](promo-video-maker/references/project-access.md)
- [Promo Video Maker pricing and approval reference](promo-video-maker/references/pricing-and-approval.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell commands, configuration snippets, project links, and file-oriented delivery notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes to public skill workflows for decks, social operations, and video production; video workflows may include quote, task status, generated assets, or workspace access.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
