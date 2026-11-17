## Description:

Create and maintain dedicated archives for each pet, including profiles, daily journals, photos, feeding logs, health records, and care reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and caregivers use this skill to keep local pet profiles, journals, photos, feeding logs, health notes, reminders, and compact history reports organized per pet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated pet IDs can cause reads or writes outside the intended pet-data folder.

Mitigation: Review or patch pet_id path handling before relying on the skill; until then, set PET_COMPANION_HOME to an isolated directory and avoid pet IDs containing slashes or dots.

Risk: Pet health notes and photo references are stored locally in plaintext.

Mitigation: Keep the storage directory private and share or export records only when the user explicitly asks.

Risk: Health records could be mistaken for veterinary diagnosis or treatment advice.

Mitigation: Use the skill to record observations and clinic notes only, and direct urgent symptoms to prompt veterinary care.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/pet-companion-journal)
- [Data Schema](references/data-schema.md)
- [Query Patterns](references/query-patterns.md)
- [Safety Boundaries](references/safety-boundaries.md)
- [Output Template](references/output-template.md)
- [Template Examples](references/template-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown responses with local JSON and Markdown records produced through helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PET_COMPANION_HOME for isolated local storage; defaults to ~/.pet-companion/.]

## Skill Version(s):

1.1.0 (source: server release metadata, skill.json, and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
