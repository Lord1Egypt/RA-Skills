## Description:

指数通 (Index Expert) helps users analyze A-share, Hong Kong, and U.S. stock indexes and ETFs by linking market news, index catalogs, and nine investment-framework perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pzc66momo](https://clawhub.ai/user/pzc66momo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to interpret index and ETF questions, connect finance news to relevant indexes, compare investment-framework viewpoints, and produce concise index-oriented analysis. It is intended for informational investment analysis and not for real-time quotes, individualized portfolio advice, or investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores user investment-profile information across conversations.

Mitigation: Inform users before saving preferences, allow use without profiling, and provide a clear way to view and delete stored profile data.

Risk: Conversation feedback can be promoted into future behavior rules.

Mitigation: Require human review before turning free-form user feedback or reflection output into persistent rules.

Risk: The skill can direct users to Tencent Licaitong finance links.

Mitigation: Label these links as optional third-party destinations and do not imply NVIDIA or ClawHub endorsement.

Risk: Finance guidance may be mistaken for individualized investment advice.

Mitigation: Keep outputs informational, preserve investment-risk disclaimers, avoid predictions and personal portfolio recommendations, and encourage users to verify current market data from authoritative sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pzc66momo/skills/indexpert)
- [Index catalog](artifact/references/index_catalog.json)
- [Trusted index sources](artifact/references/trusted_sources_index.json)
- [Trusted media sources](artifact/references/trusted_sources_media.json)
- [Investment master frameworks](artifact/references/masters/)
- [Tencent Licaitong index detail destination](https://www.txfund.com/h5/v6/pages/finance-tools/stock-index/detail?indexCode=000140)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown-style investment analysis with concise recommendations, caveats, and optional third-party index detail links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include index names and codes, risk notes, source-confidence labels, and non-advisory investment disclaimers.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
