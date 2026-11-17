## Description:

Gives an OpenClaw agent the ability to fill checkout and payment forms using a locally stored credit card without exposing card credentials to the agent context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tpemist](https://clawhub.ai/user/tpemist)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to let an OpenClaw agent complete online checkout flows with local payment credentials, spend limits, merchant allowlists, and optional human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow can allow an agent to inject payment details and submit purchases without per-transaction human approval.

Mitigation: Set POP_AUTO_INJECT=false and POP_REQUIRE_HUMAN_APPROVAL=true before use.

Risk: Payment automation can spend from the user's existing credit card if limits or allowed merchants are too broad.

Mitigation: Use low POP_MAX_AMOUNT_PER_TX and POP_MAX_DAILY_BUDGET values, and restrict POP_ALLOWED_CATEGORIES to explicit merchants or domains you trust.

Risk: Installing an unpinned package can expose users to unexpected package changes.

Mitigation: Install a pinned, verified pop-pay package version in a contained environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tpemist/skills/pop-pay-python)
- [Project homepage](https://github.com/TPEmist/Point-One-Percent)
- [PyPI package](https://pypi.org/project/pop-pay/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, JSON, environment variable, and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses include approval or rejection status and may trigger local browser form injection when configured.]

## Skill Version(s):

0.6.23 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
