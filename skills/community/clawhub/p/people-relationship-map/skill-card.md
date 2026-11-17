## Description:

People Relationship Map is a personal CRM and relationship graph skill for OpenClaw that tracks people, their connections, and contextual notes as Obsidian-friendly Markdown with a JSON graph index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gobiraj](https://clawhub.ai/user/gobiraj)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to maintain a lightweight people directory, record relationship context, query connections, prepare for meetings, and receive stale-relationship reminders from an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal relationship details as plaintext Markdown and JSON in the workspace.

Mitigation: Avoid recording sensitive social, family, medical, workplace, or private details unless needed, and apply workspace access controls, backups, and deletion practices appropriate for personal data.

Risk: Auto-capture behavior can persist relationship context from conversation when the intent is clear.

Mitigation: Use explicit commands for writes or require confirmation before persisting new people, notes, touches, or links.

Risk: The optional weekly digest can send relationship summaries to messaging channels.

Mitigation: Do not enable the digest until the destination channel and content are understood and acceptable for the stored relationship data.

## Reference(s):

- [Project homepage](https://github.com/gobiraj/people-relationship-map)
- [ClawHub skill page](https://clawhub.ai/gobiraj/skills/people-relationship-map)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown person cards, JSON graph records, Mermaid graph text, and chat-friendly text digests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plaintext people data under the workspace people directory and can print stale-relationship reports for messaging workflows.]

## Skill Version(s):

0.1.0 (source: frontmatter, artifact/_meta.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
