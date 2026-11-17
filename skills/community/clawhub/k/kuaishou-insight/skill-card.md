## Description:

Analyzes public Kuaishou videos, creator posts, and comments through keyword, profile, and video-link queries, returning structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Kuaishou creators, brand teams, and market analysts use the skill to research content topics, review public competitor posts, and examine video comments and engagement data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords or links submitted for queries may be sent to guaikei.com; the security scan also reports that some scripts were only partially interpreted.

Mitigation: Use only non-confidential keywords and public links, and review the source before installation if the data sharing or incomplete scan coverage is a concern.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/kuaishou-insight)
- [Guaikei service and token access](https://www.guaikei.com)
- [CLI options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON containing public video, creator, or comment data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the GUAIKEI_API_TOKEN plan and applicable query limits.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
