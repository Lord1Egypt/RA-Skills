## Description:

Scores backlog items with RICE/WSJF/Kano and files GitHub issues for top candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use the skill during roadmap reviews, sprint planning, and retrospectives to inventory features, compare priorities, analyze tradeoffs, and propose backlog items. It can prepare GitHub issues for suggestions the user accepts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External research may share project details, and skipped suggestions may be stored automatically.

Mitigation: Consider privacy needs before using external research. Review the capture script's behavior and storage destination before allowing automatic capture; the supplied scan was incomplete and left that script unresolved.

## Reference(s):

- [Claude Night Market plugin page (listed in skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [Classification system](modules/classification-system.md)
- [Scoring framework](modules/scoring-framework.md)
- [Multi-metric evaluation methodology](modules/multi-metric-evaluation-methodology.md)
- [Tradeoff dimensions](modules/tradeoff-dimensions.md)
- [Configuration](modules/configuration.md)
- [Research enrichment](modules/research-enrichment.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, GitHub issue drafts]

**Output Format:** [Markdown tables and recommendations, with optional issue content and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research enrichment requires the tome plugin; the skill also requires the night-market.imbue:scope-guard configuration. Issue creation follows user confirmation.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
