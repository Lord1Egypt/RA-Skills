## Description:

查询指定型号的库存和补货计划，按用户要求返回查询结果且不重新格式化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[logandx314](https://clawhub.ai/user/logandx314)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, operations, or support users can ask an agent to look up current inventory and restock plans for a product model and receive the returned inventory or replenishment details without reformatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guidance passes free-form user text into a shell command, which can create command-injection or argument-parsing risk.

Mitigation: Invoke the query program with structured arguments, strict quoting, and model validation before deployment.

Risk: Inventory and restock data may be sensitive business information.

Mitigation: Install and run the skill only in environments where the requested inventory data may be shown to the requesting user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/logandx314/skills/inventory-query)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text returned from a command-line inventory query]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The returned query output is intended to be passed through without agent-side modification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
