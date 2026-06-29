## Description: <br>
Operate Shipday delivery-order workflows through the OOMOL Shipday connector using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams that use Shipday can ask an agent to inspect action schemas and run delivery-order workflows, including creating, editing, retrieving, deleting, tracking progress, and listing active orders or carriers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Create, edit, and delete actions can change live Shipday order data. <br>
Mitigation: Confirm the exact payload, target order, and intended effect with the user before running write or destructive actions. <br>
Risk: The skill requires a connected Shipday account and API-key-backed credentials. <br>
Mitigation: Use a Shipday API key with the minimum permissions needed and reauthenticate or reconnect only after an auth, scope, or credential error. <br>
Risk: Connector schemas or required payload fields may change over time. <br>
Mitigation: Inspect the live action schema with the oo CLI before constructing payloads for connector actions. <br>


## Reference(s): <br>
- [ClawHub Shipday skill page](https://clawhub.ai/oomol/oo-shipday) <br>
- [Shipday homepage](https://www.shipday.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL Shipday connection setup](https://console.oomol.com/app-connections?provider=shipday) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands run through the oo CLI and may return JSON responses from Shipday connector actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
