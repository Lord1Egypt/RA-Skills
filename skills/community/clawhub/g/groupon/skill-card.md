## Description:

Find, compare, and vet Groupon vouchers with fine-print checks, refund rules, and redemption planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find, shortlist, and vet Groupon offers before purchase or redemption. It helps compare true cost, merchant quality, fine print, booking friction, and support or refund paths while keeping money-impacting actions user-approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deal searches, location context, deal URLs, and ordinary browsing context may be sent to Groupon, merchants, review sites, booking sites, or marketplace pages during evaluation.

Mitigation: Use the skill with explicit browsing boundaries for sensitive locations, travel, booking, merchant disputes, or private purchase contexts.

Risk: Local notes under ~/groupon/ can expose preferences, purchase follow-up history, or incident details if written too broadly.

Mitigation: Keep local notes minimal and avoid storing payment methods, login secrets, full voucher barcodes, claim codes, or other sensitive voucher details.

Risk: Merchant availability, deal terms, refund rules, and support policies can change and may be incomplete or ambiguous.

Mitigation: Verify live deal terms, booking paths, voucher status, and current Groupon help-page wording before buying, booking, redeeming, or requesting support.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/groupon)
- [Skill Homepage](https://clawic.com/skills/groupon)
- [Groupon](https://www.groupon.com/)
- [Groupon Help](https://help.groupon.com/)
- [Groupon Deal Qualification](deal-qualification.md)
- [Merchant Checks](merchant-checks.md)
- [Recovery](recovery.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with structured verdicts, checklists, support packet drafts, and occasional shell commands for local setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local notes under ~/groupon/ after user confirmation; does not store payment details, login secrets, full voucher barcodes, or claim codes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
