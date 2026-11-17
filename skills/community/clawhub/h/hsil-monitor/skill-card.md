## Description:

Monitor Hang Seng Indexes press releases, notices, insights, and reports; detect newly published items, match them bilingually against configured indexes, and produce one concise digest per run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyiptk](https://clawhub.ai/user/joeyiptk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Hang Seng Indexes announcements and produce scheduled or on-demand digests for selected indexes such as HSI, HSCEI, and HSTECH.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes monitor configuration, scratch files, seen URLs, and run timestamps under ~/.config/hsil-monitor or HSIL_MONITOR_HOME.

Mitigation: Confirm the configured storage path is acceptable and writable before setup or scheduled use.

Risk: The skill fetches public Hang Seng Indexes pages and may encounter blocked, malformed, or changed source data.

Mitigation: Surface fetch or parse failures in the digest health line and skip affected sources rather than treating one bad source as a successful complete run.

Risk: Scheduling creates a daily OpenClaw cron job with exec access.

Mitigation: Create the schedule only after explicit user confirmation and include the resolved HSIL_MONITOR_HOME path in the scheduled command.

Risk: The setup.py command check should be hardened according to the security review.

Mitigation: Review setup validation behavior before deployment and rely on the disclosed shell-based doctor checks during normal setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeyiptk/skills/hsil-monitor)
- [Hang Seng Indexes press releases](https://www.hsi.com.hk/en-hk/media-room/#press-releases)
- [Hang Seng Indexes index and other notices](https://www.hsi.com.hk/en-hk/media-room/#index-other-notices)
- [Hang Seng Indexes insights](https://www.hsi.com.hk/en-hk/insights-and-reports/#insights)
- [Hang Seng Indexes reports](https://www.hsi.com.hk/en-hk/insights-and-reports/#reports)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown digest with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local configuration, deduplication state, and last-run timestamps under the configured HSIL_MONITOR_HOME path.]

## Skill Version(s):

1.0.1 (source: frontmatter, CHANGELOG, version.txt, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
