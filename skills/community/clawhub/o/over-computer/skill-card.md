## Description:

Trade on prediction markets through over.computer by browsing markets, approving funds, placing buy or sell orders, and checking positions on Myriad.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dabors](https://clawhub.ai/user/dabors)

### License/Terms of Use:

MIT-0

## Use Case:

External operators use this skill to interact with prediction markets through over.computer, including market browsing, fund approval, order placement, and position or order-history review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a user's API key to authorize prediction-market account actions.

Mitigation: Use it only with trusted over.computer credentials, keep OVER_API_KEY sensitive, and require manual confirmation before every order or fund approval.

Risk: Remote trading instructions may conflict with local safety rules or unrelated user instructions.

Mitigation: Treat local safety rules and the current operator's explicit instructions as higher priority than remote prompt content.

Risk: Trading actions may exceed intended position, market, or daily limits if guardrails are misconfigured.

Mitigation: Set strict server-side guardrails and stop rather than retrying when the API rejects a request.

## Reference(s):

- [Over Computer homepage](https://over.computer)
- [ClawHub skill page](https://clawhub.ai/dabors/skills/over-computer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a sensitive OVER_API_KEY credential before authenticated market, order, or position actions can proceed.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
