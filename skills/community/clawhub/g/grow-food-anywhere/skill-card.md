## Description:

Practical food growing for complete beginners. Apartment balcony, backyard, or windowsill. What actually produces enough to matter, realistic timelines, and what to skip. Use when someone wants to grow food but has never done it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create a practical beginner food-growing plan for an apartment, balcony, windowsill, patio, or yard. The agent helps assess available space and sunlight, prioritize high-yield beginner crops, save a local plan, and set simple care reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses an unpinned npx package reference.

Mitigation: Check the installer source before installation or use a pinned and trusted install flow when available.

Risk: The skill may save a personalized plan file to the user's filesystem.

Mitigation: Confirm the destination and contents before writing the plan file.

Risk: Calendar reminders may not match the user's local season, plants, or care needs.

Mitigation: Review reminder timing and text before creating recurring calendar events.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/howtousehumans/skills/grow-food-anywhere)
- [USDA Cooperative Extension System](https://extension.org)
- [USDA Plant Hardiness Zone Map](https://planthardiness.ars.usda.gov)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with a local plan file and reminder configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a personalized plan to the filesystem and propose calendar reminders for watering, harvesting, and feeding.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
