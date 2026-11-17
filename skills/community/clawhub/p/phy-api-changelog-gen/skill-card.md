## Description:

Generates human-readable changelogs, CI-oriented JSON, and migration guidance by semantically comparing OpenAPI 3.x or Swagger 2.0 API specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API maintainers use this skill to compare API specs before releases, identify breaking changes, and produce changelog or migration-guide text for docs, pull requests, and CI review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads specified local OpenAPI or Swagger files and may compare versions from git history.

Mitigation: Use explicit prompts and pass only the intended spec paths or git revisions.

Risk: Generated changelogs, JSON output, git comparison behavior, and deprecation handling may be incomplete or incorrect for a given API release.

Mitigation: Review outputs against representative specs before using the results in documentation or CI enforcement.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-api-changelog-gen)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown changelog, JSON for CI pipelines, and migration-guide prose with inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works from local YAML or JSON OpenAPI and Swagger specs, with optional git comparisons; no external API use is evidenced.]

## Skill Version(s):

1.0.3 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
