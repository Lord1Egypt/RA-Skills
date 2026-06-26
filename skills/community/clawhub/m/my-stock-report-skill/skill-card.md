## Description: <br>
Runs a local Python analysis engine for specified U.S. stock tickers, supports configurable analyst modules, and archives generated conclusions and reports to DingTalk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to trigger U.S. stock analysis, generate decision and full-report documents, and record the resulting report metadata in a DingTalk table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stock reports, summaries, conclusions, and document links are written to the configured DingTalk workspace and report table. <br>
Mitigation: Before first use, verify that the workspace ID, parent node, companion DingTalk skills, and account belong to the intended organization and are appropriate for the reports' sensitivity. <br>
Risk: The workflow runs a local stock-analysis command and then archives its outputs. <br>
Mitigation: Confirm the target ticker, analyst modules, language, and working directory before execution, and review generated reports before relying on or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canonxu/my-stock-report-skill) <br>
- [DingTalk document overwriteContent endpoint](https://api.dingtalk.com/v1.0/doc/suites/documents/{docKey}/overwriteContent?operatorId={OPERATOR_ID}) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown table plus generated report files and DingTalk document links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ticker, analysis timestamp, conclusion, summary, conclusion document link, and full report document link.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
