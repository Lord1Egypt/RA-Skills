## Description:

Profiles backlink quality and AI-assistant referral traffic for a domain, producing source-tagged off-site signal reports with recommended link-building, disavow-review, or monitoring actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and SEO/GEO analysts use this skill to evaluate a domain's off-site signals from backlink exports, referring-domain data, GA4/GSC exports, or server logs. It supports backlink profile review, toxic-link triage, competitor link-gap analysis, and AI-assistant referral monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process private analytics exports, Search Console data, or server logs.

Mitigation: Share only the needed slice of data and redact user identifiers before analysis.

Risk: Optional connector command references may depend on local scripts from outside the released artifact.

Mitigation: Use connector commands only when those local scripts are present and have been reviewed.

Risk: Monitoring saves can retain sensitive traffic summaries or follow-up items.

Mitigation: Save memory only with user approval and limit saved content to monitoring summaries and action items.

## Reference(s):

- [Backlink Analysis Templates](artifact/references/backlinks-analysis-templates.md)
- [Link Quality Rubric](artifact/references/link-quality-rubric.md)
- [Outreach Templates](artifact/references/outreach-templates.md)
- [Cloudflare Radar AI Insights](https://radar.cloudflare.com/ai-insights)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with source-tagged metrics, tables, and optional shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a reusable monitoring handoff summary when the user approves saving results.]

## Skill Version(s):

19.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
