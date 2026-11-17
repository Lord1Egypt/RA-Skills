## Description:

Acts as the user's personal care and grooming assistant in the Hygiene topic, tracking grooming routines, skincare, dental care, haircuts, and purchases of hygiene products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gekacross](https://clawhub.ai/user/gekacross)

### License/Terms of Use:


## Use Case:

External users who run personal OpenClaw assistants use this skill to track hygiene routines, grooming products, haircuts, dental visits, and related reminders in workspace memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal grooming, skincare, dental, haircut, and product details in workspace memory.

Mitigation: Install it only when that retention is desired, and review or delete knowledge/personal/hygiene.md if those details should not be retained.

Risk: The artifact directs the assistant to update the hygiene memory file when the user shares new routine or product information.

Mitigation: Review memory-file changes during use, especially after sharing sensitive personal-care details.

Risk: The documentation and commands are primarily Russian, which may affect review by non-Russian-speaking users.

Mitigation: Have a qualified reviewer translate or inspect the artifact before deployment in non-Russian-language environments.

## Reference(s):

- [Personal Hygiene ClawHub Skill Page](https://clawhub.ai/gekacross/skills/personal-hygiene)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown and conversational text, with updates to a disclosed workspace memory file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update knowledge/personal/hygiene.md when the user provides new routine, product, haircut, or dental-visit information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
