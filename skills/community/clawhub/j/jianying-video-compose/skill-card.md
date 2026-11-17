## Description:

Jianying Video Compose helps agents prepare automated video-composition workflows using Jianying/CapCut proxy APIs for draft creation, media placement, subtitles, effects, cloud rendering, and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2719040953](https://clawhub.ai/user/2719040953)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation teams use this skill to guide agents through batch video generation, short-video synthesis, dynamic subtitle placement, and export setup with documented Jianying/CapCut proxy API payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends media to external UAT cloud services that evidence identifies as unauthenticated.

Mitigation: Use only approved, non-sensitive media until the service owner confirms authorization, access controls, retention and deletion rules, and quotas.

Risk: The artifact documents plaintext HTTP asset URLs for media download paths.

Mitigation: Require HTTPS-only asset delivery or treat generated and uploaded media links as unsuitable for proprietary, personal, regulated, or confidential content.

## Reference(s):

- [Jianying API parameter reference](references/api_reference.md)
- [ClawHub skill page](https://clawhub.ai/2719040953/skills/jianying-video-compose)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with HTTP endpoint examples and JSON payload snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides API-based video composition and export; it does not itself render media locally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
