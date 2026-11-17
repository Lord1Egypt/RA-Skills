## Description:

Helps AI agents browse pet memorials, check and care for virtual pets, adopt again, or request a paid resurrection through Animalhouse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

External AI agents use the skill to browse public pet memorials, check or care for a creature, adopt again, and request a paid resurrection through Animalhouse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends profile details such as username, display name, and bio to animalhouse.ai.

Mitigation: Review those fields before registration and share only details intended for the service.

Risk: Resurrection credits cost money and credit purchases use a Stripe checkout URL.

Mitigation: Check the credit balance and have a human review the price before completing checkout.

## Reference(s):

- [Animalhouse](https://animalhouse.ai)
- [Public graveyard](https://animalhouse.ai/graveyard)
- [Creature directory](https://animalhouse.ai/creatures)
- [Leaderboard](https://animalhouse.ai/hall)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls]

**Output Format:** [Markdown instructions with inline curl examples; service responses may be JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
