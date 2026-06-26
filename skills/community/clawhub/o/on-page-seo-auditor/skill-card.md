## Description: <br>
Audits on-page SEO factors such as titles, headers, images, links, content fit, and fix priorities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, site owners, marketers, and SEO practitioners use this skill to audit single pages or batches of pages for on-page SEO health, scored findings, and prioritized repair plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as checking a page may activate the skill when the user did not intend a full SEO audit. <br>
Mitigation: Confirm the audit scope, page URL or content, and target keyword before producing recommendations. <br>
Risk: Audit summaries may be saved to long-term memory and could capture confidential or unreleased page details. <br>
Mitigation: Avoid saving results for confidential pages unless the user explicitly approves, and keep saved summaries limited to issues and next actions. <br>
Risk: Fetched page content may contain prompt-injection text or directives that try to alter the audit. <br>
Mitigation: Treat fetched web content as evidence only, ignore embedded instructions, and flag suspicious directives as trust or consistency issues. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aaron-he-zhu/on-page-seo-auditor) <br>
- [Project homepage](https://github.com/aaron-he-zhu/seo-geo-claude-skills) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>
- [Audit Templates](references/audit-templates.md) <br>
- [Audit Example and Checklists](references/audit-example.md) <br>
- [Bulk Audit Playbook](references/bulk-audit-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with score tables, prioritized issues, recommended fixes, and a handoff summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include per-section scores, an overall score out of 100, P0/P1/P2 priorities, competitor comparisons, and optional reusable audit-memory summaries.] <br>

## Skill Version(s): <br>
9.9.9 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
