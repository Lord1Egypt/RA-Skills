## Description: <br>
Provides PipiAds-powered TikTok and Facebook ad intelligence for researching ads, products, stores, landing pages, advertisers, competitors, creative hooks, campaigns, and image-based search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, ecommerce operators, and competitive intelligence analysts use this skill to research TikTok, Facebook, Meta Ad Library, TikTok Shop, store, advertiser, app, and campaign data through PipiAds. It helps narrow ad research, inspect campaign and product details, summarize patterns, and manage explicit monitoring tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a pinned local npm MCP server with access to a PipiAds API key. <br>
Mitigation: Install only if comfortable with the package and run it in a dedicated or isolated environment when stronger supply-chain controls are needed. <br>
Risk: Search queries and optional image inputs are sent to the external PipiAds service. <br>
Mitigation: Avoid sensitive personal data, private customer information, confidential campaign assets, and unnecessary image uploads. <br>
Risk: Broad searches can consume paid PipiAds credits. <br>
Mitigation: Narrow searches by platform, region, time range, category, or target object before requesting large result sets. <br>
Risk: Monitoring and notification tools can create, update, group, delete, or cancel remote monitoring resources. <br>
Mitigation: Confirm the exact advertiser, group, notification target, and intended change before using monitoring-management tools. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/fanyanggod/pipiads) <br>
- [PipiAds homepage](https://www.pipiads.com) <br>
- [PipiSpy API portal](https://www.pipispy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown narrative with tables, summaries, and inline setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ad, product, store, advertiser, campaign, ranking, monitoring, or image-search summaries derived from PipiAds API results.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
