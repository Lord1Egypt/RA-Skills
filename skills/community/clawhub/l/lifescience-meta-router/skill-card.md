## Description:

Routes life-science questions about targets, drugs, diseases, companies, biomarkers, and related patent, market, commercial, regulatory, clinical, deal, and safety topics to specialist analysis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fubian-ai](https://clawhub.ai/user/fubian-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Life-science analysts and agent builders use this router to identify biomedical entities, classify analysis intent, plan specialist workflows, and synthesize results for pharma, biotech, clinical, regulatory, commercial, patent, and market questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims broad routing control over life-science questions, which can override other analysis paths or produce overly expansive workflows.

Mitigation: Review the routing behavior before installation and use it only when Patsnap-centered life-science routing is intended.

Risk: The artifact documents an API-key-in-URL MCP connection pattern.

Mitigation: Prefer protected credential handling or header-based authentication when supported, and avoid URL-based API keys unless the platform reliably redacts URLs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fubian-ai/skills/lifescience-meta-router)
- [Patsnap pharma-intelligence MCP server](https://open.patsnap.com/marketplace/mcp-servers/245f3ce8-79e4-4c2a-927c-e155c293f097)

## Skill Output:

**Output Type(s):** [guidance, markdown, analysis]

**Output Format:** [Markdown with routing decisions, tables, and optional inline HTML visual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require configured Patsnap MCP credentials for full data retrieval.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
