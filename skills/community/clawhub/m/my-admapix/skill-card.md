## Description: <br>
Ad intelligence and app analytics assistant for searching ad creatives, analyzing apps, viewing rankings, tracking downloads and revenue, and getting market insights via api.admapix.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockyzhuo](https://clawhub.ai/user/rockyzhuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and growth teams use this skill to query AdMapix for ad creative discovery, app analytics, rankings, download and revenue estimates, market analysis, and competitive research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and forwards AdMapix API credentials and business queries to remote AdMapix services. <br>
Mitigation: Use a dedicated revocable API key, avoid pasting keys into shared chats, and avoid submitting confidential strategy or market research unless remote processing is acceptable. <br>
Risk: Deep research reports may be hosted as shareable remote links. <br>
Mitigation: Share only non-confidential queries and ask the publisher to document report access controls before relying on the skill for sensitive work. <br>
Risk: Download and revenue outputs are third-party estimates and may be mistaken for official app-store data. <br>
Mitigation: Keep the estimate disclaimer in user-facing summaries and validate figures before making commercial decisions. <br>


## Reference(s): <br>
- [AdMapix website](https://www.admapix.com) <br>
- [AdMapix API base](https://api.admapix.com) <br>
- [README](README.md) <br>
- [Creative API reference](references/api-creative.md) <br>
- [Distribution API reference](references/api-distribution.md) <br>
- [Download and revenue API reference](references/api-download-revenue.md) <br>
- [Market API reference](references/api-market.md) <br>
- [Product API reference](references/api-product.md) <br>
- [Ranking API reference](references/api-ranking.md) <br>
- [Parameter mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with API-derived summaries, tables, links to generated H5 or HTML reports, and occasional shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AdMapix API key; download and revenue figures are third-party estimates and should be labeled as such.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
