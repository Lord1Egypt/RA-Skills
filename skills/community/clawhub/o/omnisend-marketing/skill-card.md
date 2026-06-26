## Description: <br>
Manage contacts, campaigns, automations, and ecommerce marketing workflows in Omnisend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, ecommerce teams, and support agents use this skill to inspect Omnisend data, manage contacts, review campaigns and automations, and prepare customer-impacting marketing actions through a connected Omnisend account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-backed access to a connected Omnisend account, so tool use can expose or modify real marketing data. <br>
Mitigation: Install only when the user intends to connect Omnisend through ClawLink, and verify the active integration before calling Omnisend tools. <br>
Risk: Confirmed write actions can affect contacts, campaigns, automations, email, SMS, and live customer workflows. <br>
Mitigation: Preview and confirm the target resource and intended effect before create, update, delete, send, or automation-triggering actions. <br>


## Reference(s): <br>
- [Omnisend skill page](https://clawhub.ai/hith3sh/omnisend-marketing) <br>
- [Omnisend API Documentation](https://api-docs.omnisend.com/) <br>
- [Omnisend Integrations](https://www.omnisend.com/integrations/) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Omnisend account through ClawLink; write actions should be previewed and explicitly confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
