## Description: <br>
Diagnose why Telegram forum topics do not reliably route into OpenClaw ACP sessions backed by codex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grey0758](https://clawhub.ai/user/grey0758) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot Telegram forum topic routing into OpenClaw ACP sessions backed by codex. It helps distinguish Telegram delivery, gateway health, routing, token, duplicate poller, and agent-binding issues before recommending the next best action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Log and session review may expose private Telegram messages, bot tokens, or configuration secrets. <br>
Mitigation: Review only relevant log and session entries, redact secrets and private messages before sharing, and follow the skill constraint not to reveal env, 1Password, or config values. <br>
Risk: A premature source-code patch could mask a Telegram delivery, gateway, token, duplicate poller, or routing problem. <br>
Mitigation: Exhaust the documented delivery, gateway health, command log, session proof, and routing checks before recommending source-level Telegram plugin investigation. <br>
Risk: Granting broad Telegram bot admin permissions can increase operational exposure. <br>
Mitigation: Grant admin permissions only when needed for the group and topic behavior being tested, then re-test the same topic with the documented verification checklist. <br>


## Reference(s): <br>
- [OpenClaw ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub) <br>
- [OpenClaw Telegram ACP Troubleshooter on ClawHub](https://clawhub.ai/grey0758/openclaw-telegram-acp-troubleshooter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Troubleshooting guidance] <br>
**Output Format:** [Markdown with ordered conclusions, evidence, next actions, verification checks, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese operator guidance; no standalone executable code.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
