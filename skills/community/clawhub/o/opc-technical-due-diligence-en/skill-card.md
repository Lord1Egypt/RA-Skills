## Description:

Screens technology projects before investment by assessing technical feasibility, team background, patent claims, business logic, and risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT

## Use Case:

External analysts, investors, and due-diligence teams use this skill to perform rapid first-pass reviews of technology ventures, including feasibility checks, founder and patent verification, TRL assessment, red-flag screening, and structured investment-risk reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential deal materials may be imported into or persisted in an external IMA knowledge base.

Mitigation: Use only approved IMA tenants and scoped API keys, require explicit customer consent before importing files or writing reports, and confirm the destination knowledge base or document before each write.

Risk: Web searches or external lookups may expose sensitive project details.

Mitigation: Disable or sanitize web searches for confidential engagements and remove sensitive identifiers from queries when external search is not approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-technical-due-diligence-en)
- [Coze platform](https://coze.cn)
- [OPC platform](https://opc.cn)
- [Coze+IMA collaborative due diligence workflow](references/Coze-IMA协同尽调流程.md)
- [Technology readiness levels reference](references/TRL_levels.md)
- [Technical due diligence case studies](references/case_studies.md)
- [Technology scam signal checklist](references/scam_signals.md)
- [Technical parameter reference tables](references/tech_parameters.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, API Calls]

**Output Format:** [Markdown due-diligence report with risk ratings, verification notes, checklists, and recommended next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference external search results and IMA knowledge-base material when those tools are configured.]

## Skill Version(s):

1.0.0 (source: artifact metadata and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
