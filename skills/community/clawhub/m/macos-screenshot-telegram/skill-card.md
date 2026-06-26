## Description: <br>
Take a screenshot on macOS and send it to Telegram when the user asks to capture their screen or send a screen capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoyin258](https://clawhub.ai/user/hoyin258) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to capture a full macOS screenshot and deliver it to a specified Telegram chat through a configured Telegram bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill captures the full macOS screen and uploads the image to Telegram, which can expose private or sensitive visible information. <br>
Mitigation: Verify that no sensitive information is visible before running the skill and confirm that screen capture and Telegram upload are intended. <br>
Risk: A wrong chat ID or overly privileged bot token can send screenshots to an unintended recipient or broaden access to captured media. <br>
Mitigation: Confirm the target chat ID and profile before execution, use a dedicated low-privilege Telegram bot token, and rotate the token if exposure is suspected. <br>
Risk: The screenshot remains saved in the OpenClaw workspace after sending. <br>
Mitigation: Delete the workspace screenshot after use when it contains private information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoyin258/macos-screenshot-telegram) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a macOS screenshot file in the OpenClaw workspace and sends it through the Telegram Bot API.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
