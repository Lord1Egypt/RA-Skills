## Description: <br>
Get stock screener list data from Intellectia API (no auth) and summarize results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[intellectiaAI](https://clawhub.ai/user/intellectiaAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch public Intellectia stock screener data, apply documented query filters, and summarize returned instruments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock screener filter values are sent to Intellectia's public API. <br>
Mitigation: Review filter values before making requests and avoid sending confidential trading strategies or sensitive business criteria. <br>
Risk: The Python example may require installing the third-party requests package. <br>
Mitigation: Install dependencies in a controlled Python environment and follow normal package review practices. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/intellectiaAI/intellectia-stock-screener) <br>
- [Intellectia Stock Screener API Endpoint](https://api.intellectia.ai/gateway/v1/stock/screener-list) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline cURL and Python examples, plus summarized JSON API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No authentication is required; network calls send stock screener filters to Intellectia's API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
