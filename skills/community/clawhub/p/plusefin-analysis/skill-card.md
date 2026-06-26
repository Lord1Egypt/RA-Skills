## Description: <br>
AI-ready stock analysis with financial data, options, sentiment, and structured research framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghsinche](https://clawhub.ai/user/wanghsinche) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch PlusE financial data and assemble structured stock research covering fundamentals, price history, options, sentiment, holdings, news, earnings, insiders, and macroeconomic series. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial queries and the PlusE API token are sent to PlusE's service. <br>
Mitigation: Install only if that data flow is acceptable, keep PLUSEFIN_API_KEY out of prompts, screenshots, commits, and logs, and rotate the token if exposure is suspected. <br>
Risk: Financial outputs may be incomplete, stale, or unsuitable as investment advice. <br>
Mitigation: Treat outputs as research support, verify key conclusions against cited sources, and apply independent review before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wanghsinche/plusefin-analysis) <br>
- [PlusE Skill Homepage](https://github.com/plusefin/plusefin-skill) <br>
- [PlusE API Endpoint](https://mcp.plusefin.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and text data returned from the PlusE API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PLUSEFIN_API_KEY and produces research support, not investment advice.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
