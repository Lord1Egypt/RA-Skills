## Description: <br>
Measure US equity market breadth using advance/decline lines, percentage of stocks above moving averages, and new highs/lows via the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch Finskills market breadth data, assess whether US equity market participation is broad or narrow, detect breadth divergences, and produce a market health report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key and uses results to generate market-health analysis that could influence financial decisions. <br>
Mitigation: Keep the API key private, confirm trust in Finskills before installation, and verify important investment decisions against additional sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/market-breadth-analyzer) <br>
- [Finskills market-breadth analyzer homepage](https://github.com/finskills/market-breadth-analyzer) <br>
- [Finskills API](https://finskills.net) <br>
- [Market breadth endpoint](https://finskills.net/v1/free/market/breadth) <br>
- [Market summary endpoint](https://finskills.net/v1/market/summary) <br>
- [Short volume endpoint](https://finskills.net/v1/free/market/short-volume-top) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown market breadth report with calculated indicators, divergence checks, market health score, and investor-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and returns research support, not financial advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
