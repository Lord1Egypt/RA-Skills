## Description: <br>
Ad intelligence and app analytics assistant for searching ad creatives, analyzing apps, viewing rankings, tracking download and revenue estimates, and getting market insights through the AdMapix API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query AdMapix for ad creative discovery, app intelligence, rankings, distribution analysis, market trends, and competitor comparisons in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AdMapix API key, so unrelated secrets could be exposed if users paste them into prompts or API parameters. <br>
Mitigation: Configure only the required SKILLBOSS_API_KEY value and avoid entering unrelated secrets in prompts or request parameters. <br>
Risk: Download and revenue outputs are third-party estimates and may be mistaken for official figures. <br>
Mitigation: Label download and revenue values as estimates and use them as directional analytics rather than official reporting. <br>


## Reference(s): <br>
- [AdMapix website](https://www.admapix.com) <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-admapix) <br>
- [Creative Search API](artifact/references/api-creative.md) <br>
- [Product Analysis API](artifact/references/api-product.md) <br>
- [Ranking API](artifact/references/api-ranking.md) <br>
- [Download and Revenue API](artifact/references/api-download-revenue.md) <br>
- [Ad Distribution API](artifact/references/api-distribution.md) <br>
- [Market Analysis API](artifact/references/api-market.md) <br>
- [Parameter Mappings](artifact/references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries, tables, comparisons, links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SKILLBOSS_API_KEY for AdMapix API access; download and revenue outputs are third-party estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
