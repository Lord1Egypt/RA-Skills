## Description:

Track book availability on Libby/OverDrive libraries, search library catalogues, manage a watchlist, and get notified when books are added.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexpolonsky](https://clawhub.ai/user/alexpolonsky)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to search public Libby/OverDrive catalog data, keep per-user book watchlists, and check when watched titles appear in a library catalog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes local watchlist and configuration JSON files in the default data directory.

Mitigation: Use `--data-dir` or `LIBBY_BOOK_MONITOR_DATA` to place data in an expected location and review stored watchlist contents before sharing the machine or backups.

Risk: The skill queries a public Libby/OverDrive catalog API using watched titles and library codes.

Mitigation: Use only watchlist entries and library codes you are comfortable sending to the catalog service, and avoid placing sensitive notes in book titles or profile names.

Risk: Recurring cron or notification examples can repeatedly run network checks and send availability results through external notification tools.

Mitigation: Enable scheduled checks only when desired, review the notification destination, and keep the documented one-second API delay for multi-book checks.

Risk: Catalog matching is substring based and may produce incorrect matches for short or common titles.

Mitigation: Review reported matches before acting on them, especially for short titles or searches without an author.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexpolonsky/skills/libby-book-monitor)
- [Publisher profile](https://clawhub.ai/user/alexpolonsky)
- [OverDrive](https://www.overdrive.com/)
- [OverDrive Thunder API](https://thunder.api.overdrive.com/v2/libraries)
- [Agent Skills format](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI can create or update local JSON config and watchlist files under the configured data directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
