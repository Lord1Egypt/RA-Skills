## Description:

Step-by-step guide for integrating Moonshot AI (Kimi) and Kimi Code models into Clawdbot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evgyur](https://clawhub.ai/user/evgyur)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure Moonshot AI and Kimi Code providers in Clawdbot, set model aliases, verify connectivity, and troubleshoot authentication or model-listing issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe API-key handling could expose Moonshot or Kimi Code credentials through shell history, shared config files, logs, screenshots, or support transcripts.

Mitigation: Store keys in restricted environment files or a secret manager, avoid printing keys, and rotate any key that may have been exposed.

Risk: The connection test script sends a bearer token and a test prompt to Moonshot/Kimi endpoints.

Mitigation: Run the script only when comfortable sending that data to those endpoints, and prefer scoped or disposable credentials for testing.

## Reference(s):

- [Configuration Examples](references/config-examples.md)
- [Moonshot AI Documentation](https://platform.moonshot.cn/docs)
- [Kimi Code API](https://api.kimi.com/coding/docs)
- [Clawdbot Model Providers](https://docs.clawd.bot/concepts/model-providers)
- [ClawHub Skill Page](https://clawhub.ai/evgyur/skills/kimi-integration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider setup steps, model selection examples, and an optional shell script for endpoint testing.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
