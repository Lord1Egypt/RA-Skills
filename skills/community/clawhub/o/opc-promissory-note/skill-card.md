## Description:

即期本票全流程技能，帮助用户掌握票据法合规要求、票据知识、真伪鉴别、诈骗识别、银行验证、佣金审查和审核决策。核心价值是识别和防范票据诈骗，保护客户资产安全。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and advisors use this Chinese-language reference skill to review promissory-note compliance, authenticity, fraud indicators, bank verification steps, commission structures, and transaction decision templates. It supports risk review workflows but should not replace bank, legal, tax, or regulatory advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may submit sensitive ticket numbers, account data, SWIFT confirmations, customer names, authentication materials, or bank messages during review.

Mitigation: Redact sensitive identifiers and use only approved data before sharing transaction materials with an assistant.

Risk: The skill covers high-stakes banking, SBLC, tax, green-channel, and transaction-decision topics that may be mistaken for binding professional advice.

Mitigation: Treat outputs as non-binding background and verify real transactions through the relevant bank, counsel, and official regulators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-promissory-note)
- [票据法核心条文](references/01-票据法核心条文.md)
- [三票对比与六项要素](references/02-三票对比与六项要素.md)
- [真伪鉴别手册](references/03-真伪鉴别手册.md)
- [诈骗识别手册](references/04-诈骗识别手册.md)
- [诈骗风险评估打分卡](references/05-诈骗风险评估打分卡.md)
- [银行验证流程](references/06-银行验证流程.md)
- [佣金审查清单](references/07-佣金审查清单.md)
- [审核决策模板](references/08-审核决策模板.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Configuration]

**Output Format:** [Markdown and structured checklist-style guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language financial risk-reference material; no executable code or persistence detected in release evidence.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
