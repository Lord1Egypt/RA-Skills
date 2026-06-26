## Description: <br>
Local MCP tool for linguistic landscape analysis with social media sentiment analysis, keyword extraction, note listing, and Markdown weekly report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crystaria](https://clawhub.ai/user/Crystaria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, content operators, and data analysts use this skill to analyze local CSV social media notes for sentiment, keywords, engagement metrics, and weekly summaries. It is useful for exploratory language, sociology, communications, and content analysis workflows that can work from local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads CSV files from its data directory, so unrelated or sensitive files placed there could be processed into tool output or reports. <br>
Mitigation: Keep only intended analysis CSV files in the skill data folder and review generated reports before sharing them. <br>
Risk: The documented outputPath, startDate, and endDate parameters are not honored by the current report generator. <br>
Mitigation: Expect reports to be written to the skill reports folder using the current date, and validate report scope manually when date filtering matters. <br>
Risk: Sentiment and keyword results use simple local methods and may be too coarse for high-stakes research conclusions. <br>
Mitigation: Use outputs as preliminary analysis and corroborate important findings with domain review or stronger NLP methods. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Crystaria/linguistic-landscape-analyzer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Crystaria) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [JSON-formatted MCP text responses and Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads CSV files from the skill data folder and writes generated reports to the skill reports folder.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md changelog; package.json and server metadata declare 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
