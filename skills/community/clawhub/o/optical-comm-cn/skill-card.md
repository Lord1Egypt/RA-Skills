## Description:

A Chinese-language agent skill for analyzing optical-communications investment themes, related equities, technology routes, supply-chain positioning, and curated reference updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcchris1995](https://clawhub.ai/user/pcchris1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to structure Chinese-language optical-communications investment research, compare CPO/NPO/XPO/OCS and InP/silicon-photonics/TFLN routes, map suppliers and stocks, and produce cautious reference-backed analysis. Optional update workflows help incorporate user-reviewed new Xueqiu article content into the skill's reference notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional update workflow may use a logged-in Xueqiu browser profile and can modify local reference notes.

Mitigation: Prefer manually supplied article text or an isolated browser profile, run updates only when explicitly requested, and review note changes before relying on them.

Risk: Investment and market judgments in the references are time-sensitive and may become outdated.

Mitigation: Treat outputs as research structure rather than financial advice, verify current market data and company disclosures, and preserve uncertainty labels for unconfirmed claims.

## Reference(s):

- [光通信投资分析框架](artifact/SKILL.md)
- [闷得而蜜光通信投资框架（精炼版）](artifact/references/core-framework.md)
- [光通信技术路线全景](artifact/references/tech-landscape.md)
- [光通信产业链与标的分析](artifact/references/supply-chain.md)
- [光通信投资方法论](artifact/references/methodology.md)
- [更新日志](artifact/references/update-log.md)
- [闷得而蜜 Xueqiu profile](https://xueqiu.com/u/5672579962)
- [查尔斯大风车 Xueqiu profile](https://xueqiu.com/u/8755156034)
- [2026-04-21 查尔斯大风车 Xueqiu article](https://xueqiu.com/8755156034/384873103)
- [ClawHub skill page](https://clawhub.ai/pcchris1995/skills/optical-comm-cn)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Chinese-language Markdown analysis and reference-update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock-analysis structure, route comparisons, supplier mapping, risk caveats, and optional instructions for updating local reference notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
