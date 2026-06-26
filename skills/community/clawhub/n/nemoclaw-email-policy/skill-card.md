## Description: <br>
Enforce email safety policies at the network level with NemoClaw for production email agents, including NemoClaw setup, the Outlook preset, and policy enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure network-level controls for MCP-based email agents, especially Microsoft 365 and Outlook workflows. It helps enforce endpoint restrictions, recipient allowlists, and draft-first email handling for production agent deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides configuration for email agents that may use OAuth tokens and access sensitive mailbox data. <br>
Mitigation: Review requested permissions at install and runtime, and grant only the mailbox, Microsoft Graph, and filesystem access needed for the intended workflow. <br>
Risk: The Outlook preset allows POST requests to Microsoft Graph endpoints, which can include send operations. <br>
Mitigation: Use an email-agent-mcp recipient allowlist or a stricter custom NemoClaw policy when send operations should be blocked or limited. <br>
Risk: Incorrect network policy changes can block required OAuth refresh, mail, calendar, or Outlook endpoints. <br>
Mitigation: Verify the active policy with NemoClaw tooling and test allowed and blocked endpoints before relying on the policy in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/nemoclaw-email-policy) <br>
- [email-agent-mcp GitHub repository](https://github.com/UseJunior/email-agent-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review before applying email, OAuth, or network policy changes.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
