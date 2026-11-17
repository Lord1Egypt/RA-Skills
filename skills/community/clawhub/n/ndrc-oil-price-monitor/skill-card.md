## Description:

Monitor NDRC (National Development and Reform Commission) website for oil price adjustment announcements, checking every 10 working days at 17:30 from 2026-04-07 and pushing notifications via Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manucode2000-max](https://clawhub.ai/user/manucode2000-max)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers use this skill to monitor China's NDRC news releases for refined oil price adjustment notices and receive scheduled Feishu/OpenClaw announcements. It can also report upcoming adjustment windows and recent NDRC news for manual checks.

### Deployment Geography for Use:

Global, with China-focused data sources and scheduling logic.

## Known Risks and Mitigations:

Risk: Security evidence marks the release suspicious because unsafe adjacent Python imports and an unnecessary subprocess search stub require review before installation.

Mitigation: Review the skill before installing, run it only where the skills directory is not writable by less-trusted code, and remove or disable the subprocess search stub if it is not required.

Risk: The skill depends on chinese-workdays and unpinned Python packages.

Mitigation: Verify the chinese-workdays dependency and pin or lock Python dependencies before operational use.

Risk: The skill performs scheduled NDRC web requests and sends stdout announcements through the configured OpenClaw/Feishu path.

Mitigation: Confirm the scheduled request frequency, Feishu delivery path, and Chinese-language output are intended for the deployment environment.

## Reference(s):

- [NDRC news releases](https://www.ndrc.gov.cn/xwdt/xwfb/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown/plain text status messages and notification text emitted to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes calculated adjustment-window dates, NDRC article titles, source URLs, and cautionary text to confirm against official notices.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
