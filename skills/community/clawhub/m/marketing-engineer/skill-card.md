## Description:

Marketing Engineer helps agents build and operate evidence-based product marketing workspaces, content workflows, GEO/SEO planning, and a single-file dashboard for workspace status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iguoguo](https://clawhub.ai/user/iguoguo)

### License/Terms of Use:

MIT

## Use Case:

Marketing teams, founders, and agents use this skill to scaffold a product marketing workspace, maintain shared source-of-truth files, run content and GEO/SEO workflows, and generate a dashboard that shows file status, schedules, and campaign work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dashboard generation and localhost serving can expose broad workspace contents, including internal text.

Mitigation: Keep secrets and sensitive customer or business data out of served workspaces, use the no-text snapshot mode for sensitive projects, and stop the local server when finished.

Risk: Apple Calendar import or AppleScript automation can write local calendar events.

Mitigation: Require explicit user confirmation before any Apple Calendar import or AppleScript automation, and use the documented .ics fallback when direct automation is blocked.

Risk: Marketing plans, content drafts, or dashboard-derived guidance can be incorrect or misleading if source files are stale or incomplete.

Mitigation: Review generated outputs before deployment, maintain source evidence in the workspace, and require human approval before publishing.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/iguoguo/marketing-engineer)
- [ClawHub skill page](https://clawhub.ai/iguoguo/skills/marketing-engineer)
- [README](README.md)
- [English README](README_EN.md)
- [Usage manual](references/usage-manual.md)
- [Workspace structure](references/workspace-structure.md)
- [Content production workflow](references/workflow-content-production.md)
- [GEO/SEO playbook](references/geo-playbook.md)
- [Dashboard playbook](references/dashboard-playbook.md)
- [Brand consistency audit](references/brand-consistency-audit.md)
- [Shann Holmberg methodology reference](https://x.com/shannholmberg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with generated workspace files, dashboard HTML, JSON-LD, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a marketing workspace, dashboard.html, cache files, scripts, and structured content artifacts.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
