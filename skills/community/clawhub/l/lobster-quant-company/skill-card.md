## Description: <br>
龙虾量化研究公司 multi-agent 架构，可召唤完整的量化投研团队，包含直属、研究、执行、内容四大部门共17名专家。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swyxh](https://clawhub.ai/user/swyxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to coordinate a quant-research agent team for research analysis, compliance review, risk assessment, strategy development, testing, operations, and content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quant research and betting-market workflows could be mistaken for approval to trade, deploy, configure market-data credentials, or publish recommendations. <br>
Mitigation: Keep explicit human confirmation before any real trading, deployment, market-data credential setup, betting-market action, or public publishing. <br>
Risk: The skill coordinates specialist agent roles but does not itself provide live market data, execution controls, or legal review. <br>
Mitigation: Use real data sources and require compliance and risk review before strategy development moves to execution. <br>


## Reference(s): <br>
- [Agent configuration](references/agents-config.json) <br>
- [ClawHub skill page](https://clawhub.ai/swyxh/lobster-quant-company) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with role and workflow references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only template; no code, persistence, credential access, or hidden automation in the artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and references/agents-config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
