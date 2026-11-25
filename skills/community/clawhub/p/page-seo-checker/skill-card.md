## Description:

Check SEO compliance of any domain page based on internal SEO standards and page launch checklist, generating a visual HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notegpt-official](https://clawhub.ai/user/notegpt-official)

### License/Terms of Use:

MIT-0

## Use Case:

Content, SEO, and web teams use this skill to audit a live page before publishing. It checks page metadata, structure, content, links, images, structured data, localization, and brand usage, then reports findings and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional keyword validation may send page-derived keywords to an external service. The security review is incomplete because one referenced path could not be resolved.

Mitigation: Use keyword validation only with non-sensitive terms or skip it; review the unresolved reference and complete security review before deployment.

## Reference(s):

- [GitHub source repository (server-resolved provenance)](https://github.com/notegpt-official/notegpt-skills/tree/main/skills/seo/page-seo-checker)
- [ClawHub skill listing](https://clawhub.ai/notegpt-official/skills/page-seo-checker)
- [SEO compliance checklist](references/seo-checklist.md)
- [HTML report template](references/report-template.html)

## Skill Output:

**Output Type(s):** [HTML report, Text, Guidance]

**Output Format:** [Standalone HTML audit report with pass/fail findings, a score, and actionable fix recommendations, plus a concise summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a live page URL and brand name. The optional keyword difficulty check may use an external service.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
