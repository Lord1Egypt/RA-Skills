## Description:

Content moderation plugin for OpenClaw/Moltbot AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegdsks](https://clawhub.ai/user/thegdsks)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add profanity detection and moderation behavior to OpenClaw or Moltbot chat agents across Discord, Slack, Telegram, and similar chat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated moderation actions can delete messages, block users, or ban repeat offenders before moderators verify detection quality.

Mitigation: Start with warn, censor, or log-only modes, test against representative chat data, and require moderator review plus a reversal process before enabling deletes or bans.

Risk: Moderator notifications and logs may expose user, channel, and violation details.

Mitigation: Limit bot permissions, restrict log access, define retention limits, and treat moderation records as sensitive workspace data.

Risk: The package is installed from npm and no server-resolved provenance is available for this release.

Mitigation: Pin the dependency version and audit the npm package before installing it in a production chat workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thegdsks/skills/openclaw-profanity)
- [npm package](https://www.npmjs.com/package/openclaw-profanity)
- [Core library docs](https://www.typeweaver.com/docs/glin-profanity)
- [Referenced GitHub package path](https://github.com/GLINCKER/glin-profanity/tree/release/packages/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples and npm installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include moderation actions such as warn, censor, block, log, or custom violation handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
