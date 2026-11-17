## Description:

Screens medical-science literature by collecting paper evidence locally, submitting records for cloud screening, auditing results, and producing Excel review workbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ez-hq](https://clawhub.ai/user/ez-hq)

### License/Terms of Use:

MIT

## Use Case:

Medical-science researchers and review teams use the skill to gather and assess literature evidence, then organize screened papers into a Paper Sheet and Reading List. Cloud screening requires the separately installed LoomLoom CLI, a user-approved destination, and review of the quoted cost and transferred evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud screening sends paper evidence to a paid third-party service and incurs quoted costs.

Mitigation: Before each run, confirm the destination, transferred evidence, and quoted cost; minimize payload data and obtain explicit user approval.

Risk: An excluded-paper validation bug can block legitimate review deliverables.

Mitigation: Fix the validation bug before relying on complete results; do not omit excluded papers just to pass validation.

## Reference(s):

- [Project releases](https://github.com/ez-hq/literature-review-paper-screener/releases)
- [ClawHub listing](https://clawhub.ai/ez-hq/skills/literature-review-paper-screener)
- [Architecture reference](references/architecture.md)
- [Metadata validation gate](references/metadata-validation-gate.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Excel spreadsheets, Plain-language summaries]

**Output Format:** [Per-paper evidence records and Excel Paper Sheet and Reading List workbooks, with a short summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paper per evidence record; evidence availability levels A–D.]

## Skill Version(s):

1.5.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
