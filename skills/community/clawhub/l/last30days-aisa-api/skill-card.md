## Description: <br>
Researches the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search, returning a ranked and clustered brief with citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to scan recent public social, market, developer, and web evidence about a topic, company, product, person, or comparison. It is suited for trend scans, competitor comparisons, launch reactions, community sentiment checks, and structured research briefs for downstream agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, generated subqueries, and source lookups are sent to AIsa and public platform APIs. <br>
Mitigation: Avoid secrets, unreleased product names, sensitive personal data, and confidential investigations in prompts; restrict sources with --search when needed. <br>
Risk: Optional GitHub retrieval can use a user-provided token. <br>
Mitigation: Use a least-privilege token and omit GH_TOKEN or GITHUB_TOKEN when GitHub results are not needed. <br>
Risk: Optional account-backed or local integrations may use sources tied to an authenticated account. <br>
Mitigation: Enable those integrations only when the account-backed source is intentionally in scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/last30days-aisa-api) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa API Reference](https://aisa.one/docs/api-reference) <br>
- [AIsa model guide](https://aisa.one/docs/guides/models) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Markdown brief by default; JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output can include the query plan, ranked candidates, clusters, items by source, provider runtime, and source-level errors.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
