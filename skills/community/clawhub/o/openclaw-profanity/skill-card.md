## Description: <br>
Content moderation plugin for OpenClaw/Moltbot AI agents. Use when building chatbots that need profanity filtering, moderating user messages in Discord/Slack/Telegram bots, or adding content moderation to OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegdsks](https://clawhub.ai/user/thegdsks) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and bot operators use this skill to add profanity filtering and moderation behavior to OpenClaw or Moltbot agents for Discord, Slack, Telegram, and similar chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can trigger automatic moderation actions such as message deletion or bans. <br>
Mitigation: Configure moderation actions deliberately, test them before deployment, and keep bot permissions to the least privilege needed. <br>
Risk: Violation logging can expose user identifiers, flagged text, or other moderation records. <br>
Mitigation: Define retention, access, and review rules for violation logs before enabling logging in production. <br>
Risk: A mismatched npm package or repository could lead to installing unintended code. <br>
Mitigation: Verify the package and linked repository are the intended sources and pin the dependency version before deployment. <br>


## Reference(s): <br>
- [OpenClaw Profanity Plugin on ClawHub](https://clawhub.ai/thegdsks/openclaw-profanity) <br>
- [openclaw-profanity npm package](https://www.npmjs.com/package/openclaw-profanity) <br>
- [glin-profanity OpenClaw package](https://github.com/GLINCKER/glin-profanity/tree/release/packages/openclaw) <br>
- [Core library docs](https://www.typeweaver.com/docs/glin-profanity) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation commands, configuration options, moderation actions, and platform examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
