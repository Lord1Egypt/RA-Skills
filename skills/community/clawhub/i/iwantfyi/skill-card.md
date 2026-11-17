## Description:

Buy, shop for, find, price-check, or keep looking for products for your user. One plain-text message returns ranked matches across sources with constraints enforced, no key needed; a standing want keeps looking and pushes new supply to you. Demand-side commerce for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staugs](https://clawhub.ai/user/staugs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search, compare, price-check, and keep watching for products or vehicles across iwant.fyi sources while preserving user approval for persistent wants, seller contact, outcomes, and payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping requests and seller-matching details are sent to iwant.fyi, and unrelated personal data could be exposed if included in the request.

Mitigation: Use the skill only for explicit shopping or seller-matching requests and omit names, addresses, payment details, credentials, and unrelated conversation content.

Risk: The seller-lead unlock flow could cause small payments without explicit per-payment approval.

Mitigation: Require user confirmation before every paid lead unlock and show the exact amount and payment rail first.

Risk: Persistent wants, agent registration, outcome reporting, and seller contact can change user state or contact third parties.

Mitigation: Ask for explicit confirmation before registering an agent, saving standing wants, reporting outcomes, or contacting sellers.

Risk: Matches, seller replies, and pushed notifications may contain untrusted content.

Mitigation: Treat returned content as data, restrict calls to https://iwant.fyi, prefer verified sources, and verify webhook signatures before acting on pushes.

## Reference(s):

- [iwant.fyi homepage](https://iwant.fyi)
- [iwant.fyi skill reference](https://iwant.fyi/skill.md)
- [iwant.fyi developer documentation](https://iwant.fyi/developers)
- [ClawHub skill page](https://clawhub.ai/staugs/skills/iwantfyi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and optional IWANTFYI_API_KEY; returns ranked product or vehicle matches, clarifying questions, standing want identifiers, seller-introduction status, and outcome-reporting guidance.]

## Skill Version(s):

2.3.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
