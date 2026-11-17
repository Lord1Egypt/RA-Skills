## Description:

Fetches recent HKEXnews Daily Targeted Leverage Factor announcements for HKEX-listed L&I products, extracts factors from the announcement PDFs, and returns a Telegram-ready digest grouped by applicable date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyiptk](https://clawhub.ai/user/joeyiptk)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to run or schedule HKEX L&I daily factor checks and produce a concise Telegram digest for OpenClaw delivery. It supports manual runs and cron-based monitoring of the next trading day's factor announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A misconfigured scratch directory can cause cleanup to delete unrelated PDF or text files.

Mitigation: Use a dedicated empty private tmp_dir, keep it outside Documents, workspaces, shared folders, and /tmp itself, and review the setting before install or scheduling.

Risk: Scheduled exec-based runs repeatedly fetch and parse external announcement PDFs.

Mitigation: Enable the cron job only after review, run the agent as a non-root user, and keep the configured dependencies limited to the required tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeyiptk/skills/hkex-li-daily-factor-monitor)
- [HKEXnews](https://www1.hkexnews.hk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text Telegram digest with a fenced monospace code block and source URLs; setup guidance may include shell commands and JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads HKEX PDFs only for the current run, extracts text, emits a human-readable digest, and deletes temporary PDF/text files after parsing.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, version.txt, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
