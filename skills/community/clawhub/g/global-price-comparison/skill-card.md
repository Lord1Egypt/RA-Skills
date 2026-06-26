## Description: <br>
Discover and compare the same product across multiple countries and source types using Brave and/or Tavily web search, then normalize all offers to USD for ranking and spread analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsjwong](https://clawhub.ai/user/wsjwong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and analysts use this skill to discover candidate product listings across countries, record verified offers, and compare USD-normalized prices for same-product market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product search terms are sent to Brave or Tavily when discovery is used. <br>
Mitigation: Use limited provider API keys, avoid sensitive product queries, or skip discovery and compare a locally prepared CSV when search disclosure is not acceptable. <br>
Risk: Price rankings can be misleading when offers differ by product variant, tax basis, shipping, seller quality, warranty, or new/refurbished condition. <br>
Mitigation: Verify the same model and variant, keep tax and shipping treatment consistent, separate new from refurbished or used listings, and retain URL plus capture-time evidence. <br>
Risk: USD normalization depends on an external exchange-rate lookup at comparison time. <br>
Mitigation: Record the comparison timestamp and review exchange-rate assumptions before using results for purchasing or reporting decisions. <br>


## Reference(s): <br>
- [Data Shape and Source Type Guide](references/data-shape-and-source-types.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wsjwong/global-price-comparison) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown, JSON, or CSV comparison output with optional shell commands and local CSV templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Discovery can use BRAVE_API_KEY or TAVILY_API_KEY; comparison reads local offer CSV data and normalizes prices to USD.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
