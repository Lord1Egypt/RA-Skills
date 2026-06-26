## Description: <br>
Real-time price comparison for Hong Kong supermarkets using the Consumer Council's daily pricewatch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenho1394](https://clawhub.ai/user/stevenho1394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to compare Hong Kong supermarket prices for an English or Chinese product query and return the cheapest matching item with a fixed-budget quantity estimate. <br>

### Deployment Geography for Use: <br>
Hong Kong <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the artifact files were not available for a full artifact-level inspection in the supplied scan context. <br>
Mitigation: Review the packaged SKILL.md and support files before installing or publishing the skill. <br>
Risk: The skill downloads supermarket price data from an external public CSV source and may be unable to answer if that source is unavailable or stale. <br>
Mitigation: Confirm the data source is reachable and review output freshness before relying on price comparisons. <br>


## Reference(s): <br>
- [Consumer Council Price Watch CSV](https://online-price-watch.consumer.org.hk/opw/opendata/pricewatch_en.csv) <br>
- [ClawHub skill page](https://clawhub.ai/stevenho1394/hk-supermarket-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single product-query response; may answer in English or Traditional Chinese based on the query language.] <br>

## Skill Version(s): <br>
1.2.3 (source: frontmatter, package.json, clawhub.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
