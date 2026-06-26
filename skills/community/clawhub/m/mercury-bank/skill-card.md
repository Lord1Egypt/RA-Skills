## Description: <br>
Mercury bank API for Digital 4 Jesus LLC (US entity). Use when the user asks about Mercury account balances, transactions, invoices, customers, or sending money. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GodsBoy](https://clawhub.ai/user/GodsBoy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Authorized operators of the Digital 4 Jesus LLC Mercury business account use this skill to inspect balances, transactions, invoices, customers, recipients, and organization details, and to prepare account actions through Mercury API commands. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a live Mercury banking API token and can change financial records. <br>
Mitigation: Install only when authorized for this exact Mercury business account, use a least-privilege token, and require manual review before invoice, customer, or payment actions. <br>
Risk: Untrusted text passed into invoice commands may affect generated API payloads. <br>
Mitigation: Avoid feeding untrusted text into invoice commands until argument handling is fixed. <br>
Risk: The local secrets file contains sensitive credentials. <br>
Mitigation: Keep the secrets file private and restrict access to the Mercury API token. <br>


## Reference(s): <br>
- [Mercury API Reference](references/api.md) <br>
- [Mercury API](https://api.mercury.com/api/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/GodsBoy/mercury-bank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Mercury API token and a local secrets file before commands can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
