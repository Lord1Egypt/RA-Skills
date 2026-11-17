## Description:

Tracks trending Douyin short drama content, clusters results by genre, and generates local HTML daily reports with engagement data and creative insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, MCN operators, and content analysts use this skill to monitor Douyin short drama trends, identify high-engagement genres and creators, and produce recurring local reports for topic research and operations planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted remote API content is written into generated HTML reports without escaping.

Mitigation: Install only if the RedFoxHub data source is trusted, review generated reports before sharing them, and avoid opening reports in highly privileged browser sessions until report generation is hardened.

Risk: The skill requires a RedFoxHub API key and contacts redfox.hk.

Mitigation: Use a revocable key with the minimum practical scope, keep it in REDFOX_API_KEY, and rotate it if it is exposed in logs, prompts, or output files.

Risk: The skill creates local cache and report files and opens generated reports in the browser.

Mitigation: Run it under a normal user account, inspect the configured output directory, and clear local cache or reports when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/playlet-douyin-feed)
- [Core workflow](artifact/references/core_workflow.md)
- [Usage examples](artifact/references/examples.md)
- [RedFoxHub](https://redfox.hk/)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?souce=github)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown trend summary with shell commands and generated local HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY, writes local cache and report files, and may open generated reports in the user's browser.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
