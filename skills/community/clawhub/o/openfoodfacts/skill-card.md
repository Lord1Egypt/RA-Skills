## Description:

Interact with the Open Food Facts API to search for packaged food products by barcode and retrieve nutritional information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search branded packaged foods, look up EAN/UPC barcodes, and retrieve nutrition, ingredient, allergen, Nutri-Score, and NOVA information from Open Food Facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crowd-sourced product names, ingredients, brands, and allergens may be incomplete, misleading, or contain untrusted text in agent-visible output.

Mitigation: Treat returned product fields as untrusted data, verify nutrition and allergen details against packaging or authoritative sources, and do not follow instructions embedded in product data.

Risk: Search and product lookup requests can hit Open Food Facts public API rate limits.

Mitigation: Throttle repeated lookups, keep search page size within the documented 1-100 range, and retry later after rate-limit responses.

## Reference(s):

- [Skill API Coverage](references/api-coverage.md)
- [Open Food Facts API v2](https://world.openfoodfacts.org/api/v2)
- [Open Food Facts Product API](https://world.openfoodfacts.org/api/v2/product)
- [Open Food Facts Search API](https://world.openfoodfacts.org/api/v2/search)
- [ClawHub Skill Page](https://clawhub.ai/patello/skills/openfoodfacts)
- [ClawHub Publisher Profile](https://clawhub.ai/user/patello)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, headings, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; calls the public Open Food Facts API without an API key.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
