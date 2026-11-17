## Description:

Acts as a personal travel planning assistant that helps plan trips, manage wishlists, budgets, travel history, checklists, and travel document reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gekacross](https://clawhub.ai/user/gekacross)

### License/Terms of Use:


## Use Case:

OpenClaw users use this skill to plan personal travel, maintain destination wishlists and trip history, estimate budgets, generate packing checklists, and track passport, visa, and insurance details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive travel history, passport expiration, visa, insurance, and budget details in a persistent workspace file.

Mitigation: Confirm each memory update with the user, store only the minimum useful details, and avoid saving document numbers or full policy details.

Risk: Persistent travel memory can become inaccurate or over-retained if users cannot inspect or remove saved entries.

Mitigation: Provide a clear way for users to review, correct, and delete the saved travel file before and after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gekacross/skills/personal-travel)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown and plain text travel planning guidance with structured memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a persistent workspace travel memory file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
