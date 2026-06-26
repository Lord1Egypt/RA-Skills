## Description: <br>
NeverDie helps OpenClaw stay available by checking provider-diverse LLM fallbacks, deploying a local Node.js monitor, and optionally alerting through Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephtandle](https://clawhub.ai/user/josephtandle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to assess LLM fallback diversity, install a recurring local failure monitor, and configure optional alerts for provider outages or authentication failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Telegram alert path stores a bot token locally and sends outbound requests when configured. <br>
Mitigation: Use a dedicated Telegram bot, protect .neverdie-config.json, and leave Telegram unset when file-only local alerts are sufficient. <br>
Risk: The monitor is designed to run as a recurring local job and may continue running after it is no longer needed. <br>
Mitigation: Review the installed cron job and use the provided uninstall command when monitoring should be removed. <br>
Risk: Local alert files can contain operational log details even though Telegram messages are limited to fixed strings. <br>
Mitigation: Keep alert files local, avoid sharing them without review, and rely on the skill's diagnostic path that only outputs model IDs and provider names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/josephtandle/neverdie) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with JSON and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local OpenClaw monitor, cron, state, alert, and NeverDie configuration files when the user chooses setup actions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
