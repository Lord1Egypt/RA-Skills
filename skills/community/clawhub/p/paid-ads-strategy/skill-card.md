## Description: <br>
Guides paid ads strategy, including channel selection, budget allocation, product-market-fit testing, ad-to-landing-page alignment, and cross-platform best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kostja94](https://clawhub.ai/user/kostja94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, founders, and growth teams use this skill to plan paid acquisition strategy, choose channels, allocate budget, align ads with landing pages, and decide when paid media is appropriate for product-market-fit testing or conversion-driven campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid media recommendations could lead to budget waste or unintended campaign changes if treated as authorization to execute. <br>
Mitigation: Require explicit approval before invoking downstream ad-platform skills that create campaigns, change public ads, or spend budget. <br>
Risk: The skill may read local project context that contains sensitive business, audience, budget, or funnel details. <br>
Mitigation: Review project-context files for sensitive information before use and share only the details needed for planning. <br>
Risk: Planning guidance can be incorrect, stale, or mismatched to a specific product, market, or tracking setup. <br>
Mitigation: Review recommendations before execution and validate decisions against current conversion tracking, CAC, ROAS, and landing-page data. <br>


## Reference(s): <br>
- [Marketing Cactus - Using Google Ads to Test Product-Market Fit](https://mktcactus.com/en/using-google-ads-to-test-product-market-fit-before-launching/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with tables, recommendations, budgets, metrics, and routing notes to platform-specific ad skills] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend channels, PMF readiness checks, budget approach, landing page requirements, and metrics to track.] <br>

## Skill Version(s): <br>
1.7.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
