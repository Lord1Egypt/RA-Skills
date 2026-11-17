## Description:

Read and analyze Borsa Istanbul equities, TEFAS funds, KAP disclosures, VIOP futures, Turkish macro data, delayed prices, and inflation-adjusted returns through rules guidance and an optional Oracle-X instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yigtwxx](https://clawhub.ai/user/yigtwxx)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agents use this skill to answer Turkish market questions, select the correct Oracle-X BIST endpoint, and explain BIST returns in nominal, real, and USD frames. It also helps avoid common VIOP margin and Takasbank data mistakes when no Oracle-X server is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may point ORACLE_X_URL at an untrusted Oracle-X instance, and documented radar job endpoints do not use per-user tokens.

Mitigation: Use only Oracle-X instances the operator controls or trusts, and treat shared instances as able to observe or influence returned market data.

Risk: Delayed or derived market data could be mistaken for live trading advice.

Mitigation: State delay and data frame explicitly, and present outputs as market analysis rather than live trading instructions.

Risk: VIOP price scan ranges can be misread as margin-call prices.

Mitigation: Describe scan ranges as clearing-house risk parameters and do not compute margin-call prices from public data.

## Reference(s):

- [Oracle-X BIST on ClawHub](https://clawhub.ai/yigtwxx/skills/oracle-x-bist)
- [Oracle-X project homepage listed by the skill](https://github.com/Yigtwxx/OracleX)
- [Oracle-X Borsa Istanbul endpoint reference](references/endpoints.md)
- [Reading Takasbank's price scan range](references/viop-margins.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint names, curl examples, and market-analysis prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on ORACLE_X_URL for live endpoint calls; rules guidance works without a server.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
