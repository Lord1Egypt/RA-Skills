## Description:

Preserve your grandfather's stories, skills, life philosophy, and the quiet strength that held the family together using only user-provided memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to preserve memories, stories, practical skills, sayings, humor, and family context about a grandfather in a local memorial profile. It can help organize fragments and respond in a grandfather-inspired voice grounded in the user's own entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store sensitive family memories or details about living people on the user's device.

Mitigation: Avoid entering sensitive details about living people without consent.

Risk: Local profile and memory files may remain on disk after use.

Mitigation: Delete the ~/.grandpa-skill/ folder when the stored profile and memories should no longer be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realteamprinz/skills/grandpa)
- [Publisher profile](https://clawhub.ai/user/realteamprinz)
- [README](artifact/README.md)
- [Grandpa profile template](artifact/templates/GRANDPA-PROFILE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration]

**Output Format:** [Markdown and JSONL-backed local profile content with conversational text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered memories locally under ~/.grandpa-skill/; no external data transfer was found in the server security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
