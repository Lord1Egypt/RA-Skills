## Description: <br>
Slack integration - Send messages, manage channels, and automate Slack workflows <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukaizj](https://clawhub.ai/user/lukaizj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send Slack messages, list channels, and create Slack channels from an OpenClaw workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Slack bot token that grants access to workspace actions. <br>
Mitigation: Use a least-privilege bot token and store it as a protected environment variable. <br>
Risk: Tool calls can post real Slack messages and create real Slack channels. <br>
Mitigation: Review requested channel and message actions before execution in production workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lukaizj/lukaizj-slack) <br>
- [Skill homepage](https://github.com/lukaizj/slack-integration-skill) <br>
- [Slack app setup](https://api.slack.com/apps) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [JSON-like tool results with success flags, error messages, timestamps, channel IDs, or channel lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SLACK_BOT_TOKEN and can post messages or create channels in the connected Slack workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: claw.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
