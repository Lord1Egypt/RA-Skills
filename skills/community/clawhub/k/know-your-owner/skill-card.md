## Description:

Collects data from logged-in Douyin, Xiaohongshu, Weibo, Douban, and Bilibili accounts, cross-analyzes it into a personal profile, and generates USER.md and MEMORY.md for onboarding and personalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophie-xin9](https://clawhub.ai/user/sophie-xin9)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill during onboarding or personalization setup to build local user context from the user's own logged-in social-platform data. It can also support personal data review tasks such as exporting platform lists, refreshing a profile, or reusing collected platform JSON files for later analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses logged-in browser sessions to read broad social-platform profile, activity, favorites, follows, ratings, and comment data.

Mitigation: Run it only after explicit user consent, keep unrelated browser work closed, and limit collection to platforms the user has selected.

Risk: The skill stores raw collected profile data locally in know-your-owner-data files.

Mitigation: Review USER.md, MEMORY.md, and know-your-owner-data after generation, then delete any raw platform JSON or profile content the user does not want retained.

Risk: The skill can auto-install a mutable ManoBrowser dependency for browser automation.

Mitigation: Prefer a pinned and reviewed ManoBrowser version before use, and inspect the dependency before allowing browser-control workflows.

Risk: The bundled workflows include broad browser automation actions.

Mitigation: Review workflow behavior before execution and use a constrained browser profile when collecting sensitive social-account data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sophie-xin9/skills/know-your-owner)
- [ManoBrowser Dependency](https://github.com/ClawCap/ManoBrowser)
- [Artifact README](artifact/README.md)
- [Primary Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, JSON, Guidance]

**Output Format:** [Markdown profile files plus local JSON data files and agent-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces USER.md, MEMORY.md, and know-your-owner-data/*.json after user review and confirmation.]

## Skill Version(s):

2.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
