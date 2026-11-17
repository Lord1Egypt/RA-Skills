## Description:

Jingdong Redirect routes legacy jingdong requests to jd-shopping for JD.com shopping assistance while keeping login, checkout, order submission, and payment out of scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this legacy entry point to redirect JD.com shopping requests to the maintained jd-shopping skill for search, review checks, price comparison, SKU selection, and cart preparation without completing purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The redirect points users to jd-shopping, which is not included or audited in this package.

Mitigation: Review the separate jd-shopping skill before relying on the transferred shopping workflow.

Risk: Generic JD mentions may invoke this legacy redirect unexpectedly.

Mitigation: Confirm that the user intends JD.com shopping before handing off to jd-shopping.

Risk: Shopping workflows can involve credentials, checkout, order submission, or payment actions.

Mitigation: Keep those actions outside the agent boundary and have the user recheck final price, stock, delivery, coupons, and after-sales terms before purchase.

## Reference(s):

- [Jingdong Redirect on ClawHub](https://clawhub.ai/harrylabsj/skills/jingdong)
- [harrylabsj publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redirect guidance only; no credentials, checkout, order submission, or payment actions.]

## Skill Version(s):

2.1.0 (source: server release evidence, clawhub.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
