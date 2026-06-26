## Description: <br>
Searches real market information for products in any region, separates official and community sources, and produces credibility-rated tables and analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyyfaith](https://clawhub.ai/user/zyyfaith) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and research agents use this skill to gather product pricing, sales, reviews, trends, and channel information for a specified region. It supports purchase research, regional market comparison, and evidence-labeled market summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional continuous tracking can create a persistent cron job without enough scoping or removal guidance. <br>
Mitigation: Before enabling tracking, require the agent to show the exact schedule, command, sources, output destination, end date, and removal command; approve it only when background recurring searches are intended. <br>


## Reference(s): <br>
- [Product Market Research on ClawHub](https://clawhub.ai/zyyfaith/product-market-research) <br>
- [Credibility Guide](reference/credibility-guide.md) <br>
- [Output Templates](reference/output-templates.md) <br>
- [Search Strategies](reference/search-strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with tables, source links, credibility labels, and optional follow-up choices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or create scheduled tracking when explicitly requested by the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
