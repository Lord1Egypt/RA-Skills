## Description: <br>
Send and receive SMS/RCS via Google Messages web interface (messages.google.com). Use when asked to "send a text", "check texts", "SMS", "text message", "Google Messages", or forward incoming texts to other channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kesslerio](https://clawhub.ai/user/kesslerio) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users and developers use this skill to automate Google Messages for Web through an agent, including pairing, sending SMS/RCS messages, checking conversations, and optionally forwarding incoming message previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SMS notification webhook can execute shell commands built from message content. <br>
Mitigation: Review before installing and do not enable the webhook or persistent service unless shell-based forwarding is replaced with argument-based command invocation. <br>
Risk: Forwarded SMS previews may include private conversations, account recovery links, or one-time codes. <br>
Mitigation: Use a dedicated browser profile, pair only on a trusted machine, and forward previews only to channels approved for sensitive message content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kesslerio/google-messages) <br>
- [Observer Injection](references/observer-injection.md) <br>
- [JavaScript Snippets](references/snippets.md) <br>
- [Google Messages Web](https://messages.google.com/web) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser automation, Node.js, a paired Google Messages web session, and optional notification environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
