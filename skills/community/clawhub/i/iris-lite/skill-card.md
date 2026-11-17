## Description:

Iris Lite scans the last 25 Gmail emails, shows urgency scores and a priority list, and drafts 2 quick replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users can run this skill to triage a small Gmail inbox sample, prioritize recent messages, and generate quick reply drafts. It is suited for lightweight personal productivity workflows that can tolerate manual review before acting on results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires sensitive Gmail mailbox credentials and reads message headers and snippets.

Mitigation: Use a dedicated Gmail app password that can be revoked, and review the mailbox access implications before running the skill.

Risk: The documented dependency install targets the system Python environment.

Mitigation: Install and run the dependency in an isolated virtual environment instead of using the system Python environment.

Risk: The release includes advertising links for a separate Pro component.

Mitigation: Treat the Pro install and purchase links as separate from the Lite inbox scan and review them independently.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/iris-lite)
- [ClawHub metadata homepage](https://clawhub.ai/occupythemilkyway/iris-lite)
- [Publisher profile](https://clawhub.ai/user/occupythemilkyway)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces a priority table, urgency scores, summary counts, and up to 2 draft replies for human review.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
