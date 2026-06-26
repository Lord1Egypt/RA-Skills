## Description: <br>
PromptDome integrates prompt-injection screening into OpenClaw by installing an automatic incoming-message hook and an optional promptdome_scan agent tool for untrusted content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tschew72](https://clawhub.ai/user/tschew72) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use PromptDome to add automatic prompt-injection screening to incoming messages and to give agents a callable scan tool for external or untrusted content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incoming messages and manually scanned content are sent to PromptDome or the configured self-hosted endpoint. <br>
Mitigation: Install only when that data flow is acceptable for the workspace, and review endpoint configuration before enabling the hook or agent tool. <br>
Risk: The integration stores PROMPTDOME_API_KEY locally and writes scan logs that may include sensitive snippets. <br>
Mitigation: Use a dedicated revocable API key, protect ~/.openclaw/openclaw.json and ~/.openclaw/logs, and periodically remove logs that may contain sensitive content. <br>
Risk: The hook fails open when the PromptDome API is unreachable or returns an error, so messages may pass without a warning during outages. <br>
Mitigation: Monitor scan failures and logs, and use a reliable configured endpoint when stronger availability is required. <br>


## Reference(s): <br>
- [PromptDome documentation](https://promptdome.cyberforge.one/docs) <br>
- [PromptDome API key dashboard](https://promptdome.cyberforge.one/dashboard/api-keys) <br>
- [PromptDome ClawHub release page](https://clawhub.ai/tschew72/promptdome) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; the agent tool returns text summaries and JSON scan results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PROMPTDOME_API_KEY and network access to the configured PromptDome endpoint; scans up to 50,000 characters per request.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
