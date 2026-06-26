## Description: <br>
计算中国法院诉讼费、案件受理费和申请费，并根据《诉讼费用交纳办法》第十三条和第十四条给出分段明细与提示。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and legal operations teams use this skill to estimate and compare Chinese court filing, case acceptance, and application fees for common civil, administrative, enforcement, preservation, bankruptcy, arbitration, and maritime scenarios. It is useful for fee planning and explanation, but outputs should be treated as estimates rather than legal advice. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Fee outputs may be mistaken for legal advice or final court determinations. <br>
Mitigation: Present results as estimates and direct users to verify the fee with the relevant court or qualified counsel. <br>
Risk: Range-based fees and local court standards may differ from the skill's lower-bound default. <br>
Mitigation: Call out when a fee is a lower-bound reference and confirm the applicable local standard before relying on it. <br>
Risk: Fee rules can change or vary by jurisdiction. <br>
Mitigation: Verify current rules and jurisdiction-specific practice for the case before filing or budgeting. <br>


## Reference(s): <br>
- [诉讼费用交纳办法费用计算依据](references/litigation-fee-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolalam/litigation-fee-calculator) <br>
- [Publisher Profile](https://clawhub.ai/user/coolalam) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured fee tables, calculation breakdowns, notes, and optional command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Decimal monetary inputs, rounds to 0.01 CNY, and defaults range-based fees to the lower bound with local-standard reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
