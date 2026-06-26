## Description: <br>
Search for products on Naver Shopping. Use when the user wants to find product prices, links, or compare items in the Korean market. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dryoo](https://clawhub.ai/user/dryoo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and shopping agents use this skill to search Naver Shopping for Korean-market products, prices, and product links, then compare results by relevance, date, or price. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Naver's API and may reveal product interests or shopping intent. <br>
Mitigation: Use only queries appropriate to share with Naver and avoid including sensitive personal or confidential information. <br>
Risk: The skill requires Naver Search API credentials in environment variables. <br>
Mitigation: Keep credentials out of logs and version control, use the narrowest available API scope, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [Naver Shopping Search API endpoint](https://openapi.naver.com/v1/search/shop.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [JSON search results or Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NAVER_Client_ID and NAVER_Client_Secret environment variables; result count and sort order are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
