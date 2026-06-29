## Description: <br>
BTCPay Server lets an agent read, create, and update BTCPay Server data through the OOMOL btcpay_server connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate BTCPay Server stores and invoice workflows from an agent, including store lookup, invoice creation, invoice listing, metadata updates, and manual invoice status changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change BTCPay Server invoice state or metadata. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before running actions tagged as write. <br>
Risk: Connector access depends on signed-in OOMOL credentials, an active BTCPay Server connection, and available billing credit. <br>
Mitigation: Use the documented first-time setup and retry steps only after an action fails with the matching authentication, connection, scope, expiration, app, or billing error. <br>


## Reference(s): <br>
- [BTCPay Server homepage](https://btcpayserver.org) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-btcpay-server) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return connector JSON responses when actions are executed with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
