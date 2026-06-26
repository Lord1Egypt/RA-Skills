## Description: <br>
MedPilot manages a single-patient medication and health-tracking workflow for ingesting doctor orders, logging medication intake and home metrics, and generating follow-up summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for single-patient self-management workflows: recording doctor orders, confirming active medications, logging doses or skipped doses, tracking blood pressure or glucose, and preparing follow-up summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release scanner found that examples can cross into medical interpretation and follow-up advice despite the stated boundary against diagnosis or treatment decisions. <br>
Mitigation: Review the skill before installation, keep use to logging medications, vitals, and doctor orders, and avoid diagnosis, test-result interpretation, medication changes, or care decisions unless stronger clinical safety and privacy boundaries are added. <br>


## Reference(s): <br>
- [MedPilot Self-Use Quickstart](references/quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI and local API command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include structured order summaries, medication state, intake logs, metric alerts, and weekly follow-up reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
