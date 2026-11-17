## Description:

Drafts a slide-by-slide narration script and shot plan locally, then uses OnePress to render a narrated deck or topic as an MP4 after user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getonepress](https://clawhub.ai/user/getonepress)

### License/Terms of Use:

MIT

## Use Case:

Creators and teams use this skill to plan narration for a slide deck or explainer topic, review the script and shot plan, and optionally produce a narrated MP4 through OnePress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A deck, narration plan, and optional voice sample are sent to OnePress for cloud rendering.

Mitigation: Send only material approved for upload; review the local narration plan before connecting or rendering.

Risk: A OnePress API key grants access to the connected account.

Mitigation: Use browser pairing or a scoped key, keep ONEPRESS_API_KEY in a secret or environment store, and revoke it when no longer needed.

## Reference(s):

- [OnePress Deck Video on ClawHub](https://clawhub.ai/getonepress/skills/onepress-deck-video)
- [OnePress](https://www.getonepress.com)

## Skill Output:

**Output Type(s):** [Markdown, Video file]

**Output Format:** [Markdown narration plan and MP4 video]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The plan includes per-slide narration, timing, and shot notes; rendering requires user approval and a OnePress connection.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
