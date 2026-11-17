## Description:

Investor Harness is an open prompt stack for public-market investment research with routed workflows for company deep dives, earnings previews, consensus checks, catalyst monitoring, red-team review, and PM-ready briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joansongjr](https://clawhub.ai/user/joansongjr)

### License/Terms of Use:

MIT-0

## Use Case:

Investment analysts, portfolio managers, and research teams use this skill to structure public-market research, maintain coverage workflows, prepare earnings and catalyst reviews, and produce decision-oriented summaries with explicit evidence grading and compliance boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent research-state files may capture confidential client, firm, or investment-decision information.

Mitigation: Use a dedicated investment-research workspace and review generated memory, coverage, bias, decision-log, checkpoint, and archive files before relying on or sharing them.

Risk: Automatic routing and batch refresh workflows can trigger broad, high-impact research actions from a small prompt.

Mitigation: Require explicit confirmation before batch refresh, automatic routing, or other workflows that affect many tickers, files, or future finance-related conversations.

Risk: Generated investment research can be mistaken for investment advice or approved recommendations.

Mitigation: Keep the skill's compliance boundary visible: outputs support research only, do not promise returns or create buy/sell instructions, and require human review for ratings, target prices, and forecast changes.

## Reference(s):

- [Investor Harness on ClawHub](https://clawhub.ai/joansongjr/skills/investor-harness)
- [Publisher Profile](https://clawhub.ai/user/joansongjr)
- [Skill Definition](artifact/SKILL.md)
- [Manifest](artifact/manifest.yaml)
- [Compliance Boundaries](artifact/core/compliance.md)
- [Data Adapter Protocol](artifact/core/adapters.md)
- [Evidence Grading](artifact/core/evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown research briefs, checklists, routing plans, and workspace guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include evidence labels, compliance notes, missing-data sections, and suggested archive paths.]

## Skill Version(s):

0.6.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
