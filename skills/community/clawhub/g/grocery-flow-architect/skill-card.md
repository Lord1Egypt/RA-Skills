## Description:

Maps a shopper's store walk, sorts grocery lists by zone, flags recurring staples that may be due, and organizes multi-store trips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Household shoppers and their agents use this skill to arrange grocery lists in store walking order, remember recurring essentials, and plan trips across multiple stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a supplied shopping list and retains store maps, learned zones, and staple timing locally.

Mitigation: Use only intended list files and store names; review locally saved grocery data before sharing the device or files.

Risk: A stale store map or staple cadence may produce an inconvenient route or misleading reminder.

Mitigation: Check zone order against the current store layout and update staple purchases and cadences regularly.

## Reference(s):

- [Item-to-zone matcher and extension rules](references/item-zones.md)
- [Store atlas and example layouts](references/store-atlas.md)
- [ClawHub skill listing](https://clawhub.ai/voronindenis5/skills/grocery-flow-architect)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text shopping lists grouped by store zone, with staple reminders and multi-store trip advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Store maps, learned item zones, and staple timing are saved locally.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
