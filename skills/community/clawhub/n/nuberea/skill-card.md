## Description: <br>
Bible research platform for AI agents with access to original-language Hebrew and Greek morphology, lexicons, KJV Bible text, Dead Sea Scrolls, New Testament manuscript transcriptions, Septuagint data, and SQL-queryable research tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[streamsapps](https://clawhub.ai/user/streamsapps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use this skill for Bible study, biblical language research, exegesis, word studies, Scripture lookup, lexicon lookup, morphological parsing, manuscript comparison, and read-only SQL analysis across bundled ancient-text datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries may be sent to the MCP backend and could include private or sensitive text. <br>
Mitigation: Avoid submitting sensitive text unless the user is comfortable sending it to the backend. <br>
Risk: Research outputs may rely on source texts, lexicons, or manuscript datasets with their own licensing considerations. <br>
Mitigation: Verify source licensing before redistributing research outputs. <br>


## Reference(s): <br>
- [NuBerea MCP Tools Reference](references/tools.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/streamsapps/nuberea) <br>
- [Publisher Profile](https://clawhub.ai/user/streamsapps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, SQL queries, tool calls, guidance] <br>
**Output Format:** [Markdown, text, JSON-like tool-call arguments, and SQL query snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only MCP lookup and analytics tools; outputs may summarize or cite retrieved Bible, lexicon, morphology, manuscript, and scroll data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
