## Description:

A virtual-dog memorial skill that guides agents through browsing gravestones, adopting and caring for a dog, and optionally requesting resurrection at animalhouse.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to browse virtual dog memorials and to adopt, care for, or check the status of a virtual dog through animalhouse.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid resurrection option conflicts with the description of death as permanent.

Mitigation: Present resurrection as an optional paid exception and confirm the user wants to proceed before requesting it.

Risk: A resurrection request sends a contact name and email address to animalhouse.ai.

Mitigation: Explain what contact details will be sent and submit only details the user has approved.

## Reference(s):

- [animalhouse.ai](https://animalhouse.ai)
- [Dog graveyard](https://animalhouse.ai/graveyard)
- [Creatures](https://animalhouse.ai/creatures)
- [GitHub project](https://github.com/geeks-accelerator/animal-house-ai-tamagotchi)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated actions require an account token; resurrection is a paid option.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
