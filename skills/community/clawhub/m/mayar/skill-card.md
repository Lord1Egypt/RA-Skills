## Description: <br>
Interact with the Mayar payment platform for invoices, products, payments, customers, transactions, webhooks, and QR codes from an AI agent or shell. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayar](https://clawhub.ai/user/mayar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through authenticated Mayar CLI workflows for payment account operations, including listing, creating, closing, reopening, and registering payment resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad authority to modify payment account resources through the Mayar CLI. <br>
Mitigation: Require explicit user confirmation before creating, closing, reopening, or registering resources in a real payment account. <br>
Risk: The skill invokes an unpinned CLI package with npx -y mayar@latest. <br>
Mitigation: Prefer a pinned Mayar CLI version before production use. <br>
Risk: The skill requires a sensitive Mayar API key. <br>
Mitigation: Use a least-privileged or test API key where possible and avoid passing keys on the command line. <br>


## Reference(s): <br>
- [Mayar ClawHub Skill Page](https://clawhub.ai/mayar/mayar) <br>
- [Mayar CLI Homepage](https://github.com/mayarid/mayar-cli) <br>
- [Mayar Web Dashboard](https://web.mayar.id) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands rely on a Mayar API key and may return JSON when invoked with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
