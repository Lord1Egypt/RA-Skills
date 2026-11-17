## Description:

Prism Auto Config Map helps agents produce visual automotive configuration planning reports that combine competitive benchmarking, QFD and Matrix Analysis, PatSnap patent and literature signals, and supply-chain evidence for next-generation vehicle decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Product planning, competitive intelligence, R&D, procurement, and sales/demo teams use this skill to benchmark vehicle configurations, identify next-generation feature opportunities, and explain recommendations with market, patent, literature, and supply-chain evidence. It is not intended for FTO legal opinions, precise BOM/TCO costing, or broad company strategy analysis outside vehicle configuration decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on authorized PatSnap/Zhihuiya MCP services for live patent, literature, market, and supply-chain evidence.

Mitigation: Configure only approved MCP services and credentials, and treat missing connectivity as a reason to produce framework-only analysis rather than sourced conclusions.

Risk: Licensed data, commercial configuration sources, or crawling fallbacks may have source-permission constraints.

Mitigation: Verify data-use permissions before production use and label any fallback or unverified source clearly in the generated report.

Risk: Patent and supplier analysis may be mistaken for legal advice or definitive supplier confirmation.

Mitigation: Keep FTO/legal conclusions out of scope, disclose patent-publication lag, and mark supplier relationships by evidence status such as verified cooperation, joint patent filing, product announcement lead, or lead to verify.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/prism-auto-config-map)
- [PatSnap/Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [PatSnap/Zhihuiya MCP marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [Methodology reference](artifact/references/methodology.md)
- [Data sources reference](artifact/references/data_sources.md)
- [PatSnap data lens reference](artifact/references/patsnap_data_lens.md)
- [Supply-chain lens reference](artifact/references/supply_chain_lens.md)
- [Output templates reference](artifact/references/output_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, files]

**Output Format:** [Static HTML report files, Markdown summaries, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected report outputs use local assets, offline-friendly HTML, evidence tables, dashboards, heatmaps, QFD and matrix boards, and patent-pool detail pages when supported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
