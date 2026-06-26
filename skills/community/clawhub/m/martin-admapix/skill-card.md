## Description: <br>
AdMapix is an ad intelligence and app analytics skill that searches ad creatives, analyzes apps, views rankings, tracks estimated downloads and revenue, and summarizes market insights through the AdMapix API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and growth teams use this skill to query AdMapix for ad creative discovery, app intelligence, rankings, download and revenue estimates, ad distribution, market analysis, and competitor comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends ad intelligence searches, app names, competitor names, and related business terms to AdMapix. <br>
Mitigation: Use the skill only when AdMapix is approved for that data, and avoid entering personal identifiers or highly sensitive unreleased campaign details. <br>
Risk: The skill requires an AdMapix API key. <br>
Mitigation: Use a dedicated API key, never expose it in outputs, and rotate the key if it is ever exposed. <br>
Risk: Download and revenue figures are third-party estimates rather than official metrics. <br>
Mitigation: Present those figures with the provided estimate disclaimer and avoid treating them as authoritative financial or store-reported data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/martin-admapix) <br>
- [AdMapix website](https://www.admapix.com) <br>
- [Creative Search API](references/api-creative.md) <br>
- [Product & Company API](references/api-product.md) <br>
- [Ranking API](references/api-ranking.md) <br>
- [Download & Revenue API](references/api-download-revenue.md) <br>
- [App Distribution API](references/api-distribution.md) <br>
- [Market Analysis API](references/api-market.md) <br>
- [Parameter Mapping Reference](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with tables, summaries, links, and inline shell commands when setup or API-key checks are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses adapt between English and Chinese and include disclaimers for third-party download and revenue estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
