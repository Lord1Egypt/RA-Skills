## Description:

Manage Kaiten.ru project boards through the Kaiten REST API, including cards, spaces, boards, columns, tags, comments, checklists, and time tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nixprosoft](https://clawhub.ai/user/nixprosoft)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Kaiten project-management workspaces from an agent, including viewing boards and cards, creating or updating tasks, adding comments, managing tags and members, working with checklists, and logging time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete live Kaiten project data.

Mitigation: Use a least-privilege Kaiten token and require confirmation of the exact card, board, and operation before create, update, move, delete, membership, tag, checklist, comment, or time-log actions.

Risk: A wrong Kaiten domain can direct authenticated requests to the wrong tenant.

Mitigation: Check KAITEN_DOMAIN carefully and prefer the expected tenant hostname before running commands.

Risk: Persisted last-used board and space context can make ambiguous phrases such as current board or same board resolve incorrectly.

Mitigation: Inspect the stored state and ask for explicit board, space, column, and lane identifiers when the request is ambiguous.

## Reference(s):

- [Kaiten API Reference](artifact/references/api-reference.md)
- [Kaiten Developer Documentation](https://developers.kaiten.ru)
- [ClawHub Skill Page](https://clawhub.ai/nixprosoft/skills/kaiten)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute authenticated Kaiten REST API reads and writes when configured with a Kaiten token and domain.]

## Skill Version(s):

1.1.0 (source: evidence release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
