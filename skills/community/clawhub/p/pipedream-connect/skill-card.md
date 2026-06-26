## Description: <br>
Connect OpenClaw agents to thousands of apps via Pipedream Connect with per-agent OAuth isolation, first-class MCP tool exposure, live connected-account discovery, and dynamic full-catalog browsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up, maintain, and troubleshoot OpenClaw's Pipedream Connect integration. It guides per-agent OAuth app connections, dynamic app catalog handling, first-class MCP tool exposure, and related configuration checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful Pipedream credentials and OAuth access tokens. <br>
Mitigation: Install only when OpenClaw agents need Pipedream app access, protect ~/.openclaw/secrets.json and mcporter configuration files, and restrict access to the Pipedream dashboard. <br>
Risk: Optional token-refresh cron setup can create ongoing background token refresh behavior. <br>
Mitigation: Run the cron setup only when persistent background refresh is required, review the generated cron entry, and remove it when no longer needed. <br>
Risk: Gateway RPCs can connect, activate, test, and disconnect Pipedream app integrations. <br>
Mitigation: Review which users and agents can call the Pipedream gateway methods before enabling the integration in shared environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/pipedream-connect) <br>
- [Installation Guide](artifact/INSTALL.md) <br>
- [Reference Implementation](artifact/reference/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include configuration paths, validation checklists, troubleshooting steps, and code reference pointers.] <br>

## Skill Version(s): <br>
1.6.0 (source: server evidence and changelog, released 2026-03-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
