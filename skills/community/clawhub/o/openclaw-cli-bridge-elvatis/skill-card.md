## Description: <br>
Bridge local AI CLIs + web browser sessions (Grok, Gemini, Claude.ai, ChatGPT) into OpenClaw as model providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homeofe](https://clawhub.ai/user/homeofe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to expose local AI CLIs, OAuth-backed Codex access, local inference, and authenticated browser sessions as OpenClaw model providers with slash commands for model switching, health checks, and session status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access local OAuth tokens and persistent browser session cookies. <br>
Mitigation: Install only when the publisher is trusted, protect local auth files and browser profiles, and avoid use on shared or sensitive machines. <br>
Risk: The local proxy and CLI bridge can execute local AI CLI subprocesses and modify OpenClaw provider configuration. <br>
Mitigation: Review configuration and auth-store changes before enabling, use a strong proxy API key, and restrict localhost access. <br>
Risk: Expired browser sessions can trigger automatic WhatsApp notifications to a fixed recipient. <br>
Mitigation: Remove or reconfigure the hard-coded WhatsApp recipient before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/homeofe/openclaw-cli-bridge-elvatis) <br>
- [Publisher profile](https://clawhub.ai/user/homeofe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with slash commands, configuration guidance, status messages, and local proxy responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch local CLI subprocesses, modify OpenClaw provider configuration, read local OAuth credentials, and use persistent browser profiles for web providers.] <br>

## Skill Version(s): <br>
2.8.1 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
