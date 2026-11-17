## Description:

面向亚马逊卖家的 1688 找货源与利润分析专家，用于根据 ASIN 匹配 1688 供应商、验证同款候选、核算 FBA 成本，并按预期净利润排序推荐货源。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and sourcing analysts use this skill to start from an ASIN, discover comparable 1688 supplier candidates, verify visual/product matches, calculate FBA-based costs, and rank sourcing options by expected monthly net profit.

### Deployment Geography for Use:

United States marketplace workflows; supplier discovery uses 1688 sourcing inputs.

## Known Risks and Mitigations:

Risk: The server security summary flags automatic feedback telemetry and credential-handling choices for review before installation.

Mitigation: Install only in a trusted environment, review the feedback behavior before use, and store LinkFox API keys in a secure credential manager rather than shell profiles.

Risk: Endpoint override environment variables can redirect LinkFox API traffic.

Mitigation: Keep LinkFox endpoint override variables unset unless the operator fully controls the destination service.

Risk: The file upload helper can publish local files through a public URL.

Mitigation: Upload only content that is approved for public access and review generated reports or datasets before sharing.

Risk: Generated HTML reports may contain active content.

Mitigation: Treat generated reports as active content and open or distribute them only in trusted contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-1688-sourcing-expert)
- [LinkFox Skills](https://skill.linkfox.com/)
- [Top-level workflow](artifact/SKILL.md)
- [1688 source profiler workflow](artifact/skills/linkfox-1688-source-profiler/SKILL.md)
- [AIGC prompt templates](artifact/skills/linkfox-1688-source-profiler/references/aigc-prompt-templates.md)
- [FBA fee table](artifact/skills/linkfox-1688-source-profiler/references/fba-fee-table.md)
- [1688 image search API](artifact/skills/linkfox-1688-search-by-image/references/api.md)
- [Amazon search API](artifact/skills/linkfox-amazon-search/references/api.md)
- [Keepa product detail API](artifact/skills/linkfox-keepa-product-request/references/api.md)
- [Keepa product history API](artifact/skills/linkfox-keepa-product-series/references/api.md)
- [SIF ASIN keywords API](artifact/skills/linkfox-sif-asin-keywords/references/api.md)
- [SIF ASIN summary API](artifact/skills/linkfox-sif-asin-summary/references/api.md)
- [Jiimore niche keyword API](artifact/skills/linkfox-jiimore-get-niche-info-by-keyword/references/api.md)
- [DLD product search API](artifact/skills/linkfox-dld-product-search/references/api.md)
- [AIGC text generation API](artifact/skills/linkfox-aigc-textgen/references/api.md)
- [Report layout reference](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)
- [File upload API](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with JSON data files and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a supplied ASIN; defaults to the US marketplace; writes full workflow data and long-form reports to local paths.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
