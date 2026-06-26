## Description: <br>
Adds a new Telegram bot agent to an OpenClaw configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoxiaowei2117](https://clawhub.ai/user/gaoxiaowei2117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect Telegram bot agent details, update OpenClaw configuration, create an agent workspace, and restart OpenClaw after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens and allowed user IDs are sensitive configuration values. <br>
Mitigation: Use a dedicated bot token, restrict allowFrom to trusted Telegram user IDs, and avoid exposing real tokens in logs, screenshots, or chat. <br>
Risk: Editing openclaw.json incorrectly can break existing OpenClaw agents or bindings. <br>
Mitigation: Confirm the OpenClaw config path, back up openclaw.json before editing, and review the generated agent, binding, and Telegram account entries before restarting OpenClaw. <br>
Risk: New agent workspaces may share state if configured carelessly. <br>
Mitigation: Prefer an isolated workspace for the new agent and confirm memory isolation requirements before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gaoxiaowei2117/openclaw-add-agent) <br>
- [Publisher profile](https://clawhub.ai/user/gaoxiaowei2117) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides step-by-step OpenClaw configuration guidance and examples for Telegram bot bindings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
