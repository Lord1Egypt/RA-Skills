## Description:

Provides Meituan RMS Open Platform API and solution reference material for agents helping developers search, browse, and reason about restaurant-system integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration teams use this skill to locate Meituan RMS API documentation, solution guides, message references, and example command-line lookups for POS, ordering, CRM, finance, data, and supply-chain integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags the bundle as suspicious because it includes unsafe scraping guidance and examples around powerful POS, finance, member, and account operations.

Mitigation: Install only when Meituan RMS/Open Platform reference material is needed, and require human confirmation before using APIs that pay, recharge, delete, upload files, change member data, send coupons, or deduct points.

Risk: The bundled scraping scripts include anti-automation bypass behavior.

Mitigation: Do not run the scraping scripts outside a disposable, least-privilege environment, and confirm authorization and platform terms before any use.

Risk: Authentication examples or copied snippets may expose tokens if used directly.

Mitigation: Do not copy examples that log authorization tokens; redact credentials and keep secrets out of logs, prompts, and generated documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woai36d/skills/meituan-api-fetcher)
- [Meituan developer platform](https://developer.meituan.com)
- [Artifact overview](artifact/SKILL.md)
- [Scrape report](artifact/scrape_report.json)
- [API detail summary](artifact/api_details/_summary.json)
- [Base data API list](artifact/references/基础档案类_API列表.md)
- [Data reports API list](artifact/references/数据报表类_API列表.md)
- [Orders API list](artifact/references/订单类_API列表.md)
- [Sold-out API list](artifact/references/沽清类_API列表.md)
- [Member marketing API list](artifact/references/会员营销类_API列表.md)
- [Supply chain API list](artifact/references/供应链旗舰版_API列表.md)
- [Dine-in QR ordering solution](artifact/solutions/堂食扫码点餐.md)
- [Self-operated delivery ordering solution](artifact/solutions/自营外卖下单.md)
- [Third-party CRM integration solution](artifact/solutions/第三方会员CRM对接.md)
- [Third-party finance integration solution](artifact/solutions/第三方财务对接.md)
- [Third-party data platform solution](artifact/solutions/第三方数据中台.md)
- [Third-party supply chain integration solution](artifact/solutions/第三方供应链对接.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with local reference paths, JSON-backed facts, and optional command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reference Chinese-language Meituan API documentation and bundled artifact files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
