## Description:

Helps users compare online offers, prepare a checkout through Portage, and purchase only after they approve the exact total or complete payment themselves in a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomtom87](https://clawhub.ai/user/tomtom87)

### License/Terms of Use:

MIT-0

## Use Case:

People asking an agent to buy or reorder an item use this skill to compare offers, review a priced checkout, and approve a purchase or finish payment themselves. It also helps them configure Portage and track orders placed through it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A purchase could charge the user or select an unexpected merchant or total.

Mitigation: Keep approval required, set spending caps, and review the merchant and exact dry-run total before approving.

Risk: Shopping credentials and address details could be exposed if shared in chat.

Mitigation: Configure credentials locally through Portage and never paste secrets into chat.

Risk: An untrusted or outdated Portage installation could affect a high-impact purchase.

Mitigation: Install only if you trust the Portage CLI and check its available commands and version before buying.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tomtom87/skills/portage-buy)
- [Portage documentation](https://portage.readthedocs.io/en/latest/)
- [Checkout outcomes](references/outcomes.md)
- [Hand-off-only retailers](references/handoff-only.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational text and Markdown with Portage commands, offer comparisons, checkout quotes, and order updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Purchases require user approval of the exact total; some retailers require browser hand-off for payment.]

## Skill Version(s):

0.10.5 (source: skill frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
