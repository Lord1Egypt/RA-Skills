## Description: <br>
Holmes guides an agent to analyze problems with abductive reasoning, mental models, logic formulas, active information gathering, and structured case records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangqi-7](https://clawhub.ai/user/jiangqi-7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to make an agent structure investigations, enumerate hypotheses, acquire missing evidence, and present reasoned conclusions with confidence and boundaries. It is also used to record and review cases so future reasoning workflows can be refined. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist case records that contain sensitive user, third-party, or regulated information. <br>
Mitigation: Require explicit user approval before case logging and avoid recording private, regulated, or third-party personal information. <br>
Risk: Autoresearch guidance can lead an agent to modify skill or reference files and propose repository commits. <br>
Mitigation: Review proposed file edits and commits before execution, and keep repository changes separate from unrelated work. <br>
Risk: The skill asks the agent to use broad web search for missing facts or uncertain reasoning steps. <br>
Mitigation: Require approval for external web searches when needed and cite sources for claims that affect the conclusion. <br>
Risk: The reasoning workflow can produce confident but incorrect inferences if assumptions are not checked. <br>
Mitigation: Preserve explicit confidence levels, boundary statements, and evidence gaps in final answers. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Autoresearch mechanism](references/autoresearch.md) <br>
- [Case logger](references/case_logger.md) <br>
- [Case closing report](references/case_closing_report.md) <br>
- [Checklist](references/checklist.md) <br>
- [Decision rules](references/decision_rule.md) <br>
- [Mental models](references/mental-models.md) <br>
- [Case studies](references/case-studies.md) <br>
- [Skill page](https://clawhub.ai/jiangqi-7/holmes) <br>
- [Publisher profile](https://clawhub.ai/user/jiangqi-7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown reasoning summaries with optional shell commands and local case-record files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local case records and propose skill edits when case logging or autoresearch is used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
