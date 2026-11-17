## Description:

Audits a single page's on-page SEO signals, including title, meta description, headings, keyword usage, links, and images, then returns scored findings and prioritized fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and marketing teams use this skill to audit page-level SEO health for a URL or supplied page content, compare against competitors, and produce a prioritized repair plan. It is scoped to on-page structure and should hand off deeper content-quality, crawl, indexing, Core Web Vitals, legal, or accessibility conclusions to specialist review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce light E-E-A-T, performance, accessibility, or bulk-audit judgments outside its primary on-page SEO scope.

Mitigation: Use those findings as triage only and route final content-quality, Core Web Vitals, crawl, indexing, legal, and accessibility decisions to dedicated specialist workflows.

Risk: Some metrics may be estimated when page data, keyword data, competitor data, or rendered-page data is unavailable.

Mitigation: Keep each metric labeled as measured, user-provided, or estimated, and validate estimated keyword or search-volume assumptions before acting on production recommendations.

Risk: Raw page fetches can miss client-side rendered structured data, which may lead to false missing-schema findings.

Mitigation: Confirm structured data in the rendered DOM or with a rich-results validation tool before reporting schema as absent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/on-page-seo-checker)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Scoring Rubric](references/scoring-rubric.md)
- [Audit Templates](references/audit-templates.md)
- [Audit Example & Checklists](references/audit-example.md)
- [Bulk Audit Playbook](references/bulk-audit-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with scored sections, prioritized fixes, and a handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores are labeled by evidence quality as measured, user-provided, or estimated when source data is incomplete.]

## Skill Version(s):

19.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
