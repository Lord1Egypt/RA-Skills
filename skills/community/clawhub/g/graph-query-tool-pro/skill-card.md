## Description:

Enables agents to query on-chain data through free and paid endpoints with budget controls, payment previews, receipts, and batch analysis support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trading teams use this skill to route blockchain data questions to on-chain data endpoints, analyze prediction market and wallet activity, and manage paid x402 calls with spending controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording could route ordinary analytics tasks into a payment-capable workflow.

Mitigation: Use the skill only for explicit on-chain or blockchain data tasks and review the selected endpoint before approving any paid call.

Risk: Paid endpoints and autonomous mode can cause unintended spending.

Mitigation: Enable per-call payment confirmation, set a low total budget, use a dedicated low-balance wallet, and configure stop conditions before autonomous operation.

Risk: The reported license differs between server evidence and artifact frontmatter.

Mitigation: Confirm the authoritative release license before publishing or redistributing the skill card.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/graph-query-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and JSON-like structured responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status, result data, execution timing, metadata, logs, and error details.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
