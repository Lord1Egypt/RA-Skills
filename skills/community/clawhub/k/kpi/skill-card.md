## Description: <br>
Manages KPI metrics, execution tasks, progress updates, scoring, and retrospectives in a local KPI memory file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DawnLck](https://clawhub.ai/user/DawnLck) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and agents use this skill to turn business goals into measurable KPIs, track execution tasks, calculate completion rates, and close each cycle with a scored retrospective. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KPI and retrospective records may contain sensitive performance information retained locally in ~/.openclaw/workspace/memory/kpi.md. <br>
Mitigation: Review the local KPI memory file periodically and avoid storing sensitive personal performance details unless local retention is intended. <br>
Risk: Inconsistent KPI definitions, measurement methods, or formulas can produce misleading completion rates and retrospective scores. <br>
Mitigation: Confirm each KPI definition and measurement method before setting targets, preserve change notes, and use only the allowed scoring scale. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DawnLck/kpi) <br>
- [Publisher profile](https://clawhub.ai/user/DawnLck) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance and structured KPI records for memory/kpi.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains KPI cycles, task status, progress values, completion rates, retrospective notes, and allowed review scores.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
