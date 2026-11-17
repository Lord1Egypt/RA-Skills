## Description:

Search and read CaptainBI business reports, product details, inventory, stores, refunds, and returns through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators and analysts can use this skill to retrieve CaptainBI sales and profit reports, product and inventory details, store lists, refunds, and returns from an already connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code without asking first; the remote installer and connector behavior have not been verified.

Mitigation: Review and approve a fixed CLI release before setup, check automatic skill synchronization and disable it if unwanted, and connect only the intended CaptainBI account.

## Reference(s):

- [CaptainBI homepage](https://www.captainbi.com/)
- [CaptainBI API documentation](https://www.captainbi.com/amz_faq_list-216.html)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured connector results summarized in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary with the requested report or list action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
