## Description: <br>
Forwards state, action, or historical user requests with text prompts to a configured n8n_dispatch MCP service and returns its response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enchantedmotorcycle](https://clawhub.ai/user/enchantedmotorcycle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to route OpenClaw requests into an existing n8n workflow for status checks, actions, or historical queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts are sent to the configured n8n_dispatch service, which may expose sensitive data to the workflow. <br>
Mitigation: Send secrets or sensitive personal data only when the n8n workflow is intended and authorized to receive it. <br>
Risk: The configured n8n workflow may perform real-world actions for action requests. <br>
Mitigation: Add n8n-side validation and confirmation gates before workflows execute actions. <br>
Risk: An untrusted or unprotected n8n_dispatch endpoint could receive or alter dispatched requests. <br>
Mitigation: Register only a trusted local or protected HTTPS endpoint that the user controls. <br>


## Reference(s): <br>
- [N8n Dispatch ClawHub page](https://clawhub.ai/enchantedmotorcycle/n8n-dispatch) <br>
- [Publisher profile](https://clawhub.ai/user/enchantedmotorcycle) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forwards a requestType and text prompt to a configured n8n_dispatch MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
