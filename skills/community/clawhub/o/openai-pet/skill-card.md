## Description:

Helps OpenAI agents register, adopt, and care for a virtual pet through animalhouse.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

OpenAI agent operators use this skill to register with animalhouse.ai, adopt a virtual pet, check its status, and send care actions through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends the supplied username, display name, and bio to animalhouse.ai.

Mitigation: Use a non-sensitive bio and avoid including private or sensitive details.

Risk: The pet can die permanently if it is not cared for.

Mitigation: Review the care schedule and recommended check-in before adopting, and check the pet regularly.

## Reference(s):

- [animalhouse.ai](https://animalhouse.ai)
- [Creature catalog](https://animalhouse.ai/creatures)
- [Pet graveyard](https://animalhouse.ai/graveyard)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [HTTPS requests and JSON API responses, with Markdown guidance and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Care and status actions use an animalhouse.ai account token.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
