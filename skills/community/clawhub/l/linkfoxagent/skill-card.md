## Description: <br>
LinkFoxAgent helps agents perform cross-border e-commerce research, marketplace analysis, product and keyword discovery, review mining, patent checks, image and PDF analysis, web search, and optional Lingxing ERP data workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce operators, analysts, and developers use this skill to submit product research, competitor analysis, sourcing, trend, review, listing, patent, and marketplace data tasks to LinkFoxAgent and related tools. Users with Lingxing ERP credentials can also retrieve ERP-side ads, order, listing, inventory, finance, and FBA data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: E-commerce prompts and artifacts are sent to LinkFox and related third-party services. <br>
Mitigation: Do not include secrets, private customer data, internal URLs, confidential strategy, or regulated personal data in prompts or uploaded files. <br>
Risk: Successful runs can produce public share links containing the execution trace and downloadable artifacts. <br>
Mitigation: Review task inputs and generated artifacts before sharing links, and avoid submitting information that should not become public. <br>
Risk: Lingxing ERP workflows use separate ERP credentials and may reach write-capable endpoints. <br>
Mitigation: Use least-privilege Lingxing credentials, confirm intended endpoint behavior before execution, and avoid mutating endpoints unless explicitly intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfoxagent) <br>
- [LinkFoxAgent Homepage](https://agent.linkfox.com/) <br>
- [Keepa Tool Reference](references/keepa.md) <br>
- [Amazon Frontend Tool Reference](references/amazon-frontend.md) <br>
- [Amazon Data Insight Tool Reference](references/amazon-data-insight.md) <br>
- [Seller Sprite Tool Reference](references/seller-sprite.md) <br>
- [Sorftime Tool Reference](references/sorftime.md) <br>
- [Sif Data Analysis Tool Reference](references/sif.md) <br>
- [Jimu Tool Reference](references/jimu.md) <br>
- [Google Trends Tool Reference](references/google-trends.md) <br>
- [Web Search Tool Reference](references/web-search.md) <br>
- [TikTok E-commerce Tool Reference](references/tiktok.md) <br>
- [Walmart Tool Reference](references/walmart.md) <br>
- [eBay Tool Reference](references/ebay.md) <br>
- [Shopee Tool Reference](references/youying.md) <br>
- [1688 Tool Reference](references/1688.md) <br>
- [Ozon Tool Reference](references/mpstats-ozon.md) <br>
- [Patent Tool Reference](references/patent.md) <br>
- [AI Tools Reference](references/ai-tools.md) <br>
- [Sandbox Tool Reference](references/sandbox.md) <br>
- [Lingxing ERP OpenAPI Reference](references/lingxing-erp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, status text, public share URLs, local JSON and CSV result files, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY for LinkFoxAgent calls; Lingxing ERP workflows require separate Lingxing credentials.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence; artifact _meta.json reports 1.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
