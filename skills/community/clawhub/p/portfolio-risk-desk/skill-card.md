## Description:

Generate a portfolio-aware daily or on-demand risk analysis brief from public market data, company updates, earnings material, and macro context, then emit a host-consumable handoff for persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prashamshah115](https://clawhub.ai/user/prashamshah115)

### License/Terms of Use:

MIT-0

## Use Case:

Individual investors, analysts, and market-focused teams use Portfolio Risk Desk to turn a portfolio, watchlist, or theme into an evidence-led public-markets brief with exposure mapping, scenario analysis, source traceability, and watchpoints. It is designed for research and monitoring, not trade execution or price targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Apify retrieval can expose credentials if broad tokens, custom API endpoints, or failed-run outputs are handled carelessly.

Mitigation: Use a narrowly scoped Apify token, keep APIFY_BASE_URL fixed to the real Apify API, and review failed live-provider outputs before sharing generated briefs.

Risk: Local state handling may write outside intended workspace or profile paths when LOCAL_STATE_DIR is unconstrained.

Mitigation: Disable local state in shared deployments or tightly constrain LOCAL_STATE_DIR until workspace and profile path validation is confirmed.

Risk: Generated Notion and memory handoffs can persist sensitive portfolio context.

Mitigation: Treat Notion and memory outputs as durable copies of user portfolio data and apply the host's normal access controls, retention policy, and review process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prashamshah115/skills/portfolio-risk-desk)
- [Publisher profile](https://clawhub.ai/user/prashamshah115)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Tool contract](artifact/intelligence_desk_brief_tool_contract.json)
- [Output template](artifact/intelligence_desk_brief_output_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown brief plus structured JSON handoff payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source traceability, uncertainty notes, audit metadata, delivery status, and optional Notion handoff metadata.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and pyproject.toml report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
