## Description: <br>
One-prompt Facebook Page AI setup that helps connect Pages, detect business type, and load industry-specific skills through PageClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[proship1](https://clawhub.ai/user/proship1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and page operators use this skill to connect a Facebook Page to PageClaw, select a page, confirm a business type, and activate relevant page-management skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Page OAuth and page data access are delegated to PageClaw. <br>
Mitigation: Verify the requested Facebook OAuth permissions and confirm how access can be revoked before installing. <br>
Risk: The skill can guide public-facing posts or customer replies after remote skill prompts are loaded. <br>
Mitigation: Require explicit human approval before publishing posts or sending customer replies. <br>
Risk: Customer conversations and page data may be handled by PageClaw/OneChat. <br>
Mitigation: Confirm storage, sharing, and retention practices before connecting a production page. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/proship1/pageclaw-onechat) <br>
- [PageClaw](https://pageclaw.onechat.ai) <br>
- [OneChat.ai](https://onechat.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Conversational text with setup links and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides OAuth-based page connection, business-type confirmation, and skill activation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
