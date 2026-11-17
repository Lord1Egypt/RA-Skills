## Description:

PD helps an agent build and maintain a local plaintext productivity system for goals, projects, tasks, habits, reviews, energy management, and task breakdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starsbottle](https://clawhub.ai/user/starsbottle)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to have an agent plan, prioritize, review, and organize personal development work in a single local productivity system. It is intended for goals, projects, tasks, habits, focus sessions, routines, overload resets, and periodic reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration guidance can reorganize existing productivity notes and remove legacy goals, projects, tasks, or someday folders.

Mitigation: Back up ~/productivity/, review the proposed moves, verify the new files, and approve cleanup explicitly before any deletion.

Risk: The system stores personal priorities, commitments, preferences, and review notes as plaintext local files.

Mitigation: Install only when plaintext local storage is acceptable, and save preferences or memory entries only after explicit user approval.

Risk: Incorrect routing could scatter daily, weekly, monthly, or commitment records across old and new folder structures.

Mitigation: Use the documented ~/productivity/ structure, avoid deprecated paths, and check migration results before relying on the system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/starsbottle/skills/pd)
- [Publisher profile](https://clawhub.ai/user/starsbottle)
- [Setup guide](artifact/setup.md)
- [Migration guide](artifact/migration.md)
- [Productivity system template](artifact/system-template.md)
- [Feel-Good integration guide](artifact/feel-good-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional local Markdown files, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update plaintext files under ~/productivity/ only after explicit user approval.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 2.7.0 and artifact metadata reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
