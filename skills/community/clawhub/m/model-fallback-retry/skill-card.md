## Description: <br>
Detects large-language-model quota, rate-limit, and overload failures, queues the original message, and retries delivery with exponential backoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hehe973781230](https://clawhub.ai/user/hehe973781230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to reduce message loss when model calls fail because of rate limits, quota exhaustion, or temporary service overload. It captures retryable failures, tracks queued messages, and sends due retries back to the original session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Failed prompts and model responses may be written to local plaintext JSON queue and log files. <br>
Mitigation: Review the queue and log storage locations, restrict local file permissions, and disable or reduce verbose logging where possible. <br>
Risk: Queued conversation content may be automatically resent by the retry job. <br>
Mitigation: Install only for sessions where automatic replay is acceptable, review retry limits and intervals, and monitor queued items before enabling scheduled retries. <br>
Risk: The clear command can remove queued retry work. <br>
Mitigation: Limit command access to trusted users and confirm queued item status before using bulk clear operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hehe973781230/model-fallback-retry) <br>
- [README.md](README.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>
- [Plugin manifest](plugin/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When installed, the plugin maintains local JSON queue and log files for retry tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact package.json, and CHANGELOG.md released 2026-06-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
