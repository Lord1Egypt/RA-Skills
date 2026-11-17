## Description:

Operate Deck.co by listing or retrieving agents and sources, creating sources, and testing API key connectivity through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Deck.co agents and sources, create sources, and check API key connectivity through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code that has not been independently verified.

Mitigation: Review and install a fixed, verified CLI release before use; consider disabling automatic skill synchronization.

Risk: Deck.co requests use the connected account and may include proposed writes.

Mitigation: Confirm the connected account and review each proposed write before running it.

## Reference(s):

- [Deck.co](https://www.deck.co)
- [Deck.co API documentation](https://docs.deck.co/api/using-the-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-deck-co)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Guidance with inline shell commands and JSON-backed action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result content depends on the selected Deck.co action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
