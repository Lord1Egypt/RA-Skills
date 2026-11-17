## Description:

Researches a product feature from current public sources, decomposes it into stable technical dimensions, retrieves and reviews related patents, maps disclosed patent evidence to those dimensions, ranks relevance under a transparent rubric, and generates a self-contained interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and IP researchers use this skill to map a product feature to related patent disclosures across technical dimensions and produce an evidence-backed HTML report. The workflow supports technical correspondence research and is not a legal opinion about patent coverage, infringement, validity, ownership, or freedom to operate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential product details may be shared with web research sources or PatSnap MCP services during live research.

Mitigation: Confirm the user's confidentiality and data-sharing boundary before research, and avoid submitting confidential details unless sharing is approved.

Risk: Patent mappings could be mistaken for legal conclusions about coverage, infringement, validity, ownership, or freedom to operate.

Mitigation: Label results as technical correspondence research, preserve uncertainty, and direct legal conclusions to qualified review.

Risk: Ambiguous product scope, incomplete public evidence, or retrieval caps can make patent results incomplete or misleading.

Mitigation: Clarify product and feature boundaries, record sources, queries, limits, and unresolved uncertainty, and stop or narrow the task when evidence is insufficient.

Risk: Unverified patent, image, or source links could create misleading report evidence.

Mitigation: Use links only when returned by verified connectors or current official sources, validate URLs, and state unavailable when a link or image cannot be verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/map-product-features-to-patents-ip)
- [PatSnap Advanced Patent Search MCP Marketplace](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP Marketplace](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Deep Patent Mining MCP Marketplace](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)
- [PatSnap Global Core Patent Database MCP Marketplace](https://open.patsnap.com/marketplace/mcp-servers/core-patents)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Self-contained HTML report with cited evidence, technical-dimension mappings, relevance explanations, accessible filters, and supporting text or markdown guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current public research and verified PatSnap MCP connector results; patent relevance is technical correspondence, not legal advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
