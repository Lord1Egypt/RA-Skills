## Description:

Send and receive SMS/RCS via Google Messages web interface (messages.google.com). Use when asked to "send a text", "check texts", "SMS", "text message", "Google Messages", or forward incoming texts to other channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kesslerio](https://clawhub.ai/user/kesslerio)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and OpenClaw users use this skill to automate Google Messages for Web, including sending texts, checking conversations, and optionally forwarding incoming SMS/RCS notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private SMS/RCS content and can forward message previews outside Google Messages.

Mitigation: Use it only with conversations approved for forwarding, set notification targets deliberately, and keep paired browser sessions private.

Risk: The supplied security evidence reports a serious command-injection risk in webhook forwarding.

Mitigation: Do not run the current webhook server with real forwarding targets until the webhook command construction is fixed and reviewed.

Risk: Persistent notification forwarding can expose incoming messages continuously.

Mitigation: Avoid enabling persistent notification services unless the security issues are resolved and the forwarding destination is trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kesslerio/skills/google-messages)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Google Messages for Web](https://messages.google.com/web)
- [Observer Injection](references/observer-injection.md)
- [JavaScript Snippets](references/snippets.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with browser automation commands, shell commands, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser automation, Node.js, Google Messages pairing, and optional notification environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
