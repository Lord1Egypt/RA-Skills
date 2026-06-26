## Description: <br>
Routes explicit requests to add or query U.S. stock analysis report conclusions in a specified DingTalk multidimensional table via the dingtalk-ai-table skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to archive validated U.S. stock analysis report conclusions into a DingTalk table and retrieve matching report records as Markdown results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist new stock analysis report records into a specific DingTalk table. <br>
Mitigation: Use it only for the intended table and require all six documented fields to be validated before insertion. <br>
Risk: Queries may retrieve all rows from the configured sheet through the dependent dingtalk-ai-table skill. <br>
Mitigation: Confirm the dependent skill is trusted and permission-limited before installation or use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/canonxu/my-stock-report-mgnt-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown tables or concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Insert requests require six validated fields; summaries are limited to 300 Chinese characters before insertion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
