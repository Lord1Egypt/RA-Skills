## Description:

Provides commercial pension insurance analysis, pension account simulation, retirement income estimates, and financial portfolio guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for personal pension planning, including pension insurance analysis, pension account simulation, retirement income estimates, and asset-allocation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce sensitive finance-oriented outputs involving statements, tax details, holdings, and retirement planning assumptions.

Mitigation: Only provide transaction, statement, tax, billing, or holdings data when the user intentionally asks for account-specific analysis, and review outputs before relying on them for financial decisions.

Risk: Users may mistake the skill for an authorized account-management tool.

Mitigation: Do not allow the skill to initiate transfers or account changes without separate trusted controls, and require independent confirmation for high-value actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text financial-planning analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May discuss account balances, statements, taxes, holdings, risk status, and allocation suggestions when the user intentionally supplies that context.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
