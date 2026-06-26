## Description: <br>
Kuaidi100 User is a shipping assistant that helps users place shipment orders after SSO login, query logistics, manage orders, compare carriers, parse addresses, and estimate package weight. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuaidi100-api](https://clawhub.ai/user/kuaidi100-api) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to coordinate kuaidi100 shipping workflows through a CLI, including authenticated shipment creation, logistics lookup, order management, carrier comparison, address parsing, and weight lookup. It guides the agent to require SSO login for shipment and order actions, use server-side address books for authenticated flows, and collect user confirmation before order creation or cancellation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles shipping addresses, order details, and SSO browser login flows. <br>
Mitigation: Install only when the kuaidi100 CLI package is trusted, and confirm browser-opened login and order links match the expected kuaidi100 flow. <br>
Risk: Shipment creation or cancellation can affect real orders. <br>
Mitigation: Require user review and confirmation of order or cancellation details before running the corresponding CLI command. <br>
Risk: Unauthenticated or stale sessions could expose incomplete or misleading address, order, or logistics state. <br>
Mitigation: Check authentication status before protected workflows, reauthenticate on key-required errors, and avoid local cached address data for shipment flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kuaidi100-api/kuaidi100-user) <br>
- [Workflow reference](artifact/references/workflow.md) <br>
- [Field reference](artifact/references/fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-aware CLI output handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires kuaidi100-cli or kd100 on PATH; authenticated shipping and order workflows require SSO login.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
