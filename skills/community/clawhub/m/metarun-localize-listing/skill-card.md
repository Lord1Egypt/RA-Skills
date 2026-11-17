## Description:

Helps localize and edit App Store listing text across languages, with the agent writing translations and MetaRun previewing and applying changes per locale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iderasyh](https://clawhub.ai/user/iderasyh)

### License/Terms of Use:

MIT-0

## Use Case:

App developers and listing managers use this skill to translate, review, and update App Store listing copy across locales through MetaRun.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translations or listing edits may be inaccurate, incomplete, or exceed field limits.

Mitigation: Review translated copy and previews, check field limits, and verify locale coverage after applying changes.

Risk: Promotional text on a live app can publish immediately.

Mitigation: Treat promotional-text changes as a publication and obtain explicit confirmation before applying them.

Risk: MetaRun can read and update listing metadata using account credentials; running an unpinned CLI package adds supply-chain exposure.

Mitigation: Limit access to intended listings and consider a pinned or preinstalled MetaRun CLI instead of fetching the latest package with npx.

## Reference(s):

- [MetaRun agents](https://metarun.dev/agents)
- [MetaRun: localize listing on ClawHub](https://clawhub.ai/iderasyh/skills/metarun-localize-listing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Localized listing copy and preview or apply summaries in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-locale copy is subject to App Store character limits and editability.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
