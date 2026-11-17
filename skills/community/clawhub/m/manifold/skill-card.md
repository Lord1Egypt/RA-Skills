## Description:

Read and trade on Manifold Markets by searching markets, fetching probabilities, inspecting users and bets, and placing bets, sales, or comments only after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crotalus](https://clawhub.ai/user/crotalus)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to read Manifold Markets data and prepare authenticated market actions. Write actions are intended to proceed only after the user confirms the market, payload, and exact action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use MANIFOLD_API_KEY to perform authenticated actions on a user's Manifold account.

Mitigation: Keep MANIFOLD_API_KEY private and install the skill only when account interaction is intended.

Risk: Bets or share sales can affect the user's Manifold holdings if executed with the wrong market, side, amount, or payload.

Mitigation: Fetch the market first, restate the exact market and payload, and proceed only after explicit user confirmation.

Risk: Comments submitted through the API may be public and may incur fees.

Mitigation: Confirm the target market and exact comment text before posting.

Risk: Rate limits and access restrictions may affect API results, including private or unlisted markets.

Mitigation: Treat API failures or missing data as platform constraints and consult the Manifold API documentation before retrying or changing behavior.

## Reference(s):

- [Manifold Markets](https://manifold.markets)
- [Manifold API Documentation](https://docs.manifold.markets/api)
- [ClawHub Skill Page](https://clawhub.ai/crotalus/skills/manifold)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated write actions require MANIFOLD_API_KEY and explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
