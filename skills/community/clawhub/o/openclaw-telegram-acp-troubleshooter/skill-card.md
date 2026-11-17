## Description:

Diagnoses why Telegram forum topics do not reliably route into OpenClaw ACP sessions backed by codex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grey0758](https://clawhub.ai/user/grey0758)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose unreliable Telegram forum-topic routing into OpenClaw ACP sessions backed by codex. It helps distinguish Telegram delivery, gateway health, routing configuration, token, poller, and ACP execution issues before recommending the next action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostics may expose sensitive OpenClaw command logs, codex session files, bot identifiers, tokens, group IDs, or message bodies.

Mitigation: Inspect only the relevant time window and topic/session, redact raw values before sharing diagnostics, and avoid revealing secret values from environment variables, 1Password, or configuration.

Risk: Recommended actions can affect service behavior, such as removing or re-adding the bot, promoting it to admin, or restarting the gateway.

Mitigation: Confirm with the operator before taking service-impacting actions and retest the same Telegram topic after each change.

Risk: Premature source changes could address the wrong failure class when Telegram delivery or routing has not been verified.

Mitigation: Verify gateway health, routing bindings, command logs, and session files before recommending source-level Telegram plugin investigation.

## Reference(s):

- [OpenClaw ClawHub documentation](https://docs.openclaw.ai/tools/clawhub)
- [ClawHub skill page](https://clawhub.ai/grey0758/skills/openclaw-telegram-acp-troubleshooter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown response with an ordered conclusion, evidence, next best action, and follow-up test; may include inline shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Troubleshooting guidance is ordered by probability and constrained to avoid exposing secrets.]

## Skill Version(s):

1.0.1 (source: server release metadata and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
