## Description:

Paw.skill helps agents preserve owner-described pet memories, including personality, habits, sounds, routines, special moments, and remembrance prompts for pets who have died.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn owner-provided pet memories into local pet profiles, sound dictionaries, routines, bond maps, and remembrance interactions. It is not intended for veterinary, medical, or health-tracking decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal pet memories are persisted in a local folder.

Mitigation: Use the skill only when local persistence is acceptable, and remove ~/.paw-skill/pets/ to delete stored profiles.

Risk: Pet observations or health details could be mistaken for veterinary advice.

Mitigation: Do not rely on the skill for veterinary or medical decisions.

Risk: Remembrance interactions can involve emotionally sensitive grief content.

Mitigation: Follow the skill's grief-aware behavior: do not rush grief, do not suggest replacement pets, and ground responses in memories the owner provided.

## Reference(s):

- [Paw.skill ClawHub page](https://clawhub.ai/realteamprinz/skills/paw)
- [Publisher profile: realteamprinz](https://clawhub.ai/user/realteamprinz)
- [Species Guide](artifact/references/species-guide.md)
- [Pet Profile Template](artifact/templates/PET-PROFILE.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown pet profiles, JSONL memory logs, and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores pet profiles and memories locally under ~/.paw-skill/pets/ when used as described.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
