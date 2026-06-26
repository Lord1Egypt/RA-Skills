## Description: <br>
Install PPQ.AI Private Mode for end-to-end encrypted AI inference in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattius459](https://clawhub.ai/user/mattius459) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to install the PPQ.AI Private Mode proxy, configure private encrypted model access, and restart the OpenClaw gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for a PPQ.AI API key and stores it in local OpenClaw plugin configuration. <br>
Mitigation: Treat the API key as sensitive, avoid exposing it in logs or screenshots, and confirm the destination configuration before saving. <br>
Risk: Restarting the OpenClaw gateway can interrupt active sessions. <br>
Mitigation: Back up ~/.openclaw/openclaw.json and restart the gateway only when interruption is acceptable. <br>
Risk: The setup installs a referenced third-party GitHub plugin. <br>
Mitigation: Install only if the user trusts PPQ.AI and the referenced plugin source. <br>


## Reference(s): <br>
- [PPQ.AI Private Mode Skill Page](https://clawhub.ai/mattius459/ppq-private-mode) <br>
- [PPQ.AI API Documentation](https://ppq.ai/api-docs) <br>
- [PPQ.AI](https://ppq.ai) <br>
- [PPQ Private Mode Proxy](https://github.com/PayPerQ/ppq-private-mode-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for a PPQ.AI API key and provides OpenClaw provider and plugin configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
