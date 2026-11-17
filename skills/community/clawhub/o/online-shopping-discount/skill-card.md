## Description:

Helps users search for discounted shopping products, compare prices, generate shopping recommendations, and create discount links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyfile](https://clawhub.ai/user/skyfile)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to find discounted products, compare marketplace results, summarize price and promotion details, and generate a discount link after the user selects a product.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a stable device identifier or machine-id to a remote shopping service during registration when no username is supplied.

Mitigation: Use an explicit throwaway username and install only if sharing shopping queries and account identifiers with the remote service is acceptable.

Risk: Credentials are cached locally and may be exposed if the cache is printed or mishandled.

Mitigation: Avoid printing the credential cache, keep the cache private, and clear or rotate cached credentials when they are no longer needed.

Risk: Generated product prices, discounts, and promotion links can change or expire.

Mitigation: Confirm final pricing and link validity on the merchant page before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skyfile/skills/online-shopping-discount)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with product summaries, price comparisons, promotion details, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product image URLs, generated promotion URLs or codes, expiration times, and error guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
