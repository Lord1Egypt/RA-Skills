## Description: <br>
Monitors OpenRouter free models for expiration notices and new model discovery, with optional scheduled Feishu summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suidge](https://clawhub.ai/user/suidge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor configured OpenRouter free models, detect upcoming removals, discover newly free endpoints, and produce concise summaries or Feishu notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local OpenClaw model configuration and write a local status file. <br>
Mitigation: Review configured paths before use and run dry-run or no-notify mode first when validating behavior. <br>
Risk: The optional bb-browser fallback can start Chrome with remote debugging on port 9222. <br>
Mitigation: Prefer API-only operation when possible, avoid shared machines for remote-debugging runs, and close any Chrome process started with remote debugging after use. <br>
Risk: Feishu notifications can be sent to the configured target. <br>
Mitigation: Verify the Feishu target and cron delivery settings before enabling scheduled runs; use no-notify mode for cron delivery to avoid duplicate messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suidge/openrouter-free-helper) <br>
- [Cron task reference](references/cron-task.md) <br>
- [OpenRouter page structure reference](references/openrouter-structure.md) <br>
- [OpenRouter frontend models API](https://openrouter.ai/api/frontend/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown summaries with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a local JSON status file and can send Feishu messages when configured; supports dry-run and no-notify modes.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
