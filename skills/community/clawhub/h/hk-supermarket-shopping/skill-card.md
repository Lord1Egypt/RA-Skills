## Description:

Real-time price comparison for Hong Kong supermarkets using the Consumer Council's daily pricewatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenho1394](https://clawhub.ai/user/stevenho1394)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask for Hong Kong supermarket products in English or Chinese and receive the cheapest matching store, current price, and estimated quantity purchasable with HK$100.

### Deployment Geography for Use:

Hong Kong

## Known Risks and Mitigations:

Risk: The skill contacts the Consumer Council pricewatch site and stores a short-lived CSV cache inside the skill directory.

Mitigation: Confirm that outbound access to the public pricewatch URL and local cache storage are acceptable for the deployment environment.

Risk: A packaging inconsistency in openclaw.plugin.json may affect compatibility.

Mitigation: Review package metadata before marketplace publication or automated installation.

## Reference(s):

- [Consumer Council Pricewatch CSV](https://online-price-watch.consumer.org.hk/opw/opendata/pricewatch_en.csv)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text, single-line answer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in English or Traditional Chinese based on the query language and includes supermarket, product, price, and HK$100 budget quantity when data is available.]

## Skill Version(s):

1.2.3 (source: server release metadata, artifact frontmatter, package.json, clawhub.json, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
