## Description: <br>
儿童积分管理助手 - 语意识别，自动记账，跨 Session 数据一致 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cowboy231](https://clawhub.ai/user/cowboy231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and families use this OpenClaw agent skill to record children's earned points, expenses, balances, logs, and optional daily reports from natural-language messages, audio, or image attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child-related text may be sent to third-party processing and messaging services. <br>
Mitigation: Review the external processing paths before use, require explicit user configuration for MiniMax, SenseAudio, and Feishu, and avoid sending sensitive child details unless the destination is approved. <br>
Risk: The release includes hardcoded credentials and fixed Feishu destinations. <br>
Mitigation: Remove embedded credentials, rotate any exposed keys, and require all API keys and chat destinations to be supplied through user-controlled configuration. <br>
Risk: Shell-based ASR/TTS execution paths may be unsafe. <br>
Mitigation: Disable or patch shell execution for voice features before deployment, and validate or safely pass all text and attachment paths. <br>
Risk: Local logs, reports, and archives can contain children's activity details. <br>
Mitigation: Store generated files in protected locations, limit retention, and purge logs, reports, audio, and image archives when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cowboy231/kids-points) <br>
- [Publisher profile](https://clawhub.ai/user/cowboy231) <br>
- [SenseAudio](https://senseaudio.cn) <br>
- [README.md](artifact/README.md) <br>
- [CRON.md](artifact/CRON.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses, local JSON records, log files, report files, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write balance, request, log, archive, audio, and daily-report files under the configured workspace and /tmp paths.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata; package.json reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
