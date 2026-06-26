## Description: <br>
This skill helps an agent operate HubSpot by reading, searching, creating, and updating CRM data through an OOMOL-connected HubSpot account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external operators, and developers use this skill to let an agent read, search, create, and update HubSpot CRM records through an OOMOL-connected HubSpot account. It is suited to contact, company, deal, and property-definition workflows where the agent should inspect the live action schema before running a connector action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HubSpot write actions can create or update CRM records. <br>
Mitigation: Confirm the exact action, target records, payload, and expected effect with the user before running create or update actions. <br>
Risk: The optional oo CLI installer runs a remote install script. <br>
Mitigation: Use the official install guide or review the installer script before running it, especially in managed environments. <br>
Risk: Connector access depends on the connected HubSpot account, scopes, credentials, and billing status. <br>
Mitigation: Run setup or reconnection steps only after an auth, scope, credential, app, or billing error identifies the required remediation. <br>


## Reference(s): <br>
- [HubSpot homepage](https://www.hubspot.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [HubSpot connection page](https://console.oomol.com/app-connections?provider=hubspot) <br>
- [HubSpot icon metadata](https://static.oomol.com/logo/third-party/HubSpot.svg) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-hubspot) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects containing data and meta.executionId when actions are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
