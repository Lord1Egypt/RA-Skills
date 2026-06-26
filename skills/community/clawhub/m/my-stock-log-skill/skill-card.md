## Description: <br>
This skill helps agents archive and query U.S. stock analysis conclusions in a DingTalk multidimensional table when the user explicitly requests the analysis log table or my_stock_log_skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who maintain U.S. stock research logs use this skill to validate required fields, append conclusions to a DingTalk table through dingtalk-ai-table, and query matching records as Markdown tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill targets a specific DingTalk Base ID and Sheet ID, so using it without authorization could store records in the wrong table. <br>
Mitigation: Verify that the DingTalk table is owned or authorized before inserting real records, and review the dingtalk-ai-table skill that performs the API writes. <br>
Risk: Malformed or incomplete stock-analysis data could be recorded if required fields are missing or incorrectly formatted. <br>
Mitigation: Collect and validate the symbol, analysis time, conclusion, and summary before insertion; ask the user for missing fields and keep summaries within the documented limit. <br>
Risk: A real record may be inserted when the user only intended to discuss or draft an analysis note. <br>
Mitigation: Ask the agent to confirm before each insert when handling real records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canonxu/my-stock-log-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown tables and structured field mappings for downstream table operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Insert workflows require a stock symbol, analysis time, conclusion, and summary of 300 characters or fewer before a record is added.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
