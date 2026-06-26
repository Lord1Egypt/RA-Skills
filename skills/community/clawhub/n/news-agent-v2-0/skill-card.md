## Description: <br>
舆情监测智能体V2 gathers daily technology and company news across AI, compute, collaboration tools, HarmonyOS, and 彩讯股份, scores items, generates analysis, creates an H5 report, and sends it to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mia-liu842](https://clawhub.ai/user/mia-liu842) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and analysts use this skill to collect daily technology news, score and filter items, summarize industry trends, produce company-focused analysis, and share a Feishu-ready report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web-sourced text and links are assembled into an HTML report without clear safeguards around sanitization or link validation. <br>
Mitigation: Review generated reports before sharing, escape web-sourced text, and validate links before generating the H5 report. <br>
Risk: The skill can send stock-related analysis and web-sourced news to Feishu. <br>
Mitigation: Confirm the Feishu recipient and review the report, especially company and stock-related analysis, before sending. <br>
Risk: The report generator uses a fixed local output path. <br>
Mitigation: Make the output path configurable and check the target location before writing the HTML report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mia-liu842/news-agent-v2-0) <br>
- [Configuration](artifact/config.md) <br>
- [Scoring rules](artifact/scoring.md) <br>
- [Output rules](artifact/output_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown summary plus generated HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters news below a 60-point score and includes title, original link, summary, score, and source for each retained item.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
