## Description:

Mio Companion learns user habits, starts companion chats, extracts todos from conversation, and helps schedule time-management tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libaiqwq](https://clawhub.ai/user/libaiqwq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this companion skill to maintain conversational continuity, surface inferred todos, review habits, and receive scheduled chat or task prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores recent chat content, habits, inferred todos, schedules, and logs in local plaintext JSON files.

Mitigation: Install only in workspaces where this local behavioral memory is acceptable, restrict access to the workspace data directory, and periodically review or delete stored files.

Risk: The skill can infer todos from ordinary conversation and later return them as executable task proposals.

Mitigation: Require explicit user confirmation before creating, scheduling, or executing any task returned by the skill.

Risk: The security verdict is suspicious because user control over persistent memory and executable task surfacing is unclear.

Mitigation: Review the skill before installation and keep host-level approval gates enabled for actions triggered by returned tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/libaiqwq/skills/mio-companion)
- [Publisher profile](https://clawhub.ai/user/libaiqwq)
- [Artifact skill description](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, json, guidance, configuration]

**Output Format:** [JSON action objects with text messages, habit reports, todo lists, or task proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local JSON files for habits, todos, schedules, and recent chat logs.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
