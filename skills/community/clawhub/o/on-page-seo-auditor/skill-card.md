## Description:

Audits single-page on-page SEO signals including title tags, meta descriptions, header structure, keyword placement, links, images, and page-level tags, then returns scored findings and prioritized fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, SEO practitioners, and content teams use this skill to audit a page or small batch of pages for on-page SEO health and diagnose likely structural contributors to ranking drops. It produces scored evidence, priority fixes, quick wins, and a handoff summary for follow-up optimization work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce broader SEO conclusions than a strict on-page audit, including E-E-A-T, accessibility, Core Web Vitals, indexing, or bulk-site findings.

Mitigation: Treat those areas as preliminary signals and confirm them with specialized quality, technical SEO, accessibility, performance, or indexing tools before acting.

Risk: Some metrics may be unavailable from fetched page content and therefore estimated by the agent.

Mitigation: Require the audit to label each metric as measured, user-provided, estimated, or N/A, and avoid treating estimated values as measured evidence.

## Reference(s):

- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [On Page Seo Auditor on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/on-page-seo-auditor)
- [Audit Example & Checklists](references/audit-example.md)
- [Audit Templates](references/audit-templates.md)
- [Bulk Audit Playbook](references/bulk-audit-playbook.md)
- [Scoring Rubric](references/scoring-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with scored tables, prioritized recommendations, and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated metrics when source data is unavailable; estimates should be labeled separately from measured or user-provided data.]

## Skill Version(s):

17.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
