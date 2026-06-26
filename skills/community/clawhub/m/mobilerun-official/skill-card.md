## Description: <br>
Give an OpenClaw agent control of a real Android phone through the official Mobilerun API, including screenshots, UI tree reading, taps, swipes, typing, and app management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PeLae1](https://clawhub.ai/user/PeLae1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to let an agent operate Android apps on a personal or cloud device for testing, data collection, social media workflows, or other phone tasks the user would otherwise perform manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent and Mobilerun observe and control a real Android phone, including screenshots, the accessibility tree, text entry, app navigation, and app management. <br>
Mitigation: Use a non-sensitive device or screen where possible, supervise sessions, and disconnect the Portal app when the task is complete. <br>
Risk: Phone automation can perform sensitive or destructive actions such as posting content, making purchases, changing accounts, entering private text, or installing and uninstalling apps. <br>
Mitigation: Require explicit user approval before sensitive account changes, purchases, public posts, private text entry, or app installation and removal. <br>
Risk: Access depends on a Mobilerun API key that can control the user's connected devices. <br>
Mitigation: Store the API key only in MOBILERUN_API_KEY, avoid exposing it in prompts or logs, and revoke or rotate it from the Mobilerun dashboard when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PeLae1/mobilerun-official) <br>
- [Mobilerun API Base URL](https://api.mobilerun.ai/v1) <br>
- [Mobilerun API Keys](https://cloud.mobilerun.ai/api-keys) <br>
- [Droidrun Portal APK](https://droidrun.ai/portal) <br>
- [Mobilerun Billing](https://cloud.mobilerun.ai/billing) <br>
- [Setup Guide](setup.md) <br>
- [Phone Control API Reference](phone-api.md) <br>
- [Platform API Reference](api.md) <br>
- [Plans and Subscriptions](subscription.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with REST API request patterns and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOBILERUN_API_KEY and a ready Android device connected through Mobilerun.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
