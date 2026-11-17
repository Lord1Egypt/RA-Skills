## Description:

Generates structured public mutual fund performance attribution reports focused on excess return sources, stock selection, market timing, allocation support, and performance sustainability using Investoday finance data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External finance users and agents use this skill to analyze public mutual fund performance attribution, including whether excess return appears driven by alpha, beta exposure, stock selection, market timing, asset allocation, or manager history. The output is analytical reference material and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake fund attribution analysis for investment instructions.

Mitigation: Present conclusions as reference analysis only, avoid buy, sell, redemption, allocation, or market-timing advice, and remind users to verify financial conclusions independently.

Risk: Fund identity can be ambiguous when the user provides only a name.

Mitigation: Use entity recognition first and request a complete fund name or six-digit fund code when the match is not stable and unique.

Risk: Attribution conclusions can be misleading when evidence is missing or active-management metrics are applied to passive or index-tracking products.

Mitigation: Require numerical evidence for attribution conclusions, state when data is insufficient, and explain analysis boundaries for passive or index-tracking funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenneth-bro/skills/investoday-fund-performance-attribution-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown fund performance attribution report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public fund data and requires independent verification of financial conclusions.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
