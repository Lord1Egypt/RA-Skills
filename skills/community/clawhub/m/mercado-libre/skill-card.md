## Description:

Use Mercado Libre to search, compare, buy, sell, and automate decisions with pricing, safety, and dispute workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External marketplace users use this skill to make Mercado Libre buying, selling, pricing, dispute, and automation decisions with comparison matrices, safety checks, and explicit confirmation before live actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace history, watchlists, automation logs, and dispute notes are persisted locally under ~/mercado-libre/.

Mitigation: Periodically review or delete local memory, watchlist, automation, and dispute logs, and store only information that improves future decisions.

Risk: Conflicting memory guidance could lead credentials, MFA codes, payment details, or session data to be saved in plaintext.

Mitigation: Keep secrets out of ~/mercado-libre/ memory files and use a secret manager or keychain for API tokens and other sensitive values.

Risk: Buying, listing, messaging, inventory, and automation workflows can affect a live Mercado Libre account.

Mitigation: Require explicit confirmation before any purchase, listing update, message, inventory change, or other live marketplace action.

## Reference(s):

- [ClawHub Mercado Libre Skill](https://clawhub.ai/ivangdavila/skills/mercado-libre)
- [Mercado Libre](https://www.mercadolibre.com)
- [Mercado Libre API](https://api.mercadolibre.com)
- [Mercado Libre Developers](https://developers.mercadolibre.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown decision summaries, comparison tables, checklists, and scoped automation plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local memory under ~/mercado-libre/ and requires explicit confirmation before live marketplace actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
