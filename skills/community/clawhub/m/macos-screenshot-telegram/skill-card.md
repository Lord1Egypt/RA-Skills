## Description:

Take a screenshot on macOS and send it to Telegram when the user asks to capture their screen, take a screenshot, or send a screen capture to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoyin258](https://clawhub.ai/user/hoyin258)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to capture a macOS screen and send the image to a selected Telegram chat through a configured Telegram bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A full-screen screenshot may accidentally include sensitive information and be sent to the wrong Telegram destination.

Mitigation: Run only after an explicit send-to-Telegram request, confirm the destination chat ID, and prefer previewing or limiting the capture area before upload.

Risk: Telegram bot token handling may expose credentials during command execution.

Mitigation: Avoid passing the bot token in command-line arguments where possible, restrict the bot to an allowlisted chat, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hoyin258/skills/macos-screenshot-telegram)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for macOS screenshot capture and Telegram Bot API upload using a user-provided chat ID and OpenClaw profile.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
