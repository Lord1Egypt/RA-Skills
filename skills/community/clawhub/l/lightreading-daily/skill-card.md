## Description:

Fetches LightReading and TechCrunch technology news, prepares Chinese summaries, and sends the digest to Enterprise WeChat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophieliiiiii](https://clawhub.ai/user/sophieliiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and agents use this skill to collect current telecom and technology articles, prepare Chinese news summaries, and publish scheduled Enterprise WeChat digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shipped Enterprise WeChat webhook key could send messages to an unintended workspace or expose an existing integration.

Mitigation: Remove the bundled key, rotate it if it was ever valid, and configure a new webhook through a secret or environment variable.

Risk: The optional email webhook can expose a network listener without built-in authentication or request limits.

Mitigation: Avoid running the webhook unless it is bound to localhost or protected by authentication, request limits, and network access controls.

Risk: Automated scheduled publishing can distribute unreviewed or stale generated summaries.

Mitigation: Run the workflow in dry-run or manual mode first, review generated Chinese summaries, and restrict cron automation until the output is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sophieliiiiii/skills/lightreading-daily)
- [LightReading RSS feed](https://www.lightreading.com/rss.xml)
- [TechCrunch RSS feed](https://techcrunch.com/feed/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text summaries with Python scripts and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces generated news files and Enterprise WeChat payloads when executed.]

## Skill Version(s):

5.9.1 (source: server release metadata and SKILL.md version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
