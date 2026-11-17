## Description:

Generate a structured daily or weekly markdown digest from an OPML list of RSS/Atom feeds, optionally filtered by keywords, for Obsidian or Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with OPML feed lists use this skill to parse feeds, fetch recent RSS/Atom articles, optionally filter by keyword, and produce daily or weekly markdown digests for Obsidian, Discord, email, or scheduled reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OPML feed entries can cause outbound requests to arbitrary local or network URLs.

Mitigation: Use OPML files only from trusted sources, review feed URLs before running the fetch script, and run the skill with least privilege in non-sensitive environments.

Risk: Cron examples can repeatedly fetch remote content and write digest files without interactive review.

Mitigation: Avoid enabling scheduled jobs until URL validation, size limits, logging, monitoring, and an easy removal plan are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/skills/nai-rss-digest)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown digest files and JSON arrays emitted by command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progress and warnings are written to stderr; digest content can be written to stdout or an output file.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
