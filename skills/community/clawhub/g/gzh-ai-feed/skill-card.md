## Description:

AI公众号信息源 scans AI WeChat public account articles, ranks hot content by read count, clusters articles into topics, and generates a styled HTML daily report with metrics, cover images, search, and subscription support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

AI professionals, content creators, and industry researchers use this skill to monitor popular AI WeChat public account articles, identify trending topics, and produce daily local HTML briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts redfox.hk using a RedFox API key.

Mitigation: Install and run it only when comfortable sending requests to RedFox, and verify the API key origin, scope, validity period, and reset or revocation support before use.

Risk: The subscription option installs a persistent daily scheduled task.

Mitigation: Avoid --subscribe unless persistent local scheduling is expected, and review or remove the installed launch agent or crontab entry when no longer needed.

Risk: Generated reports include remote article metadata in HTML.

Mitigation: Treat generated reports as untrusted local HTML and review content before sharing or opening in sensitive browser contexts.

Risk: API key handling and subscription command construction need review according to the security guidance.

Mitigation: Prefer environment-variable based key configuration, avoid hardcoding or logging keys, and do not use subscription with sensitive API keys until those issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/gzh-ai-feed)
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Terminal text plus local HTML report files and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save reports under ~/Downloads/QoderReports, start a localhost search proxy, and optionally install a daily scheduled subscription task.]

## Skill Version(s):

1.0.3 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
