## Description: <br>
Chargebee operates an OOMOL-connected Chargebee account through the oo CLI for reading billing data and creating customer records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to work with Chargebee customer, invoice, item price, and subscription data through an OOMOL-connected account. It supports read actions and customer creation while requiring review before write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive billing and customer data from a connected Chargebee account. <br>
Mitigation: Install it only for intended OOMOL-connected Chargebee accounts and treat returned customer, invoice, pricing, and subscription data as sensitive. <br>
Risk: The create_customer action changes Chargebee account state. <br>
Mitigation: Review and confirm the exact customer payload and expected effect with the user before running the write action. <br>
Risk: First-time setup can involve running a remote oo CLI install command. <br>
Mitigation: Use an existing trusted oo CLI installation when available, or review the remote install source before running the install command. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-chargebee) <br>
- [Chargebee Homepage](https://www.chargebee.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector runs may return JSON responses containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
