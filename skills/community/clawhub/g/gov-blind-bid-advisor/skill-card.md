## Description:

A Chinese-language government procurement bidding assistant that uses public procurement data and optional IMA retrieval to discover bid opportunities, rank them against an enterprise profile, and produce go/no-go bid decision and risk self-check reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement teams use this skill to find public Chinese government procurement opportunities, compare them with a local enterprise profile, and prepare bid decision, match ranking, and risk self-check reports for human review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security summary reports that the live web collector can escape its stated host boundary through redirects.

Mitigation: Review or harden redirect validation before enabling collection, and restrict network access to the approved ccgp.gov.cn host boundary.

Risk: The security guidance warns that some reference documentation describes broader external enterprise enrichment than the manifest grants.

Mitigation: Disable or require explicit approval for broader WebFetch-style external lookups unless the deployment policy grants those accesses.

Risk: Enterprise profiles and generated bid reports may contain sensitive business strategy or qualification details.

Mitigation: Keep profiles and reports in a dedicated local working directory and avoid sharing generated artifacts outside the intended review workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chesaram/skills/gov-blind-bid-advisor)
- [README](README.md)
- [Anti-Scraping Best Practices](references/anti-scraping-best-practices.md)
- [Bid Decision Rubric](references/bid-decision-rubric.md)
- [Category Codes](references/category-codes.md)
- [Compliance Guardrails](references/compliance-guardrails.md)
- [Enterprise Profiling](references/enterprise-profiling.md)
- [IMA Knowledge Bases](references/ima-knowledge-bases.md)
- [Procurement Platforms](references/procurement-platforms.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports, JSON analysis files, and concise text guidance with optional local script commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are decision-support artifacts only and should be reviewed by the user before bidding, complaint, or procurement actions.]

## Skill Version(s):

1.0.1 (source: frontmatter, manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
