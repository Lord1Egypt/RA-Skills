## Description: <br>
Notice Monitor monitors configured website announcement pages, filters notices by keywords and categories, deduplicates results, and can send scheduled notification reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryharbin](https://clawhub.ai/user/jerryharbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor procurement, government, education, medical, IT, or other announcement sites and receive filtered notice summaries on a schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DingTalk notification handling can execute local shell commands influenced by scraped website text or configuration values. <br>
Mitigation: Run the skill in an isolated environment and avoid enabling DingTalk notifications or cron until notifier shell interpolation is fixed. <br>
Risk: Example notification targets and monitored sites may expose messages or credentials to unintended recipients if reused unchanged. <br>
Mitigation: Replace example DingTalk targets, monitor only trusted sites, and treat webhook credentials or notification targets as sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jerryharbin/notice-monitor) <br>
- [README](artifact/README.md) <br>
- [Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text notice reports with YAML configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can persist local deduplication state and send DingTalk notifications when configured] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
