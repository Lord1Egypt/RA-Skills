## Description:

Deep web information search and archival skill for comprehensive research on persons, organizations, or products using multiple search engines, browser-based content extraction, SQLite URL deduplication, structured local storage, and configurable output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[expeditionhub](https://clawhub.ai/user/expeditionhub)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use InfoSeek to gather, deduplicate, extract, and archive web information about people, organizations, or products for background research, due diligence, media monitoring, competitive intelligence, or information archive building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search subjects to external search and browsing providers while its artifact text under-discloses that behavior.

Mitigation: Review network disclosure before use, avoid sensitive search subjects unless external-provider sharing is acceptable, and document which providers will receive queries.

Risk: Research and archived content may include personal data in local folders, SQLite records, and logs.

Mitigation: Use people research only with a clear lawful purpose, set a retention plan, and review archive, database, and log contents before sharing or retaining them.

Risk: The deletion command may target paths outside the intended archive and uses platform-specific recycle-bin or trash implementations.

Mitigation: Avoid the deletion command until deletion is restricted to the InfoSeek archive and implemented through safer platform APIs; delete files through reviewed workspace controls instead.

Risk: The skill depends on other search and browser skills without pinned or verified versions.

Mitigation: Pin, inspect, and verify required dependency skills before installation or execution.

## Reference(s):

- [InfoSeek ClawHub skill page](https://clawhub.ai/expeditionhub/skills/infoseek)
- [expeditionhub publisher profile](https://clawhub.ai/user/expeditionhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and locally archived files in md, json, txt, csv, xlsx, html, or docx formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-subject archive folders, a local SQLite deduplication database, operation logs, and task reports.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact version history, released 2026-04-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
