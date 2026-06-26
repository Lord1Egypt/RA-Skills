## Description: <br>
Provides HoneyBook client-portal MCP workflows for checking vendor contracts, invoices, proposals, payment methods, and user-confirmed sign or pay deep links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents working with HoneyBook client-portal data use this skill to review wedding-vendor contracts, invoices, proposals, sessions, and payment status, and to obtain portal deep links for user-confirmed signing or payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Magic links and the local HoneyBook session cache can function like login credentials. <br>
Mitigation: Install only on a trusted personal machine, treat magic links and ~/.honeybook-mcp/sessions.json as credentials, and delete the session cache when retained access is no longer needed. <br>
Risk: The skill can surface contracts, invoices, payment-method metadata, and sign or pay links tied to financial actions. <br>
Mitigation: Review returned details before acting; signing and payment flows require explicit confirmation and complete in the browser with device or SCA handling. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured MCP tool outputs with setup snippets, status summaries, and deep links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May expose sensitive HoneyBook contract, invoice, payment-method, and session information to the agent.] <br>

## Skill Version(s): <br>
0.3.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
