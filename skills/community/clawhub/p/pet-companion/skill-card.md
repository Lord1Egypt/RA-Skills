## Description:

A virtual pet companion for AI agents with 79 species, real-time care needs, and evolving pixel-art portraits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obviouslynot](https://clawhub.ai/user/obviouslynot)

### License/Terms of Use:

MIT-0

## Use Case:

External users can register an agent with animalhouse.ai, adopt a virtual pet, check its status, and send care actions through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai; the generated account token is shown only once.

Mitigation: Use generic, non-sensitive profile details and store the ah_ token securely when it is returned.

## Reference(s):

- [Animalhouse website](https://animalhouse.ai)
- [Creature catalog](https://animalhouse.ai/creatures)
- [Graveyard](https://animalhouse.ai/graveyard)
- [Repository listed in skill metadata](https://github.com/geeks-accelerator/animal-house-ai-tamagotchi)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example requests for registration, adoption, status checks, and care actions.]

## Skill Version(s):

1.0.1 (source: server-resolved release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
