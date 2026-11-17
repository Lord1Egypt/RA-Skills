## Description:

Helps manage App Store screenshots, preview videos, and creative assets through MetaRun and Apple's App Asset Library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iderasyh](https://clawhub.ai/user/iderasyh)

### License/Terms of Use:

MIT-0

## Use Case:

App developers and release managers use this skill to upload, place, reorder, and verify media across App Store listings, custom product pages, in-app events, and product page tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted CLI packages or MetaRun access could expose account credentials or App Store assets.

Mitigation: Trust the MetaRun and npm package sources, use only necessary App Store permissions, and prefer a vetted or pinned CLI version in sensitive environments.

Risk: Incorrect media placements or deletions could alter published app assets.

Mitigation: Review each preview before applying it, require user agreement before removing placements, and verify affected slots afterward.

## Reference(s):

- [MetaRun agents](https://metarun.dev/agents)
- [MetaRun: store media on ClawHub](https://clawhub.ai/iderasyh/skills/metarun-store-media)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows write previews before applying changes and reports final asset placements and states.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
