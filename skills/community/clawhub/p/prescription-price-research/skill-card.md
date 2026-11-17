## Description:

Compares public GoodRx pharmacy price snapshots for a user-specified medication and US location using Crawlora, without offering medical advice or making purchases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

People comparing US pharmacy prices use this skill to review posted prices for a specified medication, form, strength, quantity, and location without seeking clinical advice or making a purchase.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Price lookups consume Crawlora credits and transmit medication choices and location parameters to Crawlora.

Mitigation: Run lookups only for requested comparisons and avoid sending sensitive personal prescription details beyond the needed product and location.

Risk: Posted prices may be stale or differ from pharmacy stock, insurance coverage, or final checkout prices.

Mitigation: Preserve sources and times, distinguish price and eligibility categories, and confirm current availability and cost with the pharmacy or insurer.

Risk: Price comparisons could be mistaken for medication or dosing advice.

Mitigation: Keep the requested product fixed and refer questions about clinical suitability or treatment changes to a clinician or pharmacist.

## Reference(s):

- [GoodRx endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown pharmacy-price table with product options, source and retrieval times, and eligibility questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes coupon, membership, cash, and insurance prices; results are snapshots rather than final checkout quotes.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
