## Description: <br>
Manage OzBargain daily-deal automation in OpenClaw via cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laofangxose](https://clawhub.ai/user/laofangxose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, update, manually run, and troubleshoot OpenClaw cron jobs that filter OzBargain deals, deduplicate previously sent links, and deliver concise deal summaries to a selected chat destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled cron jobs may send deal summaries to an unintended chat destination if the channel or destination ID is wrong. <br>
Mitigation: Use only chat or group IDs you control, review the destination before enabling scheduled delivery, and verify delivery with OpenClaw run history. <br>
Risk: The workflow stores a local sent-link history file for deduplication. <br>
Mitigation: Choose a user-specific dedupe state path and confirm that the local file location is acceptable before scheduled runs. <br>
Risk: The cron prompt controls filtering, delivery, and deal-quality behavior. <br>
Mitigation: Review the cron prompt before enabling scheduled delivery and keep user-specific schedule, topic, language, and destination values configurable. <br>


## Reference(s): <br>
- [Prompt template](references/prompt-template.txt) <br>
- [ClawHub release page](https://clawhub.ai/laofangxose/ozbargain-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configurable prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw and user-provided schedule, destination, topic priority, language, and dedupe state path.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
