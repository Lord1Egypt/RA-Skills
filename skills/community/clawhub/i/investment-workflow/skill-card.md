## Description: <br>
Investment Workflow helps agents run scenario-driven investment research across stock analysis, industry analysis, market scanning, event impact analysis, and discussion workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to structure investment research, retrieve market data, compare viewpoints, and produce decision-oriented reports for stocks, industries, market scans, and investment discussions. It is intended for research support and educational analysis, not personalized financial advice or trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce direct trading-style signals that users could mistake for personalized financial advice. <br>
Mitigation: Tell users the output is research support only, ask for market, time horizon, risk tolerance, and constraints, and avoid presenting conclusions as personalized advice. <br>
Risk: Investment conclusions can be misleading when market data is stale, unavailable, or incomplete. <br>
Mitigation: Require source and timestamp labels for market data, reduce confidence when data is missing, and state the data gap in the final recommendation. <br>
Risk: Users may ask the agent to execute trades or control an account. <br>
Mitigation: Keep the workflow limited to analysis, cost review, screening methodology, and educational explanations; do not perform account control or trade execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lj22503/investment-workflow) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/lj22503) <br>
- [Shared Skill Modules](references/shared-skills.md) <br>
- [Data Layer Integration](references/data-layer-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown reports, ranked recommendations, meeting notes, and formatted investment research summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include data source and timestamp notes, confidence levels, and a clear buy, sell, hold, or watch recommendation when the workflow has enough evidence.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and artifact/clawhub.yaml; artifact/SKILL.md frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
