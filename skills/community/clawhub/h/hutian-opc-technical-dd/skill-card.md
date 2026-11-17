## Description:

Technical due diligence screening skill for pre-investment feasibility assessment, team background checks, patent validation, business-model analysis, and identification of false or exaggerated technology claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and investment teams use this skill to run an initial technical due diligence review of technology projects and produce structured findings, red flags, risk ratings, and follow-up verification items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential investment, patent, financial, or personal data may be sent to an external knowledge base during IMA-mode workflows.

Mitigation: Confirm the destination account and workspace, obtain permission for each uploaded document, redact unnecessary sensitive data, and use narrowly scoped credentials.

Risk: Promotional sections and hard-coded example report scripts could be mistaken for neutral due diligence output.

Mitigation: Treat those sections as publisher-provided examples, remove unrelated promotional text, and require reviewers to verify all generated claims against cited sources.

Risk: Risk ratings and investment recommendations may be produced from incomplete public or user-provided evidence.

Mitigation: Use the output as initial screening only and require qualified human review, original-source verification, and deeper diligence before investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/hutian-opc-technical-dd)
- [Coze platform](https://coze.cn)
- [OPC platform](https://opc.cn)
- [Coze-IMA collaborative due diligence workflow](references/Coze-IMA协同尽调流程.md)
- [Technology readiness levels](references/TRL_levels.md)
- [Due diligence case studies](references/case_studies.md)
- [Scam signal checklist](references/scam_signals.md)
- [Technical parameter reference](references/tech_parameters.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown due diligence reports, red-flag checklists, risk ratings, recommendations, and optional report-generation scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use web search, file operations, Coze workflows, and IMA knowledge-base APIs when configured by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
