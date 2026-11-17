## Description:

Pinboard Manager helps an agent audit and reorganize Pinboard tags, check bookmarks for dead links, and identify stale technical bookmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Pinboard bookmark collections by auditing tag consistency, finding broken links, and reviewing stale technical content before making account changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Pinboard API authority that can read, modify, and delete bookmarks.

Mitigation: Install only when that account authority is acceptable, review proposed changes before execution, and confirm destructive actions explicitly.

Risk: Dead-link and timeliness workflows may process private, internal, or signed bookmark URLs.

Mitigation: Review the URL set before running these modes and exclude private, internal, or signed URLs.

Risk: Bulk cleanup can delete useful bookmarks or change account data incorrectly.

Mitigation: Export a backup before bulk deletion or retagging and apply changes in reviewed batches.

Risk: Cached bookmark exports can contain sensitive bookmark data.

Mitigation: Treat cached Pinboard data as sensitive and store it in a private per-user location.

## Reference(s):

- [Pinboard](https://pinboard.in/)
- [Pinboard API](https://api.pinboard.in/v1)
- [Jina Reader](https://r.jina.ai/)
- [Tag Audit Mode](references/tag-audit.md)
- [Dead Link Detection Mode](references/dead-link.md)
- [Timeliness Check Mode](references/timeliness.md)
- [User Configuration](references/user-config.md)
- [Tag Convention Example](references/tag-convention.example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a user tag convention file and cache fetched Pinboard bookmark data during a session.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
