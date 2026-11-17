## Description:

Yuan Dian (open.chineselaw.com). Use this skill for ANY Yuan Dian request — searching and reading data. Whenever a task involves Yuan Dian, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Legal researchers, lawyers, and business analysts use this skill to search Chinese laws and cases, retrieve legal and enterprise records, and check legal text for potentially inconsistent citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run an unverified remote installer automatically.

Mitigation: Review and install the oo CLI yourself; prevent automatic execution of its download-and-run fallback. Review the CLI's bundled-skill installation behavior and restrict it to intended agent hosts.

Risk: Queries and submitted legal text pass through OOMOL to Yuan Dian.

Mitigation: Avoid sending unnecessary confidential information.

## Reference(s):

- [Yuan Dian](https://open.chineselaw.com)
- [Yuan Dian API documentation](https://open.chineselaw.com/api-square/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured JSON results and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested action and available Yuan Dian data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
