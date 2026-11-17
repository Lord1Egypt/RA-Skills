## Description:

Create and manage Privacy.com virtual cards, including single-use and merchant-locked cards, spending limits, card states, and transaction lookup via the Privacy.com API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnielee](https://clawhub.ai/user/johnielee)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to generate and administer Privacy.com virtual cards, adjust spending limits and card state, and review transaction data through Privacy.com API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may expose Privacy.com API keys or full payment-card credentials while following the skill.

Mitigation: Use a sandbox or least-privilege API key where possible, and avoid printing, logging, saving, or sharing full card numbers or CVVs.

Risk: Agents may create cards, change spending limits, pause cards, or permanently close cards without enough user control.

Mitigation: Require explicit confirmation before creating cards, changing limits, pausing cards, or permanently closing cards.

## Reference(s):

- [Privacy.com API Reference](references/api.md)
- [Privacy.com](https://privacy.com)
- [Privacy Cards ClawHub Listing](https://clawhub.ai/johnielee/skills/privacy-cards)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with curl command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRIVACY_API_KEY and access to the Privacy.com production or sandbox API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
