## Description:

生活记忆记录器。帮你记录人际交往中的重要细节（生日、喜好、承诺），自动提醒跟进，让你成为更贴心的人。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-productivity agents use this skill to record relationship details, commitments, dates, preferences, and follow-up reminders in a structured memory system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist relationship, health, event, and follow-up details in local memory files and indexes.

Mitigation: Use it only with clear consent, review stored records periodically, and delete records that are no longer needed.

Risk: Sensitive third-party details could be retained or exposed through reminders, indexes, or search summaries.

Mitigation: Confirm before storing sensitive details, avoid sharing one person's information with another person, and implement deletion across person files, indexes, events, and reminders.

Risk: Memory files may contain private personal data.

Mitigation: Prefer safe generated IDs, restricted file permissions, and storage locations appropriate for private user data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/life-memory-logger)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON memory records and reminder/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces person-specific memory entries, event lists, follow-up queues, search summaries, reminders, and scheduled-task configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
