## Description: <br>
Outlook sidebar add-in that brings the full power of your OpenClaw agent into Microsoft Outlook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nachtsheim](https://clawhub.ai/user/nachtsheim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Outlook users use this skill to connect Microsoft Outlook with a local OpenClaw Gateway, chat with an agent about selected email, access agent tools, and draft replies from the Outlook sidebar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected Outlook email content may be sent to the local OpenClaw agent and any model providers configured behind that agent. <br>
Mitigation: Install only when the referenced project and configured providers are trusted, and review sensitive emails before using the sidebar. <br>
Risk: The Outlook add-in connects to a local Gateway and can expose agent tools from the email workflow. <br>
Mitigation: Keep the Gateway allowed origin limited to the exact localhost add-in URL and keep high-impact tools behind confirmation. <br>
Risk: Sideloading an Outlook manifest changes the Outlook client surface available to the add-in. <br>
Mitigation: Inspect the Outlook manifest before sideloading and keep the add-in development server bound to the expected local URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nachtsheim/outlook-addin) <br>
- [OpenClaw Outlook Add-in repository](https://github.com/nachtsheim/openclaw-outlook-addin) <br>
- [OpenClaw Outlook Add-in README](https://github.com/nachtsheim/openclaw-outlook-addin#readme) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
