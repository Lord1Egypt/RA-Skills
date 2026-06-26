## Description: <br>
Open Stocki provides financial Q&A by sending market and investment research questions to the Stocki analyst agent for analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17817942676](https://clawhub.ai/user/17817942676) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Open Stocki to answer financial or investment research questions, including market outlooks, company fundamentals, macro trends, and scheduled financial monitoring. It is analysis-only and does not execute trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial research questions are sent to the Stocki/Miti remote service and may expose sensitive financial details. <br>
Mitigation: Avoid account numbers, exact holdings, proprietary plans, or other sensitive financial details unless the user trusts that service. <br>
Risk: Recurring financial monitoring can be created without enough user-facing control or privacy disclosure. <br>
Mitigation: Confirm the monitoring schedule, timezone, and cancellation path explicitly before setting up recurring checks. <br>
Risk: Fallback update commands include global git configuration changes and directory deletion. <br>
Mitigation: Prefer the ClawHub update command unless the user understands the fallback commands and their local effects. <br>


## Reference(s): <br>
- [Open Stocki on ClawHub](https://clawhub.ai/17817942676/open-stocki) <br>
- [Open Stocki homepage](https://repo.miti.chat/wangzhikun/open_stocki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or cleaned plain text answer with optional footnote-style links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers are returned from a remote Stocki service; timezone defaults to Asia/Shanghai and can be overridden.] <br>

## Skill Version(s): <br>
0.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
