## Description:

Reading intelligence that logs books, captures quotes, and surfaces saved reads when they are relevant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilyabelikin](https://clawhub.ai/user/ilyabelikin)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Pages to maintain a private, local reading log that helps their agent save books, quotes, recommendations, and relevant reading context during conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified self-update instructions and README install examples can replace skill content from a moving upstream source.

Mitigation: Prefer a pinned, reviewed release and avoid replacing SKILL.md directly from the main branch.

Risk: Reading logs may contain sensitive personal notes, recommendations, and relationship context.

Mitigation: Keep notes local by default and review before enabling web lookups or Peeps and Haah integrations.

Risk: Recurring HEARTBEAT or cron checks can surface reading context unexpectedly.

Mitigation: Enable recurring checks only after explicit approval and review the schedule and output behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilyabelikin/skills/pages)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Haah integration](https://github.com/haah-ing/haah-skill)
- [Peeps integration](https://github.com/haah-ing/peeps-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reading-log entries, brief confirmations, grep or shell commands, and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under mind/pages/; optional web lookups, Peeps or Haah integrations, and recurring checks should be explicitly approved.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
