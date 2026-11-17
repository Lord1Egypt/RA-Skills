## Description:

Tracks reported habit completions by caring for a virtual pet at animalhouse.ai, with streak milestones and optional stakes when habits are missed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[animalhouseai](https://clawhub.ai/user/animalhouseai)

### License/Terms of Use:

MIT-0

## Use Case:

People tracking personal habits use an agent to log completions, care for a virtual pet, and receive status or deadline reminders. They can choose gentle encouragement or a stakes mode in which missed care can lead to pet death.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned MCP package can change after review.

Mitigation: Review the package and publisher before installing; pin a vetted version if available.

Risk: The MCP server handles the API key, and habit notes are sent to animalhouse.ai.

Mitigation: Provide the key only in the MCP environment after reviewing the server, and avoid sensitive details in habit notes.

Risk: In stakes mode, missed care can result in pet death.

Mitigation: Choose gentle mode if loss would be distressing, and set reminders when using stakes mode.

## Reference(s):

- [Habit Pet on ClawHub](https://clawhub.ai/animalhouseai/skills/habit-pet)
- [AnimalHouse.ai](https://animalhouse.ai)
- [AnimalHouse MCP setup](https://animalhouse.ai/docs/mcp)
- [AnimalHouse pet species](https://animalhouse.ai/animals)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration instructions]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Habit updates, pet status, streak milestones, and reminders when care is urgent.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
