## Description: <br>
Calculates Kelly Criterion position sizes from win-rate and payoff assumptions to support educational risk-management analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danpian1](https://clawhub.ai/user/danpian1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-oriented agents use this skill to calculate Kelly Criterion bet or position sizes, compare full, half, and quarter Kelly variants, and frame conservative position-sizing decisions. It should be used as educational risk-management guidance rather than trading authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat Kelly outputs as trading instructions even though the skill has no trading authority and depends on user-supplied assumptions. <br>
Mitigation: Present results as educational sizing guidance, verify win-rate and payoff assumptions independently, and do not grant the skill account access or trading permissions. <br>
Risk: Incorrect or overconfident probability estimates can produce oversized positions. <br>
Mitigation: Use conservative variants such as half or quarter Kelly, apply portfolio caps, and review assumptions before acting. <br>


## Reference(s): <br>
- [Kelly calculator quick reference](references/kelly-calculator.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with formulas, tables, and worked examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Educational calculations only; no account access, order placement, code execution, or network use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
