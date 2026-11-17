## Description:

Autonomous Meta Ads agent guidance for creating campaigns, generating creatives, monitoring CPA/ROAS/CTR, pausing underperforming ads, and reporting alerts across multiple ad accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, agencies, and developers use this skill to guide Meta Ads campaign setup, account audits, creative generation, stop-loss decisions, landing-page checks, and concise executive reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful Meta or Habilis credentials could be exposed if pasted into chat.

Mitigation: Configure tokens through a secure local secret mechanism and restrict them to the minimum scopes and ad accounts needed.

Risk: Automated ad-account actions can pause or change campaigns beyond the user's intent.

Mitigation: Use dry-run mode or manual approval for pauses, campaign changes, and activation decisions.

Risk: Broad account sweeps, cron prompt searches, and URL health checks can expand operational and network exposure.

Mitigation: Run only explicitly authorized account scopes and execute URL checks through a constrained validator or sandboxed egress path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rafacpti23/skills/meta-ads-subagent)
- [Habilis developer portal](https://xvix.com.br)
- [Meta Ads API insights and documented behavior](references/meta_ads_optimization_insights.md)
- [Visual creative framework](references/visual_creative_framework.md)
- [Naming conventions and briefing standards](references/naming_conventions_and_briefing_standards.md)
- [Habilis SaaS MCP Gateway and zero-storage architecture guide](references/habilis_saas_architecture_and_zero_storage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, API-call guidance, and HTML template references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise executive reports intended for a single Telegram or manager-update message.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
