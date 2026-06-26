## Description: <br>
Connects agents to SaaS tools through Maton AI with Clawdbot Gateway UI integration for API key setup, OAuth app connection, and connection management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure Maton in Clawdbot Gateway, connect SaaS applications through OAuth, and manage those app connections from the gateway UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Maton API key and manages OAuth connections to SaaS accounts. <br>
Mitigation: Install only if you trust Maton with connected SaaS accounts, rotate the Maton API key, and review or remove unused app connections regularly. <br>
Risk: Starting OAuth flows or deleting connections can change access to external SaaS tools. <br>
Mitigation: Confirm the selected app and connection before authorizing OAuth flows or deleting existing connections. <br>


## Reference(s): <br>
- [Maton Reference Implementation](reference/README.md) <br>
- [Maton](https://maton.ai) <br>
- [Maton API base URL](https://ctrl.maton.ai) <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/maton-agent-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Code, Shell commands] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reference implementation files for Clawdbot Gateway UI and Maton API integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
