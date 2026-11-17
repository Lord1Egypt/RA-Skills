## Description:

Helps home buyers assess listings against their needs, verify available market evidence, compare properties, and prepare decision reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohwald](https://clawhub.ai/user/ohwald)

### License/Terms of Use:

MIT-0

## Use Case:

Home buyers and their agents use this skill to clarify priorities, screen and compare listings, examine available price and policy evidence, and document viewing, negotiation, and contract considerations.

### Deployment Geography for Use:

China, supported European markets, Hong Kong (China), Singapore, and Japan

## Known Risks and Mitigations:

Risk: Locally saved buyer profiles and property history can contain sensitive financial, household, and eligibility details.

Mitigation: Restrict access to saved profiles and history; remove config/profile.yml, modes/_profile.md, reports/, and data/ when no longer needed.

Risk: Shared reports and maps may reveal personal preferences and listing history.

Mitigation: Review and remove sensitive profile and listing information before sharing reports or data/map.html.

## Reference(s):

- [ClawHub house-ops release](https://clawhub.ai/ohwald/skills/house-ops)
- [European market coverage](artifact/docs/markets/eu.md)
- [Asia-Pacific market coverage](artifact/docs/markets/apac.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown reports, JSON data, HTML maps]

**Output Format:** [Text guidance, Markdown reports, structured scan data, and local HTML maps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reported figures identify their evidence level; unverified listings are not treated as valid assessments.]

## Skill Version(s):

1.0.8 (source: ClawHub release evidence; bundled package.json: 0.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
