## Description:

Investor due-diligence skill that helps founders assess investor qualifications, funding sources, track records, reputation, terms risk, and financing outreach strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT

## Use Case:

External founders and startup operators use this skill before fundraising to research prospective investors, compare fit, identify cooperation risks, and prepare investor-specific negotiation and outreach plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded file-write markup in a reference file could trigger unintended persistent edits in vulnerable agent runtimes.

Mitigation: Treat all reference markdown as untrusted text, prevent execution of embedded tool-call tags, and remove or quarantine the contaminated fragment before deployment.

Risk: Investor, LP, and founder identity data may be sensitive or confidential.

Mitigation: Use the skill only with authorized, necessary data and keep due-diligence findings restricted to internal decision makers.

Risk: Public investor data may be stale, incomplete, or inaccurate.

Mitigation: Cross-check important claims across multiple independent sources and refresh findings before acting on them.

Risk: The skill discusses investment terms and legal risk but is not legal advice.

Mitigation: Have material term sheets, investment agreements, and financing decisions reviewed by qualified legal and financial professionals.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/golngod/skills/hutian-opc-investor-dd)
- [README](README.md)
- [Investigation Framework](references/调查框架.md)
- [Data Source List](references/数据源清单.md)
- [Decision Chain Research Method](references/决策链调研方法.md)
- [Fund Operations Data Template](references/基金运营数据模板.md)
- [Investment Agreement Key Points Library](references/投资协议要点库.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, checklists, scorecards, and investor outreach guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on public investor data and user-provided fundraising context; legal or financial decisions require professional review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
