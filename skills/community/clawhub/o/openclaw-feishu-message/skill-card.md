## Description: <br>
Send Feishu/Lark direct messages and work follow-ups from OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systransform88](https://clawhub.ai/user/systransform88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and workspace operators use this skill to resolve Feishu/Lark contacts, cache recipient identifiers, create 1:1 chats on request, and send bot-authored direct messages or work follow-up nudges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can use Feishu/Lark bot authority to search employees and send workplace messages without an enforced confirmation step. <br>
Mitigation: Install only for trusted publishers, configure the Feishu account explicitly, and set allowSend=false unless the runtime or operator provides a confirmation workflow. <br>
Risk: The release bundles and persists contact cache data containing recipient identifiers and contact details. <br>
Mitigation: Delete the bundled contact cache before use and avoid shared hosts where cached contact data could be exposed. <br>
Risk: Tenant policy, app visibility, and bot availability may still block delivery even when Feishu/Lark scopes are granted. <br>
Mitigation: Confirm required tenant scopes and delivery policy before relying on the skill for operational follow-ups. <br>


## Reference(s): <br>
- [API notes](references/api-notes.md) <br>
- [ClawHub skill listing](https://clawhub.ai/systransform88/openclaw-feishu-message) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Guidance] <br>
**Output Format:** [JSON-formatted text returned by the feishu_message tool, with Feishu/Lark messages sent through configured bot actions when sending is enabled.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return resolved contact identifiers, preview text, send results, or structured error details; dry_run actions return previews without sending.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
