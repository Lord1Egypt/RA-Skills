## Description:

Erstelle und verwalte Verkaufsanzeigen speziell auf kleinanzeigen.de.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simon83s](https://clawhub.ai/user/simon83s)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to prepare Kleinanzeigen.de sale listings by collecting item details, researching comparable prices, drafting listing text, and creating a saved draft for user review.

### Deployment Geography for Use:

Germany

## Known Risks and Mitigations:

Risk: The skill asks the user to provide a password and SMS login code in chat.

Mitigation: Pause at authentication and have the user enter credentials and one-time codes directly on Kleinanzeigen.de, then resume only after login succeeds.

Risk: Using third-party product photos can create copyright issues.

Mitigation: Prefer user-provided photos; use only clearly licensed sources such as Wikimedia Commons or official press pages, and ask the user to take photos when rights are uncertain.

Risk: Generated listing details or price recommendations may be inaccurate or incomplete.

Mitigation: Keep listings as drafts and require user review of item details, price, shipping, photos, and publication decision.

## Reference(s):

- [Kleinanzeigen Kategorien](references/categories.md)
- [Preisrecherche](references/pricing.md)
- [ClawHub skill page](https://clawhub.ai/simon83s/skills/kleinanzeigen-de-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with listing fields, price rationale, and browser workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft listing content and a saved-draft handoff; the user remains responsible for review and publication.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
