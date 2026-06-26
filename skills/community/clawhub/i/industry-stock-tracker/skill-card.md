## Description: <br>
Generates Chinese stock or industry tracking reports from a user query, returning report text plus optional PDF and DOCX attachments from Eastmoney. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask for structured Chinese tracking reports on named industries, sectors, indexes, or stocks. The skill uses the query to generate a concise report body, local attachment paths, and a share link when the upstream service returns them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires EM_API_KEY and uses it to call an external report service. <br>
Mitigation: Store EM_API_KEY only in the agent environment, rotate it if exposed, and avoid printing it in prompts, logs, or shared reports. <br>
Risk: Stock or industry prompts are sent to Eastmoney's service. <br>
Mitigation: Do not include confidential account data, proprietary research, or restricted business information in prompts unless that sharing is approved. <br>
Risk: Generated financial reports, attachments, and share links may be incomplete, stale, or unsuitable as a sole basis for decisions. <br>
Mitigation: Verify generated content and attachments against trusted financial sources before relying on or redistributing them. <br>
Risk: Returned PDF/DOCX attachments are written to local storage. <br>
Mitigation: Use an appropriate output directory, apply normal file access controls, and scan or review attachments before sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/financial-ai-analyst/industry-stock-tracker) <br>
- [Publisher Profile](https://clawhub.ai/user/financial-ai-analyst) <br>
- [Eastmoney Report Service Endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/write/tracking/report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration] <br>
**Output Format:** [Chinese Markdown-style report text with optional PDF and DOCX file paths plus a share link; the helper script emits JSON for the agent to format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY; sends report prompts to Eastmoney and may store generated PDF/DOCX attachments locally.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
