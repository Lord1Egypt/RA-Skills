## Description: <br>
Install and configure the OpenClaw Zulip channel plugin from npm. Use when OpenClaw needs to add Zulip support, switch from a local path install to the published npm package, validate Zulip plugin health, or help a user configure Zulip bot credentials, streams, DM policy, and stream behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ftlc-ian](https://clawhub.ai/user/ftlc-ian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install the published Zulip channel plugin, configure Zulip bot credentials and stream/DM behavior, and verify plugin health after deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Zulip bot credentials and OpenClaw configuration can expose chat access if handled casually. <br>
Mitigation: Use least-privilege credentials and store secrets only in supported OpenClaw config or environment mechanisms, not in chat. <br>
Risk: Installing or changing the channel plugin in an untrusted repository context can affect gateway behavior. <br>
Mitigation: Install only in a trusted ClawHub/Convex repo context and verify changes with gateway restart, doctor checks, and smoke tests. <br>
Risk: Moderation, review, or broad access settings may allow unintended messages or reviewers. <br>
Mitigation: Review moderation commands and access policies before approving them, and consider disabling full-access autoreview or external fallback reviewers for sensitive code. <br>


## Reference(s): <br>
- [OpenClaw Zulip Channel on ClawHub](https://clawhub.ai/ftlc-ian/openclaw-zulip-channel) <br>
- [Publisher profile: ftlc-ian](https://clawhub.ai/user/ftlc-ian) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, configuration, credential-handling, and verification guidance.] <br>

## Skill Version(s): <br>
2026.4.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
