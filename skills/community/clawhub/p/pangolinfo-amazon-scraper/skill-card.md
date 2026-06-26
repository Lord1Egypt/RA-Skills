## Description: <br>
Pangolinfo Amazon Scraper guides an agent to use Pangolinfo MCP tools to fetch Amazon product details, keyword results, category and seller listings, bestseller and new-release lists, reviews, and custom Amazon URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangolinfo](https://clawhub.ai/user/pangolinfo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to direct agents through Amazon scraping workflows for product research, search result summaries, category or seller listings, bestseller and new-release snapshots, and review analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential setup guidance conflicts about whether the agent should read a Pangolinfo API key directly or rely on MCP credential injection. <br>
Mitigation: Use a limited Pangolinfo API key, configure one credential path, and avoid exposing the key in chat or logs. <br>
Risk: Live Amazon scraping can return incomplete, rate-limited, or costly review data. <br>
Mitigation: Confirm review-page budgets, follow the documented concurrency limits, and report missing returned fields instead of filling gaps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pangolinfo/pangolinfo-amazon-scraper) <br>
- [Pangolinfo website](https://www.pangolinfo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, tables, product cards, CSV-style lists, JSON-formatted MCP tool arguments, and setup snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Pangolinfo MCP tools and API credentials; review-page scraping should be budget-confirmed before use.] <br>

## Skill Version(s): <br>
3.1.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
