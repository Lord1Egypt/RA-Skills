## Description: <br>
Manage AI-built websites via NiceBox OpenClaw API. Supports article publishing, viewing messages, and checking site status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ravchen](https://clawhub.ai/user/ravchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to manage a NiceBox-hosted website from an agent workflow, including publishing articles, listing inbound messages or leads, and checking site status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AIBOX_API_KEY to authenticate live NiceBox API requests. <br>
Mitigation: Keep AIBOX_API_KEY private and avoid exposing command output or logs that could reveal credentials or sensitive request context. <br>
Risk: Article publishing can change a live website. <br>
Mitigation: Review title, content, summary, author, cover URL, and publish status before running the publishing script. <br>
Risk: Listed messages or leads may contain sensitive user data. <br>
Mitigation: Treat message output as private data and avoid sharing or logging it unnecessarily. <br>
Risk: Overriding AIBOX_BASE_URL can send credentials and site data to a different endpoint. <br>
Mitigation: Use the default NiceBox endpoint unless the alternate base URL is trusted. <br>


## Reference(s): <br>
- [NiceBox OpenClaw API base URL](https://ai.nicebox.cn/api/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/ravchen/nicebox-site-manager) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text, JSON] <br>
**Output Format:** [Command-line instructions and formatted JSON responses from NiceBox API scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AIBOX_API_KEY; optional AIBOX_BASE_URL overrides the default NiceBox OpenClaw endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
