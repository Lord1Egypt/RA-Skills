## Description:

潜力市场专家 helps Amazon sellers identify moderate-volume, recently listed products with positive sales growth, then export scouting and scoring results for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon marketplace sellers and ecommerce operators use this skill to scout potential product opportunities, compare sorting strategies, continue paginated searches, schedule recurring scouting work, and run preference-based ASIN scoring before deeper product research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports bundled tools that can persistently alter agent instructions.

Mitigation: Install only in a trusted runtime, review bundled tools before execution, and avoid the CLAUDE.md patch utility unless persistent instruction changes are intended.

Risk: The scanner reports that credentials may be sent to endpoints selected through environment variables.

Mitigation: Pin LinkFox gateway environment variables to trusted HTTPS hosts and treat onboarding output and API keys as secret material.

Risk: The skill can create scheduled tasks and upload files through bundled LinkFox tools.

Mitigation: Confirm scheduled task parameters, execution cost, notification targets, and any public file upload before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-potential-market-scout)
- [Amazon Product Scout API Parameters](artifact/skills/amazon-product-scout-agent/references/api-params-catalog.md)
- [SellerSprite Product Search API](artifact/skills/linkfox-sellersprite-product-search/references/api.md)
- [ASIN Dynamic Scoring Example Expectations](artifact/skills/amazon-asin-dynamic-scoring/references/example_expectations.json)
- [LinkFox Task Scheduler API](artifact/skills/linkfox-task-scheduler/references/api.md)
- [LinkFox File Upload API](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Conversational guidance with Markdown previews plus Excel, JSON, and optional shell-command outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Excel workbooks, JSON summaries, SQLite state, scheduled tasks, and public file-upload URLs through LinkFox services.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
