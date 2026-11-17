## Description:

Multi-Platform AI Feed queries Kuaishou, WeChat Official Accounts, Bilibili, WeChat Channels, and Xiaohongshu for trending AI content, clusters topics, compares cross-platform activity, and generates a local report with investigation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

AI researchers, intelligence analysts, content operators, and brand or marketing teams use this skill to monitor AI-related trends across five Chinese content platforms, compare topic momentum, and obtain structured investigation guidance before acting on the findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and the security evidence says the subscription feature can expose or mishandle that key.

Mitigation: Use a scoped, revocable API key, avoid hardcoding or logging it, and rotate the key if it may have been exposed.

Risk: The subscription feature creates persistent scheduled tasks and the security evidence flags crontab shell construction and macOS plaintext API-key persistence.

Mitigation: Prefer one-off runs and avoid the subscription feature until those issues are fixed; if subscription was enabled, review and remove the scheduled task before deployment.

Risk: The investigation templates can be misused for personal background checks or reputational profiling.

Mitigation: Use investigation workflows only for lawful, consented, and clearly bounded purposes, and review outputs before sharing or taking action.

Risk: The skill creates local reports that may contain platform content, metrics, and investigation notes.

Mitigation: Store generated reports in an access-controlled location and review report contents before distributing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/multi-ai-feed)
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub)
- [Platform API contracts](references/platforms.md)
- [Investigation modes](references/investigation-modes.md)
- [Investigation templates](references/investigation-templates.md)
- [Engine strategy](references/engine-strategy.md)
- [Investigator configuration](references/investigator-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance]

**Output Format:** [Structured conversational report, optional normalized JSON, and local HTML daily report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a REDFOX_API_KEY credential, writes reports under a local output directory by default, and can install a daily subscription task when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
