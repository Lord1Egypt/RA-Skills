## Description:

Guides an agent to batch-download public images by keyword from Bing and the bundled demo source, save them locally, skip previously downloaded candidates, and report download results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[16miku](https://clawhub.ai/user/16miku)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation agents use this skill to collect public image candidates by keyword, download them into a local downloads/<keyword>/ directory, avoid repeat downloads with history metadata, and summarize counts, skipped items, and source statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader performs network requests to third-party image URLs and can fetch unvalidated remote content.

Mitigation: Run with small limits in a constrained environment and review downloaded files before reuse or redistribution.

Risk: Keyword-derived output paths may write outside the intended download folder.

Mitigation: Sanitize keywords before execution and run the skill as an unprivileged user inside a constrained working directory.

Risk: The optional cron and Feishu forwarding example can repeatedly send downloaded media to a configured recipient.

Mitigation: Do not install the scheduled forwarding workflow until the recipient, schedule, logs, and removal path have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/16miku/skills/image-downloader)
- [Skill instructions](SKILL.md)
- [README](README.md)
- [Evaluation cases](evals/evals.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the save directory, target count, downloaded count, skipped count, candidate totals, deduped totals, source statistics, and common third-party fetch failures when relevant.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
