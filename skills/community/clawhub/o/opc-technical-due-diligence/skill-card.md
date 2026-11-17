## Description:

The skill guides pre-investment technical due diligence by assessing feasibility, team background, patent claims, business logic, and red-flag signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External investment, strategy, and due-diligence teams use this skill to structure first-pass reviews of technology projects and produce risk-rated diligence reports before deeper expert review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may move sensitive business plans, resumes, patent files, financial records, test reports, and generated diligence reports into an external IMA knowledge base.

Mitigation: Use local-only review unless IMA integration is intentional, require explicit approval before upload or append operations, and confirm destination account, document ID, access controls, and retention policy before sharing sensitive files.

Risk: Bundled generated reports and verification scripts can be mistaken for independent due-diligence evidence.

Mitigation: Treat bundled reports and scripts as templates or examples, and verify conclusions against original project documents, public records, patent databases, and expert review before using them for investment decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/golngod/skills/opc-technical-due-diligence)
- [Coze+IMA协同尽调流程](references/Coze-IMA协同尽调流程.md)
- [技术成熟度等级 (TRL) 说明](references/TRL_levels.md)
- [常见技术骗局特征清单](references/scam_signals.md)
- [各领域技术参数对照表](references/tech_parameters.md)
- [技术尽调案例库](references/case_studies.md)
- [Coze platform](https://coze.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and structured checklists, with optional DOCX report files from bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes red-flag lists, risk ratings, investment recommendations, verification checklists, and optional IMA synchronization guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter metadata.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
