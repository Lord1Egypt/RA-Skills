## Description:

Searches for and verifies enterprise annuity information about organizations, then produces a standardized investigation report with source links, confidence labels, and error checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanwenzhe](https://clawhub.ai/user/yanwenzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to investigate whether organizations have enterprise annuity arrangements, collect supporting web evidence, and generate standardized markdown reports for review. It is designed for evidence-gathering and reporting, not authoritative benefits determination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the scripts search and report on occupational annuity despite the skill claiming an enterprise-annuity-only scope.

Mitigation: Review and fix the scripts before relying on the enterprise-annuity-only claim; treat occupational-annuity results as out of scope unless explicitly intended.

Risk: Organization names and pension-related queries may be sent to Tavily and public search engines.

Mitigation: Use only queries appropriate for external search, avoid sensitive personnel or benefits data, and review generated source links before sharing reports.

Risk: The security review flags Tavily credential handling as something users should review.

Mitigation: Use a limited Tavily key, avoid shared machines, do not commit key files, and rotate credentials after testing or batch runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanwenzhe/skills/pension-search-pro)
- [Publisher profile](https://clawhub.ai/user/yanwenzhe)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown investigation report with source links, confidence labels, summary tables, and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Tavily and public search engines; batch mode writes per-organization markdown reports and a summary.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter; artifact _meta.json and body also mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
