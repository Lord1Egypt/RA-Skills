## Description:

Compare print-on-demand (POD) supplier prices for one product, size, color and destination. Use when a seller asks which POD supplier is cheapest (Printify, Printful, Gelato, Prodigi, Apliiq, Artelo, CustomCat, Fourthwall, Inkthreadable or merchOne), what a blank costs delivered, how long delivery takes, how much they keep per sale on Etsy or Shopify, or which supplier fits their shop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[filipljubic](https://clawhub.ai/user/filipljubic)

### License/Terms of Use:

MIT-0

## Use Case:

Print-on-demand sellers use the skill to compare supplier prices, shipping, delivery estimates, and potential per-sale earnings for a configured product and destination. They can also use its supplier and product guidance to choose options for their shop.

### Deployment Geography for Use:

Global; comparisons currently support destinations in the US, UK, Germany, Canada, and Australia.

## Known Risks and Mitigations:

Risk: Seller business details may be sent to POD Benchmark without a clear user-facing disclosure.

Mitigation: Before sending seller details, explain the third-party transfer and proceed only when the seller is comfortable; pass only details the seller provided.

Risk: The optional CLI package is unpinned.

Mitigation: Avoid the optional CLI unless you can verify and restrict the package; the security report does not establish that it is malicious.

## Reference(s):

- [POD Benchmark](https://podbenchmark.com)
- [POD Benchmark MCP endpoint](https://podbenchmark.com/api/mcp)
- [POD Benchmark tool catalog](https://podbenchmark.com/api/v1/tools)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Text or Markdown with supplier comparison details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Price and delivery information is dated; unknown values remain unknown, and delivered totals exclude sales tax.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
