## Description: <br>
Patch OpenClaw to support Microsoft Teams China through endpoint diagnosis, OpenClaw and MSTeams plugin patching, China cloud configuration, and verification reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhs666](https://clawhub.ai/user/yhs666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw Microsoft Teams China integrations use this skill to diagnose authentication, Graph API, Bot Framework, and SSRF endpoint problems, then apply and verify the adapter repair workflow. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically rewrite installed OpenClaw and @openclaw/msteams code. <br>
Mitigation: Review the scripts before use, run only on hosts intended for Microsoft Teams China support, and back up or be ready to reinstall the affected packages. <br>
Risk: The skill can persist CLOUD and SERVICE_URL environment changes. <br>
Mitigation: Verify the HKCU, HKLM, or shell profile environment changes after use and remove them if the host should not target Microsoft Teams China endpoints. <br>
Risk: Heartbeat or cron auto-repair can perform unattended code changes and gateway restarts. <br>
Mitigation: Avoid unattended auto-repair unless unattended package changes and OpenClaw gateway restarts are acceptable for the deployment. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Endpoint Reference](references/endpoints.md) <br>
- [Error Code Reference](references/error-codes.md) <br>
- [Workflow Reference](references/workflow.md) <br>
- [Output Standards](references/output-standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and structured report tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide code patching, environment variable changes, and gateway restarts for the installed OpenClaw and MSTeams integration.] <br>

## Skill Version(s): <br>
10.0.2 (source: server release metadata; artifact _meta.json and CHANGELOG.md report 10.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
