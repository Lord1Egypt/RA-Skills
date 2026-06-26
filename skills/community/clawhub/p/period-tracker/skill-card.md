## Description: <br>
Period Tracker helps users record menstrual periods and symptoms, view cycle and ovulation predictions, set local reminders, and export local health records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sosshuai](https://clawhub.ai/user/sosshuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill with an agent to maintain local menstrual cycle and symptom records, estimate period and ovulation windows, review trends, manage reminders, and export their data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Menstrual and symptom history is sensitive health data stored locally and may also be exported. <br>
Mitigation: Install only on a trusted device, protect the local data directory, and treat JSON or CSV exports as sensitive files. <br>
Risk: Reminder setup can add tagged cron jobs to the user's account. <br>
Mitigation: Enable reminders only after confirming the schedule, and review or remove tagged period-tracker cron jobs when reminder needs change. <br>
Risk: Update, delete, export, and reminder changes can materially alter the local skill setup or user data. <br>
Mitigation: Confirm these actions explicitly before running them, especially when an agent translates natural language into commands. <br>
Risk: Cycle, ovulation, fertile-window, and conception-probability outputs are estimates and can be wrong for individual users. <br>
Mitigation: Use predictions as planning aids, not as medical advice or a sole basis for contraception or fertility decisions. <br>


## Reference(s): <br>
- [Period Tracker data schema](references/data-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Natural-language responses with inline shell commands; optional JSON or CSV export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local period-tracking data and tagged cron reminders when requested.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
