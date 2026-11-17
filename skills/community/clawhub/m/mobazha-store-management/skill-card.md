## Description:

Manage a Mobazha store using MCP tools — products, orders, messages, and settings. Requires an active MCP connection (see store-mcp-connect).

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengzie](https://clawhub.ai/user/fengzie)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and store operators use this skill to guide an agent through authenticated Mobazha MCP workflows for products, orders, buyer messages, discounts, collections, profile settings, notifications, exchange rates, wallets, payment providers, and marketplace search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated store operations can affect customers, inventory, revenue, refunds, order status, profile settings, and buyer communications.

Mitigation: Review tool calls before approval, especially deletes, refunds, order status changes, profile updates, and buyer messages.

Risk: MCP session credentials could be exposed if copied into agent output or logs.

Mitigation: Do not log or display tokens, and only install the skill when an authenticated Mobazha MCP workflow is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with MCP tool names, parameters, and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active authenticated MCP session established outside this skill.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
